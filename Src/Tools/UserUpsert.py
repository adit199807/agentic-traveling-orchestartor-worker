from Utilities.EnvironmentVariableLoader import loadEnvVariable
from langchain.tools import tool
from DummyDatas.UserData import USERDATA

@tool('checkAccountBalance')
def checkAccountBalance(userName:str)->str:
    """Get user's bank balance"""
    """
        arguments:
            userName : Name of user
        return:
            Amount in user's bank account
    """
    if userName not in USERDATA:
        return "User's bank balance is : 0.00"

    return f"User's bank balance is:{USERDATA[userName]['AccountBalance']}"


@tool('deductUserBalance')
def deductUserBalance(userName:str, deduct:float)->float:
    """Deduct amount from user's bank balance"""
    """       
         arguments:
            userName : Name of user
            deduct: Amount to deduct form user's bank account
        return:
            True for sucessful deduction of balance, False if not deducted
        """
    if userName not in USERDATA:
        return False
    if USERDATA[userName]['AccountBalance'] < deduct:
        return False
    USERDATA[userName]['AccountBalance'] -=  deduct
    return True

@tool('checkUserCity')
def checkUserCity(userName:str)->str:
    """Get user city"""
    """
        arguments:
            userName : Name of user
        return:
            Name of city where user lives
    """
    if userName not in USERDATA:
        return 'None'

    return f"User's city is {USERDATA[userName]['City']}"
