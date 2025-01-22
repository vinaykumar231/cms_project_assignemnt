from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "securepass123",
            "full_name": "Test User",
            "phone": "1234567890",
            "pincode": "560001",
            "username": "testuser",  
        }
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_login_user(self):
        user = User.objects.create_user(
            username="testuser", 
            email="test@example.com",
            password="securepass123"
        )
        response = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "securepass123"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        
        # Extract and print the token
        token = response.data["token"]
        print(f"Token: {token}")  # Print the token for debugging purposes
