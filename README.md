
# 📺 Gestor de Series y Actores

Este es un proyecto de escritorio desarrollado en **Python** utilizando **Tkinter** como interfaz gráfica.  
Permite gestionar **series** y **actores/actrices**, almacenando información básica como nombre, año de estreno, número de temporadas y un enlace a IMDb.

---

## 🚀 Características principales

- Registrar nuevas series y actores/actrices.
- Actualizar información existente.
- Eliminar registros.
- Visualizar detalles de cada serie o actor.
- Abrir enlaces de IMDb directamente desde la aplicación.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.x**
- **Tkinter** (interfaz gráfica)
- **Webbrowser** (para abrir enlaces)
- **Estructura basada en clases** (`Serie`, `ActorActriz`, `Persistencia`).

---

## 📂 Estructura del proyecto

```plaintext
app/
├── actor.py            # Clase ActorActriz
├── persistencia.py     # Clase Persistencia (manejo de datos)
├── serie.py            # Clase Serie
├── visual.py           # Interfaz gráfica principal
README.md           # Documentación del proyecto
```
## Cómo ejecutar el proyecto
Asegúrate de tener Python 3.x instalado en tu computadora.  
Las librerias usadas son las estandar de python, asi que no es necesario instalar ninguna
Clona este repositorio:
``` 
git clone https://github.com/SantiagoJimenez0304/Corte-Programacion.git
cd app
```
# Ejecuta la aplicación:
```
python visual.py

```
Realizado por:  
Santiago Jimenez - Enzo Gonzalez - Luis Daconte




