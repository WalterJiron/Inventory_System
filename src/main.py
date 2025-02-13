from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, Response  # Importacion de tipos de respuesta
from fastapi.requests import Request   # Importacion del tipo Request para manejar peticiones
from fastapi.staticfiles import StaticFiles   # Importacion para servir archivos estaticos
from fastapi.templating import Jinja2Templates   # Importacion del motor de plantillas Jinja2

# Rutas de navegacion
from src.routers.users_routers import user_router
from src.routers.almacen_routers import almacen_router
from src.routers.category_routers import category_router

app = FastAPI()

# Configuracion del titulo de la documentacion
app.title = 'Documentacion FastApi'

# Configuracion de la carpeta de plantillas
templates = Jinja2Templates(directory='src/views/templates')

# Configuracion de archivos estaticos
app.mount('/static', StaticFiles(directory="src/static"), name="static")

# Manejo de errores de la APP
@app.middleware('http')
async def  http_error_handle(request: Request, call_nex) -> Response | JSONResponse:
    try:
        # Intenta ejecutar la siguiente funcion en la cadena de middleware
        return await call_nex(request)
    except Exception as e:
        # En caso de error, construye una respuesta JSON con el mensaje de error
        content = f'eror: {str(e)}'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content= content, status_code= status_code)
    
@app.get('/', tags=['Home'])
def home() -> JSONResponse:
    result = {'message':'Holaaa'}
    return JSONResponse(content= result, status_code= status.HTTP_200_OK)
    
#----------------------------------- Ruras de Users ----------------------------------- #
app.include_router(router= user_router)

#----------------------------------- Ruras de Almacenes ----------------------------------- #
app.include_router(router= almacen_router)

#----------------------------------- Ruras de Categorias ----------------------------------- #
app.include_router(router= category_router)