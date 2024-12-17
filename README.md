# FlaskRetrieveAPI

1. install virtual environment : py -m venv .venv

2. .env file with DATABASE & URL & FLASK_APP=main.py

3. database:
    a. flask db init
    b. flask db migrate
    c. flask db upgrade
    d. if error:
        i. SELECT * FROM alembic_version;
        ii. DELETE FROM alembic_version;

4. python main.py | flask run
