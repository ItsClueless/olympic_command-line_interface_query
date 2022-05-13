# Warm-Up Project: Command-Line Interface Query System For Olypmic RBD
Created by: Jackson Dean, Anika Hamby, Max Heath, Dwayne Kirby

## Implementations using SQL

- Uses sqlite3 in Python
- Uses pandas as local database connection
- Query can not commence until database is made
- Database is created once. Can be updated at any time

## Parsing
- Any word or phase can be enter in without crashing, if anything that is entered that is not a command, it will display "Input command 'phrase' not found". 

## Interface
The interface is a command-line with the help menu to indicate the type of queries that can be made and an exit code. 

##### (<i>Click the arrow below for list of commands</i>) 
<details><summary><b>Commands</b></summary>
<p>

<u>Non-Query Commands</u>:
- load data : Used to first load the database, has to be ran before any queries can be made
- help : displays the help menu
quit : quits the program

<u>Query Commands</u>:
- list columns countries
- list columns athletes
- list events
- list countries
- list sports
- list athletes
- list athletes sport : sport name
- list athletes event : event name
- list athletes country : country
- population : country name
- count : medal type : country name
- count medals : country name
- nationality : athlete name
- sport athlete : name
- event athlete : name
- least : medal type
- most : medal type

<b>Any parameters that contain more than one word must be enclosed in quotes</b>

</p>
</details>