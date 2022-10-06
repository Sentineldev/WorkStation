def read_file(path):
    """This function read a file in a specific path and return its content.
    
    Return: str
    """
    with open(path, 'r') as sql_file:
        return sql_file.read()
    