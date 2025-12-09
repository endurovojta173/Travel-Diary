from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from dependencies import user_service
from services.users import UserService

router = APIRouter()

config = Config('.env')
oauth = OAuth(config)

# Registrace Googlu
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


@router.get("/login/google")
async def login_google(request: Request):
    # Kam se má Google vrátit po přihlášení
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google")
async def auth_google(
        request: Request,
        svc: UserService = Depends(user_service)
):
    try:
        # token
        token = await oauth.google.authorize_access_token(request)

        # Info o uživateli
        user_info = token.get('userinfo')

        if not user_info:
            return RedirectResponse("/login?error=Google_Auth_Failed")

        #Najít nebo Vytvořit v DB
        user = svc.get_or_create_google_user(google_email=user_info['email'],google_name=user_info['name'])

        # Uložíme do session
        request.session["user"] = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user.get("id_role", 3)
        }

        return RedirectResponse("/", status_code=303)

    except Exception as e:
        print(f"Google Login Error: {e}")
        return RedirectResponse("/login?error=Authentication_Failed")