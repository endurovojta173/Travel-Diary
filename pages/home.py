from fastapi import APIRouter,Request, Depends
from fastapi.responses import HTMLResponse
from dependencies import locations_service
from services.list_locations import LocationService

router = APIRouter()

#Router for displaying home page
@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request,svc: LocationService = Depends(locations_service)):

    random_locations = svc.get_five_random_locations()
    favorite_location = svc.get_most_favorite_location()
    newest_location = svc.get_newest_location()
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Cestovní deník",
            "random_locations": random_locations,
            "favorite_location": favorite_location,
            "newest_location": newest_location
        }
    )