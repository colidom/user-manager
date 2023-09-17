from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
import database as db


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
