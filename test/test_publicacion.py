
from app import *
import unittest

app.config.from_object('config.DevelopmentConfig')
 
class PublicacionTest(unittest.TestCase):

    def test_publicacion_route(self):
        tester = app.test_client(self)
        response = tester.get("/publicacion")
        status_code = response.status_code
        self.assertEqual(status_code,200)

    def test_publicaciones_route(self):
        tester = app.test_client(self)
        response = tester.get("/publicaciones")
        status_code = response.status_code
        self.assertEqual(status_code,200)

    def test_publicaciones_notlogedIn_not_empty(self):
        tester = app.test_client(self)
        response = tester.get("/publicaciones")
        self.assertNotIn(b'Titulo', response.data)


if __name__== '__main__':
    unittest.main()