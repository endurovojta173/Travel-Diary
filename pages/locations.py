from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
#templates = Jinja2Templates(directory="templates")

@router.get("/locations", response_class=HTMLResponse)
async def locations_page(request: Request):
    """
    Zobrazí stránku Locations.
    """
    return request.app.state.templates.TemplateResponse(
        "locations.html",
        {"request": request, "title": "Locations"}
    )