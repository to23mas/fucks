# Import potřebných modulů pro testování
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Třída pro testování hello_world view
class HelloWorldTests(TestCase):
    # Metoda setUp se spustí před každým testem
    # Zde připravujeme testovací prostředí
    def setUp(self):
        # Vytvoření testovacího klienta - simuluje webový prohlížeč
        self.client = Client()
        # Získání URL adresy pro hello_world view pomocí reverse
        self.url = reverse('hello_world:hello_world')
        # Vytvoření testovacího uživatele v databázi
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Přihlášení testovacího uživatele
        self.client.login(username='testuser', password='testpass123')

    # Test zda view existuje a vrací správný HTTP status kód
    def test_view_exists(self):
        # Odeslání GET požadavku na URL
        response = self.client.get(self.url)
        # Ověření, že status kód je 200 (OK)
        self.assertEqual(response.status_code, 200)

    # Test zda view vrací textový obsah
    def test_view_returns_text(self):
        response = self.client.get(self.url)
        # Ověření, že obsah odpovědi je textový řetězec
        self.assertIsInstance(response.content.decode(), str)

    # Test zda view vrací neprázdnou odpověď
    def test_view_not_empty(self):
        response = self.client.get(self.url)
        # Ověření, že délka obsahu je větší než 0
        self.assertTrue(len(response.content) > 0)

    # Test zda view správně reaguje na GET požadavek
    def test_view_uses_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Test zda view vyžaduje přihlášení
    def test_view_requires_login(self):
        # Vytvoření nového klienta bez přihlášení
        client = Client()
        response = client.get(self.url)
        # Ověření, že nepřihlášený uživatel je přesměrován (302)
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    # Test přístupu po odhlášení
    def test_logout_then_access(self):
        # Nejprve ověříme, že přihlášený uživatel má přístup
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Odhlášení uživatele
        self.client.logout()
        
        # Ověření, že po odhlášení nemáme přístup
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Test přístupu s neplatnými přihlašovacími údaji
    def test_invalid_credentials(self):
        client = Client()
        # Pokus o přihlášení se špatným heslem
        logged_in = client.login(username='testuser', password='wrongpassword')
        # Ověření, že přihlášení se nezdařilo
        self.assertFalse(logged_in)
        
        # Ověření, že přístup je zamítnut
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
    

