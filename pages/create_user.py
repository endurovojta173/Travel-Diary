from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from dependencies import user_service
from services.users import UserService
from model.user import UserCreate, UserCreateWithRole

router = APIRouter()


def get_user_create_form(name: str = Form(...), email: str = Form(...), password: str = Form(...),
                         role: int = Form(...)) -> dict:
    return {
        "name": name,
        "email": email,
        "password": password,
        "role": role
    }


# Router for displaying register page
@router.get("/create_user", response_class=HTMLResponse)
async def create_user_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "create_user.html",
        {
            "request": request,
            "title": "Vytvořit nového uživatele"
        }
    )


@router.post("/create_user")
async def create_user(request: Request, form_data: dict = Depends(get_user_create_form),svc: UserService = Depends(user_service)):
    try:
        user_model = UserCreateWithRole(
            name=form_data['name'],
            email=form_data['email'],
            password=form_data['password'],
            role=form_data['role']
        )
        svc.create_user(
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            role=user_model.role
        )

        return request.app.state.templates.TemplateResponse("create_user.html", {
            "request": request,
            "error_message": "Uživatel byl úspěšně vytvořen :)",
        })

    # Chyba z pydantic verifikace
    except ValidationError as e:
        error_msg = e.errors()[0]['msg'].replace("Value error, ", "")

        return request.app.state.templates.TemplateResponse("create_user.html", {
            "request": request,
            "error_message": error_msg,
            "name_value": form_data['name'],
            "email_value": form_data['email']
        })
    #Uživatel s tímto emailem již existuje
    except ValueError as e:
        return request.app.state.templates.TemplateResponse("create_user.html", {
            "request": request,
            "error_message": str(e),
            "name_value": form_data['name'],
            "email_value": form_data['email']
        })
