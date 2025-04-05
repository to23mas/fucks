# Použití oficiálního Python obrazu jako základu
# Slim-buster varianta pro menší velikost obrazu
FROM python:3.11.4-slim-buster

# Nastavení pracovního adresáře v kontejneru
WORKDIR /usr/src/app

# Nastavení proměnných prostředí pro Python
# Zabrání vytváření .pyc souborů
ENV PYTHONDONTWRITEBYTECODE 1
# Zajistí okamžitý výpis logů (bez bufferování)
ENV PYTHONUNBUFFERED 1

# Instalace cronu a dalších závislostí
# Příkaz rm -rf odstraní apt cache pro zmenšení velikosti obrazu - best practice pro Docker obrazy
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Kopírování souborů s požadavky a proměnnými prostředí
COPY ./requirements.txt requirements.txt
# Bez nakopírování proměnných be cron neměl přístup k databázi
COPY .env /etc/environment

# Aktualizace pip a instalace Python závislostí
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Vytvoření souboru pro logy a nastavení oprávnění
# Chmod 0644 nastaví oprávnění pro čtení všem a zápis pouze vlastníkovi
# Důvodem je abychom si mohli snáze přečíst logy
RUN touch /var/log/cron.log && chmod 0644 /var/log/cron.log
