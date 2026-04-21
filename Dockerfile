FROM python:3.11

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn psycopg2-binary

COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "SkyApp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]