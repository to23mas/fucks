from django.http import JsonResponse
from django.views.static import serve
import random

WORDS = [
    "PYTHON", "DJANGO", "JAVASCRIPT", "HTML", "CSS",
    "DATABASE", "FRAMEWORK", "CODING", "DEVELOPER",
    "PROGRAMMING", "WEB", "APPLICATION", "SOFTWARE",
    "COMPUTER", "ALGORITHM"
]

def index(request):
    return serve(request, 'hangman/index.html')

def get_word(request):
    random_word = random.choice(WORDS)
    return JsonResponse({'word': random_word})
