# DataPii API

## Description

DataPii API is a FastAPI application designed to manage data routes for Embrapii. It provides endpoints for authentication and data retrieval, allowing users to interact with the database to fetch and insert records.

## Installation

To set up the project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Database Initialization

Before running the application, it's important to initialize the database. Execute the following command to set up the necessary database tables and initial data:

```bash
python init_db.py
```


To run the application, execute the following command:

```bash
uvicorn main:app --reload
```

This will start the FastAPI server, and you can access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- **POST /token**: Authenticate and generate a JWT token.
- **GET /general-numbers/latest**: Retrieve the latest records from the `tb_general_numbers` table.
- **GET /general-numbers/all**: Retrieve all records from the `tb_general_numbers` table.
- **POST /general-numbers**: Insert a new record into the `tb_general_numbers` table.

Ensure you have the necessary environment variables set up as specified in the `.env` file for database connections and other configurations.
