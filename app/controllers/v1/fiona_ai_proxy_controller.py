import requests
from fastapi import APIRouter, Request, Response

from app.config.settings import settings

fiona_ai_proxy_controller = APIRouter()


def forward_headers(request: Request):
    headers = {}
    for key, value in request.headers.items():
        if key.lower() != "host":
            headers[key] = value
    return headers


@fiona_ai_proxy_controller.post("/{path:path}")
async def proxy_post(path: str, request: Request):
    body = await request.body()
    headers = forward_headers(request)
    response = requests.post(
        f"{settings.FIONA_AI_BASE_URL}/{path}",
        data=body,
        headers=headers,
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@fiona_ai_proxy_controller.get("/{path:path}")
async def proxy_get(path: str, request: Request):
    headers = forward_headers(request)
    response = requests.get(
        f"{settings.FIONA_AI_BASE_URL}/{path}",
        headers=headers,
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@fiona_ai_proxy_controller.put("/{path:path}")
async def proxy_put(path: str, request: Request):
    body = await request.body()
    headers = forward_headers(request)
    response = requests.put(
        f"{settings.FIONA_AI_BASE_URL}/{path}",
        data=body,
        headers=headers,
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@fiona_ai_proxy_controller.patch("/{path:path}")
async def proxy_patch(path: str, request: Request):
    headers = forward_headers(request)
    response = requests.patch(
        f"{settings.FIONA_AI_BASE_URL}/{path}",
        headers=headers,
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@fiona_ai_proxy_controller.delete("/{path:path}")
async def proxy_delete(path: str, request: Request):
    headers = forward_headers(request)
    response = requests.delete(
        f"{settings.FIONA_AI_BASE_URL}/{path}",
        headers=headers,
    )
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
