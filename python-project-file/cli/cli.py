#=============================================================================#
#                               Web Project                                   #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#
import os


def _main():
    '''
    Function `_main`:

    Implement your main CLI loop in this function.
    '''
    while True:
        pass


def _draw():
    '''
    Function `_main`:

    Implement your chart rendering in this function.
    '''
    while True:
        pass


def cli_start():
    # NOTE to student:
    # YOU ARE NOT SUPPOSED TO EDIT THE FUNCTION.
    #
    # This function is intended to provide a unified entrypoint for your CLI.
    # You can treat this function as a black box. Being unable to
    # know how the magic in this function works won't cause trouble to you finishing
    # the project. If you feel the need to edit it, do it at your own risk.
    # Understand every line of the file before proceed to editing. When in doubt,
    # ask on Piazza.
    pid = os.fork()
    if pid == 0:
        ppid = os.getppid()
        try:
            _draw()
        except KeyboardInterrupt:
            os.kill(ppid)
    else:
        try:
            _main()
        except KeyboardInterrupt:
            os.kill(pid)


if __name__ == "__main__":
    _main()
