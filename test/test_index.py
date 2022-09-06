from app import *
import unittest

app.config.from_object('config.DevelopmentConfig')
 
class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code,200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertIn(b'ver publicacion', response.data)
        
    # Chequea que la lista no este vacia
    def test_index_no_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertNotIn(b'Lista Vacia', response.data)
    
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        status_code = response.status_code
        self.assertEqual(status_code,200)

    # def test_create_user(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/create_user/")
    #     status_code = response.status_code
    #     self.assertEqual(status_code,200)


if __name__== '__main__':
    unittest.main()