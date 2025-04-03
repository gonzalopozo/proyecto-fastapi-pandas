# Proyecto FastAPI Pandas

[![Python](https://img.shields.io/badge/Python-3.7%2B-FFD43B?style=social&logo=python&logoColor=306998)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-%E2%9C%85-22bfda?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)  
[![Pandas](https://img.shields.io/badge/Pandas-%E2%9C%85-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)


<details>
  <summary>🇪🇸 Versión en Español</summary>

## Bienvenido a Proyecto FastAPI Pandas

Este proyecto utiliza FastAPI y Pandas para ofrecer una API de alto rendimiento, ideal para el procesamiento y análisis de datos de manera rápida y eficiente. Se ha diseñado pensando en la modularidad y escalabilidad, permitiendo en el futuro integrar una interfaz visual (Streamlit) para mejorar la experiencia de usuario.

---

## 🚀 Características

- **API súper rápida:** construida con FastAPI, ofreciendo soporte asíncrono y alta velocidad.
- **Datos con pandas:** permite procesar, analizar y transformar datos de forma sencilla.
- **Endpoints RESTful:** interfaz accesible mediante respuestas JSON para integración con múltiples clientes.
- **Arquitectura escalable:** diseño modular que facilita futuras expansiones, como la integración de una interfaz de visualización.



## 🛠 Tecnologías

- **[FastAPI](https://fastapi.tiangolo.com/):** framework moderno y rápido para construir APIs.
- **[Pandas](https://pandas.pydata.org/):** herramienta poderosa para la manipulación y análisis de datos.
- **Python 3.7+:** lenguaje de programación que garantiza un código limpio y robusto.
- **Uvicorn:** servidor ASGI para ejecutar la aplicación FastAPI con alto rendimiento.



## 📥 Cómo Empezar

### Requisitos Previos

- Python 3.7 o superior
- [pip](https://pip.pypa.io/en/stable/)

### Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/gonzalopozo/proyecto-fastapi-pandas.git
   ```

2. **Accede al directorio del proyecto:**

   ```bash
   cd proyecto-fastapi-pandas
   ```

3. **Crea un entorno virtual (recomendado):**

   - **Linux/Mac:**
     ```bash
     python -m venv env
     source env/bin/activate
     ```
   - **Windows PowerShell:**
     ```powershell
     python -m venv env
     .\env\Scripts\Activate.ps1
     ```
   - **Windows CMD/Git Bash:**
     ```bash
     python -m venv env
     env\Scripts\activate
     ```

4. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

### Ejecución de la Aplicación

Inicia el servidor FastAPI con Uvicorn:

```bash
uvicorn main:app --reload
```

Luego, abre tu navegador y visita [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para explorar la documentación interactiva de la API proporcionada por Swagger UI.

## 📁 Estructura del Proyecto

```
proyecto-fastapi-pandas/
├── main.py             # Aplicación principal de FastAPI
├── requirements.txt    # Lista de dependencias
└── ...                 # Otros módulos y archivos de configuración
```

## 🔮 Futuras Mejoras

- **[Streamlit Frontend](https://github.com/usuario/future-streamlit-repo):** se planea desarrollar una interfaz visual con Streamlit para mostrar gráficos y tablas de forma interactiva.
- **Ampliación de Endpoints de Datos:** incorporación de funcionalidades analíticas más avanzadas.

---

## 🙏 Agradecimientos

- **FastAPI:** gracias a [FastAPI](https://fastapi.tiangolo.com/) por ofrecer una herramienta tan robusta.
- **Pandas:** agradecimiento a [Pandas](https://pandas.pydata.org/) por facilitar el análisis y procesamiento de datos.

</details>

<details>
  <summary>🇬🇧 English Version</summary>

## Welcome to Proyecto FastAPI Pandas

This project leverages FastAPI and Pandas to deliver a high-performance API perfect for fast and efficient data processing and analysis. It has been designed with modularity and scalability in mind, paving the way for future enhancements like a dedicated Streamlit visualization interface.

## 🚀 Features

- **Lightning Fast API:** built with FastAPI, offering asynchronous support and high-speed performance.
- **Data Magic with Pandas:** easily process, analyze, and transform your data using Pandas.
- **RESTful Endpoints:** accessible JSON endpoints for seamless integration with multiple clients.
- **Scalable Architecture:** a modular design that facilitates future expansions, such as integrating a visualization interface.

## 🛠 Technologies

- **[FastAPI](https://fastapi.tiangolo.com/):** a modern, fast web framework for building APIs.
- **[Pandas](https://pandas.pydata.org/):** a powerful tool for data manipulation and analysis.
- **Python 3.7+:** core programming language ensuring a clean and robust codebase.
- **Uvicorn:** ASGI server used to run the FastAPI application with top-notch performance.

## 📥 Getting Started

### Prerequisites

- Python 3.7 or later
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/gonzalopozo/proyecto-fastapi-pandas.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd proyecto-fastapi-pandas
   ```

3. **Create a virtual environment (recommended):**

   - **Linux/Mac:**
     ```bash
     python -m venv env
     source env/bin/activate
     ```
   - **Windows PowerShell:**
     ```powershell
     python -m venv env
     .\env\Scripts\Activate.ps1
     ```
   - **Windows CMD/Git Bash:**
     ```bash
     python -m venv env
     env\Scripts\activate
     ```

4. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

Then, open your browser and visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the interactive API documentation powered by Swagger UI.

## 📁 Project Structure

```
proyecto-fastapi-pandas/
├── main.py             # Main FastAPI application
├── requirements.txt    # Dependencies list
└── ...                 # Additional modules and configuration files
```

## 🔮 Future Developments

- **[Streamlit Frontend](https://github.com/usuario/future-streamlit-repo):** a dedicated visualization interface using Streamlit is planned to display interactive graphs and charts.
- **Enhanced Data Endpoints:** expansion of the API with more sophisticated data analytics features.

## 🙏 Acknowledgments

- **FastAPI:** thanks to [FastAPI](https://fastapi.tiangolo.com/) for providing such a robust and user-friendly framework.
- **Pandas:** gratitude to [Pandas](https://pandas.pydata.org/) for simplifying data analysis and manipulation.

</details>
