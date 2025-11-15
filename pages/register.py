from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying register page
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):

    return request.app.state.templates.TemplateResponse(
        "register.html",
        {"request": request, "title": "Locations"}
    )