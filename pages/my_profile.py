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
    user_id =  request.session.get('user')['id']
    my_added_locations = svc.list_locations_added_by_concrete_user(user_id)
    my_favorite_locations = svc.list_my_favorite_locations(user_id)
    my_visited_locations = svc.list_my_visited_locations(user_id)
    my_pending_locations = svc.list_my_locations_with_pending_status(user_id)
    return request.app.state.templates.TemplateResponse(
        "my_profile.html",
        {
            "request": request,
            "title": "Můj profil",
            "my_added_locations": my_added_locations,
            "my_favorite_locations": my_favorite_locations,
            "my_visited_locations": my_visited_locations,
            "my_pending_locations": my_pending_locations
        }
    )