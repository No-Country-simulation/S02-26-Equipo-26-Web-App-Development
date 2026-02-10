# Documentación del Sistema de Base de Datos: Medicae2

## 1. Descripción General
Medicae2 es un sistema diseñado para la gestión y vinculación entre pacientes y cuidadores. La base de datos está normalizada para garantizar la integridad de los datos y utiliza un modelo de especialización de usuarios para manejar distintos roles (Administradores, Cuidadores y Pacientes) bajo una estructura común.

## 2. Tecnologías y Herramientas
* **Motor de Base de Datos:** PostgreSQL
* **Entorno de Desarrollo:** Visual Studio Code / pgAdmin 4
* **Lenguaje:** SQL (DDL y DML)

## 3. Diccionario de Datos

### 3.1 Tipos de Datos Personalizados (Enums)
Para restringir los valores permitidos y asegurar la integridad lógica, se definieron los siguientes tipos:

* **user_role:** Define los roles del sistema (Admin, Caregiver, Patient).
* **doc_type:** Tipos de documentos aceptados (ID_card, Criminal_record, Certification, Insurance).
* **doc_status:** Estados de validación de documentos (Pending, Approved, Rejected).
* **payment_status:** Estados de transacciones financieras (Pending, Success, Failed).

### 3.2 Estructura de Tablas

| Tabla | Descripción |
| :--- | :--- |
| **LOCATION** | Almacena la ubicación geográfica (país y ciudad) de los usuarios. |
| **USER** | Tabla principal que contiene los datos comunes de todos los usuarios del sistema. |
| **PATIENT** | Especialización que contiene la historia clínica de los pacientes. |
| **CAREGIVER** | Especialización que almacena datos laborales y financieros de los cuidadores. |
| **ADMIN** | Especialización para los usuarios con privilegios de gestión. |
| **FAMILY** | Almacena la relación de contacto familiar asociada a un paciente. |
| **DOCUMENT** | Gestiona los archivos enviados por los cuidadores para su verificación. |
| **PAYMENT** | Registra las transacciones económicas y su estado. |
| **SHIFT_REPORT** | Vincula al paciente, cuidador y pago en un reporte detallado de turno. |

## 4. Guía de Instalación y Despliegue

Para inicializar la base de datos correctamente, se deben ejecutar los scripts en el orden que se detalla a continuación para evitar errores de dependencias de claves foráneas:

### Paso 1: Creación de la Base de Datos
Ejecutar el archivo `00_init_db.sql`:
```sql
CREATE DATABASE Medicae2
WITH 
ENCODING = 'UTF8'
CONNECTION LIMIT = -1;

### Paso 2: Definición de Tipos de Datos
Ejecutar el archivo `01_types.sql`. Este paso es obligatorio antes de crear las tablas, ya que define los dominios personalizados que validan los roles y estados del sistema:
- `user_role`: Clasificación de usuarios (Admin, Caregiver, Patient).
- `doc_type`: Categorización de archivos (ID_card, Criminal_record, etc.).
- `doc_status`: Flujo de aprobación (Pending, Approved, Rejected).
- `payment_status`: Control de transacciones (Pending, Success, Failed).

### Paso 3: Creación de Tablas y Relaciones
Ejecutar el archivo `02_tables.sql`. El script ha sido organizado para respetar la integridad referencial en el siguiente orden:

1. **Entidades Base:** `LOCATION` y la tabla central `"USER"`.
2. **Especializaciones:** Creación de `PATIENT`, `CAREGIVER` y `ADMIN` vinculadas por `user_id`.
3. **Entidades Periféricas:** `FAMILY` (dependiente de Patient) y `DOCUMENT` (dependiente de Caregiver y Admin).
4. **Gestión Financiera y Operativa:** `PAYMENT` y `SHIFT_REPORT`, que consolidan la relación entre todas las entidades anteriores.

## 5. Decisiones de Diseño
* **Integridad Referencial:** Se implementó la cláusula `ON DELETE CASCADE` en las tablas de especialización. Esto garantiza que la eliminación de un registro en la tabla `"USER"` limpie automáticamente los datos asociados en las tablas de rol, manteniendo la base de datos libre de registros huérfanos.
* **Seguridad de Sintaxis:** Se utiliza el identificador `"USER"` entre comillas dobles para evitar colisiones con palabras reservadas del motor PostgreSQL, asegurando la compatibilidad del script.
* **Escalabilidad:** El uso de tipos `SERIAL` para las claves primarias y `DECIMAL(10,2)` para campos monetarios permite que el sistema escale en volumen de datos y precisión financiera sin ajustes estructurales adicionales.

---

**Proyecto:** Medicae2  
**Entorno de Entrega:** GitHub Repository  
**Estado:** Desarrollo - Estructura de Base de Datos  
**Fecha:** Febrero 2026