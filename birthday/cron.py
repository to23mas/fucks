from datetime import date, datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Birthday
import requests

def test_cron_job():
    # Testovací cron úloha spouštěná každou minutu
    # Slouží k ověření, že cron správně funguje
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("--------------------------------")
    print(f"[{current_time}] Test cron job is running!")
    print("--------------------------------")

def send_birthday_emails():
    # Funkce pro odesílání emailových upozornění na narozeniny
    # Kontroluje, zda má někdo dnes narozeniny a posílá oznámení adminovi
    today = date.today()
    # Vyhledání všech narozenin, které připadají na dnešní den
    birthdays = Birthday.objects.filter(
        birth_date__month=today.month,
        birth_date__day=today.day
    )
    
    if birthdays.exists():
        # Získání emailové adresy administrátora
        User = get_user_model()
        admin_email = User.objects.get(username='admin').email
        
        # Vytvoření obsahu emailu
        subject = f"Birthday Notifications for {today.strftime('%B %d')}"
        message = "Today's Birthdays:\n\n"
        
        # Přidání všech dnešních oslavenců do zprávy
        for birthday in birthdays:
            message += f"🎉 {birthday.name}\n"
        
        message += "\nBest wishes,\nBirthday Tracker"
        
        # Odeslání emailu administrátorovi
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )

def send_nameday_emails():
    # Funkce pro kontrolu a oznámení dnešních svátků
    # Využívá externí API pro získání informací o svátcích
    try:
        # Dotaz na REST API pro získání dnešního svátku
        response = requests.get('https://svatkyapi.cz/api/day')
        if response.status_code == 200:
            data = response.json()
            nameday_name = data['name']
            date = data['date']
            
            # Vyhledání osob v databázi, které mají svátek
            matching_birthdays = Birthday.objects.filter(calendar_name=nameday_name)
            
            if matching_birthdays.exists():
                # Získání emailu administrátora
                User = get_user_model()
                admin_email = User.objects.get(username='admin').email
                
                # Vytvoření a odeslání emailu s informacemi o svátku
                subject = f"Name Day Notification for {date}"
                message = f"Today ({date}) is the name day of {nameday_name}!\n\n"
                for birthday in matching_birthdays:
                    message += f"🎉 {birthday.name} (born {birthday.birth_date.strftime('%d/%m/%Y')})\n"
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=False,
                )
    except Exception as e:
        # Logování případných chyb při kontrole svátků
        print(f"Error checking name day: {str(e)}")
