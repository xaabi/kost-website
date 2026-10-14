import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db

# Pydantic Schema untuk input form
class SurveyCreate(BaseModel):
    full_name: str
    phone_number: str
    survey_date: str
    room_type: str

app = FastAPI(title="Eksklusif Kost Jakarta Timur")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

STATIC_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/")
async def render_homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Endpoint API simpan survei/booking
@app.post("/api/book-survey")
async def book_survey(data: SurveyCreate, db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        query = text("""
            INSERT INTO survey_bookings (full_name, phone_number, survey_date, room_type)
            VALUES (:full_name, :phone_number, :survey_date, :room_type)
        """)
        db.execute(query, {
            "full_name": data.full_name,
            "phone_number": data.phone_number,
            "survey_date": data.survey_date,
            "room_type": data.room_type
        })
        db.commit()
        return {"status": "success", "message": "Survei berhasil dijadwalkan!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)