import requests

BASE_URL = "http://127.0.0.1:8000"

def test_insert_data():
    """Insert a new doctor with all details, including degree."""
    url = f"{BASE_URL}/insert/Physicians"
    data = [
        {
            "Name": "Dr. Mohamed",
            "Speciality": "Cardiology",
            "Degree": "MD, PhD in Cardiology"
        }
    ]
    response = requests.post(url, json=data)
    print("Insert Response:", response.json())

if __name__ == "__main__":
    test_insert_data()