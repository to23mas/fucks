from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseNotFound

# Middleware pro kontrolu přihlášení uživatele
# Zajišťuje, že nepřihlášení uživatelé mají přístup pouze k přihlášení a registraci
class LoginRequiredMiddleware:
	def __init__(self, get_response):
		# Inicializace middleware s následujícím middleware v řetězci
		self.get_response = get_response

	def __call__(self, request):
		# Seznam URL adres, které jsou přístupné i bez přihlášení
		# Typicky přihlašovací a registrační stránka
		excluded_urls = [settings.LOGIN_URL, settings.REGISTER_URL]

		# Kontrola, zda je uživatel nepřihlášený a zkouší přistoupit 
		# na stránku, která není v seznamu výjimek
		if not request.user.is_authenticated and request.path not in excluded_urls:
			# Přesměrování nepřihlášeného uživatele na přihlašovací stránku
			return redirect(settings.LOGIN_URL)

		# Pokud je uživatel přihlášený nebo přistupuje k povoleným URL,
		# pokračuje se dalším middleware v řetězci
		return self.get_response(request)


# Middleware pro zpracování 404 chyb (stránka nenalezena)
# Místo zobrazení 404 stránky přesměruje uživatele
class Redirect404Middleware:
	def __init__(self, get_response):
		# Inicializace middleware s následujícím middleware v řetězci
		self.get_response = get_response

	def __call__(self, request):
		# Zpracování požadavku následujícím middleware
		response = self.get_response(request)

		# Kontrola, zda odpověď je typu 404 (stránka nenalezena)
		if isinstance(response, HttpResponseNotFound):
			# Pro nepřihlášené uživatele - přesměrování na přihlašovací stránku
			if not request.user.is_authenticated:
				return redirect(settings.LOGIN_URL)
			# Pro přihlášené uživatele - přesměrování na hlavní stránku
			return redirect('/')

		# Pokud nejde o 404, vrátí původní odpověď
		return response
