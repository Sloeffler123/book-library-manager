
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from enum import IntEnum
from pydantic import BaseModel, Field
from sql_files.sql_commands import init_connection_to_sql
from api_files.api_helper_funcs import get_main_page_data

api = FastAPI()

templates = Jinja2Templates(directory="templates")

api.mount("/static", StaticFiles(directory="static"), name="static")

@api.get('/mybooks', include_in_schema=False)
def get_main_page(request: Request):
    # layout
    # title, author, your rating, your review text, date read, remove
    try:
        data = get_main_page_data(init_connection_to_sql())
        return templates.TemplateResponse(request, "start.html", context={"data":data})
    except HTTPException:
        print("error")