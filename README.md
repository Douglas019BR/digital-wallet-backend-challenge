# FastApiBoilerPlate

Original challenge : [repositorio](https://github.com/WL-Consultings/challenges/tree/main/backend) 

## Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/) installed.

## Configuration

1. Rename the `.env.template` file to `.env` and configure the environment variables as needed.

2. Ensure that the dependencies are correctly listed in the `requirements.txt` and `requirements-dev.txt` files.

## How to Run with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t fastapi-boilerplate .
   ```

2. **Run the container**:
   ```bash
   docker run -d --name fastapi-app -p 8000:8000 fastapi-boilerplate
   ```

3. **Access the application**:
   - Open the application in your browser at: [http://localhost:8000](http://localhost:8000)
   - Access the interactive API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

## How to Run with Docker Compose

1. **Start the services**:
   ```bash
   docker-compose up -d
   ```

2. **Access the application**:
   - Open the application in your browser at: [http://localhost:8000](http://localhost:8000)
   - Access the interactive API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Development

For local development, you can use Python's virtual environment:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. Install the dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Run the local server:
   ```bash
   uvicorn main:app --reload
   ```

## License

This project is licensed under the [MIT License](LICENSE).


# Subir novamente
docker-compose up -d

# Executar as migrações
docker-compose exec web alembic upgrade head

# Aplicar o seed
docker-compose exec web python seeds/create_admin_user.py