from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import HTMLResponse
from markupsafe import escape

app = FastAPI()


@app.get("/item", response_class=HTMLResponse)
async def read_items(itemname: str):
    # deepruleid: tainted-direct-response-fastapi
    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{itemname}</h1>
        </body>
    </html>
    """
@app.get("/itemsafe", response_class=HTMLResponse)
async def read_items_safe(itemname: str):
    itemname = escape(itemname)
    # ok: tainted-direct-response-fastapi
    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{itemname}</h1>
        </body>
    </html>
    """
@app.get("/itemsafe", response_class=HTMLResponse)
async def read_items_safe(itemname: str):
    itemname = escape(itemname)
    # ok: tainted-direct-response-fastapi
    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{itemname}</h1>
        </body>
    </html>
    """


@app.get("/items/")
async def read_items2(itemname: str):
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{itemname}</h1>
        </body>
    </html>
    """
    # deepruleid: tainted-direct-response-fastapi
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/items/")
async def read_items3(itemname: str):
    html_content = f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{itemname}</h1>
        </body>
    </html>
    """
    # deepruleid: tainted-direct-response-fastapi
    return Response(content=html_content, media_type="text/html")


class CustomHTMLResponse(Response):
    media_type = "text/html"

    def render(self, content: str) -> bytes:
        return content.encode()


class CustomOtherResponse(Response):
    media_type = "application/json"

    def render(self, content: str) -> bytes:
        return content.encode()


@app.get("/", response_class=CustomHTMLResponse)
async def main(query_param: str):
    # Depends on the media_type defined in the class of the response type
    # todoruleid: tainted-direct-response-fastapi
    return query_param

@app.get("/", response_class=CustomOtherResponse)
async def main2(query_param: str):
    # Depends on the media_type defined in the class of the response type
    # ok: tainted-direct-response-fastapi
    return query_param
