import shlex # for splitting while preserving quoted substrings

valid_operations = ["quit", "help", "load", "list", "population", "count", "total medals", "nationality", "sport", "event", "country", "least", "most"]

class InputParser():
    """Accepts input at the command line and parses it into a list of commands"""
    
    def wait_for_input(self):
        """Waits for input from the user and returns it as a string"""
        return input("\nEnter query: ")
    
    def parse_input(self, user_input):
        """Parses the user input into a list of SQL commands
        Raises CommandNotFoundError if a command is not found
        """
        split = shlex.split(user_input.lower())
        if not split[0] in valid_operations:
            raise CommandNotFoundError(split[0])

        return split
            
    def get_next_user_command(self):
        """Waits for the next input from the user and returns the parsed command"""
        user_input = self.wait_for_input()
        return self.parse_input(user_input)
    
    
class CommandNotFoundError(Exception):
    """
    Exception raised when the entered command is not found.
    """
    def __init__(self, input_command):
        self.message = f"Input command '{input_command}' not found"
        super().__init__(self.message)
    