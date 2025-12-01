from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying reset password page
@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy_page(request: Request):
    return request.app.state.templates.TemplateResponse("privacy_policy.html", {
        "request": request,
        "title": "Zásady ochrany osobních údajů"
    })