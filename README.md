# Blog FastAPI

[![Actions Status](https://github.com/hazzillrodriguez/blog-fastapi/workflows/build/badge.svg)](https://github.com/hazzillrodriguez/blog-fastapi/actions)

This is a blog API with authentication, postings [CRUD], and the ability to vote on a post.

## Installation

These instructions will get you a copy of the project up and running on your local machine.

1. Git clone or download the project files.
```
git clone https://github.com/hazzillrodriguez/blog-fastapi.git && cd blog-fastapi
```

2. Create and activate the virtual environment, then install the requirements.
```
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```

3. Create `.env` file and set the environment variables.
```
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=name_of_your_database_here

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

4. Start Postgres and create a database with the same name as your `DB_NAME`.

5. Start the development server.
```
uvicorn app.main:app --reload
```

This project contains a Swagger UI.

To view this API's Swagger UI, run this application, then navigate to `http://localhost:8000/docs`.<br>
You can test out this API entirely from the Swagger UI page.

## Running the Tests

To run all the tests at once, use the command:
```
pytest -v
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Hazzill Rodriguez — [LinkedIn](https://www.linkedin.com/in/hazzillrodriguez/) — hazzillrodriguez@gmail.com

## Acknowledgments

* [Sanjeev Thiyagarajan — Python API Development Course](https://youtu.be/0sOvCWFmrtA)