import requests
import pytest
import jsonschema 
from jsonschema import validate

class TestPatientAPI:
    BASE_URL = "http://127.0.0.1:5000/patients"

    # JSON Schema for validating the response structure
    patient_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["id", "name", "email"]
    }

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # This fixture runs before each test
        yield
        # This code runs after each test
        # You can add code here to clean up if needed

    def test_create_patient(self):
        json_body = {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }

        response = requests.post(self.BASE_URL, json=json_body)
        assert response.status_code == 201
        assert response.json()["name"] == "John Doe"

        # Validate the response schema
        validate(instance=response.json(), schema=self.patient_schema)

    def test_update_patient(self):
        # First, create a patient
        json_body = {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        create_response = requests.post(self.BASE_URL, json=json_body)
        patient_id = create_response.json()["id"]

        # Now, update the patient
        update_body = {
            "name": "John Doe Updated",
            "email": "john.doe.updated@example.com"
        }
        update_response = requests.put(f"{self.BASE_URL}/{patient_id}", json=update_body)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "John Doe Updated"

        # Validate the response schema
        validate(instance=update_response.json(), schema=self.patient_schema)

    def test_delete_patient(self):
        # First, create a patient
        json_body = {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        create_response = requests.post(self.BASE_URL, json=json_body)
        patient_id = create_response.json()["id"]

        # Now, delete the patient
        delete_response = requests.delete(f"{self.BASE_URL}/{patient_id}")
        assert delete_response.status_code == 204  # No content for successful deletion

        # Verify that the patient no longer exists
        get_response = requests.get(f"{self.BASE_URL}/{patient_id}")
        assert get_response.status_code == 404
        assert get_response.json()["error"] == "Patient not found"

    def test_delete_non_existent_patient(self):
        response = requests.delete(f"{self.BASE_URL}/999")  # Non-existent ID
        assert response.status_code == 404
        assert response.json()["error"] == "Patient not found"

    @pytest.mark.parametrize("email, expected_status, expected_error", [
        ("invalid-email", 400, "Invalid email format"),
        (None, 400, "Name is required")  # Testing missing name
    ])
    def test_create_patient_with_invalid_email(self, email, expected_status, expected_error):
        json_body = {
            "name": "Jane Doe" if email is None else "John Doe",
            "email": email
        }

        response = requests.post(self.BASE_URL, json=json_body)
        assert response.status_code == expected_status
        assert response.json()["error"] == expected_error

    def test_create_patient_missing_fields(self):
        json_body = {
            "email": "john.doe@example.com"  # Missing name
        }

        response = requests.post(self.BASE_URL, json=json_body)
        assert response.status_code == 400
        assert response.json()["error"] == "Name is required"  # Adjust based on your API's error message

if __name__ == "__main__":
    pytest.main()