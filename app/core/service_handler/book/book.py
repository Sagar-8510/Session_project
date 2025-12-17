import json

from core.service_handler.user.sessions import get_session
from v1.models import Book
from fastapi import HTTPException, Request, Response
from mongoengine import Q
from v1.config import r


def add(request: Request, book):
    try:
        session_id = request.cookies.get("session_id")

        if not session_id:
            raise HTTPException(status_code=401, detail="Not authenticated")

        session = get_session(session_id)

        if not session:
            raise HTTPException(status_code=401, detail="Session Expired")

        if Book.objects(title=book.title).first():
            raise HTTPException(status_code=400, detail="Book is already exist")

        new_book = Book(**book.dict())
        new_book.save()
        return {"Message": f"New Book -> {new_book.title} is  added"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


# def fetch_book(request:Request,search:str):
#     session_id = request.cookies.get("session_id")

#     if not session_id:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     session = get_session(session_id)

#     if not session:
#         raise HTTPException(status_code=401, detail="Session Expired")

#     book=Book.objects.get(Q(title=search)|Q(author=search))
#     if not book:
#         raise HTTPException(status_code=404,detail="Not found")

#     return {"Title":book.title,"Author":book.author,"Description":book.description}


def fetch_book(request: Request, search: str):
    try:
        session_id = request.cookies.get("session_id")

        if not session_id:
            raise HTTPException(status_code=401, detail="Not authenticated")

        session = get_session(session_id)

        if not session:
            raise HTTPException(status_code=401, detail="Session Expired")

        cache_key = "book"

        cached_data = r.get(cache_key)

        if cached_data:
            data = json.loads(cached_data)
            return {"Cache": data}

        book = Book.objects.get(Q(title=search) | Q(author=search))
        if not book:
            raise HTTPException(status_code=404, detail="Not found")

        book_data = book.to_mongo().to_dict()
        book_data["_id"] = str(book_data["_id"])

        r.set(cache_key, json.dumps(book_data), ex=30)

        return {"From_DB": book_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


def fetch_all_books(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session(session_id)

    if not session:
        raise HTTPException(status_code=401, detail="Session Expired")

    book = Book.objects()
    if not book:
        raise HTTPException(status_code=404, detail="Not found")

    return {"From_DB": book}


# def fetch_all_books(request:Request):
#     session_id = request.cookies.get("session_id")

#     if not session_id:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     session = get_session(session_id)

#     if not session:
#         raise HTTPException(status_code=401, detail="Session Expired")

#     cache_key = "books"

#     cached_data = r.get(cache_key)

#     if cached_data:
#         data = json.loads(cached_data)
#         return {"Cache": data}

#     book = Book.objects()
#     if not book:
#         raise HTTPException(status_code=404, detail="Not found")

#     book_list=[]
#     for i in book:
#         book_data = i.to_mongo().to_dict()
#         book_data["_id"] = str(book_data["_id"])
#         book_list.append(book_data)
#     # book_data = book.to_mongo().to_dict()
#     # book_data["_id"] = str(book_data["_id"])

#     r.set(cache_key, json.dumps(book_list), ex=30)

#     return {"From_DB": book_list}
