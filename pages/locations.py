from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse

from dependencies import locations_service
from services.locations import LocationService

router = APIRouter()

#Router for displaying locations page
@router.get("/locations", response_class=HTMLResponse)
async def locations_page(request: Request):

    return request.app.state.templates.TemplateResponse(
        "locations.html",
        {"request": request, "title": "Locations"}
    )

@router.get("/locations-ui", response_class=HTMLResponse)
async def locations_ui(request: Request,svc: LocationService = Depends(locations_service)):
    # získání seznamu lokací z databáze
    locations = svc.list_locations()
    for location in locations:
        print(location.values())
    # templating engine z app.state
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "locations.html",
        {
            "request": request,
            "title": "Seznam míst",
            "locations": locations,
        },
    )
