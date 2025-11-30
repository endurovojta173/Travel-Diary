from fastapi import APIRouter, Request, Depends, Form
from starlette.responses import RedirectResponse, HTMLResponse
from dependencies import locations_service
from services.list_locations import LocationService

router = APIRouter()


@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request,search_term: str = "",svc: LocationService = Depends(locations_service)):
    locations = []

    # Hledáme jen, pokud uživatel něco zadal
    if search_term:
        locations = svc.search_locations(search_term)

    return request.app.state.templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "title": f"Výsledky pro: {search_term}" if search_term else "Vyhledávání",
            "search_term": search_term,
            "locations": locations,
            "number_of_locations": len(locations)
        }
    )
