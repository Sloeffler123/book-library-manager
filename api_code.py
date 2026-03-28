import sqlite3
from fastapi import FastAPI, HTTPException
from enum import IntEnum
from pydantic import BaseModel, Field
from sql_commands import init_connection_to_sql, filter_title_author_review_date_read
from constants import DATA_BASE
api = FastAPI()

@api.get('/mybooks')
def get_main_page():
    # layout
    # title, author, your rating, your review text, date read, remove
    try:
        conn = init_connection_to_sql()
        statement = filter_title_author_review_date_read(conn)
        return {"data": statement[0]}
        
    except HTTPException:
        print("error")