from fastapi import APIRouter, HTTPException, status
from typing import List
from src.controllers.category_controllers import CategoryControllers
from src.models.Categoria_models import Categoria, create_categoria, update_categia

category_router = APIRouter()

@category_router.get('/categoria', tags=['Categorias'], response_model=List[Categoria])
async def get_categorys():
    try:
        categorys = await CategoryControllers.get_category()
        return categorys
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al obtener categorias: {str(e)}'    
        ) 
    
@category_router.get('/categoria/{id_category}', tags=['Categorias'], response_model= List[Categoria])
async def get_category(id_category: int):
    try:
        category = await CategoryControllers.get_category_by_id(id_category)
        return category
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'Error al obtener categoria: {str(e)}'
        )
    
@category_router.post('/categoria', tags=['Categorias'], status_code= status.HTTP_201_CREATED)
async def category_create(category: create_categoria):
    try:
        category_create = await CategoryControllers.category_create(category)
        return category_create
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al crear una categoria: {str(e)}'
        )
    
@category_router.put('/categoria/{id_category}', tags=['Categorias'])
async def category_update(id_category: int, category: update_categia)  -> dict:
    try:
        result = await CategoryControllers.category_update(id_category, category)
        return result
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al actualizar la categoria: {str(e)}'
        )
        
@category_router.delete('/categoria/{id_category}', tags=['Categorias'])
async def almacen_delete(id_category: int):
    try:
        result = await CategoryControllers.category_delete(id_category)
        return result
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al eliminar la categoria: {str(e)}'
        )