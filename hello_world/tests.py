from django.test import SimpleTestCase
from django.http import HttpRequest
from hello_world.views import index

class HelloWorldTests(SimpleTestCase):
    def test_view_returns_http_response(self):
        # Vytvoření testovacího HTTP požadavku
        request = HttpRequest()
        # Získání odpovědi z view
        response = index(request)
        # Ověření, že status kód je 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_view_returns_text(self):
        # Vytvoření testovacího požadavku
        request = HttpRequest()
        # Získání odpovědi
        response = index(request)
        # Kontrola, že obsah lze dekódovat do textového řetězce
        self.assertIsInstance(response.content.decode(), str)

    def test_view_not_empty(self):
        # Příprava testovacího požadavku
        request = HttpRequest()
        # Získání odpovědi
        response = index(request)
        # Ověření, že odpověď není prázdná
        self.assertTrue(len(response.content) > 0)

    def test_view_returns_hello_world(self):
        # Vytvoření požadavku
        request = HttpRequest()
        # Získání odpovědi
        response = index(request)
        # Kontrola přesného obsahu odpovědi
        self.assertEqual(response.content.decode(), "Hello world!")

    def test_view_handles_different_request_methods(self):
        # Vytvoření základního požadavku
        request = HttpRequest()
        # Seznam HTTP metod k otestování
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        # Testování pro každou metodu
        for method in methods:
            # Nastavení metody požadavku
            request.method = method
            # Získání odpovědi
            response = index(request)
            # Kontrola status kódu
            self.assertEqual(response.status_code, 200)
            # Kontrola obsahu
            self.assertEqual(response.content.decode(), "Hello world!")
            # Kontrola typu obsahu
            self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
            # Kontrola absence bezpečnostních hlaviček
            self.assertFalse(response.has_header('X-Frame-Options'))
            self.assertFalse(response.has_header('Content-Security-Policy'))

