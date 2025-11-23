from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse

router = APIRouter()

#Router for displaying reset password page
@router.get("/terms-and-conditions", response_class=HTMLResponse)
async def terms_and_conditions_page(request: Request):

    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "terms-and-conditions.html",
        {
            "request": request,
         "title": "Podmínky zpracování osobních údajů"
        }
    )