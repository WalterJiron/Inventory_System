from src.controllers.login_controller import LoginController
from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from src.main import templates

login_router = APIRouter()

@login_router.get('/', tags=['Login'])
async def login(request: Request):
    return templates.TemplateResponse(
        'login.html', {'request': request},
        status_code=status.HTTP_200_OK
    )

@login_router.post('/check_login', tags=['Login'])
async def check_login(request: Request):
    try:
        form = await request.form()
        username = form.get('username')
        password = form.get('password')

        if username is None or password is None:
            raise Exception('Los campos de usuario y contraseña son requeridos.')
        
        result = await LoginController.check_login(username, password)

        if result is True:
            return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
        
        return JSONResponse(
            content={'message': 'Credenciales incorrectas'}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return JSONResponse(
            content={'message': f'Error al validar credenciales: {str(e)}'}, 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )