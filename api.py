from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

HEADERS = {'content-type': 'charset=utf8'}

app = FastAPI()


@app.get('/')
async def index():
    content = {'message': '¡Hello World!'}
    return JSONResponse(content=content, headers=HEADERS, media_type='application/json')


@app.get('/html/')
async def html():
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>¡Hello World!</title>
    </head>
    <body>
        <h1>¡Hola Mundo!</h1>
    </body>
    </html>
    """
    return Response(content=content, media_type='text/html')
