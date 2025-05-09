# Imarika Services API

## Overview

The Imarika Services API is a backend system designed to manage organizational data and operations. It provides functionality for handling entities such as organizations, branches, departments, vacancies, tenders, and more. The API is built to support scalable and efficient management of organizational workflows.

## Features

- **Organization Management**: Manage organizations, branches, and departments.
- **Vacancies and Applications**: Create and manage job vacancies and their applications.
- **Tenders**: Handle tenders and associated files.
- **File and Image Management**: Upload and manage files and images.
- **News and Events**: Manage organizational news and events.
- **User Management**: Support for user authentication and role-based access control.
- **FAQs and Messages**: Manage frequently asked questions and user messages.

## Project Structure
. ├── database/ # SQL scripts and database assets 

    │ ├── imarika.sql # Main database schema 

    │ ├── imarika-copy.sql # Backup or alternative schema 

    │ ├── imarika-erd.pdf # Entity-Relationship Diagram (PDF) 

    │ ├── imarika-erd.png # Entity-Relationship Diagram (Image) 

. ├── Downloads/ # Directory for downloaded files 

    │ └── files/ 

    │ └── download_files/ # Subdirectory for specific downloads 

. ├── org/ # Main application logic 

    │ ├── init.py # Package initialization 

    │ ├── database.py # Database connection and setup 

    │ ├── main.py # Application entry point 

    │ ├── cruds/ # CRUD operations for various entities 

    │ ├── models/ # Database models 

    │ ├── routes/ # API routes 

    │ ├── schemas/ # Pydantic schemas 

    │ └── utils/ # Utility functions 

. ├── storage/ # Directory for uploaded files and images

    │ ├── images/ # Image storage 

    │ └── StatementsPress/ # Additional storage 

. ├── .env # Environment variables 

. ├── .env-dist # Example environment variables 

. ├── .dockerignore # Docker ignore file 

. ├── .gitignore # Git ignore file 

. ├── .gitlab-ci.yml # GitLab CI/CD configuration 

. ├── Dockerfile # Docker configuration 

. ├── requirements.txt # Python dependencies 

. └── README.md # Project documentation


## Prerequisites

- Python 3.10 or higher
- PostgreSQL or MySQL database
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/imaf-server.git
   cd imaf-server

2. Create a virtual environment and activate it

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies

    ```bash
    pip install -r requirements.txt

3. Set up the ***.env*** file based on ***.env-dist***

4. Run the database schema script ***imarika.sql***

    ```bash
    mysql -u username -p databas_name < database/imarika.sql

# Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn org.main:app --port port_number --reload

2. Access the API documentation at:

    -- Swagger UI: http://127.0.0.1:8000/docs
    -- ReDoc: http://127.0.0.1:8000/redoc

# Deployment

1. Build the Docker image:

    ```bash
    docker build -t imaf-server .

2. Run the container

    ```bash
    docker run -d -p 8000:8000 --env-file .env imaf-server

# Contributions
Contributions are welcome! Please follow these steps:

    1. Fork the repository.

    2. Create a new branch for your feature or bugfix.
    
    3. Commit your changes and push them to your fork.
    
    4. Submit a pull request.

# Contact
For inquiries or support, please contact [jeremykatush@gmail.com] or [jeremykurwa02@gmail.com]. ```