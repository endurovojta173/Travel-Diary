from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from services.items import ItemsService
from dependencies import items_service  # viz níže – vložíme hned teď

router = APIRouter()


@router.get("/", name="items_ui")
async def items_ui(request: Request, svc: ItemsService = Depends(items_service)):
    items: List[Dict[str, Any]] = svc.list_items()
    total = svc.total_price()
    tpl = request.app.state.templates
    return tpl.TemplateResponse(
        "items.html",
        {"request": request, "title": "Seznam položek", "items": items, "total": total},
    )

@router.post("/", name="items_ui_post")
async def items_ui_post(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    svc: ItemsService = Depends(items_service),
):
    svc.create_item(name=name, price=price, description=description)
    return RedirectResponse(url=request.url_for("items_ui"), status_code=status.HTTP_303_SEE_OTHER)
