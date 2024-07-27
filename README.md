Here's a README file for deploying the `book_management_system` application:

---

# Book Management System

## Overview

The Book Management System is a FastAPI application designed for managing book information,user reviews,**summarization of book summary** using **GROQ API of llama3 model** and generating book **recommendations based on user genres and ratings using k-Nearest Neighbour**. It integrates with a PostgreSQL database and uses a machine learning model for recommendations.

## Folder Structure

```
book_management_system/
├── Dockerfile
├── config
│   ├── __init__.py
│   └── settings.py
├── docker-compose.yml
├── generate_data.py
├── load_model_data.py
├── main.py
├── requirements.txt
├── routers
│   ├── __init__.py
│   ├── books.py
│   ├── reviews.py
│   ├── summary.py
│   └── user_routes.py
├── sql_app
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── synthetic_books.csv
├── test_main.py
├── train_dataset
│   ├── books_df.pkl
│   ├── label_encoder.pkl
│   └── recommendation_model.pkl
├── train_model.py
└── utils
    ├── __init__.py
    ├── llama3_summary.py
    └── security.py



```

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

Create a `.env` file in the root directory of your project with the following content:

```env
DATABASE_URL=postgresql+asyncpg://airflow:airflow@db/book_management_system
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=book_management_system
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `your_secret_key` with a secure key of your choice.

## Setup and Deployment

1. **Build and Start the Application:**

   Run the following command to build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the Docker images.
   - Start the PostgreSQL database container.
   - Start the FastAPI application container.

2. **Verify the Deployment:**

   Once the containers are up, you can access the FastAPI application at `http://localhost:8000`.

3. **Initialize the Database:**

   The application will automatically create the necessary database tables on startup. Ensure that the database connection parameters in the `.env` file are correct.



5. **Trained model and dataset**

   Trained the recommendation model with synthetic_books.csv by running

   ```bash
   python train_model.py
   ```

   saved  model and dataframe pickle and label encoder files in the `train_dataset` directory.
   
6.  **Async** is used for the API's and database operations

7.  **Volumes for model data and postgres**


    Folder volume is used for the application data
    Docker volume is used for postgres data


## API Endpoints

- **User Management:**
  - `POST /users/`: Create a new user.
  - `POST /login/`: **Authenticate a user and get a JWT token.**

- **Book Management:**
  - `POST /books/`: Add a new book.
  - `GET /books/`: Retrieve all books.
  - `GET /books/{id}`: Retrieve a specific book by its ID.
  - `PUT /books/{id}`: Update a book's information by its ID.
  - `DELETE /books/{id}`: Delete a book by its ID.

- **Reviews:**
  - `POST /books/{id}/reviews`: Add a review for a book.
  - `GET /books/{id}/reviews`: Retrieve all reviews for a book.

- **Summary:**
  - `GET /books/{id}/summary`: Get a summary and aggregated rating for a book.
  - `POST /generate-summary`: Generate a summary for a given book content.

- **Recommendations:**
  - `POST /recommendations`: Get book recommendations based on user preferences.

## Testing

To run the unit tests, use:

```bash
pyyest test_main.py
```

## Notes

- Ensure that the `.env` file is correctly configured with database credentials and secret keys.
- The `docker-compose.yml` file includes configuration for both the PostgreSQL database and the FastAPI application.
- For any changes in the code or configurations, rebuild the Docker images using `docker-compose up --build`.

