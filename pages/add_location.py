from fastapi import FastAPI, Request, APIRouter, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies import locations_service
from model.location import LocationCreate
from services.locations import LocationService

router = APIRouter()

def get_location_form(name: str = Form(...),description: str = Form(...)) -> LocationCreate:
    return LocationCreate(name=name, description=description)

#router for displaying add location page
@router.get("/add_location", response_class=HTMLResponse)
async def add_location_page(request: Request):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)

    return request.app.state.templates.TemplateResponse(
        "add_location.html",
        {
            "request": request,
            "title": "Přidat lokaci"
        }
    )


@router.post("/add_location")
async def add_location(request: Request, location_data: LocationCreate = Depends(get_location_form), files: list[UploadFile] = File(...), svc: LocationService = Depends(locations_service)):
    svc.add_new_location(
        location_name=location_data.name,
        location_description=location_data.description,
        id_user=request.session['user']['id'],
        #files=files
    )
    return RedirectResponse(url="/my_profile", status_code=303)