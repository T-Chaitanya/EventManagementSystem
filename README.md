# Event Management System API

A Django REST Framework project to manage event creation, attendee registration, and event listings. It supports time zone-aware scheduling, pagination, Swagger documentation, and unit testing.

GitHub Repo: https://github.com/T-Chaitanya/EventManagementSystem  
Swagger Docs: http://localhost:8000/docs/ (after running locally)

---

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/T-Chaitanya/EventManagementSystem.git
cd EventManagementSystem
````

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

6. Access the API Docs:

* Swagger UI: [http://localhost:8000/docs/](http://localhost:8000/docs/)
* ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Features

* Events are created in IST (Asia/Kolkata), stored as UTC in the database.
* Clients can pass the `tz` query parameter to view event times in their local timezone.
* Attendee email is unique per event (duplicate emails blocked).
* Event registration will fail if capacity is reached.

---

## API Endpoints

### Create Event

POST `/api/events/`

Request Body:

```json
{
  "event_name": "Django REST Workshop",
  "event_location": "Online",
  "start_time": "2025-08-01T14:00:00",
  "end_time": "2025-08-01T16:00:00",
  "max_capacity": 100
}
```

Curl:

```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{"event_name":"Django REST Workshop","event_location":"Online","start_time":"2025-08-01T14:00:00","end_time":"2025-08-01T16:00:00","max_capacity":100}'
```

---

### List Events

GET `/api/events/`

Optional Query Params:

* `type=past` or `type=upcoming`
* `page=1&size=5`
* `tz=America/New_York` (converts times to desired timezone)

Curl:

```bash
curl "http://localhost:8000/api/events/?type=upcoming&page=1&size=5&tz=UTC"
```

---

### Register Attendee

POST `/api/events/{event_id}/register/`

Request Body:

```json
{
  "attendee_name": "Chaitanya",
  "email": "chaitanya@example.com"
}
```

Curl:

```bash
curl -X POST http://localhost:8000/api/events/1/register/ \
  -H "Content-Type: application/json" \
  -d '{"attendee_name":"Chaitanya","email":"chaitanya@example.com"}'
```

---

### List Attendees for an Event

GET `/api/events/{event_id}/attendees/`

Optional: `?page=1&size=10`

Curl:

```bash
curl "http://localhost:8000/api/events/1/attendees/?page=1&size=10"
```

---

## Pagination Response Format

All paginated endpoints return responses in this format:

```json
{
  "count": 24,
  "page": 1,
  "size": 10,
  "results": [
    {
      "id": 1,
      "event_name": "Django REST Workshop",
      "start_time": "2025-08-01T09:00:00-04:00",
      "end_time": "2025-08-01T11:00:00-04:00"
    }
  ]
}
```

---

## Timezone Support

* Internally stored in UTC.
* Use ?tz=\<timezone\_name> to convert start\_time and end\_time.
* Example: `?tz=Asia/Kolkata` or `?tz=America/New_York`.

---

## Running Unit Tests

Install dev dependencies:

```bash
pip install pytest pytest-django
```

Run tests:

```bash
pytest
```

Tests cover:

* Event creation
* Event listing (past/upcoming)
* Attendee registration and duplicates
* Attendee listing

---

## Project Structure

```
EventManagementSystem/
├── events/               # Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── tests/                # Pytest unit tests
│   ├── test_events.py
│   ├── test_attendees.py
│   └── test_registration.py
├── EventManagement/           # Django project config
│   └── settings.py
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Author

Chaitanya Tata

GitHub: [@T-Chaitanya](https://github.com/T-Chaitanya)

---

