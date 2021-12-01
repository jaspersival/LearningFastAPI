from enum import Enum

from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {"file_size": len(file), "token": token, "fileb_content_type": fileb.content_type}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile] = File(...)):
    return {"file_names": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
