import pyodbc
import pandas as pd

# from typing import Annotated
from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException
from contextlib import contextmanager

from config import Settings

from datetime import date

tags_metadata = [
    # {
    #     "name": "Describir tabla",
    #     "description": "Se obtienen las **columnas** de la tablas indicada",
    # },
    # {
    #     "name": "Albaranes por fecha completa",
    #     "description": "Se obtienen los albarenes de ese día usando un **unico parametro**, que es la fecha entera de ese día con el formato **YYYYMMDD** sin espacios",
    # },
    {
        "name": "Albaranes por día, mes y año",
        "description": "Se obtienen los albarenes de ese día usando **tres parametros diferentes**: el día, el mes y el año",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@lru_cache
def get_settings():
    return Settings()


@contextmanager
def get_db_connection():
    # Context manager para gestionar las conexiones con la DB

    # Datos para la conexion a la DB
    conn_data = get_settings()
    conn_str = (
        "DRIVER={" + conn_data.DRIVER + "};"
        f"DSN={conn_data.DSN};"
        f"HOST={conn_data.HOST};"
        f"DB={conn_data.DB};"
        f"UID={conn_data.UID};"
        f"PWD={conn_data.PWD2};"
        f"PORT={conn_data.PORT};"
    )

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
            df = df.tail(100)
            df.loc[df['doc_alb'] == 'A', 'tot_alb'] *= -1

            return {"status": "success", "message": "Request processed successfully",  "results": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

# @app.get("/api/albaranes/cabeceras/{day}", tags=["Albaranes por fecha completa"])
# def get_cabeceras_albaranes(day: str):
#     try:
#         with get_db_connection() as conn:

#             processed_date = date(int(day[:4]), int(day[4:6]), int(day[6:8]))

#             # query = f"SELECT cod_cli, doc_alb, fec_alb, raz_cli, tot_alb FROM pub.gvalcab WHERE fec_alb = {processed_date.isoformat()}"
#             query = f"SELECT cod_cli, doc_alb, fec_alb, raz_cli, tot_alb FROM pub.gvalcab WHERE fec_alb = '{processed_date.isoformat()}'"

#             print(query)
#             df = pd.read_sql_query(query, conn)
#             df.loc[df['doc_alb'] == 'A', 'tot_alb'] *= -1

#             return {"status": "success", "message": "Request processed successfully",  "results": df.to_dict(orient="records")}
#     except Exception as e:
#         raise HTTPException(status_code = 500, detail = str(e))

@app.get("/api/albaranes/cabeceras/{year}/{month}/{day}", tags=["Albaranes por día, mes y año"])
def get_cabeceras_albaranes(year: str, month: str, day: str):
    try:
        with get_db_connection() as conn:

            processed_date = date(int(year), int(month), int(day))

            query = "SELECT cod_cli, doc_alb, fec_alb, raz_cli, tot_alb FROM pub.gvalcab WHERE fec_alb = TO_DATE(?, 'YYYY-MM-DD')"

            df = pd.read_sql_query(query, conn, params=(processed_date.isoformat(),))
            df.loc[df['doc_alb'] == 'A', 'tot_alb'] *= -1

            return {"status": "success", "message": "Request processed successfully",  "results": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.get("/test/gvallin")
def get_algo():
    try:
        with get_db_connection() as conn:
            query = "SELECT TOP 5 * FROM pub.gvallin"

            df = pd.read_sql_query(query, conn)
            return {"status": "success", "message": "Request processed successfully",  "results": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))