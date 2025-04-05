from django.db import models


class Birthday(models.Model):
    # Jméno osoby, jejíž narozeniny jsou uloženy
    name = models.CharField(max_length=100)
    # Skutečné datum narození
    birth_date = models.DateField()
    # Volitelný název kalendáře, kde jsou narozeniny uloženy
    calendar_name = models.CharField(max_length=100, default='')

    class Meta:
        # Řazení narozenin podle data
        ordering = ['birth_date']
        # Zabránění duplicitním záznamům stejného jména a data narození
        unique_together = ['name', 'birth_date']
        # Správný tvar množného čísla pro administrační rozhraní
        verbose_name_plural = 'Birthdays'

    def __str__(self):
        # Formát zobrazení: "Jméno (DD/MM/YYYY)"
        return f"{self.name} ({self.birth_date.strftime('%d/%m/%Y')})"

