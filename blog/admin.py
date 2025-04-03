from django.contrib import admin
from .models import Category, Post

# Dekorátor @admin.register automaticky registruje model Category do Django administrace
# Alternativně by bylo možné použít admin.site.register(Category, CategoryAdmin)
# Dekorátor je modernější a přehlednější způsob registrace modelů
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Definuje sloupce, které se zobrazí v přehledové tabulce kategorií
    # id - unikátní identifikátor
    # name - název kategorie
    list_display = ['id', 'name']
    
    # Nastavuje pole, podle kterých lze vyhledávat v administraci
    # Umožňuje rychlé vyhledání kategorie podle jejího názvu
    search_fields = ['name']

# Dekorátor @admin.register automaticky registruje model Post do Django administrace
# Alternativně by bylo možné použít admin.site.register(Post, PostAdmin)
# Dekorátor je modernější a přehlednější způsob registrace modelů
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Definuje sloupce, které se zobrazí v přehledové tabulce příspěvků
    # id - unikátní identifikátor
    # title - název příspěvku
    # created_at - datum vytvoření
    # updated_at - datum poslední úpravy
    list_display = ['id', 'title', 'created_at', 'updated_at']
    
    # Nastavuje pole, podle kterých lze vyhledávat v administraci
    # Umožňuje vyhledávání příspěvků podle názvu nebo obsahu
    search_fields = ['title', 'content']
    
    # Definuje filtry, které se zobrazí v pravém panelu administrace
    # created_at - filtrování podle data vytvoření
    # categories - filtrování podle kategorií
    list_filter = ['created_at', 'categories']
    
    # Nastavuje widget pro výběr kategorií
    # Umožňuje pohodlný výběr více kategorií pomocí přetahování
    filter_horizontal = ['categories']
