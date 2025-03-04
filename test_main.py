import unittest
from unittest.mock import patch, MagicMock
from main import app, get_db, ReportCreate, ReportRead
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class TestMain(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.engine = create_engine("sqlite:///test_main.db")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    async def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @patch('main.get_db')
    def test_create_report(self, mock_get_db):
        report_data = {"customer_name": "John Doe", "hospital_name": "Hospital A", "ward_name": "Ward 1", "grade": "A", "date": "2022-01-01", "shift_time": "08:00"}
        response = self.client.post("/reports/", json=report_data)
        self.assertEqual(response.status_code, 200)

    @patch('main.get_db')
    def test_read_reports(self, mock_get_db):
        report_data = {"customer_name": "John Doe", "hospital_name": "Hospital A", "ward_name": "Ward 1", "grade": "A", "date": "2022-01-01", "shift_time": "08:00"}
        self.client.post("/reports/", json=report_data)
        response = self.client.get("/reports/")
        self.assertEqual(response.status_code, 200)

    @patch('main.get_db')
    def test_download_reports_csv(self, mock_get_db):
        report_data = {"customer_name": "John Doe", "hospital_name": "Hospital A", "ward_name": "Ward 1", "grade": "A", "date": "2022-01-01", "shift_time": "08:00"}
        self.client.post("/reports/", json=report_data)
        response = self.client.get("/reports/download/csv")
        self.assertEqual(response.status_code, 200)

    @patch('main.get_db')
    def test_download_reports_excel(self, mock_get_db):
        report_data = {"customer_name": "John Doe", "hospital_name": "Hospital A", "ward_name": "Ward 1", "grade": "A", "date": "2022-01-01", "shift_time": "08:00"}
        self.client.post("/reports/", json=report_data)
        response = self.client.get("/reports/download/excel")
        self.assertEqual(response.status_code, 200)

    @patch('main.get_db')
    def test_download_reports_pdf(self, mock_get_db):
        report_data = {"customer_name": "John Doe", "hospital_name": "Hospital A", "ward_name": "Ward 1", "grade": "A", "date": "2022-01-01", "shift_time": "08:00"}
        self.client.post("/reports/", json=report_data)
        response = self.client.get("/reports/download/pdf")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
