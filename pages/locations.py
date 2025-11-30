from fastapi import Request, APIRouter, Depends,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import locations_service
from dependencies import location_comments_service
from services.list_locations import LocationService
from services.location_comments import LocationCommentsService

router = APIRouter()

#Router for displaying locations page

@router.get("/locations", name="list_locations_with_photos_rating", response_class=HTMLResponse)
async def list_locations_with_photos_rating(request: Request,svc: LocationService = Depends(locations_service)):
    #Získání seznamu lokací s fotkami
    locations = svc.list_locations_with_photos_rating()

    #templating engine z app.state
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "locations.html",
        {
            "request": request,
            "title": "Seznam lokací",
            "locations": locations,  # Seznam lokací - údaje o lokaci + fotky + Rating
        },
    )

@router.get("/locations/{location_id}", name="location_detail", response_class=HTMLResponse)
async def location_detail(request: Request, location_id:int, svc_location: LocationService = Depends(locations_service), svc_comments: LocationCommentsService = Depends(location_comments_service)):
    location = svc_location.get_location_by_id_with_photos_and_rating(location_id)
    comments = svc_comments.list_comments(location_id)
    user_status = {"is_favorite":False, "is_visited":False}

    user = request.session.get("user")

    if user:
        user_status = svc_location.get_user_interaction_status(user["id"], location_id)

    return request.app.state.templates.TemplateResponse(
        "location-detail.html",
        {
            "request": request,
            "title": location["name"],
            "location": location,  #Všechny informace o lokaci
            "comments": comments,
            "user_status": user_status #Informace zda uživatel má přidanou lokaci do favorite/visited
        },
    )

#Adding to favorite
@router.post("/locations/{location_id}/favorite/add")
async def add_favorite(location_id:int, request: Request, svc: LocationService = Depends(locations_service)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    else:
        svc.add_location_to_favorite(user["id"], location_id)
        return RedirectResponse(url=f"/locations/{location_id}", status_code=303)

#Adding to visited
@router.post("/locations/{location_id}/visited/add")
async def add_visited(location_id:int, request: Request, svc: LocationService = Depends(locations_service)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    else:
        svc.add_location_to_visited(user["id"], location_id)
        return RedirectResponse(url=f"/locations/{location_id}", status_code=303)


@router.post("/locations/{location_id}/favorite/remove")
async def remove_from_favorite(location_id:int, request: Request, svc: LocationService = Depends(locations_service)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    else:
        svc.remove_location_from_favorite(user["id"], location_id)
        return RedirectResponse(url=f"/locations/{location_id}", status_code=303)

@router.post("/locations/{location_id}/visited/remove")
async def remove_from_visited(location_id:int, request: Request, svc: LocationService = Depends(locations_service)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    else:
        svc.remove_location_from_visited(user["id"], location_id)
        return RedirectResponse(url=f"/locations/{location_id}", status_code=303)

@router.post("/locations/{location_id}/add_comment")
async def add_comment(location_id:int ,request: Request, svc: LocationCommentsService = Depends(location_comments_service), comment_text:str = Form(...)):
    svc.add_comment_to_location(request.session["user"]["id"], location_id, comment_text)
    return RedirectResponse(url=f"/locations/{location_id}", status_code=303)
