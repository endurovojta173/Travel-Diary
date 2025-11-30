from fastapi import APIRouter,Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import locations_service
from dependencies import user_service
from services.list_locations import LocationService
from services.users import UserService
router = APIRouter()

#Router for displaying my profile page
@router.get("/my_profile", response_class=HTMLResponse)
async def my_profile_page(request: Request, svc_location: LocationService = Depends(locations_service), svc_user: UserService = Depends(user_service)):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)


    user_id =  request.session.get('user')['id']
    #Locations
    my_added_locations = svc_location.list_locations_added_by_concrete_user(user_id)
    my_favorite_locations = svc_location.list_my_favorite_locations(user_id)
    my_visited_locations = svc_location.list_my_visited_locations(user_id)
    my_pending_locations = svc_location.list_my_locations_with_pending_status(user_id)
    #Users
    user_stats = svc_user.get_user_statistics(user_id)
    return request.app.state.templates.TemplateResponse(
        "my_profile.html",
        {
            "request": request,
            "title": "Můj profil",
            "my_added_locations": my_added_locations,
            "my_favorite_locations": my_favorite_locations,
            "my_visited_locations": my_visited_locations,
            "my_pending_locations": my_pending_locations,
            "user_stats": user_stats
        }
    )