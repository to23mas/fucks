from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.management import call_command
from library_rest.models import Book 
import json
from jsonrpcserver import method, Success, dispatch, Result, Error

# Zobrazení hlavní stránky JSON-RPC rozhraní
def index(request):
    return render(request, 'library_rpc/index.html')

# Metoda pro získání seznamu všech knih
# - Vrací seznam knih ve formátu JSON-RPC
# - Každá kniha obsahuje všechny potřebné atributy
@method
def get_books() -> Result:
    books = Book.objects.all()
    return Success([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'pages': book.pages,
        'published_date': str(book.published_date)
    } for book in books])

# Metoda pro získání jedné knihy podle ID
# - id: ID knihy k získání
# - Vrací Error pokud kniha neexistuje
@method
def get_book(id: int) -> Result:
    try:
        book = Book.objects.get(pk=id)
        return Success({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'pages': book.pages,
            'published_date': str(book.published_date)
        })
    except Book.DoesNotExist:
        return Error(message="Book not found")

# Metoda pro vytvoření nové knihy
# - Všechny parametry jsou povinné
# - Vrací Error při chybě vytváření
@method
def create_book(title: str, author: str, isbn: str, pages: int, published_date: str) -> Result:
    try:
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            pages=pages,
            published_date=published_date
        )
        return Success({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'pages': book.pages,
            'published_date': str(book.published_date)
        })
    except Exception as e:
        return Error(message=str(e))

# Metoda pro aktualizaci existující knihy
# - id: ID knihy k aktualizaci
# - Ostatní parametry jsou volitelné
# - Aktualizuje pouze zadané atributy
@method
def update_book(id: int, title: str = None, author: str = None, 
                isbn: str = None, pages: int = None, 
                published_date: str = None) -> Result:
    try:
        book = Book.objects.get(pk=id)
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if isbn is not None:
            book.isbn = isbn
        if pages is not None:
            book.pages = pages
        if published_date is not None:
            book.published_date = published_date
        book.save()
        return Success({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'pages': book.pages,
            'published_date': str(book.published_date)
        })
    except Book.DoesNotExist:
        return Error(message="Book not found")

# Metoda pro smazání knihy
# - id: ID knihy ke smazání
# - Vrací Error pokud kniha neexistuje
@method
def delete_book(id: int) -> Result:
    try:
        book = Book.objects.get(pk=id)
        book.delete()
        return Success(True)
    except Book.DoesNotExist:
        return Error(message="Book not found")

# Handler pro JSON-RPC požadavky
# - @csrf_exempt: vypíná CSRF ochranu pro API endpoint
# - Zpracovává POST požadavky s JSON-RPC formátem
# - Vrací odpověď ve formátu JSON-RPC
@csrf_exempt
def jsonrpc_handler(request):
    if request.method == "POST":
        try:
            # Dekódování a zpracování JSON-RPC požadavku
            request_data = json.loads(request.body.decode('utf-8'))
            response = dispatch(json.dumps(request_data))
            return JsonResponse(json.loads(response), safe=False)
        except Exception as e:
            # Vrácení chyby při neplatném požadavku
            return JsonResponse({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error",
                    "data": str(e)
                },
                "id": None
            })
    return JsonResponse({"error": "Method not allowed"}, status=405)

# Metoda pro reset databáze
# - Maže všechny existující knihy
# - Načítá počáteční data z fixtures
def reset_data(request):
    try:
        Book.objects.all().delete()
        call_command('loaddata', 'library_rest/fixtures/books.json', verbosity=0)
        messages.success(request, 'Data reset successful!')
    except Exception as e:
        messages.error(request, f'Error resetting data: {str(e)}')
    return redirect('library_rpc:index') 
