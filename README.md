# Group Project Coursework

## About

The aim of the group project was to develop a quiz application with two different quiz formats that children 
could use during an open day. It was required that the teacher could create/edit/delete question packages and that
they could assign these question packages to a quiz. It was also a requirement that the teacher could view statistics
from all previous quizzes and find them by date.  

**My section of the coursework was the packages menu, parts of the questions menu and parts of the database design.**

## Installation and Setup

1. Download or clone file
2. Download Python 3.8.5
3. Open terminal/command line
5. Navigate to GroupProject directory in the command line
6. Type: pip3 install six matplotlib
7. Type: python3 run.py

Please be aware that the coursework was mainly being marked based on functionality and there
were some sections that didn't get completed due to time constraints. For example the application
currently needs to be restarted to go from the teachers menu to the students menu. Also be aware that the application was developed for the Ubuntu operating system and coloured feedback during the quiz only works on this operating system.

## Usage

**Navigating to Each Quiz**

1. Click student
2. Click on either quiz

**Navigating to The Teachers Menu**

1. Click teacher
2. Password = 'guess'

The following windows can be accessed from the teachers menu

**Question Packages Window**

To add a package: 
1. click add new package
2. input the package name
3. click create

To edit the package name: 
1. click 'edit package name'
2. update the name in the input field
3. click save

To delete a package: 
1. click delete on the package row

To assign a question package to a quiz format
1. click the quiz format dropdown menu on the row of the package you want to assign
2. select a quiz format

**Be aware that you can't assign more than one question package to the same quiz format**

To add/edit/delete/view questions in a package click 'edit package questions'

**Edit Package Questions Window**

To add a question: 
1. click add new question
2. input the question, the correct answer and the wrong answers
3. click create

To edit a question:
1. click edit
2. make the modifications
3. click save

To delete a question:
1. click delete on the question row

Any updates made in the packages or questions menu will be reflected in the quiz's

**Settings Window**

To change password:
1. input old password
2. input new password
3. input confirmation of new password
4. click change password

**Statistics Window**

* Click quiz name to get quiz data from different quizzes
* Click date dropdown to get quiz data from different dates
* Click radio buttons to get data from different quiz formats
* Click 'export event statistics as CSV' to download the current data into a CSV file





