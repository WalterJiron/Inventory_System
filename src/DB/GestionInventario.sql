
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

--------------------------------------------------- TABLA DE PROVEEDORES ---------------------------------------------------

CREATE TABLE Proveedore(
    ProveedorID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(50) NOT NULL,
    Telefono NVARCHAR(8) CHECK(Telefono LIKE'[2|5|7|8][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') NOT NULL UNIQUE,
    Email NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(MAX),
    EstadoProv BIT DEFAULT 1
);
GO

CREATE TABLE HistorialProveedor(
    HistorialID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    ProveedorID INT FOREIGN KEY REFERENCES Proveedore(ProveedorID) NOT NULL,
    Nombre NVARCHAR(50) NOT NULL,
    Telefono NVARCHAR(8) CHECK(Telefono LIKE'[2|5|7|8][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') NOT NULL,
    Gmail NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(MAX),
    FechaCambio DATETIME DEFAULT GETDATE(),
    IdUser INT FOREIGN KEY REFERENCES Usuarios(IdUser) NOT NULL
);
GO

--------------------------------------------------- TABLA DE PRODUCTOS ---------------------------------------------------

CREATE TABLE Categorias(
    IdCategoria INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(35) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Estado BIT DEFAULT 1,
);
GO

CREATE TABLE SubCartegory(
    IdSubCategory INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    NameSubCategory NVARCHAR(35) NOT NULL,
    DescrypSubCategory NVARCHAR(MAX),
    Category INT FOREIGN KEY REFERENCES Categorias(IdCategoria) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    CreateDate DATETIME DEFAULT GETDATE(),
    Estado BIT DEFAULT 1
);
GO

CREATE TABLE UnidadesMedida(
    UnidadID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(25) NOT NULL,
    Abreviatura NVARCHAR(10),
    Estado BIT DEFAULT 1
);
GO

CREATE TABLE Productos(
    IDProducto INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Nombre NVARCHAR(30) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Precio DECIMAL(18, 2) NOT NULL,
    IdSubCategory INT FOREIGN KEY REFERENCES SubCartegory(IdSubCategory) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    ProveedorID INT FOREIGN KEY REFERENCES Proveedore(ProveedorID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    UnidadID INT FOREIGN key  REFERENCES UnidadesMedida(UnidadID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    Stock INT NOT NULL,
    EstadoProduc BIT DEFAULT 1
);
GO

--- Manejar la fecha de vencimiento de los productos
CREATE TABLE Lotes(
    LoteID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    IDProducto INT FOREIGN KEY REFERENCES Productos(IDProducto) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    NumeroLote NVARCHAR(50) NOT NULL,
    FechaCaducidad DATETIME,
    Cantidad INT NOT NULL,
    EstadoLote BIT DEFAULT 1
);
GO

CREATE TABLE HistorialProductos(
    HistorialID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    IDProducto INT FOREIGN KEY REFERENCES Productos(IDProducto) NOT NULL,
    Nombre NVARCHAR(30) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Precio DECIMAL(18, 2) NOT NULL,
    IdCategoria INT  FOREIGN KEY REFERENCES Categorias(IdCategoria) NOT NULL,
    ProveedorID INT FOREIGN KEY REFERENCES Proveedore(ProveedorID) NOT NULL,
    Stock INT NOT NULL,
    FechaCambio DATETIME DEFAULT GETDATE(),
    IdUser INT FOREIGN KEY REFERENCES Usuarios(IdUser) NOT NULL,
);
GO

--------------------------------------------------- ALMACENES ---------------------------------------------------
CREATE TABLE Almacenes(
    IdAmacen INT PRIMARY KEY IDENTITY,
    NameAlmacen NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(MAX),
    CreationDateAlmac DATETIME DEFAULT GETDATE(),
    Estado BIT DEFAULT 1
);
GO

--- Gestiona el historial de todo el trafoco de los productos de los almacenes
CREATE TABLE MovimientosInventario(
    MovimientoID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    IDProducto INT FOREIGN KEY REFERENCES Productos(IDProducto) NOT NULL,
    Cantidad INT NOT NULL,
    TipoMovimiento NVARCHAR(50) NOT NULL,
    FechaMovimiento DATETIME NOT NULL,
    IdUser INT FOREIGN KEY REFERENCES Usuarios(IdUser) NOT NULL,
    IdAmacen INT FOREIGN KEY REFERENCES Almacenes(IdAmacen) NOT NULL,
    EstadoMOvimiento BIT DEFAULT 1
);
GO

--- Maneja todas las transaferencias de un Almacen a otro 
CREATE TABLE Transferencias(
    TransferenciaID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    IDProducto INT FOREIGN KEY REFERENCES Productos(IDProducto) NOT NULL,
    Cantidad INT NOT NULL,
    AlmacenOrigenID INT FOREIGN KEY REFERENCES Almacenes(IdAmacen) NOT NULL,
    AlmacenDestinoID INT FOREIGN KEY REFERENCES Almacenes(IdAmacen) NOT NULL,
    FechaTransferencia DATETIME NOT NULL,
    IdUser INT FOREIGN KEY REFERENCES Usuarios(IdUser) NOT NULL,
    EstadoTrasferencia BIT DEFAULT 1
);
GO