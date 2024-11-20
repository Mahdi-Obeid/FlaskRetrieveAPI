# FlaskRetrieveAPI

1. py -m venv .venv

2. source .venv/Scripts/activate

3. .env file with DATABASE & URL & FLASK_APP=main.py

4. database:
    a. flask db init
    b. flask db migrate
    c. flask db upgrade
    d. if error:
        i. SELECT * FROM alembic_version;
        ii. DELETE FROM alembic_version;

5. python main.py | flask run
