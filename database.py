"""Import all needed functionality like sqlite
sqlite3 for the sql
pandas for database storage
"""
from pathlib import Path
Path('warm-up-data.db').touch()
import sqlite3
import pandas as pd

# Database class
# Includes function for loading data from CSV file into SQLITE database
# Includes functions for creating and running SQL statements on a database
class Database():
  TBL_ATHLETES = {"id": "pmkAthleteID", "athlete" : "fldName", "sex" : "fldSex", "age" : "fldAge", "height" : "fldHeight", "weight" : "fldWeight", "nationality" : "fpkNationality", "year" : "fldYear", "city" : "fldCity", "sport" : "fpkSport", "event" : "fldEvent"}
  TBL_COUNTRIES = {"code" :"pmkCountryCode", "country" : "fldCountryName", "gold" : "fldNumGoldMedals", "silver" : "fldNumSilverMedals", "bronze" : "fldNumBronzeMedals", "total" : "fldTotalMedals", "population" : "fldPopulation"}
  conn = None
  # Load CSV files into a database
  # returns 0 if there is an error or data could not be loaded
  # returns 1 otherwise
  def load_data(self):
      # load the data into a Pandas DataFrame
      try:
        Database.conn = sqlite3.connect('warm-up-data.db')
        atheletes = pd.read_csv('tblOlympicAthletes.csv')
        atheletes.to_sql('tblOlympicAthletes', Database.conn, if_exists='replace', index = False)
        countries = pd.read_csv('tblCountries.csv')
        countries.to_sql('tblCountries', Database.conn, if_exists='replace', index = False)
      # If no csv files are found, return 0
      except FileNotFoundError:
        return 0
      except Exception as e:
        print(e)
        return 0
      # if database is created, return 1
      print("\nData is loaded!")
      return 1
  

  def where_clause(self, sql, conditional_fields, conditions, is_join):
    # If the number of conditional fields does not match the number of conditions, return the original sql statement
    if len(conditional_fields) != len(conditions):
      return sql
    
    sql += "WHERE "
    c = 0
    for i in range(0, len(conditional_fields)):
      if conditional_fields[i] in Database.TBL_ATHLETES.keys():
        conditional_fields[i] = Database.TBL_ATHLETES.get(conditional_fields[i])
    for i in range(0, len(conditional_fields)):
      if conditional_fields[i] in Database.TBL_COUNTRIES.keys():
        conditional_fields[i] = Database.TBL_COUNTRIES.get(conditional_fields[i])

    for field in conditional_fields:
      if(c > 0 and c < len(conditions) - 1):
        sql += "AND "
      if(field in Database.TBL_ATHLETES.values() or field in Database.TBL_ATHLETES.keys()):
        sql += "UPPER("
        if(is_join):
          sql += "tblOlympicAthletes."
        sql += field
        sql += ") "
      elif(field in Database.TBL_COUNTRIES.values() or field in Database.TBL_COUNTRIES.keys()):
        sql += "UPPER("
        if(is_join):
          sql += "tblCountries."
        sql += field
        sql += ") "
      else:
        print("INVALID FIELDS IN WHERE CLAUSE")
        # Remove where clause from sql statement
        where_index = sql.find("WHERE")
        sql = sql[0 : where_index] + ";"
        return sql
      sql += "LIKE UPPER(\"" + conditions[c] + "\")"
      c += 1
    return sql


  # constructs a SELECT sql statement
  # params:   result_fields, list of desired query result(s) columns
  #           is_conditional, boolean value of whether or not there should be a WHERE clause, yes = 1, no = 0
  #           conditional_fields, list of conditional columns (such as country_name, or type of medal)
  #           conditions, list of conditional values
  # return:   sql statement as a string
  def select_query(self, result_fields, is_conditional, conditional_fields, conditions):
    sql = 'SELECT'
    i = 0

    for field in conditional_fields:
      if field in Database.TBL_ATHLETES.keys():
        field = Database.TBL_ATHLETES.get(field)

    for field in conditional_fields:
      if field in Database.TBL_COUNTRIES.keys():
        field = Database.TBL_COUNTRIES.get(field)

    for field in result_fields:
      if field in Database.TBL_ATHLETES.keys():
        field = Database.TBL_ATHLETES.get(field)
      elif field in Database.TBL_COUNTRIES.keys():
        field = Database.TBL_COUNTRIES.get(field)
      if(i > 0 and i < result_fields -1):
        sql += ", "
      if(field in Database.TBL_ATHLETES.values() or field in Database.TBL_ATHLETES.keys()):
        table = "tblOlympicAthletes"
        
      elif(field in Database.TBL_COUNTRIES.values() or field in Database.TBL_COUNTRIES.keys()):
        table = "tblCountries"
      if field == "all":
          sql += + " " + '*'
      else:
        sql += " " + field
    sql += " FROM" + " " + table + " "

    if(is_conditional):
      sql = Database.where_clause(self, sql,conditional_fields, conditions, False)

    if len(result_fields) == 1:
      sql += " GROUP BY "
      if result_fields[0] in Database.TBL_ATHLETES.keys():
        sql += Database.TBL_ATHLETES.get(result_fields[0]) + " "
      elif result_fields[0] in Database.TBL_ATHLETES.values():
        sql += result_fields[0] + " "
      elif result_fields[0] in Database.TBL_COUNTRIES.keys():
        sql += Database.TBL_COUNTRIES.get(result_fields[0]) + " "
      elif result_fields[0] in Database.TBL_COUNTRIES.values():
        sql += result_fields[0] + " "
    sql += ";"
    # Return the string value sql statement
    return sql

  
  # constructs a SHOW sql statement to show the columns of the table
  # params:   table_name, string value for name of the table
    # return:   sql statement as a string
  def columns_query(self, table_name):
    table_list = []
    if table_name == "countries":
      for keys in Database.TBL_COUNTRIES.keys():
        table_list.append(keys)
    elif table_name == "athletes":
      for keys in Database.TBL_ATHLETES.keys():
        table_list.append(keys)

    return table_list
    

  # constructs a SELECT sql statement based on min or max condition
  # params:   result_fields, list of desired query result(s) columns
  #           max, boolean value of whether the query is searching for a min or max value, max = 1, min = 0
  #           conditional_field, field to determine the max or min value of 
  # return:   sql statement as a string
  def min_max_query(self, result_fields, max, conditional_field):
    table_name = "tblCountries"

    # Make sure that the field is the same as column header 
    for field in result_fields:
      if field in Database.TBL_ATHLETES.keys():
        field = Database.TBL_ATHLETES.get(field)

    for field in result_fields:
      if field in Database.TBL_COUNTRIES.keys():
        field = Database.TBL_COUNTRIES.get(field)


    if conditional_field in Database.TBL_ATHLETES.keys():
      conditional_field = Database.TBL_ATHLETES.get(conditional_field)
    if conditional_field in Database.TBL_COUNTRIES.keys():
      conditional_field = Database.TBL_COUNTRIES.get(conditional_field)
    sql = "SELECT "

    for i in range(0, len(result_fields)):
      if(i != len(result_fields) - 1):
        sql += result_fields[i] + ", "
      else:
        sql += result_fields[i] + " "

    sql += "FROM " + table_name + " JOIN (SELECT "
    if max == True:
      sql += "MAX(" + conditional_field + ") AS most " + " FROM " + table_name + ") " + table_name + " ON " + "most = " + conditional_field
    else:
      sql += "MIN(" + conditional_field + ") AS least " + " FROM " + table_name + ") " + table_name + " ON " +  "least = " + conditional_field

    sql += ";"
    return sql


  
  # constructs an INNER JOIN sql statement
  # param:    result_fields, list of desired query result(s) columns
  #           left_tbl_field, relational key name for left table
  #           right_tbl_field, relational key name for right table
  #           is_conditional, boolean value of whether or not there should be a WHERE clause, yes = 1, no = 0
  #           conditional_fields, list of conditional columns (such as country_name, or type of medal)
  #           conditions, list of conditional values
  # return:   sql statement as a string
  def inner_join_query(self, result_fields, left_table, right_table, left_tbl_field, right_tbl_field, is_conditional, conditional_fields, conditions):
    for field in result_fields:
      if field in Database.TBL_ATHLETES.keys():
        field = Database.TBL_ATHLETES.get(field)

    for field in conditional_fields:
      if field in Database.TBL_ATHLETES.keys():
        field = Database.TBL_ATHLETES.get(field)

    for field in result_fields:
      if field in Database.TBL_COUNTRIES.keys():
        field = Database.TBL_COUNTRIES.get(field)

    for field in conditional_fields:
      if field in Database.TBL_COUNTRIES.keys():
        field = Database.TBL_COUNTRIES.get(field)
    
    sql = "SELECT "
    for i in range(0, len(result_fields)):
      sql += left_table + "." + result_fields[i]
      if(i != len(result_fields) - 1):
        sql += ", "
      else:
        sql += " "
    sql += "FROM " + left_table + " INNER JOIN " + right_table + " ON " + left_table + "." + left_tbl_field + " = " + right_table + "." + right_tbl_field + " "
    # if there are where conditions
    if(is_conditional):
      sql = Database.where_clause(self, sql, conditional_fields, conditions, True)
    sql += ";"
    return sql

  # Run sql query and return a list of data 
  # Error handling if SQL query in invalid
  # param:    sql, a sql statement
  # return:   results from sql query
  def submit_query(self, sql):
    if('warm-up-data.db'):
      if Database.conn == None:
        # print("New Connection")
        Database.conn = sqlite3.connect('warm-up-data.db')
      cur = Database.conn.cursor()
      cur.execute(sql)
      rows = cur.fetchall()
      results = list()
      for row in rows:
        results.append(row[0])
      return results
