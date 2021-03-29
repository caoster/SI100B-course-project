#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#
from gpiozero import PWMLED,OutputDevice,OutputDeviceBadValue
from gpiozero.threads import GPIOThread
from itertools import repeat, cycle, chain
from time import sleep


class myPWMOutputDevice(OutputDevice):
    """
    Generic output device configured for pulse-width modulation (PWM).

    :type pin: int or str
    :param pin:
        The GPIO pin that the device is connected to. See :ref:`pin-numbering`
        for valid pin numbers. If this is :data:`None` a :exc:`GPIODeviceError`
        will be raised.

    :param bool active_high:
        If :data:`True` (the default), the :meth:`on` method will set the GPIO
        to HIGH. If :data:`False`, the :meth:`on` method will set the GPIO to
        LOW (the :meth:`off` method always does the opposite).

    :param float initial_value:
        If 0 (the default), the device's duty cycle will be 0 initially.
        Other values between 0 and 1 can be specified as an initial duty cycle.
        Note that :data:`None` cannot be specified (unlike the parent class) as
        there is no way to tell PWM not to alter the state of the pin.

    :param int frequency:
        The frequency (in Hz) of pulses emitted to drive the device. Defaults
        to 100Hz.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).
    """
    def __init__(
            self, pin=None, active_high=True, initial_value=0, on_value=1, off_value=0, frequency=100,
            pin_factory=None):
        self._blink_thread = None
        self._controller = None
        self.on_value = on_value
        self.off_value = off_value
        if not 0 <= initial_value <= 1:
            raise OutputDeviceBadValue("initial_value must be between 0 and 1")
        super(myPWMOutputDevice, self).__init__(
            pin, active_high, initial_value=None, pin_factory=pin_factory
        )
        try:
            # XXX need a way of setting these together
            self.pin.frequency = frequency
            self.value = initial_value
        except:
            self.close()
            raise

    def close(self):
        try:
            self._stop_blink()
        except AttributeError:
            pass
        try:
            self.pin.frequency = None
        except AttributeError:
            # If the pin's already None, ignore the exception
            pass
        super(myPWMOutputDevice, self).close()

    def _state_to_value(self, state):
        return float(state if self.active_high else 1 - state)

    def _value_to_state(self, value):
        return float(value if self.active_high else 1 - value)

    def _write(self, value):
        if not 0 <= value <= 1:
            raise OutputDeviceBadValue("PWM value must be between 0 and 1")
        super(myPWMOutputDevice, self)._write(value)

    @property
    def value(self):
        """
        The duty cycle of the PWM device. 0.0 is off, 1.0 is fully on. Values
        in between may be specified for varying levels of power in the device.
        """
        return super(myPWMOutputDevice, self).value

    @value.setter
    def value(self, value):
        self._stop_blink()
        self._write(value)

    def on(self):
        self._stop_blink()
        self._write(self.on_value)

    def off(self):
        self._stop_blink()
        self._write(self.off_value)

    def toggle(self):
        """
        Toggle the state of the device. If the device is currently off
        (:attr:`value` is 0.0), this changes it to "fully" on (:attr:`value` is
        1.0).  If the device has a duty cycle (:attr:`value`) of 0.1, this will
        toggle it to 0.9, and so on.
        """
        self._stop_blink()
        self.value = (1 - self.value)*self.on_value

    @property
    def is_active(self):
        """
        Returns :data:`True` if the device is currently active (:attr:`value`
        is non-zero) and :data:`False` otherwise.
        """
        return self.value != 0

    @property
    def frequency(self):
        """
        The frequency of the pulses used with the PWM device, in Hz. The
        default is 100Hz.
        """
        return self.pin.frequency

    @frequency.setter
    def frequency(self, value):
        self.pin.frequency = value

    def blink(
            self, on_time=1, off_time=1, fade_in_time=0, fade_out_time=0,
            n=None, background=True):
        """
        Make the device turn on and off repeatedly.

        :param float on_time:
            Number of seconds on. Defaults to 1 second.

        :param float off_time:
            Number of seconds off. Defaults to 1 second.

        :param float fade_in_time:
            Number of seconds to spend fading in. Defaults to 0.

        :param float fade_out_time:
            Number of seconds to spend fading out. Defaults to 0.

        :type n: int or None
        :param n:
            Number of times to blink; :data:`None` (the default) means forever.

        :param bool background:
            If :data:`True` (the default), start a background thread to
            continue blinking and return immediately. If :data:`False`, only
            return when the blink is finished (warning: the default value of
            *n* will result in this method never returning).
        """
        self._stop_blink()
        self._blink_thread = GPIOThread(
            target=self._blink_device,
            args=(on_time, off_time, self.on_value, self.off_value, fade_in_time, fade_out_time, n)
        )
        self._blink_thread.start()
        if not background:
            self._blink_thread.join()
            self._blink_thread = None

    def pulse(self, fade_in_time=1, fade_out_time=1, n=None, background=True):
        """
        Make the device fade in and out repeatedly.

        :param float fade_in_time:
            Number of seconds to spend fading in. Defaults to 1.

        :param float fade_out_time:
            Number of seconds to spend fading out. Defaults to 1.

        :type n: int or None
        :param n:
            Number of times to pulse; :data:`None` (the default) means forever.

        :param bool background:
            If :data:`True` (the default), start a background thread to
            continue pulsing and return immediately. If :data:`False`, only
            return when the pulse is finished (warning: the default value of
            *n* will result in this method never returning).
        """
        on_time = off_time = 0
        self.blink(
            on_time, off_time, fade_in_time, fade_out_time, n, background
        )

    def _stop_blink(self):
        if self._controller:
            self._controller._stop_blink(self)
            self._controller = None
        if self._blink_thread:
            self._blink_thread.stop()
            self._blink_thread = None

    def _blink_device(
            self, on_time, off_time, on_value, off_value, fade_in_time, fade_out_time, n, fps=25):
        sequence = []
        if fade_in_time > 0:
            sequence += [
                (on_value * i * (1 / fps) / fade_in_time, 1 / fps)
                for i in range(int(fps * fade_in_time))
                ]
        sequence.append((on_value, on_time))
        if fade_out_time > 0:
            sequence += [
                (on_value*(1 - (i * (1 / fps) / fade_out_time)), 1 / fps)
                for i in range(int(fps * fade_out_time))
                ]
        sequence.append((off_value, off_time))
        sequence = (
                cycle(sequence) if n is None else
                chain.from_iterable(repeat(sequence, n))
                )
        for value, delay in sequence:
            self._write(value)
            if self._blink_thread.stopping.wait(delay):
                break

class myPWMLED(myPWMOutputDevice):
    """
    Extends :class:`PWMOutputDevice` and represents a light emitting diode
    (LED) with variable brightness.

    A typical configuration of such a device is to connect a GPIO pin to the
    anode (long leg) of the LED, and the cathode (short leg) to ground, with
    an optional resistor to prevent the LED from burning out.

    :type pin: int or str
    :param pin:
        The GPIO pin which the LED is connected to. See :ref:`pin-numbering`
        for valid pin numbers. If this is :data:`None` a :exc:`GPIODeviceError`
        will be raised.

    :param bool active_high:
        If :data:`True` (the default), the :meth:`on` method will set the GPIO
        to HIGH. If :data:`False`, the :meth:`on` method will set the GPIO to
        LOW (the :meth:`off` method always does the opposite).

    :param float initial_value:
        If ``0`` (the default), the LED will be off initially. Other values
        between 0 and 1 can be specified as an initial brightness for the LED.
        Note that :data:`None` cannot be specified (unlike the parent class) as
        there is no way to tell PWM not to alter the state of the pin.

    :param int frequency:
        The frequency (in Hz) of pulses emitted to drive the LED. Defaults
        to 100Hz.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).
    """
    pass

class BaseController:

    def __init__(self,pin:None,status:int):
        if pin != None:
            self.lednumber = pin
            if status == 0:
                self.off()
            elif status == 1:
                self.work_once()
            elif status == 2:
                self.work_once1()
            elif status == 3:
                self.frequency()
            elif status == 4:
                self.on()

    def work_once(self):
        self.lednumber.blink(on_time=0.5,off_time=2)

    def on(self):
        self.lednumber.blink(on_time=1,off_time=0)

    def off(self):
        self.lednumber.off()

    def frequency(self):
        self.lednumber.blink(on_time=0.25,off_time=0.25)

    def work_once1(self):
        self.lednumber.blink(on_time=0.5,off_time=1,fade_in_time=0.5,fade_out_time=0.5)

    def pre_load(self,number):
        return PWMLED(pin=number)

    def pre_load1(self,number):
        return myPWMLED(pin=number,on_value=0.05,off_value=0,frequency=150)