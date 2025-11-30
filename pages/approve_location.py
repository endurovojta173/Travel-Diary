from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import approve_location_service
from dependencies import locations_service
from services.list_locations import LocationService
from services.approve_location import ApproveLocationService
router = APIRouter()

#Router for displaying my profile page
@router.get("/approve_location", name="approve_location_page", response_class=HTMLResponse)
async def approve_location_page(request: Request , svc: LocationService = Depends(locations_service)):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)


    pending_locations = svc.list_pending_locations()
    return request.app.state.templates.TemplateResponse(
        "approve_location.html",
        {
            "request": request,
            "title": "Schválit lokaci",
            "pending_locations": pending_locations
        }
    )

@router.get("/approve_location/{location_id}", name="approve_location_detail", response_class=HTMLResponse)
async def location_detail(request: Request, location_id:int, svc: LocationService = Depends(locations_service)):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)

    location = svc.get_pending_location_detail(location_id)
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "approve_location_detail.html",
        {
            "request": request,
            "title": location["name"],
            "location": location,
        },
    )


@router.post("/approve_location/{location_id}/approve")
async def approve_location_action(location_id: int, request: Request,svc: ApproveLocationService = Depends(approve_location_service)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
    svc.approve_location(location_id)
    print(1111111111111111111111111)
    return RedirectResponse(url="/approve_location", status_code=303)

@router.post("/approve_location/{location_id}/reject")
async def approve_location_action(location_id: int, request: Request,svc: ApproveLocationService = Depends(approve_location_service)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
    svc.reject_location(location_id)
    print(222222222222222222222222222)

    return RedirectResponse(url="/approve_location", status_code=303)