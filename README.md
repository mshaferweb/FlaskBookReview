# CS50 Project 1: Books

## Overview 

Books is a flask book review application connected to heroku PostgreSQL.
Users can:
- Register and log in using their username and password. 
- Once logged in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people

Screencast
https://youtu.be/s9v15aHhMpE

Setup:
```
> pip3 install -r requirements
> pip3 install -r requirements_selenium_robot

> export DATABASE_URL=<connection url>
> export GOOD_READS_KEY=<good reads key>

> cd `<project root>`
> python3 import.py -f
> flask run
> robot --outputdir ~/tmp login_tests/books_test.robot
```
Connect to: http://localhost:5000/

Files:
```
├── application.py  <== Flask application
├── books.csv
├── import.py       <== Database setup
├── login_tests
│   ├── books_test.robot    <== Robot UI tests
│   ├── myvariables.py
│   └── resource.robot  
├── README.md
├── requirements_selenium_robot.txt
├── requirements.txt
├── static
│   └── css
│       └── main.css
└── templates
    ├── book.html
    ├── books.html
    ├── error.html
    ├── index.html
    ├── layout.html
    └── register.html
```