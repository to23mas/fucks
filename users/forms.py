from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Formulář pro registraci nových uživatelů
# Rozšiřuje Django UserCreationForm o vlastní pole a styly
class RegisterForm(UserCreationForm):
    # Přidání povinného emailového pole
    email = forms.EmailField()

    class Meta:
        # Určuje, že formulář pracuje s modelem User
        model = User
        # Seznam polí, která se zobrazí ve formuláři
        # username - přihlašovací jméno
        # email - emailová adresa
        # password1 - heslo
        # password2 - potvrzení hesla
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        # Zavolání konstruktoru rodičovské třídy
        super().__init__(*args, **kwargs)

        # Přidání Tailwind CSS tříd pro styling všech polí
        # Aplikuje se na každé pole ve formuláři
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-300 focus:border-blue-500'
            })

# Vlastní formulář pro přihlášení
# Rozšiřuje Django AuthenticationForm o vlastní styly
class CustomLoginForm(AuthenticationForm):
    class Meta:
        # Určuje, že formulář pracuje s modelem User
        model = User
        # Pouze pole pro přihlášení
        # username - přihlašovací jméno
        # password - heslo
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        # Zavolání konstruktoru rodičovské třídy
        super().__init__(*args, **kwargs)
        # Přidání stejných Tailwind CSS tříd jako u registračního formuláře
        # Zajišťuje konzistentní vzhled napříč formuláři
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-300 focus:border-blue-500'
            })
