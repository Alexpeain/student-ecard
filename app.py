from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()


app = Flask(__name__)

# Access environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")


# Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_APPLICATION_CREDENTIALS, scope)

try:
    client = gspread.authorize(creds)

# Open the Google Sheet and access the specific worksheet
    sheet = client.open_by_url(SPREADSHEET_URL)
    student_sheet = sheet.worksheet("StudentInfo")
except Exception as e:
    print(f"An error occurred: {e}")

# Fetch all student data from Google Sheets
def fetch_student_data():
    data = student_sheet.get_all_records()
    return {row["StudentID"]: row for row in data}

# API to fetch student data
@app.route("/student/<student_id>", methods=["GET"])
def get_student(student_id):
    students = fetch_student_data()
    student = students.get(student_id)
    if student:
        return render_template("student_card.html", student=student)
    else:
        return jsonify({"error": "Student not found"}), 404

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
