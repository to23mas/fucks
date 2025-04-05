from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Birthday
from .forms import BirthdayForm

def birthday_list(request):
    # Zpracování formuláře pro přidání nových narozenin
    # Kontrola, zda byl formulář odeslán metodou POST
    if request.method == 'POST':
        # Vytvoření instance formuláře s daty z POST požadavku
        form = BirthdayForm(request.POST)
        # Validace formuláře a uložení dat do databáze
        if form.is_valid():
            form.save()
            # Zobrazení úspěšné zprávy uživateli
            messages.success(request, 'Birthday added successfully!')
            # Přesměrování zpět na seznam narozenin
            return redirect('birthday:birthday_list')
    else:
        # Vytvoření prázdného formuláře pro GET požadavek
        form = BirthdayForm()

    # Získání všech uložených narozenin z databáze
    # Seřazeno podle data narození (definováno v Meta třídě modelu)
    birthdays = Birthday.objects.all()

    # Vykreslení šablony s předanými daty
    return render(request, 'birthday/birthday_list.html', {
        'form': form,
        'birthdays': birthdays,
    })

def delete_birthday(request, birthday_id):
    # Smazání záznamu o narozeninách
    # Nalezení záznamu podle ID nebo 404 chyba
    birthday = get_object_or_404(Birthday, pk=birthday_id)
    # Kontrola, zda byl požadavek odeslán metodou POST
    if request.method == 'POST':
        # Smazání záznamu z databáze
        birthday.delete()
        # Zobrazení úspěšné zprávy uživateli
        messages.success(request, f'Birthday for {birthday.name} was deleted successfully!')
    # Přesměrování zpět na seznam narozenin
    return redirect('birthday:birthday_list')

from .mail import test_mail

def test_birthday_email(request):
    # Testovací pohled pro manuální odeslání emailů s připomenutím narozenin
    # Odeslání testovacího emailu
    test_mail()

    # Zobrazení úspěšné zprávy uživateli
    messages.success(request, "Birthday notification emails have been sent!")
    # Přesměrování zpět na seznam narozenin
    return redirect('birthday:birthday_list')
