# FlaskRetrieveAPI

### 1. Install virtual environment :

```bash
py -m venv .venv
```

### 2. Create .env file with :

```bash
DATABASE = "yourDataBaseName"
FLASK_APP=main.py
URL = "provided url"
```

### 3. Migrate to database:

```bash
a. flask db init
b. flask db migrate
c. flask db upgrade
d. if error:
    i. SELECT * FROM alembic_version;
    ii. DELETE FROM alembic_version;
```

### 4. Import data before running the code:

```bash
python import_data.py
```

### 5. Fetch the project's data:

```bash
python main.py
```

### 6. Run project:

```bash
flask run
```
