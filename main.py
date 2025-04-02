import pyodbc
import pandas as pd

from enum import Enum
from typing import Optional

# from typing import Annotated
from functools import lru_cache
from fastapi import FastAPI, HTTPException, Query
from contextlib import contextmanager

from config import Settings

from datetime import date

app = FastAPI()

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

class DeliveryNoteTypeCustomer(str, Enum):
    invoice = "Factura"
    payment = "Abono"

@app.get(
    "/api/albaranes/clientes/cabeceras",
    summary="Devuelve todas las cabeceras de los albaranes de los clientes",
    description="""Cada cabecera de albarán incluye los siguientes campos:  
- `cod_cli`: código del cliente.  
- `doc_alb`: indicador del tipo de documento; puede ser `"F"` para factura o `"A"` para abono.  
- `fec_alb`: fecha del albarán.  
- `raz_cli`: nombre del cliente.  
- `tot_alb`: importe del albarán; será un valor negativo si es un abono.

Además, se puede aplicar un **filtro por el tipo de albarán** mediante el parámetro query **opcional**:  
- `deliveryNoteType`: define el tipo de albarán, permitiendo filtrar exclusivamente por `"Factura"` o `"Abono"` (internamente representados como `"F"` y `"A"` respectivamente).""",
    tags=["Albaranes de clientes"]
)
def get_cabeceras_albaranes(deliveryNoteType: Optional[DeliveryNoteTypeCustomer] = Query(None, description="**Selecciona un tipo de albarán**")):
    try:
        with get_db_connection() as conn:
            query = "SELECT cod_cli, doc_alb, fec_alb, raz_cli, tot_alb FROM pub.gvalcab"

            if deliveryNoteType:
                query += " WHERE doc_alb = ?"

                match deliveryNoteType:
                    case "Factura":
                        deliveryNoteType = "F"
                    
                    case "Abono":
                        deliveryNoteType = "A"
                    
                    case _:
                        raise HTTPException(status_code=400, detail="Invalid delivery note type")
                
                df = pd.read_sql_query(query, conn, params=(deliveryNoteType,))
            else: 
                df = pd.read_sql_query(query, conn)

            df.loc[df['doc_alb'] == 'A', 'tot_alb'] *= -1

            return {
                "status": "success", 
                "message": "Request processed successfully",  
                "results": df.to_dict(orient="records")
            }
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.get(
    "/api/albaranes/clientes/cabeceras/{year}/{month}/{day}",
    summary="Devuelve todas las cabeceras de los albaranes de los clientes de un día especifico",
    description="""Para obtener los datos, se deben proporcionar los siguientes parámetros en la URL:  
- `year`: número del año (ejemplo: 2024).  
- `month`: número del mes (ejemplo: `01` para enero, `12` para diciembre).  
- `day`: número del día (ejemplo: `01` para el primero del mes, `31` para el último día de un mes de 31 días).  

**Importante:** para los meses y días con un valor menor a **10**, se debe añadir un **0** antes del número.  

Cada cabecera de albarán incluye los siguientes campos:  
- `cod_cli`: código del cliente.  
- `doc_alb`: indicador del tipo de documento; puede ser `"F"` para factura o `"A"` para abono.  
- `fec_alb`: fecha del albarán.  
- `raz_cli`: nombre del cliente.  
- `tot_alb`: importe del albarán; será un valor negativo si es un abono.

Además, se puede aplicar un **filtro por el tipo de albarán** mediante el parámetro query **opcional**:  
- `deliveryNoteType`: define el tipo de albarán, permitiendo filtrar exclusivamente por `"Factura"` o `"Abono"` (internamente representados como `"F"` y `"A"` respectivamente).""",
    tags=["Albaranes de clientes"]
)
def get_cabeceras_albaranes_clientes(year: str, month: str, day: str, deliveryNoteType: Optional[DeliveryNoteTypeCustomer] = Query(None, description="**Selecciona un tipo de albarán**")):
    try:
        with get_db_connection() as conn:

            processed_date = date(int(year), int(month), int(day))

            query = "SELECT cod_cli, doc_alb, fec_alb, raz_cli, tot_alb FROM pub.gvalcab WHERE fec_alb = TO_DATE(?, 'YYYY-MM-DD')"

            if deliveryNoteType:
                query += " AND doc_alb = ?"

                match deliveryNoteType:
                    case "Factura":
                        deliveryNoteType = "F"
                    
                    case "Abono":
                        deliveryNoteType = "A"
                    
                    case _:
                        raise HTTPException(status_code=400, detail="Invalid delivery note type")

                df = pd.read_sql_query(query, conn, params=(processed_date.isoformat(), deliveryNoteType))
            else:
                df = pd.read_sql_query(query, conn, params=(processed_date.isoformat(),))
            
            df.loc[df['doc_alb'] == 'A', 'tot_alb'] *= -1

            return {
                "status": "success",
                "message": "Request processed successfully",  
                "results": df.to_dict(orient="records")
            }
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

class DeliveryNoteTypeSupplier(str, Enum):
    charge = "Cargo"
    payment = "Abono"

class DeliveryNotePaymentMethodSupplier(str, Enum):
    credit = "Crédito"
    cash = "Contado"

@app.get(
            "/api/albaranes/proveedores/cabeceras/",
            summary="Devuelve todas las cabeceras de los albaranes de los proveedores",
            description="""Cada cabecera de albarán de proveedor incluye los siguientes campos:
- `cod_pro`: código del proveedor.
- `fec_alc`: fecha del albarán.
- `num_alc`: número del albarán.
- `car_alc`: indicador del tipo de albarán; `true` representa un cargo, mientras que `false` representa un abono.
- `nvt_fpg`: forma de pago; `1` indica que se pagó a crédito y `0` que se pagó al contado.
- `bru_alc`: importe del albarán; se mostrará como negativo si se trata de un abono.

Además, se pueden aplicar los siguientes filtros **opcionales** mediante parámetros de consulta (**query params**):
- `deliveryNoteType`: permite filtrar exclusivamente por `"Cargo"` o `"Abono"` (internamente representados como `true` y `false` respectivamente).
- `deliveryNotePaymentMethod`: permite filtrar exclusivamente por `"Crédito"` o `"Contado"` (internamente representados como `"1"` y `"0"` respectivamente).""",
            tags=["Albaranes de proveedores"]
        )
def get_cabeceras_albaranes_proveedores(deliveryNoteType: Optional[DeliveryNoteTypeSupplier] = Query(None, description="**Selecciona un tipo de albarán**"), deliveryNotePaymentMethod: Optional[DeliveryNotePaymentMethodSupplier] = Query(None, description="**Selecciona un método de pago**")):
    try:
        with get_db_connection() as conn:

            query = "SELECT cod_pro, fec_alc, num_alc, car_alc, nvt_fpg, bru_alc FROM pub.gcpacab"

            conditions = []
            params = []
            
            if deliveryNoteType:
                match deliveryNoteType:
                    case "Cargo":
                        conditions.append("car_alc = ?")
                        params.append(True)

                    case "Abono":
                        conditions.append("car_alc = ?")
                        params.append(False)

                    case _:
                        raise HTTPException(status_code=400, detail="Invalid delivery note type")
            
            if deliveryNotePaymentMethod:
                match deliveryNotePaymentMethod:
                    case "Crédito":
                        conditions.append("nvt_fpg = ?")
                        params.append(1)

                    case "Contado":
                        conditions.append("nvt_fpg = ?")
                        params.append(0)

                    case _:
                        raise HTTPException(status_code=400, detail="Invalid payment method")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            df = pd.read_sql_query(query, conn, params=tuple(params))

            df.loc[~df['car_alc'], 'bru_alc'] *= -1

            df = df.tail(100)

            return {
                "status": "success",
                "message": "Request processed successfully",
                "results": df.to_dict(orient="records")
            }
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))