from fastapi import APIRouter,HTTPException,Response,Request,Query
from core.service_handler.user.user import create_user, login_user
from v1.serializers import RegisterSchema
from v1.serializers import BookSchema
from core.service_handler.book.book import add, fetch_book,fetch_all_books
from .models import Book
from v1.config import r

router=APIRouter()


@router.post("/register")
def register_user(user:RegisterSchema):
    return create_user(user)


@router.post("/login")
def login(email:str,password:str,response:Response):
    return login_user(email,password,response)


@router.post("/logout")
def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    if session_id:
        r.delete(f"session:{session_id}")

    response.delete_cookie("session_id")

    return {"message": "Logged out"}



@router.post("/add")
def add_book(request:Request,book:BookSchema):
    return add(request,book)


@router.get("/book")
def get_book(request:Request,search:str):
    return fetch_book(request,search)

@router.get("/all")
def get_all_books(request:Request):
    return fetch_all_books(request)
