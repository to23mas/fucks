# Použití oficiálního Python image, verze 3.11.4, ve verzi "slim-buster" (menší velikost)
FROM python:3.11.4-slim-buster  

# Nastavení pracovního adresáře uvnitř kontejneru
WORKDIR /usr/src/app  

# Zabránění zápisu bytecode souborů (.pyc), což zlepšuje výkon v kontejneru
ENV PYTHONDONTWRITEBYTECODE 1  

# Zajištění, že výstup z Pythonu bude ihned viditelný v logu (nebude bufferován)
ENV PYTHONUNBUFFERED 1  

# Kopírování souboru requirements.txt (seznam závislostí) do pracovního adresáře
COPY ./requirements.txt requirements.txt  

# Aktualizace správce balíčků pip na nejnovější verzi
RUN pip install --upgrade pip  

# Instalace všech závislostí uvedených v requirements.txt
RUN pip install -r requirements.txt 
