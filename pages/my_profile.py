from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying my profile page
@router.get("/my_profile", response_class=HTMLResponse)
async def my_profile_page(request: Request):

    return request.app.state.templates.TemplateResponse(
        "my_profile.html",
        {"request": request, "title": "Locations"}
    )