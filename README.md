# FastAPI Investment App

## Description
A FastAPI application designed to process company turnover files and provide valuable information to investors.

## Features
- **User Authentication and Authorization**
- **File Upload and Processing**: Supports Excel, PDF, and CSV formats
- **Asynchronous Task Processing**: Powered by Celery
- **Logging and Monitoring**
- **Unit Tests and CI/CD Pipeline**
- **Containerization**: Using Docker and Docker Compose

## Installation
Clone the repository and set up the virtual environment:
```sh
git clone https://github.com/anuup22/BizMetrics.git
cd BizMetrics
python -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application
Start the FastAPI application with:
```sh
uvicorn app.main:app --reload
```

## Running with Docker
Build and run the application using Docker Compose:
```sh
docker-compose up --build
```

## Running Tests
Execute the tests using:
```sh
pytest
```

## API Documentation
Access the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
