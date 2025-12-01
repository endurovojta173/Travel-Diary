# app/main.py
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
#Pro session
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
from pages.home import router as home_router
from pages.locations import router as locations_router
from pages.rankings import router as rankings_router
from pages.add_location import router as add_location_router
from pages.login import router as login_router
from pages.register import router as register_router
from pages.reset_password import router as reset_password_router
from pages.my_profile import router as my_profile_router
from pages.privacy_policy import router as terms_and_conditions_router
from pages.approve_location import router as approve_location_router
from pages.all_users import router as all_users_router
from pages.create_user import router as create_user_router
from pages.search import router as search_router
from pages.google_auth import router as google_auth
from pages.contact import router as contact_router

def create_app() -> FastAPI:
    app = FastAPI(title = "FastAPI")

    #Mount for static files, like css, js, logos, icons...
    app.mount("/static", StaticFiles(directory="static"), name="static")
    #Mount for images of locations in database
    app.mount("/database", StaticFiles(directory="database"), name="database")
    #Pro session
    app.add_middleware(
        SessionMiddleware,
        secret_key= os.getenv("SECRET_KEY"), #Beru klic z .env kterou neverzuji skrze safety
        max_age = 86400, #Po jednom dni se smaže cookies
        same_site="lax", #Ochrana proti Cross-Site Request Forgery
    )

    app.state.templates = Jinja2Templates(directory="templates")



    #INCLUDES OF THE ROUTERS !!!! ALL PAGES MUST BE INCLUDED
    app.include_router(home_router)
    app.include_router(locations_router)
    app.include_router(add_location_router)
    app.include_router(rankings_router)
    app.include_router(login_router)
    app.include_router(reset_password_router)
    app.include_router(register_router)
    app.include_router(my_profile_router)
    app.include_router(terms_and_conditions_router)
    app.include_router(approve_location_router)
    app.include_router(all_users_router)
    app.include_router(create_user_router)
    app.include_router(search_router)
    app.include_router(google_auth)
    app.include_router(contact_router)

    return app

app = create_app()


