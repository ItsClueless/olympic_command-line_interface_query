from importlib.util import resolve_name
from input_parser import InputParser, CommandNotFoundError
from database import Database

   
class NoResultException(Exception):
    def __init__(self, message):
        self.message = message

class Application():
    """Handles the main application loop, including:
        - printing help message
        - error handling
        - I/O with the database class
        - quitting the application
        """
    
    def __init__(self):
        self.parser = InputParser()
        self.database = Database()
        self.quit = False
        
    def print_welcome_message(self):
        print("\nOlympics Database")
        print("Type 'help' for instructions")
        print("Type 'quit' to exit")
        
    def run(self):
        """Runs the command line interface main loop"""
        none = list()
        output_column_count = 1
        response_pre = ""
        response_suf = ""
        self.print_welcome_message()
        while not self.quit:
            try:
                command = self.parser.get_next_user_command() # wait for command from user
                
                # handle 'special' commands
                if command[0] == 'help':
                    self.print_help()
                    continue # don't pass to database
                elif command[0] == 'quit':
                    self.quit = True
                    continue # don't pass to database
                elif command[0] == 'load':
                    if command[1] == 'data':
                        # load data into database
                        success = self.database.load_data()
                        if not success:
                            raise(Exception("Error loading data"))
                    else:
                        raise (CommandNotFoundError(command))
                    continue 
                
                sql = ""
                
                # pass command to database 
                if command[0] == "list": #list
                    if command[1] == "columns":
                        response = self.database.columns_query(command[2])
                        if response == none:
                            print("No table named '{}'".format(command[2]))
                        else:
                            # show response
                            print()
                            for line in response:
                                print(line)   
                        print() # print blank line
                    elif len(command[1:]) == 1:
                        # e.g. list [athletes, countries, events, sports]
                        output_column_count = 2
                        if command[1] == "sports":
                            sql = self.database.select_query(["sport"], False, none, none) 
                        elif command[1] == "events":
                            sql = self.database.select_query(["event"], False, none, none) 
                        elif command[1] == "countries":
                            sql = self.database.select_query(["country"], False, none, none) 
                        elif command[1] == "athletes":
                            sql = self.database.select_query(["athlete"], False, none, none) 
                        else:
                            raise (CommandNotFoundError(command))
                    elif len(command[1:]) > 2:
                        # e.g. list athletes [sport, event] [sport name, event name]
                        if command[1] == "athletes":
                            if command[2] in ["sport", "event", "country"]:
                                if command[2] == "sport":
                                    sql = self.database.select_query(["athlete"], True, [command[2]], [command[3]])
                                elif command[2] == "event":
                                    sql = self.database.select_query(["athlete"], True, [command[2]], [command[3]])
                                elif command[2] == "country":
                                    sql = self.database.inner_join_query(["fldName"], "tblOlympicAthletes", "tblCountries", "fpkNationality", "pmkCountryCode", True, ["fldCountryName"], [command[3]])
                            else:
                                raise (CommandNotFoundError(command))
                        else:
                            raise(CommandNotFoundError(command))
                    elif len(command[1:])>1 and command[1] == "athletes":
                        print("Wrong format, should be: list athletes [sport, event] [sport name, event name]")
                        raise (CommandNotFoundError(command))
                    else:
                        raise (CommandNotFoundError(command))
                    
                elif command[0] == "population":    
                    sql = Database.select_query(self,["fldPopulation"],True,["fldCountryName"],[command[1]])
                    response_pre = "There are "
                    response_suf = "people in " + command[1]
                elif command[0] == "count":
                    if command[1] in ["bronze", "silver", "gold"]:
                        response_pre = command[2] + " has"
                        sql = self.database.select_query([command[1]], True, ["fldCountryName"], [command[2]])
                        response_suf = command[1] + " medals"
                    elif command[1] == "medals":
                        response_pre = command[2] + " has"
                        sql = self.database.select_query(["total"], True, ["fldCountryName"], [command[2]])
                        response_suf = command[1] 
                    else:
                        raise (CommandNotFoundError(command))
                elif command[0] == "nationality":
                    # command 1 should be a name
                    response_pre = command[1] + " is from"
                    sql = self.database.inner_join_query(['fldCountryName'], "tblCountries", "tblOlympicAthletes", "pmkCountryCode", "fpkNationality", True, ["fldName"], [command[1]])
                    
                elif command[0] == "sport":
                    # command 2 should be a name
                    sql = self.database.select_query([command[0]], True, ["athlete"], [command[2]])
                elif command[0] == "event":
                    # command 2 should be a name
                    sql = self.database.select_query([command[0]], True, ["athlete"], [command[2]])
                elif command[0] == "least" or command[0] == "most":
                    if command[1] in ["bronze", "silver", "gold"]:
                        sql = self.database.min_max_query(["fldCountryName"], (command[0]=="most"), command[1])
                    elif command[1] == "medals":
                        sql = self.database.min_max_query(["fldCountryName"], (command[0]=="most"), "total")
                    else:
                        raise (CommandNotFoundError(command))
                else:
                    raise (CommandNotFoundError(command))

                try:
                    if(sql):
                        response = Database.submit_query(Database, sql)
                        if len(response) == 0:
                            raise(NoResultException("\nNo results found"))
                        #print(response) # show the user the result of their command   
                        print()
                        if len(response) > 30: 
                            output_column_count = 2
                        if output_column_count == 1:
                            for line in response:
                                if(response_pre != ""):
                                    print(response_pre, end =" ")
                                print(line, end=" ")
                                if(response_suf != ""):
                                    print(response_suf, end="")
                                print()

                        elif output_column_count == 2:
                            i = 0
                            max_chars = 0
                            for str in response:
                                if len(str) > max_chars:
                                    max_chars = len(str)
                            col_width = max_chars + 3
                            while i < len(response):
                                print(f"* {response[i]:{col_width}s}", end="\t")
                                if i + 1 < len(response):
                                    print("*",response[i+1])
                                i += 2
                        
                        print() # print a blank line
                except NoResultException as e:
                    self.print_error(e)
                except Exception as e:
                    print("\nPlease Load Data First")

            
            except KeyboardInterrupt:
                self.quit = True

            except CommandNotFoundError as command_not_found:
                self.print_error(command_not_found)
            
            except Exception as e:
                print("\nAn unexpected error occurred:")
                self.print_error(e)
            
    def print_help(self):
        print()
        print("Instructions:")
        print("\"load data\" must be called before any other command")
        print("Valid commands:")
        print("""\tload data 
\thelp 
\tquit
\tlist columns countries
\tlist columns athletes
\tlist events
\tlist countries
\tlist sports
\tlist athletes
\tlist athletes sport <sport name>
\tlist athletes event <event name>
\tlist athletes country <country>
\tpopulation <country name>
\tcount  <medal type> <country name>
\tcount medals <country name>
\tnationality <athlete name>
\tsport athlete <name>
\tevent athlete <name>
\tleast <medal type>
\tmost <medal type>""")
        print("Any parameters that contain more than one word must be enclosed in quotes")
    
    def print_error(self, error):
        print(error) 
        
if __name__ == "__main__":
    app = Application()
    app.run()
    
 