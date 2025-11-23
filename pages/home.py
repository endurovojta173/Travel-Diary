from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying home page
@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):

    return request.app.state.templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Cestovní deník"
            "random_locations"
            "favorite_location"
            "newest_location"
        }
    )