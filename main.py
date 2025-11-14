# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pages.home import router as home_router
from pages.locations import router as locations_router

def create_app() -> FastAPI:
    app = FastAPI(title = "FastAPI")

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.state.templates = Jinja2Templates(directory="templates")



    #INCLUDES OF THE ROUTERS !!!! ALL PAGES MUST BE INCLUDED
    app.include_router(home_router)
    app.include_router(locations_router)


    # DEBUG: vypiš zaregistrované cesty - Pro ladění
    print("=== ROUTES ===")
    for r in app.routes:
        #print(repr(r.name), r.path)
        try:
            print(getattr(r, "methods", ""), getattr(r, "path", ""))
        except Exception:
            pass
    return app

app = create_app()


