from django import forms
from django.core.exceptions import ValidationError
from .models import Birthday

class BirthdayForm(forms.ModelForm):
    # Inicializace formuláře s vlastním nastavením stylů pro popisky
    # Metoda __init__ je volána při vytváření instance formuláře
    def __init__(self, *args, **kwargs):
        # Volání rodičovské metody pro základní inicializaci
        super().__init__(*args, **kwargs)
        # Nastavení CSS tříd pro všechny popisky polí ve formuláři
        # Použití Tailwind CSS tříd pro konzistentní vzhled
        for field in self.fields.values():
            field.label_attrs = {'class': 'block text-sm font-medium text-gray-700 mb-2'}

    # Vlastní validace formuláře pro kontrolu duplicitních záznamů
    # Metoda clean je volána při validaci formuláře
    def clean(self):
        # Získání vyčištěných dat z rodičovské metody
        cleaned_data = super().clean()
        # Extrakce hodnot jména a data narození z formuláře
        name = cleaned_data.get('name')
        birth_date = cleaned_data.get('birth_date')

        # Kontrola existence záznamu se stejným jménem a datem narození
        # Validace probíhá pouze pokud jsou obě pole vyplněna
        if name and birth_date:
            # Dotaz do databáze pro kontrolu existence duplicitního záznamu
            if Birthday.objects.filter(name=name, birth_date=birth_date).exists():
                # Vyhození výjimky s chybovou zprávou při nalezení duplicity
                raise ValidationError('A birthday entry with this name and date already exists.')
        # Vrácení vyčištěných dat pro další zpracování
        return cleaned_data

    class Meta:
        # Definice modelu a polí použitých ve formuláři
        # Model Birthday je použit jako základ pro formulář
        model = Birthday
        # Seznam polí, která budou zobrazena ve formuláři
        # Pořadí polí odpovídá pořadí v seznamu
        fields = ['calendar_name', 'name', 'birth_date']
        # Nastavení widgetů a jejich atributů pro jednotlivá pole
        # Widgety definují HTML elementy a jejich vlastnosti
        widgets = {
            # Textové pole pro jméno s vlastním stylingem
            'name': forms.TextInput(attrs={
                # Tailwind CSS třídy pro responzivní design
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                # Placeholder text pro nápovědu uživateli
                'placeholder': 'Enter name'
            }),
            # Datové pole s vlastním typem inputu
            'birth_date': forms.DateInput(attrs={
                # HTML5 date input pro lepší UX
                'type': 'date',
                # Stejné CSS třídy jako u ostatních polí pro konzistentní vzhled
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500'
            }),
            # Textové pole pro název kalendáře
            'calendar_name': forms.TextInput(attrs={
                # Konzistentní styling s ostatními poli
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                # Nápověda pro uživatele
                'placeholder': 'Enter calendar name'
            })
        } 
