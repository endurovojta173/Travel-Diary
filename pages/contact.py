from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return request.app.state.templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "Kontaktní údaje"
    })