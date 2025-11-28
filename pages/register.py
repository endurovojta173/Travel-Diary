from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from dependencies import user_service
from services.users import UserService
from model.user import UserCreate

router = APIRouter()


def get_register_form(name: str = Form(...), email: str = Form(...), password: str = Form(...)) -> dict:
    return {
        "name": name,
        "email": email,
        "password": password
    }


# Router for displaying register page
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": "Registrace"
        }
    )


@router.post("/register")
async def register_user(request: Request, form_data: dict = Depends(get_register_form), svc: UserService = Depends(user_service), ):
    try:
        user_model = UserCreate(
            name=form_data['name'],
            email=form_data['email'],
            password=form_data['password']
        )
        svc.register_user(
            name=user_model.name,
            email=user_model.email,
            password=user_model.password
        )

        return RedirectResponse(url="/login", status_code=303)
    #Chyba z pydantic verifikace
    except ValidationError as e:
        error_msg = e.errors()[0]['msg'].replace("Value error, ", "")

        return request.app.state.templates.TemplateResponse("register.html", {
            "request": request,
            "error_message": error_msg,
            "name_value": form_data['name'],
            "email_value": form_data['email']
        })
