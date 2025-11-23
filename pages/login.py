from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from dependencies import user_service
from services.users import UserService

router = APIRouter()

#Router for displaying login page

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Locations"}
    )


@router.post("/login")
async def login_user(request: Request,email: str,password: str,svc: UserService = Depends(user_service)):
    #Porovnání hashe
    user = svc.authenticate_user(email, password)

    if not user:
        # CHYBA: Buď neexistuje user, nebo špatné heslo (z bezpečnostních důvodů neříkáme co přesně)
        tpl = request.app.state.templates
        return tpl.TemplateResponse("login.html", {
            "request": request,
            "error_message": "Nesprávný e-mail nebo heslo.",
            "email_value": email
        })

    # ÚSPĚCH: Uložíme uživatele do Session
    request.session["user"] = {
        "id": user["id"],
        "name": user["name"],
        "role": user["id_role"]
    }

    # Přesměrujeme na domovskou stránku (nebo dashboard)
    return RedirectResponse(url="/my_profile", status_code=303)