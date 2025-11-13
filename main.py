# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pages.items import router as items_router  # ← DŮLEŽITÉ: přímý import modulu
from dependencies import items_service
from services.items import ItemsService

def create_app() -> FastAPI:
    app = FastAPI(title="Mini FastAPI – Items")

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.state.templates = Jinja2Templates(directory="templates")

    app.include_router(items_router, prefix="/items", tags=["items"])
    

    # DEBUG: vypiš zaregistrované cesty
    print("=== ROUTES ===")
    for r in app.routes:
        try:
            print(getattr(r, "methods", ""), getattr(r, "path", ""))
        except Exception:
            pass

    # Pokud používáš override přes třídu, nech, jinak ho klidně vyhoď
    app.dependency_overrides[ItemsService] = items_service
    return app

app = create_app()


