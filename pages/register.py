from fastapi import APIRouter,Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import user_service
from services.users import UserService
from model.user import UserCreate
router = APIRouter()

def get_register_form(name:str = Form(...), email:str = Form(...), password:str = Form(...))->UserCreate:
    return UserCreate(name = name,email = email, password = password)



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
async def register_user(request: Request, user_data: UserCreate = Depends(get_register_form), svc: UserService = Depends(user_service),):
    try:
        svc.register_user(name = user_data.name,email= user_data.email, password = user_data.password)

        #ÚSPĚCH -> Přesměrujeme na přihlášení
        return RedirectResponse(url="/login", status_code=303)

    except HTTPException as e:
        # CHYBA -> Znovu vykreslíme formulář
        tpl = request.app.state.templates
        return tpl.TemplateResponse("register.html", {
            "request": request,
            #"error_message": e.detail,
            "name_value": user_data.name,
            "email_value": user_data.email
        })