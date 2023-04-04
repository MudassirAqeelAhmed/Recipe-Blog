import unittest
from main import create_app
from config import TestConfig
from exts import db

class APITestcase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.create_all()

    def test_signup(self):
        response = self.client.post('/auth/signup',
        json = {"username": "testuser",
                "email": "test@test.com",
                "password": "testpassword"}
        )
        json = response.json
        status_code = response.status_code
        self.assertEqual(json,{'message': 'User created successfully'}) 

    def test_login(self):
        signup_response = self.client.post('/auth/signup',
        json = {"username": "testuser",
                "email": "test@test.com",
                "password": "testpassword"}
        )

        login_response = self.client.post('/auth/login',
        json = {"username": "testuser",
                "password": "testpassword"}
        )
        status_code = login_response.status_code

        self.assertEqual(status_code,200)


    def test_get_all_recipes(self):
        """Test get_all_recipes"""
        response = self.client.get('/recipe/recipes')
        status_code = response.status_code

        self.assertEqual(status_code,200)

    def test_get_one_recipes(self):
        id = 1
        response = self.client.get(f"/recipe/recipe/{id}")
        status_code = response.status_code

        self.assertEqual(status_code, 404)

    def test_create_recipe(self):
        signup_response = self.client.post('/auth/signup',
        json = {"username": "testuser",
                "email": "test@test.com",
                "password": "testpassword"}
        )

        login_response = self.client.post('/auth/login',
        json = {"username": "testuser",
                "password": "testpassword"}
        )
        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post('/recipe/recipes',
                                json = {"title": "Test recipe",
                                        "description": "Test recipe description"},
                                headers = {"Authorization": f"Bearer {access_token}"}
                                )
        status_code = create_recipe_response.status_code
        self.assertEqual(status_code,201)

    def test_update_recipe(self):
        signup_response = self.client.post('/auth/signup',
        json = {"username": "testuser",
                "email": "test@test.com",
                "password": "testpassword"}
        )

        login_response = self.client.post('/auth/login',
        json = {"username": "testuser",
                "password": "testpassword"}
        )
        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post('/recipe/recipes',
                                json = {"title": "Test recipe",
                                        "description": "Test recipe description"},
                                headers = {"Authorization": f"Bearer {access_token}"}
                                )
        id = 1
        update_response = self.client.put(f'/recipe/recipe/{id}',
                        json = {"title": "Test recipe",
                                "description": "Test description"},
                        headers = {"Authorization": f"Bearer {access_token}"}
                        )
        description = update_response.json['description']
        self.assertEqual(description, "Test description")

    def test_delete_recipe(self):
        signup_response = self.client.post('/auth/signup',
        json = {"username": "testuser",
                "email": "test@test.com",
                "password": "testpassword"}
        )

        login_response = self.client.post('/auth/login',
        json = {"username": "testuser",
                "password": "testpassword"}
        )
        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post('/recipe/recipes',
                                json = {"title": "Test recipe",
                                        "description": "Test recipe description"},
                                headers = {"Authorization": f"Bearer {access_token}"}
                                )
        id = 1
        delete_response = self.client.delete(f'/recipe/recipe/{id}',
                          headers = {"Authorization": f"Bearer {access_token}"})
        
        status_code = delete_response.status_code
        self.assertEqual(status_code,200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()