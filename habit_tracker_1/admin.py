from django.contrib import admin
from .models import Habit

# Dekorátor @admin.register automaticky registruje model Habit do Django administrace
# Alternativně by bylo možné použít admin.site.register(Habit, HabitAdmin)
# Dekorátor je modernější a přehlednější způsob registrace modelů
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # Definuje sloupce, které se zobrazí v přehledové tabulce návyků
    # id - unikátní identifikátor
    # name - název návyku
    # completed - stav splnění
    # date_completed - datum posledního splnění
    # completion_count - počet splnění
    list_display = ['id', 'name', 'completed', 'date_completed', 'completion_count']
    
    # Nastavuje pole, podle kterých lze vyhledávat v administraci
    # Umožňuje rychlé vyhledání návyku podle jeho názvu
    search_fields = ['name']
    
    # Definuje filtry, které se zobrazí v pravém panelu administrace
    # completed - filtrování podle stavu splnění (splněno/nesplněno)
    # date_completed - filtrování podle data splnění
    list_filter = ['completed', 'date_completed']
