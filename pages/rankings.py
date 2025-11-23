from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


#Router for displaying rankings page
@router.get("/rankings")
async def rankings_page(request: Request, response_class=HTMLResponse):
    return request.app.state.templates.TemplateResponse(
        "rankings.html",
        {
            "request": request,
            "title": "Žebříček"
        }
    )