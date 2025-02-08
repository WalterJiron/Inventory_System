
CREATE DATABASE GestionInventario;

GO

USE GestionInventario;

GO

--------------------------------------------------- ROLES Y USERS ---------------------------------------------------
CREATE TABLE Roles(
    RolID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    NameRol NVARCHAR(30) NOT NULL,
    CreationDateRol DATETIME DEFAULT GETDATE(),
    EstadoRol BIT DEFAULT 1
);
GO

CREATE TABLE Usuarios(
    IdUser INT IDENTITY(1,1) PRIMARY KEY,
    NameUser NVARCHAR(25) NOT NULL,
    Clave  NVARCHAR(MAX) NOT NULL,
    RolID INT FOREIGN KEY REFERENCES Roles(RolID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    CreationDateUser DATETIME DEFAULT GETDATE(),
    EstadoUser BIT DEFAULT 1 
);
GO

-------------------CATEGORIAS-------------------------
CREATE TABLE Categoria(
    IdCategoria INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(50) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Estado BIT NOT NULL DEFAULT 1
);
GO

---------------------UNIDAD DE MEDIDA---------
CREATE TABLE UnidadesMedida(
    UnidadID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(25) NOT NULL,
    Abreviatura NVARCHAR(10),
    Estado BIT NOT NULL DEFAULT 1
);
GO

---------------SUBCATEGORIA
CREATE TABLE Subcategoria (
    id_subcategoria INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(MAX),
    idCategoria INT FOREIGN KEY REFERENCES Categoria(IdCategoria) ON DELETE CASCADE,
    Estado BIT NOT NULL DEFAULT 1
);
GO

-- Tabla de Almacenes
CREATE TABLE Almacenes (
    AlmacenID INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(MAX),
    Capacidad INT, -- Capacidad total del almacén
    Estado BIT NOT NULL DEFAULT 1
);
GO

-- Tabla de Ubicaciones dentro de un Almacén
CREATE TABLE UbicacionesAlmacen(
    UbicacionID INT PRIMARY KEY IDENTITY(1,1),
    AlmacenID INT FOREIGN KEY REFERENCES Almacenes(AlmacenID) ON DELETE CASCADE,
    CodigoUbicacion NVARCHAR(50) NOT NULL, -- Código único para la ubicación
    Descripcion NVARCHAR(MAX),
    Capacidad INT, -- Capacidad de la ubicación específica
    Estado BIT NOT NULL DEFAULT 1
);
GO

------------------PROVEEDORES
CREATE TABLE Proveedores(
    ProveedorID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(50) NOT NULL,
    Telefono NVARCHAR(15) CHECK(Telefono LIKE '+[0-9]%'), -- Permite números internacionales
    Email NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(MAX),
    EstadoProv BIT NOT NULL DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE()
); GO

------------------PRODUCTO----------------------------------
CREATE TABLE Producto(
    IDProducto INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(30) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Precio DECIMAL(18, 2) NOT NULL CHECK (Precio >= 0),
    IdCategoria INT FOREIGN KEY REFERENCES Categoria(IdCategoria) ON DELETE CASCADE NOT NULL,
    ProveedorID INT FOREIGN KEY REFERENCES Proveedores(ProveedorID) ON DELETE CASCADE NOT NULL,
    UnidadID INT FOREIGN KEY REFERENCES UnidadesMedida(UnidadID) ON DELETE CASCADE NOT NULL,
    UbicacionID INT FOREIGN KEY REFERENCES UbicacionesAlmacen(UbicacionID) ON DELETE CASCADE NOT NULL,
    SKU NVARCHAR(50) UNIQUE, -- Código único para identificar el producto
    Stock INT NOT NULL DEFAULT 0 CHECK (Stock >= 0),
    EstadoProduc BIT NOT NULL DEFAULT 1
);
GO

--- Gestiona el historial de todo el tráfico de los productos de los almacenes
CREATE TABLE MovimientosInventario(
    MovimientoID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    IDProducto INT FOREIGN KEY REFERENCES Producto(IDProducto) NOT NULL,
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    TipoMovimiento NVARCHAR(20) NOT NULL CHECK (TipoMovimiento IN ('Entrada', 'Salida', 'Ajuste')),
    FechaMovimiento DATETIME DEFAULT GETDATE(),
    IdUser INT FOREIGN KEY REFERENCES Usuarios(IdUser) NOT NULL,
    AlmacenID INT FOREIGN KEY REFERENCES Almacenes(AlmacenID) NOT NULL,
    Comentario NVARCHAR(MAX),
    EstadoMovimiento BIT NOT NULL DEFAULT 1
);
GO

--- Maneja todas las transferencias de un Almacen a otro
CREATE TABLE Transferencias(
    TransferenciaID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    IDProducto INT FOREIGN KEY REFERENCES Producto(IDProducto) NOT NULL,
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    AlmacenOrigenID INT FOREIGN KEY REFERENCES Almacenes(AlmacenID) ON DELETE CASCADE NOT NULL,
    AlmacenDestinoID INT FOREIGN KEY REFERENCES Almacenes(AlmacenID) ON DELETE CASCADE NOT NULL,
    FechaTransferencia DATETIME DEFAULT GETDATE(),
    IdUser INT FOREIGN KEY REFERENCES Usuarios(IdUser) NOT NULL,
    Comentario NVARCHAR(MAX),
    EstadoTransferencia NVARCHAR(20) NOT NULL CHECK (EstadoTransferencia IN ('Pendiente', 'Completada', 'Cancelada')) DEFAULT 'Pendiente'
);
GO
