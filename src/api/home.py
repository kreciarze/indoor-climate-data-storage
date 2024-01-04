from fastapi import status
from fastapi.responses import HTMLResponse

from api.base_router import BaseRouter

router = BaseRouter()


@router.api_route(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def home() -> HTMLResponse:
    html_content = """
        <html>

        <head>
            <title>Krecik IOT</title>
        </head>

        <body>
            <header>
                <h1>Welcome to Indoor Climate Data Storage API</h1>
        </header>
            <section>
            <img src="https://krecik.cytr.us/krecik-ok.png"></img>
            </section>
        </body>

        </html>"""
    return HTMLResponse(content=html_content)
