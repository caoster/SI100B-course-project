# Project Report - Week 3

# SI100B Project Report - Control Panel

Please submit this report as a PDF file along with your code to receive full score of the project. 

## Workload Division

- Fill in the names and email addresses of your group members and describe how you divide works among team members;

## Preliminary Comment

- Please cite any online or offline resources you consulted in this project;

- Please describe the difficulties you encountered in this project;

  How to use Flask

  The meaning of os.fork() and there exists zombie processes after the os.fork(), and can not be killed by KeyboardInterrupt.

  The previous part of our project such as state.py and fr24_crawler.py does not fit well with main.py.

## Easy: Use CLI

- How do you get the user input in Python when building your CLI program?
- Briefly describe how you design the scheme of the command? Give example command for doing the following things:
    - Change the central coordinate to 30N 101W;
    - Change the range to 100 nm;
    - Change the frequency of data crawling to once per 5 sec.

## Advanced: Use Flask and HTML

Answering the following questions with a concrete example is desirable.

- How to serve the request sent from the client for a specific path? For example, if a request is requesting the path `\public` on your server and another one is requesting `\confidential` on your server, how could you distinguish them and send different responses?

  By using `@web_server.route()` function, the first parameter is a string type, which is a specific path. Once the client request for a specific path, the server will match the path in the parameter of many route function. If it find a function with the parameter of the specific path, the server will run the function code below it, or it will return a page shows that 404 Not Found with status code 404. So in the example, if a request is requesting the path `\public` on my server,the function code under `@web_server.route("\public")` will be run. And if another one is requesting `\confidential` on my server

- How to serve the different request methods? For example, one request is sent to your server for the path `\public` with a `GET` method and another one with a `POST` method, how could you distinguish them and send different responses?

  When the client send a request to the server, the method of the request is accessible by using `request.method` and type of `request.method` is string. By using `if request.method == 'GET':` and `if request.method == 'POST':` we can distinguish one request is sent to our server for the path `\public` with a `GET` method and another one with a `POST` method. There can also be parameter `methods=` in ` @web_server.route()` to limit the request method from the client, if the client's request method is not in `methods`, the server will return 405 Method Not Allowed with status code 405.

- How to render a HTML template in Flask? How to create a simple template in Flask?

  

- How to get the form data a user sends to your server in a `POST` request? Which data type is it?

- How to specify the title of a web page? How to add a paragraph to a web page? How to add a title to a web page?

- How to design a form on a web page? How to add text box to your form? How to add an option to your form?

- How to send the content of the form to the server? What HTTP methods are generally used for those requests? In Flask, how do you handle the request containing a form?

## Implementation

- How do you share the flight data between the crawler and the control panel? Which approach do you choose?
- Which parameters in your program is allowed to be changed?

