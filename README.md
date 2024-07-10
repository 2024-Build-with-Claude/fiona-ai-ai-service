# Fiona AI

Fiona AI is an innovative tool designed to streamline the resume creation process for the next generation of job seekers.

## Description

Fiona AI leverages advanced AI technology to revolutionize the way resumes are built. By allowing users to create resumes using natural language, Fiona AI provides a superior resume building experience, helping users construct more comprehensive resumes in less time.

## Features

- Natural language resume building
- AI-powered content suggestions
- Fast and efficient resume creation
- Comprehensive resume output

## Installation

1. Clone the repository:


2. Install the required dependencies:

```bash
poetry install
```

3. Set up your PostgreSQL database and update the database URL in your project configuration.

4. Initialize Alembic:

```bash
alembic init alembic
```

5. Update the `alembic.ini` file with your database URL:

```ini
sqlalchemy.url = postgresql://username:password@localhost/dbname
```

6. add your own enviroment variables to `.env`

7. Create your first migration:

```bash
alembic revision --autogenerate -m "Initial migration"
```

8. Apply the migration:

```bash
alembic upgrade head
```

## Usage

1. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to `http://localhost:8000/docs` to see the Swagger UI documentation.

3. Use the API endpoints to interact with your database.

4. To make changes to your database schema:

- Update your SQLAlchemy models
- Create a new migration:
  ```bash
  alembic revision --autogenerate -m "Description of changes {time}"
  ```
- Apply the migration:
  ```bash
  alembic upgrade head
  ```

## Contributing

We welcome contributions to Fiona AI!

## License

This project is licensed under the MIT License.

## Acknowledgments

- (List any libraries, tools, or resources you've used)
- (Credit any inspirations or similar projects)

## Contact

For any queries or feedback, please reach out to [taiwanesesound@gmail.com](taiwanesesound@gmail.com).