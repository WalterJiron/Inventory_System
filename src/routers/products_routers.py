from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.Producto_models import Producto, ProductoCreate, ProductoUpdate
from src.controllers.producto_controllers import ProductosControllers

products_router = APIRouter()

@products_router.get("/productos", tags=["Productos"], response_model=List[Producto])
async def get_products():
    """
    Obtiene todos los productos activos
    """
    try:
        products = await ProductosControllers.get_productos()
        
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )
    
@products_router.get("/productos/{product_id}", tags=["Productos"], response_model=Producto)
async def get_product(product_id: int):
    """
    Obtiene un producto por su ID.
    
    - **product_id**: El ID del producto a buscar.
    """
    try:
        product = await ProductosControllers.get_producto_by_id(product_id)
    
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener producto: {str(e)}"
        )
    
@products_router.post("/productos", tags=["Productos"], status_code=status.HTTP_201_CREATED)
async def create_new_product(product: ProductoCreate):
    """
    Crea un nuevo producto.
    
    - **product**: Datos del producto a crear.
    """
    try:
        result = await ProductosControllers.create_producto(product)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear producto: {str(e)}"
        )
    
@products_router.put("/productos/{product_id}", tags=["Productos"])
async def update_product(product_id: int, product: ProductoUpdate) -> dict:
    """
    Actualiza un producto por su ID.
    
    - **product_id**: El ID del producto a actualizar.
    - **product**: Datos del producto a actualizar.
    """
    try:
        result = await ProductosControllers.update_producto(product_id, product)
    
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar producto: {str(e)}"
        )
    
@products_router.delete("/productos/{product_id}", tags=["Productos"])
async def delete_product(product_id: int) -> dict:
    """
    Elimina un producto por su ID.
    
    - **product_id**: El ID del producto a eliminar.
    """
    try:
        result = await ProductosControllers.delete_producto(product_id)
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar producto: {str(e)}"
        )
    