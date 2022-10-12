


def isInteger(data:str) -> bool:

    """
    
    Tries to convert the given string to an integer
    if an en exceptions occurs then the given string is not a number

    return : bool

    """

    try:
        int(data)
    except:
        return False
    else:
        return True


def validateDate(date:str) -> bool:


    """
    First splits the string using the char '/'
    to make sure it's using the format separated by slashes
    then checks that only contains numbers.
    and last it checks if it's using the YYYY DD and MM format
    the first number must be a 4 digit number
    second a two digit number and the third same as the second.

    return: bool
    
    """
    splitted_date = date.split("-")
    if not (len(splitted_date) == 3):
        return False
    elif not(isInteger(splitted_date[0]) and isInteger(splitted_date[1]) and isInteger(splitted_date[2]) ):
        return False
    elif not ( len(str(splitted_date[0])) == 4 and len(str(splitted_date[1])) == 2 and len(str(splitted_date[2])) == 2):
        return False
    else:
        return True

def ValidateCreateRoomForm(form) -> dict:

    """
    
    Checks that the room title it's not empty and it's length
    is less than 64.

    also checks if the room description length is less that 512.
    

    return: dict with a message:str and a status: bool
    
    """

    room_title : str = form['room_title']
    room_description : str = form['room_description']

    if not (len(room_title) > 0 and len(room_title) <= 64):
        return {"message":"Room title must contain > 0 characters and <= 64 characters","status": False}
    elif not (len(room_description) <= 512):
        return {"message":"Room Description must contain <= 512 characters","status":False}
    else:
        return {"message":"","status":True}


def ValidateCreatePostForm(form) -> dict:
    """
    Checks that the post tittle it's not empty and it's length 
    is less than 64.

    Also check if the post description it's not empty and if lenght 
    is not greater than 8192.

    return: dict with a message: str and a status: bool
    """

    post_title : str = form['post_title']
    post_description : str = form['post_description']

    if not(len(post_title) > 0 and len(post_title) <= 64):
        return {"message": "Post title must contains > 0 characters and <= 64 characters", "status": False}
    elif not(len(post_description) > 0 and len(post_description) <= 8192):
        return {"message": "Post description must contains > 0 characters and <= 8192 characters", "status": False}
    else:
        return {"message": "", "status": True}
    

def ValidateCreateAssignmentForm(form):
    """
    Check that the assignment tittle it's not empty and it's length
    is less than 64.
    
    Check if the assignment description it's not empty and if length
    is not greater than 8192.
    
    Check that the expiration date it in the correct format. 
    
    Also check if the assignment ponderation it's not empty and 
    not greater than 100.

    return: dict with a message: str and a status: bool
    """
    
    assignment_title : str = form['assignment_title']
    assignment_description : str = form['assignment_description']
    assignment_ponderation : int = int(form['assignment_ponderation'])
    expiration_date : str = form['expiration_date']
    
    if not(len(assignment_title) > 0 and len(assignment_title) <= 64):
        return {"message": "Assignment title must contains > 0 characters and <= 64 characters", "status": False}
    elif not(len(assignment_description) > 0 and len(assignment_description) <= 8192):
        return {"message": "Assignment description must contains > 0 characters and <= 8192 characters", "status": False}
    elif not(assignment_ponderation >= 5 and assignment_ponderation <= 100):
        return {"message": "Assignment ponderation must have >= 5 percent and <= 100 percent", "status": False}
    elif not(validateDate(expiration_date)):
        return {"message":"Invalid Date format must be YYYY/MM/DD","status":False}
    else:
        return {"message": "", "status": True}


def ValidateRegisterUserForm(form) -> dict:


    """
    
    Checks that the username it's no empty and it's length is less than or equal to 32.
    Checks that the password it's not empty and it's length is less than or equal to 128.
    Checks that the name and last name are not empty and their length is less or equal to 32 
    same criteria applies to country
    Check that the email is not empty and it's length is less that 128 or equal.

    Checks that the phone number length is not empty  and it's length is less or equal to 16
    also check's that only contains numbers.

    Check that the birth date it in the correct format.

    return" dict with a message:str and a status: bool
    
    """

    username = form['username']
    password = form['password']
    
    name = form['name']
    last_name = form['last_name']
    email= form['email']
    country = form['country']
    birthdate = form['birth_date']
    phone_number = form['phone']

    if not(len(username) > 0 and len(username) <= 32):
        return {"message":"Username must contain > 0 characters and <= 32 characters","status":False}
    elif not(len(password) > 0 and len(password) <= 128):
        return {"message":"Password must contain > 0 characters and <= 128 characters","status":False}
    elif not (len(name) > 0 and len(name) <= 32):
        return {"message":"Name must contain > 0 characters and <= 32 characters","status":False}
    elif not (len(last_name) > 0 and len(last_name) <= 32):
        return {"message":"Last Name must contain > 0 characters and <= 32 characters","status":False}
    elif not (len(country) > 0 and len(country) <= 32):
        return {"message":"Country must contain > 0 characters and <= 32 characters","status":False}
    elif not (len(email) > 0 and len(email) <= 128):
        return {"message":"Email must contain > 0 characters and <= 128 including @ and such characters","status":False}
    elif not (isInteger(phone_number) and (len(phone_number) > 0 and len(phone_number) <= 16)):
        return {"message":"Phone must contain > 0 digits and <= 16 digits","status":False}
    elif not(validateDate(birthdate)):
        return {"message":"Invalid Date format must be YYYY/MM/DD","status":False}
    else:
        return {"message":"","status":True}