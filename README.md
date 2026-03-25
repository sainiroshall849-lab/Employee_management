# Employee Management System

A robust FastAPI-based Employee Management System with comprehensive error handling, validation, and logging.

## Features

- ✅ **Complete CRUD Operations**: Create, Read, Update, Delete employees
- ✅ **Input Validation**: Comprehensive validation with Pydantic schemas
- ✅ **Error Handling**: Detailed error handling with proper HTTP status codes
- ✅ **Logging**: Structured logging to files and console
- ✅ **Database**: SQLite with SQLAlchemy ORM
- ✅ **API Documentation**: Interactive Swagger UI at `/docs`
- ✅ **Type Safety**: Full Python type annotations
- ✅ **CORS Support**: Cross-Origin Resource Sharing enabled

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/employees` | Create employee |
| GET | `/api/v1/employees` | List all employees |
| GET | `/api/v1/employees/{id}` | Get employee by ID |
| PUT | `/api/v1/employees/{id}` | Update employee |
| DELETE | `/api/v1/employees/{id}` | Delete employee |

## Example Usage

**Create Employee:**
```bash
curl -X POST "http://localhost:8000/api/v1/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "salary": 50000,
    "field": "Engineering"
  }'
```

**Get All Employees:**
```bash
curl "http://localhost:8000/api/v1/employees"
```

## Validation Rules

- **Name**: 2-100 characters, letters/spaces/hyphens/apostrophes only
- **Email**: Valid email format, unique in system
- **Salary**: Non-negative integer, max 10,000,000
- **Field**: 2-100 characters

## Error Responses

The API returns appropriate HTTP status codes:
- `201` - Created (successful creation)
- `200` - OK (successful operations)
- `400` - Bad Request (validation errors)
- `404` - Not Found (employee not found)
- `422` - Unprocessable Entity (invalid data format)
- `500` - Internal Server Error (server issues)

## Logging

Application logs are stored in `logs/app.log` with the following levels:
- INFO: General operations
- WARNING: Validation failures
- ERROR: Database/server errors

## Project Structure

```
Employee_management/
├── main.py                 # FastAPI application
├── Config/
│   └── config.py          # Configuration settings
├── Models/
│   └── employee_models.py # Database models
├── Routes/
│   └── employee_routes.py # API endpoints
├── Schemas/
│   └── employee_schemas.py # Pydantic schemas
├── Services/
│   └── employee_services.py # Business logic
├── db/
│   └── database.py        # Database setup
├── logs/                  # Application logs
├── requirements.txt       # Dependencies
└── .gitignore            # Git ignore rules
```