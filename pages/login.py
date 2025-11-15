from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying login page

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Locations"}
    )