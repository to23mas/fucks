from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import RegisterForm, CustomLoginForm

# Třída pro zpracování registrace nových uživatelů
# Používá generickou třídu FormView pro zpracování formulářů
class RegisterView(FormView):
    # Cesta k šabloně pro registrační formulář
    template_name = 'users/register.html'
    # Třída formuláře která se použije pro registraci
    form_class = RegisterForm
    # Po úspěšné registraci přesměruje na přihlašovací stránku
    # reverse_lazy se používá místo reverse protože URLs se načítají až později
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Metoda volaná když jsou data formuláře validní
        # Uloží nového uživatele do databáze
        form.save()
        # Zavolá rodičovskou metodu pro dokončení zpracování
        return super().form_valid(form)

# Vlastní třída pro přihlašování uživatelů
# Dědí z Django LoginView pro využití vestavěné funkcionality
class CustomLoginView(LoginView):
    # Vlastní šablona pro přihlašovací formulář
    template_name = 'users/login.html'
    # Vlastní třída formuláře pro přihlášení
    form_class = CustomLoginForm

    def form_valid(self, form):
        # Metoda volaná při úspěšném přihlášení
        # Používá výchozí chování z LoginView
        return super().form_valid(form)

    def form_invalid(self, form):
        # Metoda volaná když přihlášení selže (špatné heslo apod.)
        # Používá výchozí chování z LoginView
        return super().form_invalid(form)

