from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers


class CustomerModel(BaseModel):
    dni: constr(min_length=9, max_length=9)
    name: constr(min_length=2, max_length=30)
    surname: constr(min_length=2, max_length=30)


class CustomerCreationModel(CustomerModel):
    @validator('dni')
    def validate_dni(cls, dni):
        if helpers.validate_dni(dni, db.Customers.customers_list):
            return dni
        raise ValueError("Existing Customer or DNI is not correct!")


HEADERS = {'content-type': 'charset=utf8'}

app = FastAPI(
    title="User Manager API",
    description="🍉Provides the different methods for making a CRUD in the application",
)


@app.get('/', tags=["Generic"])
async def index():
    content = {'message': '¡Hello! Welcome to User Manager API REST'}
    return JSONResponse(content=content, headers=HEADERS, media_type='application/json')


@app.get('/customers/', tags=["Customers"])
async def customers():
    content = [customer.to_dict() for customer in db.Customers.customers_list]
    return JSONResponse(content, headers=HEADERS)


@app.get('/customers/find/{dni}', tags=["Customers"])
async def find_by_dni(dni: str):
    customer = db.Customers.find(dni=dni)
    if not customer:
        # Client not found, returns a response with an appropriate message and status code 404
        raise HTTPException(status_code=404, detail="Customer not found")

    return JSONResponse(content=customer.to_dict(), headers=HEADERS)


@app.post('/customers/create', tags=["Customers"])
async def create_customer(data: CustomerCreationModel):
    customer = db.Customers.create(data.dni, data.name, data.surname)

    if customer:
        return JSONResponse(content=customer.to_dict(), headers=HEADERS)
    else:
        # Client not created, returns a response with an appropriate message and status code 404
        raise HTTPException(status_code=404, detail="Customer not created")


@app.put('/customers/update', tags=["Customers"])
async def update_customer(data: CustomerModel):
    if db.Customers.find(data.dni):
        customer = db.Customers.update(data.dni, data.name, data.surname)
        if customer:
            return JSONResponse(content=customer.to_dict(), headers=HEADERS)
        else:
            # Client not found, returns a response with an appropriate message and status code 404
            raise HTTPException(status_code=404, detail="Customer not found")


@app.delete('/customers/delete/{dni}', tags=["Customers"])
async def delete_customer(dni: str):
    if db.Customers.find(dni):
        customer = db.Customers.delete(dni=dni)
        return JSONResponse(content=customer.to_dict(), headers=HEADERS)
    # Client not found, returns a response with an appropriate message and status code 404
    raise HTTPException(status_code=404, detail="Customer not found")
