# 🛒 M8 Ecommerce
### Portafolio Final – Desarrollo Full Stack Python

![Python](https://img.shields.io/badge/Python-3.14.5-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.0.6-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue?logo=postgresql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![Git](https://img.shields.io/badge/Git-Version_Control-orange?logo=git)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 🔗 Repositorio

https://github.com/naty180482/m8_ecommerce

---

# Descripción

**M8 Ecommerce** es una aplicación web desarrollada utilizando **Django**, **PostgreSQL** y **Bootstrap 5**, creada como proyecto final del Bootcamp **Desarrollo de Aplicaciones Full Stack Python**.

El proyecto implementa un flujo completo de comercio electrónico, permitiendo la administración de productos, autenticación de usuarios, carrito de compras y registro de órdenes mediante el ORM de Django.

El objetivo fue aplicar buenas prácticas de desarrollo, separación entre frontend y backend, persistencia de datos y documentación profesional utilizando Git y GitHub.

---

# Vista previa del proyecto

## Home
![Home](assets/img/home.png)

## Catálogo
![Catálogo](assets/img/catalogo.png)

## Carrito
![Carrito](assets/img/carrito.png)

## Panel Administrador
![Admin](assets/img/admin.png)

## Compra realizada
![Checkout](assets/img/checkout.png)

---

# Características principales

## Cliente

- Inicio de sesión
- Catálogo de productos
- Detalle de productos
- Carrito de compras
- Actualización de cantidades
- Eliminación de productos
- Confirmación de compra
- Historial de pedidos

## Administrador

- Administración de productos
- Crear productos
- Editar productos
- Eliminar productos
- Gestión de categorías
- Administración mediante Django Admin

---

# Tecnologías utilizadas

| Tecnología | Uso |
|------------|----------------|
| Python | Lenguaje principal |
| Django | Framework Backend |
| PostgreSQL | Base de datos |
| Bootstrap 5 | Frontend Responsive |
| HTML5 | Plantillas |
| CSS3 | Estilos |
| JavaScript | Interactividad |
| Git | Control de versiones |
| GitHub | Repositorio |

---

# Arquitectura del proyecto
Cliente
│
▼
Bootstrap
│
Django Templates
│
Views
│
ORM Django
│
PostgreSQL

---

# Flujo de navegación
Inicio
│
▼
Login
│
▼
Catálogo
│
▼
Detalle Producto
│
▼
Agregar al carrito
│
▼
Carrito
│
▼
Confirmar compra
│
▼
Pedido registrado


---

# Estructura del proyecto
m8_ecommerce/
│
├── config/
├── tienda/
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ └── urls.py
│
├── templates/
├── static/
├── media/
├── requirements.txt
├── README.md
├── .env.example
└── manage.py

---

# Instalación

## 1. Clonar el repositorio

git clone https://github.com/naty180482/m8_ecommerce.git
cd m8_ecommerce
2. Crear entorno virtual
Windows
python -m venv venv
venv\Scripts\activate
Linux / macOS

python3 -m venv venv
source venv/bin/activate
3. Instalar dependencias
pip install -r requirements.txt

4. Crear Base de Datos PostgreSQL
CREATE DATABASE m8_ecommerce_db;
CREATE USER m8_ecommerce_user WITH PASSWORD 'ClaveSegura.2026#';
GRANT ALL PRIVILEGES ON DATABASE m8_ecommerce_db TO m8_ecommerce_user;
ALTER DATABASE m8_ecommerce_db OWNER TO m8_ecommerce_user;

5. Crear archivo .env
Tomar como referencia .env.example

Contenido:

env
SECRET_KEY=TU_SECRET_KEY
DEBUG=True
DB_NAME=m8_ecommerce_db
DB_USER=m8_ecommerce_user
DB_PASSWORD=ClaveSegura.2026#
DB_HOST=localhost
DB_PORT=5432

6. Ejecutar migraciones
python manage.py migrate

7. Crear superusuario
python manage.py createsuperuser

8. Ejecutar servidor
python manage.py runserver
Abrir: http://127.0.0.1:8000/

Credenciales de prueba
Administrador
Usuario: admin
Contraseña: admin12345

Cliente
Usuario: cliente
Contraseña: cliente12345