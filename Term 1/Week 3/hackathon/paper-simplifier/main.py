from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import pdfplumber
import io

from simplifier import check_domain, simplify_paper
from glossary_db import init_db, add_terms, get_all_terms

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

init_db()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/simplify")
async def simplify(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Accepts EITHER pasted text OR an uploaded PDF (not both).
    Runs domain check, then simplification, then saves glossary terms.
    """
    paper_text = ""

    if file is not None:
        contents = await file.read()
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(layout=True)
                if page_text:
                    paper_text += page_text + "\n"
        source_name = file.filename
    elif text:
        paper_text = text
        source_name = "pasted_text"
    else:
        return JSONResponse(status_code=400, content={"error": "No text or file provided."})

    if not paper_text.strip():
        return JSONResponse(status_code=400, content={"error": "Could not extract any text."})

    is_it_paper = check_domain(paper_text)

    result = simplify_paper(paper_text)

    if result.get("glossary"):
        add_terms(result["glossary"], source_paper=source_name)

    return {
        "domain_warning": None if is_it_paper else "This doesn't look like an IT/CS paper — results may be less accurate.",
        "sections": result["sections"],
        "glossary": result["glossary"]
    }


@app.get("/glossary")
async def glossary():
    return get_all_terms()