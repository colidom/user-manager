from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers


class userModel(BaseModel):
    dni: constr(min_length=9, max_length=9)
    name: constr(min_length=2, max_length=30)
    surname: constr(min_length=2, max_length=30)


class userCreationModel(userModel):
    @validator('dni')
    def validate_dni(cls, dni):
        if helpers.validate_dni(dni, db.Users.users_list):
            return dni
        raise ValueError("Existing User or DNI is not correct!")


HEADERS = {'content-type': 'charset=utf8'}

app = FastAPI(
    title="User Manager API",
    description="🍉Provides the different methods for making a CRUD in the application",
)


@app.get('/', tags=["Generic"])
async def index():
    content = {'message': '¡Hello! Welcome to User Manager API REST'}
    return JSONResponse(content=content, headers=HEADERS, media_type='application/json')


@app.get('/users/', tags=["Users"])
async def users():
    content = [user.to_dict() for user in db.Users.users_list]
    return JSONResponse(content, headers=HEADERS)


@app.get('/users/find/{dni}', tags=["Users"])
async def find_by_dni(dni: str):
    user = db.Users.find(dni=dni)
    if not user:
        # Client not found, returns a response with an appropriate message and status code 404
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(content=user.to_dict(), headers=HEADERS)


@app.post('/users/create', tags=["Users"])
async def create_user(data: userCreationModel):
    user = db.Users.create(data.dni, data.name, data.surname)

    if user:
        return JSONResponse(content=user.to_dict(), headers=HEADERS)
    else:
        # Client not created, returns a response with an appropriate message and status code 404
        raise HTTPException(status_code=404, detail="User not created")


@app.put('/users/update', tags=["Users"])
async def update_user(data: userModel):
    if db.Users.find(data.dni):
        user = db.Users.update(data.dni, data.name, data.surname)
        if user:
            return JSONResponse(content=user.to_dict(), headers=HEADERS)
        else:
            # Client not found, returns a response with an appropriate message and status code 404
            raise HTTPException(status_code=404, detail="User not found")


@app.delete('/users/delete/{dni}', tags=["Users"])
async def delete_user(dni: str):
    if db.Users.find(dni):
        user = db.Users.delete(dni=dni)
        return JSONResponse(content=user.to_dict(), headers=HEADERS)
    # Client not found, returns a response with an appropriate message and status code 404
    raise HTTPException(status_code=404, detail="User not found")
