import os
from dotenv import load_dotenv
load_dotenv()

def loadEnvVariable(variable:str)->str:
    return os.environ.get(variable,'')
