# Backend code

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import csv
import io
import pandas as pd
from fastapi.responses import StreamingResponse
import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///main_db.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    hospital_name = Column(String, index=True)
    ward_name = Column(String, index=True)
    grade = Column(String, index=True)
    date = Column(Date, index=True)
    shift_time = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class ReportCreate(BaseModel):
    customer_name: str
    hospital_name: str
    ward_name: str
    grade: str
    date: datetime.date
    shift_time: str

class ReportRead(BaseModel):
    id: int
    customer_name: str
    hospital_name: str
    ward_name: str
    grade: str
    date: datetime.date
    shift_time: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/reports/", response_model=ReportRead)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports/", response_model=List[ReportRead])
def read_reports(
    customerName: Optional[str] = Query(None),
    hospitalName: Optional[str] = Query(None),
    wardName: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Report)
    print(customerName,hospitalName,wardName,search)
    if customerName:
        query = query.filter(Report.customer_name.contains(customerName))
    if hospitalName:
        query = query.filter(Report.hospital_name.contains(hospitalName))
    if wardName:
        query = query.filter(Report.ward_name.contains(wardName))
    if search:
        query = query.filter(
            (Report.customer_name.contains(search)) |
            (Report.hospital_name.contains(search)) |
            (Report.ward_name.contains(search)) |
            (Report.grade.contains(search)) |
            (Report.shift_time.contains(search))
        )

    return query.all()

@app.get("/reports/download/csv")
def download_reports_csv(db: Session = Depends(get_db)):
    reports = db.query(Report).all()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Id", "Customer Name", "Hospital Name", "Ward Name", "Grade", "Date", "Shift Time"])
    writer.writeheader()
    for report in reports:
        writer.writerow({
            "Id": report.id,
            "Customer Name": report.customer_name,
            "Hospital Name": report.hospital_name,
            "Ward Name": report.ward_name,
            "Grade": report.grade,
            "Date": report.date,
            "Shift Time": report.shift_time
        })
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=reports.csv"})

@app.get("/reports/download/excel")
def download_reports_excel(db: Session = Depends(get_db)):
    reports = db.query(Report).all()
    df = pd.DataFrame([{
        "Id": report.id,
        "Customer Name": report.customer_name,
        "Hospital Name": report.hospital_name,
        "Ward Name": report.ward_name,
        "Grade": report.grade,
        "Date": report.date,
        "Shift Time": report.shift_time
    } for report in reports])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Reports")
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=reports.xlsx"})

@app.get("/reports/download/pdf")
def download_reports_pdf(db: Session = Depends(get_db)):
    reports = db.query(Report).all()
    df = pd.DataFrame([{
        "Id": report.id,
        "Customer Name": report.customer_name,
        "Hospital Name": report.hospital_name,
        "Ward Name": report.ward_name,
        "Grade": report.grade,
        "Date": report.date,
        "Shift Time": report.shift_time
    } for report in reports])
    pdf = df.to_markdown(index=False)
    return StreamingResponse(io.BytesIO(pdf.encode()), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=reports.pdf"})

@app.post("/reports/reset/", response_model=List[ReportRead])
def reset_filters(db: Session = Depends(get_db)):
    return db.query(Report).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)