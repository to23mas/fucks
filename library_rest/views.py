from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book
from datetime import datetime
from django.core.management import call_command
from django.contrib import messages

# Dekorátor @login_required zajišťuje, že přístup mají pouze přihlášení uživatelé
@login_required
def index(request):
    # Zobrazení hlavní stránky knihovny
    return render(request, 'library_rest/index.html')

# @csrf_exempt dočasně vypíná CSRF ochranu pro testovací účely
# V produkčním prostředí by měla být CSRF ochrana aktivní
@csrf_exempt
@login_required
def book_list(request):
    # Implementace kolekce knih (GET a POST metody)
    # GET: Vrací seznam všech knih
    # POST: Vytvoří novou knihu
    
    if request.method == 'GET':
        # Získání všech knih z databáze a jejich převod do JSON formátu
        # Použití list comprehension pro efektivní převod na JSON
        books = Book.objects.all()
        return JsonResponse({'books': [book.to_dict() for book in books]})
    
    elif request.method == 'POST':
        try:
            # Zpracování JSON dat z požadavku
            # Očekává se validní JSON s povinnými poli
            data = json.loads(request.body)
            # Konverze data publikování z řetězce na datetime objekt
            # Pokud datum není poskytnuto, použije se None
            published_date = datetime.strptime(data.get('published_date'), '%Y-%m-%d').date() if data.get('published_date') else None
            
            # Vytvoření nové knihy v databázi s poskytnutými daty
            # Všechna pole jsou volitelná, ale doporučuje se poskytnout alespoň title a author
            book = Book.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                isbn=data.get('isbn'),
                pages=data.get('pages'),
                published_date=published_date
            )
            # Vrácení dat nově vytvořené knihy se statusem 201 (Created)
            # Status 201 indikuje úspěšné vytvoření nového zdroje
            return JsonResponse(book.to_dict(), status=201)
        except json.JSONDecodeError:
            # Chyba při parsování JSON - vrácení chybové zprávy se statusem 400
            # Status 400 indikuje chybný požadavek
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValueError as e:
            # Chyba při konverzi data - vrácení chybové zprávy se statusem 400
            return JsonResponse({'error': f'Invalid date format. Use YYYY-MM-DD. {str(e)}'}, status=400)

@csrf_exempt
@login_required
def book_detail(request, pk):
    # Implementace detailu knihy (GET, PUT, DELETE metody)
    # GET: Vrací detail konkrétní knihy
    # PUT: Aktualizuje existující knihu
    # DELETE: Smaže knihu
    
    try:
        # Pokus o získání knihy podle primárního klíče
        # Použití get() místo filter() pro jednoznačný výsledek
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        # Kniha nebyla nalezena - vrácení chybové zprávy se statusem 404
        # Status 404 indikuje, že požadovaný zdroj neexistuje
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        # Vrácení detailů konkrétní knihy v JSON formátu
        # Použití to_dict() pro konzistentní formát odpovědí
        return JsonResponse(book.to_dict())
    
    elif request.method == 'PUT':
        try:
            # Aktualizace existující knihy
            # Metoda PUT by měla být idempotentní (opakované volání má stejný efekt)
            data = json.loads(request.body)
            # Aktualizace pouze těch polí, která byla poslána
            # Použití get() s výchozí hodnotou pro zachování původních dat
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            # ISBN a počet stran jsou aktualizovány pouze pokud jsou poskytnuty
            # Toto zabraňuje nechtěnému vymazání dat
            if 'isbn' in data:
                book.isbn = data['isbn']
            if 'pages' in data:
                book.pages = data['pages']
            if 'published_date' in data:
                book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date()
            book.save()
            return JsonResponse(book.to_dict())
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date format. Use YYYY-MM-DD. {str(e)}'}, status=400)
    
    elif request.method == 'DELETE':
        # Smazání knihy z databáze
        # Metoda DELETE by měla být idempotentní
        book.delete()
        # Vrácení prázdné odpovědi se statusem 204 (No Content)
        # Status 204 indikuje úspěšné smazání bez potřeby vracet data
        return JsonResponse({}, status=204)

@login_required
def reset_data(request):
    # Pomocná funkce pro reset databáze na výchozí stav
    # Používá se pro testovací a vývojové účely
    try:
        # Smazání všech existujících dat z tabulky Book
        # Pozor: Tato operace je nevratná
        Book.objects.all().delete()
        
        # Načtení výchozích dat z fixtures souboru
        # verbosity=0 potlačuje výstup příkazu
        call_command('loaddata', 'library_rest/fixtures/books.json', verbosity=0)
        
        # Zobrazení úspěšné zprávy uživateli pomocí Django messages frameworku
        messages.success(request, 'Data reset successful!')
    except Exception as e:
        # Zobrazení chybové zprávy v případě selhání
        messages.error(request, f'Error resetting data: {str(e)}')
    
    # Přesměrování na hlavní stránku knihovny
    return redirect('library_rest:index')

# Create your views here.
