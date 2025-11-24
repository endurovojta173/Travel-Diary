from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

#router for displaying add location page
@router.get("/add_location", response_class=HTMLResponse)
async def add_location_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "add_location.html",
        {
            "request": request,
            "title": "Přidat lokaci"
        }
    )
