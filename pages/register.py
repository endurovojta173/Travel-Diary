from fastapi import APIRouter,Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import user_service
from services.users import UserService
from model.user import UserCreate
router = APIRouter()

#Router for displaying register page
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
async def register_user(request: Request, name: str, email: str, password: str, svc: UserService = Depends(user_service),):
    try:
        svc.register_user(name, email, password)

        #ÚSPĚCH -> Přesměrujeme na přihlášení
        return RedirectResponse(url="/login", status_code=303)

    except HTTPException as e:
        # CHYBA -> Znovu vykreslíme formulář
        tpl = request.app.state.templates
        return tpl.TemplateResponse("register.html", {
            "request": request,
            "error_message": e.detail,
            "name_value": name,
            "email_value": email
        })