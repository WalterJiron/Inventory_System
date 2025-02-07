from fastapi import FastAPI, status

from fastapi.responses import JSONResponse, Response

from fastapi.requests import Request

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

app = FastAPI()

app.title = 'Documentacion FastApi'

templates = Jinja2Templates(directory='src/views/templates')

app.mount('/static', StaticFiles(directory="src/static"), name="static")

# Manejo de errores de la APP
@app.middleware('http')
async def  http_error_handle(request: Request, call_nex) -> Response | JSONResponse:
    try:
        return await call_nex(request)
    except Exception as e:
        content = f'eror: {str(e)}'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content= content, status_code= status_code)
    
@app.get('/', tags=['Home'])
def home():
   pass