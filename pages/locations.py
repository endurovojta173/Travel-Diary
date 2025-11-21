from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from dependencies import locations_service
from services.locations import LocationService

router = APIRouter()

#Router for displaying locations page

@router.get("/locations", name="list_locations_with_photos_rating", response_class=HTMLResponse)
async def list_locations_with_photos_rating(
    request: Request,
    svc: LocationService = Depends(locations_service)
):
    #Získání seznamu lokací s fotkami
    locations = svc.list_locations_with_photos_rating()

    #Kontrola do konzole
    for location in locations:
        print(f"Lokace: {location['name']},rating: {location['avg_rating']}, počet fotek: {len(location['photos'])}")
        for photo in location['photos']:
            print(f" - Fotka: {photo['url']}")

    #templating engine z app.state
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "locations.html",
        {
            "request": request,
            "title": "Seznam lokací",
            "locations": locations,  # každá lokace obsahuje seznam fotek
        },
    )