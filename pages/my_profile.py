from fastapi import APIRouter,Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import locations_service
from services.locations import LocationService
router = APIRouter()

#Router for displaying my profile page
@router.get("/my_profile", response_class=HTMLResponse)
async def my_profile_page(request: Request , svc: LocationService = Depends(locations_service)):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)

    #Locations added by this user
    my_added_locations = svc.list_locations_added_by_concrete_user(request.session.get('user')['id'])
    return request.app.state.templates.TemplateResponse(
        "my_profile.html",
        {
            "request": request,
            "title": "Můj profil",
            "my_added_locations": my_added_locations
        }
    )