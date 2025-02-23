from fastapi import APIRouter

routers = APIRouter()

# Llamamos a las rutas de navegacion
from src.routers.users_routers import user_router
from src.routers.almacen_routers import almacen_router
from src.routers.category_routers import category_router
from src.routers.inventory_movement_routers import inven_mov_router
from src.routers.products_routers import products_router
from src.routers.proveedores_routers import proveedor_router
from src.routers.rols_routers import rol_router
from src.routers.subcategorys_routers import subcat_router
from src.routers.transferencias_routers import transferencia_router
from src.routers.ubicacionAlm_routers import ubicacion_alm_router
from src.routers.unidad_medida_routers import unidad_md_router

#----------------------------------- Ruras de Users ----------------------------------- #
routers.include_router(router= user_router)

#----------------------------------- Ruras de Almacenes ----------------------------------- #
routers.include_router(router= almacen_router)

#----------------------------------- Ruras de Categorias ----------------------------------- #
routers.include_router(router= category_router)

#----------------------------------- Ruras de Movimientos de Inventario ----------------------------------- #
routers.include_router(router= inven_mov_router)

#----------------------------------- Ruras de Productos ----------------------------------- #
routers.include_router(router= products_router)

#----------------------------------- Rutas de Proveedores ----------------------------------- #
routers.include_router(router= proveedor_router)

#----------------------------------- Rutas de Roles ----------------------------------- #   
routers.include_router(router= rol_router)

#----------------------------------- Rutas de Subcategorias ----------------------------------- #
routers.include_router(router= subcat_router)

#----------------------------------- Rutas de Transferencias ----------------------------------- #
routers.include_router(router= transferencia_router)

#----------------------------------- Rutas de Ubicaciones de Almacen ----------------------------------- #
routers.include_router(router= ubicacion_alm_router)

#----------------------------------- Rutas de Unidades de Medida ----------------------------------- #
routers.include_router(router= unidad_md_router)