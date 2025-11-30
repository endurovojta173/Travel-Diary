from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from dependencies import user_service
from services.users import UserService
router = APIRouter()

#Router for displaying my profile page
@router.get("/all_users", response_class=HTMLResponse)
async def all_users_page(request: Request, svc: UserService = Depends(user_service)):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)

    #Users
    all_users = svc.list_all_users()
    return request.app.state.templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "title": "Seznam všech uživatelů",
            "all_users": all_users
        }
    )

@router.post("/all_users/update")
async def approve_location_action(request: Request, svc: UserService = Depends(user_service), user_id:int = Form(...), role:int = Form(...)):

    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)

    svc.update_user_role(user_id, role)

    return RedirectResponse(url="/all_users", status_code=303)