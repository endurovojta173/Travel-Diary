from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from dependencies import user_service
from services.users import UserService
from model.user import UserLogin

router = APIRouter()


def get_login_form(email:str = Form(...),password:str = Form(...))->UserLogin:
    return UserLogin(email=email,password=password)

#Router for displaying login page
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Přihlášení"
        }
    )


@router.post("/login")
async def login_user(request: Request, login_data: UserLogin = Depends(get_login_form),svc: UserService = Depends(user_service)):
    #Porovnání hashe
    user = svc.authenticate_user(login_data.email, login_data.password)

    if not user:
        # CHYBA: Buď neexistuje user, nebo špatné heslo
        tpl = request.app.state.templates
        return tpl.TemplateResponse("login.html", {
            "request": request,
            "error_message": "Nesprávný e-mail nebo heslo.",
            "email_value": login_data.email
        })

    #Uložíme uživatele do Session
    request.session["user"] = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["id_role"]
    }

    #Dashboard
    return RedirectResponse(url="/my_profile", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse(url="/login", status_code=303)