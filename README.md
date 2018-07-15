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

### Create a Mysql Database:
  mysql> CREATE DATABASE db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

### Create a Mysql user:
  mysql> CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';

### Give all rights to the user:
  mysql> GRANT ALL ON db.* TO 'user'@'localhost';


## TODO:

### 1. Download the repository by clicking on clone or download:
  if it is not done yet...
  $ git clone https://github.com/MarcoDaphne/pur_beurre.git

### 2. Install the virtual environment

### 3. Activate the virtual environment

### 4. Install useful libraries:
  $ pip install -r requirements.txt

### 5. Match the database, the user and his password with the program:
  - Open the file 'constants.py' in the 'src' folder of the program.
  - Replace the database, the user and his password
    with the information previously entered.
    
    Example:
      Before: "mysql+mysqlconnector://root:root@localhost/pur_beurre_p5?charset=utf8mb4"

      After:  "mysql+mysqlconnector://user:password@localhost/db?charset=utf8mb4"

### 6. Download products:
  $ python product_downloader.py

### 7. Launch the program
  $ python pur_beurre.py