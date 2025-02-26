from fastapi import APIRouter, Request, status
from src.main import templates

home_router = APIRouter()

@home_router.get('/home', tags=['Home'])
def home(request: Request):
    return templates.TemplateResponse(
        'index.html', {'request': request, 'message':"Que nota!"},
        status_code= status.HTTP_200_OK
    )
    