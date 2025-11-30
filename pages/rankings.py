from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from dependencies import locations_service
from services.list_locations import LocationService

router = APIRouter()


#Router for displaying rankings page
@router.get("/rankings")
async def rankings_page(request: Request, sort:str = "sort", svc: LocationService = Depends(locations_service) ):
    titles_map = {
        "rating": "Nejoblíbenější lokace podle hodnocení",
        "comments": "Nejvíce diskutované lokace",
        "newest": "Nejnovější přidané lokace"
    }
    page_title = titles_map.get(sort, "Žebříček lokací")

    locations = {}
    if sort == "rating":
        locations = svc.list_locations_by_avg_rating()
    elif sort == "comments":
        locations = svc.list_locations_by_most_comments()
    elif sort == "newest":
        locations = svc.list_locations_by_newest()
    else:
        locations = svc.list_locations_by_newest()

    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "rankings.html",
        {
            "request": request,
            "title": page_title,
            "locations": locations
        }
    )