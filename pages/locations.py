from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse

from dependencies import locations_service
from services.locations import LocationService

router = APIRouter()

#Router for displaying locations page
@router.get("/locations", response_class=HTMLResponse)
async def locations_page(request: Request, svc: LocationService = Depends(locations_service)):



    #Výpis všech lokací
    locations = svc.list_locations()
    # Ověření pro consoli
    for location in locations:
        print("1. test")
        print(type(locations))
        print(location.values())


    #Co router vrací stránce jako proměnné
    return request.app.state.templates.TemplateResponse(
        "locations.html",
        {
            "request": request,
            "title": "Lokace",
            "locations": locations,

        },
    )

@router.get("/locations/list", name="list_locations",response_class=HTMLResponse)
async def list_locations(request: Request, svc: LocationService = Depends(locations_service)):
    # získání seznamu lokací z databáze
    locations = svc.list_locations()
    #Ověření pro consoli
    for location in locations:
        print("1. test")
        print(type(locations))
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
