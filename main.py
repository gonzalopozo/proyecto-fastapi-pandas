import pyodbc
from fastapi import FastAPI, HTTPException
from contextlib import contextmanager

# Your existing ODBC connection string
conn_str = (
    "DRIVER=;"
    "DSN=;"
    "HOST=;"
    "DB=;"
    "UID=;"
    "PWD=;"
    "PORT="
)

app = FastAPI()

@contextmanager
def get_db_connection():
    # Context manager for database connections
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
            cursor = conn.cursor()
            cursor.execute("SELECT nom_fis, fec_fac, fvt_ppg FROM pub.gmtesoc")
            rows = cursor.fetchmany(100)

            # Column names for dictionary keys
            columns = ["nom_fis", "fec_fac", "fvt_ppg"]

            # Use zip to map column names to values
            result = [dict(zip(columns, row)) for row in rows]

            return {"message": "Connected via pyodbc", "results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
