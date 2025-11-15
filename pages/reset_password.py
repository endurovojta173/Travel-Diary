from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying reset password page
@router.get("/reset_password", response_class=HTMLResponse)
async def reset_password_page(request: Request):

    return request.app.state.templates.TemplateResponse(
        "reset_password.html",
        {"request": request, "title": "Locations"}
    )