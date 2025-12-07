from pydantic import BaseModel

class LoginPayLoad(BaseModel):
    user_name : str
    password : str 