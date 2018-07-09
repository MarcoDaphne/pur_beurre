# **pur_beurre**
Use public data from the Open Food Facts

## Features:

  - Data research on Open Food Facts.
  - Create tables and foreign keys in the database.
  - Insert the data into the database.
  - Format the data for display in terminal.
  - Display five categories of French products.
  - Display ten products whose nutrition grade is between C and E according to
    the user's choice of category.
  - Display five substitutes whose nutrition grade is between A and B.
  - Request login or user registration if he wants to register a substitute.
  - Record user substitute as favorite in the database.
  - Request login if the user wants to find his favorites.
  - Display the user's favorites. 

## Prerequisites:

  - Open the Mysql terminal:
    If you do not have it, install MAMP and add the path in the environment variables.
    
    For Windows or macOS:
    https://www.mamp.info/en/downloads/

    For the first connection use the user 'root' and password 'root'.

  - Open the command prompt:
    open the search bar and type 'cmd.exe' and enter.

  - Have an email address.

## TODO:

### 1. Create a Mysql Database:
  mysql> CREATE DATABASE db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

### 2. Create a Mysql user:
  mysql> CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';

### 3. Give all rights to the user:
  mysql> GRANT ALL ON db.* TO 'user'@'localhost';

### 4. Download the repository by clicking on clone or download:
  if it is not done yet...
  command line> git clone https://github.com/MarcoDaphne/pur_beurre.git

### 5. Install the virtual environment:
  command line> virtualenv env

### 6. Activate the virtual environment:
  command line> env\scripts\activate

### 7. Install useful libraries:
  (env)command line> pip install -r requirements.txt

### 8. Match the database, the user and his password with the program:
  - Open the folder hosting the program.
  - Open the folder 'src'.
  - Open the file 'constants.py'.
  - Go to the line 4 then replace the database, the user and his password
    with the information previously entered.
    Example:
      Before: "mysql+mysqlconnector://root:root@localhost/pur_beurre_p5?charset=utf8mb4"
      After:  "mysql+mysqlconnector://user:password@localhost/db?charset=utf8mb4"

### 9. Download products:
  (env)command line> py product_downloader.py

### 10. Launch the program
  (env)command line> py pur_beurre.py

### Have fun and do not forget to disable the virtual environment:
  (env)command line> deactivate