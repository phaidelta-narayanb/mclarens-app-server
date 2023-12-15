
from fastapi import Request, Body
from fastapi.responses import FileResponse


async def make_pdf(request: Request, content: str = Body(None, media_type="text/html")):
    '''Create a PDF file from the given HTML source'''
    return FileResponse(request.app.extra['report_exporter'].make_pdf(content))
