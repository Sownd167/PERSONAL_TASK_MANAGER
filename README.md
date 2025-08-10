A Personalised Task Manager which help us to manage our tasks amidst our busy schedule and also reminds us 1 or 2 days before the deadline. Through this we won't forget our important works.

The Front-end part is made with the help of HTML and CSS with some Javascript. AJAX is also used here for real-time updates without reloading the page (in Deleting task).

For Back-end SQLite Database is used since it is a small website with minimal users, SQLite database is similar to SQL but a lighter version which is easy to connect and store the data, it's syntax is much similar to that of MYSQL. Here we have two databases to store the user credentials and their respective tasks.

Front-end and Back-end is connected with the help of inbuilt Python Web Framework FLASK  which is a lightweight framework, in Flask we have JINJA2 library which is a template engine which makes the HTML content Dynamic.

Core Functionality of the application is to
    1) CREATE A TASK
    2) UPDATE A TASK
    3) LIST OF TASKS
    4) DELETE TASK
    
Also it has a reminder.py file we can make it run at certain time as a desktop notification by configuring our system settings to run this python file which is done with the help of PLYER library.

To run a Flask application the following command is used
    flask --app <file-name>.py --debug run
