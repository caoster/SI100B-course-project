# Project Report - Control Panel Week 3



## Workload Division

- Team members: 

  ​					李炳楠 libn@shanghaitech.edu.cn

  ​					秦一帆 qinyf1@shanghaitech.edu.cn

  ​					陈溯汀 chenst@shanghaitech.edu.cn

- Workload division:

  ​					李炳楠：I wrote the primary frame of Flask in the `server.py` and wrote some html templates. I also beautified the user interface in the home page html templates. I wrote the judge javascript in the home page.

  ​					秦一帆：I processed the data sent to the server and enabled the communication between crawler and the server. Due to the code in `main.py`, I made some changes to the `state.py`, the crawler and the light controller.

  ​					陈溯汀：I figured out the `render_templates` function in the `server.py` and wrote another some html templates. I also beautified the user interface in the home page and handler html templates.

## Preliminary Comment

- Online resources: 

  1. https://www.w3school.com.cn/html/index.asp
  2. https://dormousehole.readthedocs.io/en/latest/
  3. https://www.w3school.com.cn/js/index.asp
  4. https://matplotlib.org
  5. https://blog.csdn.net/u010510187/article/details/100356624
  6. https://www.cnblogs.com/hanguidong/p/9381317.html

- Offline resources:

  1. Eric Matthes (2016, July). Python Crash Course: A Hands-on, Project-Based Introduction to Programming. No Starch Press, p.162~186
2. Eric Matthes (2016, July). Python Crash Course: A Hands-on, Project-Based Introduction to Programming. No Starch Press, p.312~321

- Please describe the difficulties you encountered in this project;

  How to use Flask

  The meaning of os.fork() and there exists zombie processes after the os.fork(), and can not be killed by KeyboardInterrupt.

  The previous part of our project such as state.py and fr24_crawler.py does not fit well with main.py.

## Advanced: Use Flask and HTML

Answering the following questions with a concrete example is desirable.

- How to serve the request sent from the client for a specific path? For example, if a request is requesting the path `\public` on your server and another one is requesting `\confidential` on your server, how could you distinguish them and send different responses?

  By using `@web_server.route()` function, the first parameter is a string type, which is a specific path. Once the client request for a specific path, the server will match the path in the parameter of many route function. If it find a function with the parameter of the specific path, the server will run the function code below it, or it will return a page shows that 404 Not Found with status code 404. So in the example, if a request is requesting the path `\public` on my server,the function code under `@web_server.route("\public")` will be run. And if another one is requesting `\confidential` on my server

- How to serve the different request methods? For example, one request is sent to your server for the path `\public` with a `GET` method and another one with a `POST` method, how could you distinguish them and send different responses?

  When the client send a request to the server, the method of the request is accessible by using `request.method` and type of `request.method` is string. By using `if request.method == 'GET':` and `if request.method == 'POST':` we can distinguish one request is sent to our server for the path `\public` with a `GET` method and another one with a `POST` method. There can also be parameter `methods=` in ` @web_server.route()` to limit the request method from the client, if the client's request method is not in `methods`, the server will return 405 Method Not Allowed with status code 405.

- How to render a HTML template in Flask? How to create a simple template in Flask?

  Create a file holder named "template" in "web_server", put all the html files into it so that server can reach it.

  Any html can be regarded as a template. By using `{{ID}} ` in a html file, server.py will automatically replace it with a specific variable.

- How to get the form data a user sends to your server in a `POST` request? Which data type is it?

  Use (for example) `loc_lat = request.form.get('data_loc_lat')` is meaning to get data named  `data_loc_lat` from the user and store it in a variable named `loc_lat`.

- How to specify the title of a web page? How to add a paragraph to a web page? How to add a title to a web page?

  Specify the title: Find `<title>name</title>` label in html file, the value of "name" is the title

  Add a paragraph: Use` <p></p>` to define a paragraph

  Add a title: Use` <title></title>`  in `<head></head> `to define a title of web page

- How to design a form on a web page? How to add text box to your form? How to add an option to your form?

  Design a form: Use `<form></form>` to define a form

  Add text box: Use `<input>` in ` <form></form>` to define a text box

  Add an option: First, use `<select></select>` to define a pull-down list. Second, use `<option></option>` to add an option in the pull-down list.

- How to send the content of the form to the server? What HTTP methods are generally used for those requests? In Flask, how do you handle the request containing a form?

  Send the content: Add a  submit button`<button></button>` to submit the content, and add `action` in `<form>` to define the address of the web after clicking, for example:`<form action="/config">` 
  
  HTTP methods: Generally, `POST` and `GET`  are the most common ways to request, we can add `method` in `<form>` to define the method  of request, for example:`<form action="/config" method="POST">` or `<form action="/config" method="GET">`
  
  Handle the form: use`request.form.get("id")` and`request.args.get("id")` to get data from request with "POST"method and "GET" method respectively
  
  

## Implementation

- How do you share the flight data between the crawler and the control panel? Which approach do you choose?

  We choose the first approach, by using files to commute the data. For example, the `rng`, the `loc`, the interval time and the working type chosen by  the users will be saved under the path `./data_source/status.csv`. And by using `os.path("filepath").st_mtime`, we can get the time when the file is last changed. By comparing the time, we can know that whether the file has been changed. And if it is changed, the state will get the newest settings and pass the settings to the crawler.

- Which parameters in your program is allowed to be changed?

  The parameters sent by the users. The parameters sent to crawler to change its settings.

