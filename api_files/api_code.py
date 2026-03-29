
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates

from enum import IntEnum
from pydantic import BaseModel, Field
from sql_commands import init_connection_to_sql, filter_title_author_review_date_read
from api_helper_funcs import get_main_page_data

api = FastAPI()

templates = Jinja2Templates(directory="templates")

@api.get('/mybooks')
def get_main_page():
    # layout
    # title, author, your rating, your review text, date read, remove
    try:
        get_main_page_data(init_connection_to_sql())
    except HTTPException:
        print("error")