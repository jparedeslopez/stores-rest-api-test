from ...tests.base_test import BaseTest
from ...models.user import UserModel
import json


class UserTest(BaseTest):
    def test_register(self):
        with self.app() as client: #we need a client for doing request
            with self.app_context():#for the db
                request = client.post('/register', data = {'username': 'test_name', 'password': '123'}) #the data here is sent as a form.

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test_name'))
                self.assertDictEqual({'message': 'User created successfully'},
                                     json.loads(request.data)) #need to convert the form data back to json.

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data = {'username': 'test_name', 'password': '123'}) #the data here is sent as a form.
                auth_request = client.post('/auth',
                                           data = json.dumps({'username': 'test_name', 'password': '123'}), #/auth endpoints requires the data to be sont as a json
                                           headers = {'Content-Type': 'application/json'}) #web apps look into headers to know the kinf of data (for example) they are getting

                self.assertIn('access_token', json.loads(auth_request.data).keys()) #to be sure the access token was returned on the data. It converts the data into json. It ges the access_token from that list.

    def test_user_error(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data = {'username': 'test_name', 'password': '123'})
                request = client.post('/register', data={'username': 'test_name', 'password': '123'})

                self.assertDictEqual({'message': 'A user with this username already exists.'},
                                     json.loads(request.data))
                self.assertEqual(request.status_code, 400)