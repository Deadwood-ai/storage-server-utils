from typing import Union, Generator, Literal

from supabase import create_client
from supabase.client import Client
from contextlib import contextmanager

from .settings import settings


def login(user: str, password: str):
    # create a supabase client
    client = create_client(settings.supabase_url, settings.supabase_key)

    auth_response = client.auth.sign_in_with_password({'email': user, 'password': password})
    
    client.auth.sign_out()
    # return the response
    return auth_response


def verify_token(jwt: str) -> Union[Literal[False], str]:
    # make the authentication
    with use_client(jwt) as client:
        response = client.auth.get_user(jwt)
    
    # check the token
    try:
        return response.user.id
    except Exception:
        return False
    

@contextmanager
def use_client(access_token: str) -> Generator[Client, None, None]:
    # create a supabase client
    client = create_client(settings.supabase_url, settings.supabase_key)

    # yield the client
    try:
        # set the access token to the postgrest (rest-api) client
        client.postgrest.auth(token=access_token)
        
        yield client
    finally:
        client.auth.sign_out()

    