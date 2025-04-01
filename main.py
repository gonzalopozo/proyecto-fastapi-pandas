import pyodbc
import pandas as pd

# from typing import Annotated
from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException
from contextlib import contextmanager

from config import Settings

@lru_cache
def get_settings():
    return Settings()

app = FastAPI()

@contextmanager
def get_db_connection():
    # Context manager para gestionar las conexiones con la DB

    # Datos para la conexion a la DB
    conn_data = get_settings()
    conn_str = (
        f"DRIVER={conn_data.DRIVER};"
        f"DSN={conn_data.DSN};"
        f"HOST={conn_data.HOST};"
        f"DB={conn_data.DB};"
        f"UID={conn_data.UID};"
        f"PWD={conn_data.PWD};"
        f"PORT={int(conn_data.PORT)}"
    )

    print(conn_str)

    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        yield conn
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.get("/test")
def test_api():
    try:
        with get_db_connection() as conn:
            query = "SELECT nom_fis, fec_fac, fvt_ppg FROM pub.gmtesoc"
            df = pd.read_sql_query(query, conn)  # Datos obtenidos se devuelven como un objeto de tipo DataFrame
            df = df.head(10)  # Limite de 10 filas para probar la API
            
            return {"message": "Connected via pyodbc", "results": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.get("/api/albaranes/cabeceras")
def get_cabeceras_albaranes():
    try:
        with get_db_connection() as conn:
            query = "SELECT cod_cli, doc_alb, fec_alb, raz_cli, tot_alb FROM pub.gvalcab"
            df = pd.read_sql_query(query, conn)
            df = df.head(100)
            df.loc[df['doc_alb'] == 'A', 'tot_alb'] *= -1

            return {"status": "success", "message": "Request processed successfully",  "results": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
