from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying reset password page
@router.get("/reset_password", response_class=HTMLResponse)
async def reset_password_page(request: Request):

    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "reset-password.html",
        {
            "request": request,
            "title": "Zapomenuté heslo"
        }
    )