To install:
1. python -m venv .venv
2. ./.venv/Scripts/activate
3. pip install -r requirements.txt
4. Install PostgreSQL 17
5. Create a DB and a user account
6. Create a file called .env and fill in the following properties:
  SECRET_KEY
  DEBUG
  DB_NAME
  DB_USER
  DB_PASSWORD
  DB_HOST
  DB_PORT
  DB_SSLMODE
7. python manage.py migrate
8. python manage.py createsuperuser
