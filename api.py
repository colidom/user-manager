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

app = FastAPI()


@app.get('/')
async def index():
    content = {'message': '¡Hello World!'}
    return JSONResponse(content=content, headers=HEADERS, media_type='application/json')


@app.get('/customers/')
async def customers():
    content = [customer.to_dict() for customer in db.Customers.customers_list]
    return JSONResponse(content, headers=HEADERS)


@app.get('/customers/find/{dni}')
async def find_by_dni(dni: str):
    customer = db.Customers.find(dni=dni)
    if not customer:
        # Client not found, returns a response with an appropriate message and status code 404
        raise HTTPException(status_code=404, detail="Customer not found")

    return JSONResponse(content=customer.to_dict(), headers=HEADERS)


@app.post('/customers/create')
async def create_customer(data: CustomerCreationModel):
    customer = db.Customers.create(data.dni, data.name, data.surname)

    if customer:
        return JSONResponse(content=customer.to_dict(), headers=HEADERS)
    else:
        # Client not created, returns a response with an appropriate message and status code 404
        raise HTTPException(status_code=404, detail="Customer not created")


@app.put('/customers/update')
async def update_customer(data: CustomerModel):
    if db.Customers.find(data.dni):
        customer = db.Customers.update(data.dni, data.name, data.surname)
        if customer:
            return JSONResponse(content=customer.to_dict(), headers=HEADERS)
        else:
            # Client not found, returns a response with an appropriate message and status code 404
            raise HTTPException(status_code=404, detail="Customer not found")


@app.delete('/customers/delete/{dni}')
async def delete_customer(dni: str):
    if db.Customers.find(dni):
        customer = db.Customers.delete(dni=dni)
        return JSONResponse(content=customer.to_dict(), headers=HEADERS)
    # Client not found, returns a response with an appropriate message and status code 404
    raise HTTPException(status_code=404, detail="Customer not found")
