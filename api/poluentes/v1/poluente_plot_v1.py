import io

from fastapi import APIRouter, Query
from fastapi.responses import Response, FileResponse
from starlette.responses import StreamingResponse, FileResponse
from app.user.schemas import (
    ExceptionResponseSchema,
)

poluente_plot_router = APIRouter()

@poluente_plot_router.get(
    "/{file_name}",
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_poluente_scrap_by_id(
        file_name: str = Query("", description="nome do arquivo, exemplo: MP10_20220104_11.0_32.0_movel.png"),
):
    # file = FileResponse(f"/mnt/vdb1/png_movel/{file_name}", media_type="image/png")
    # image: bytes = open(f"/mnt/vdb1/png_movel/{file_name}", "rb").read()
    # return Response(content=image, media_type="image/png")
    image_path = "/home/caue/Imagens/Captura de tela de 2022-03-16 21-16-21.png"

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    return FileResponse("/home/caue/Imagens/Captura de tela de 2022-03-16 21-16-21.png")
