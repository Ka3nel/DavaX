# 🧮 Math Microservice API (FastAPI + SQLite)

A lightweight, production-ready Python microservice that exposes a RESTful API to perform common math operations:

- Exponentiation (`pow`)
- Fibonacci numbers (`fib`)
- Factorials (`fact`)

All API calls are logged to an SQLite database and protected by an API token.

---

## 🚀 Features

- ✅ **FastAPI** for blazing-fast REST API
- ✅ **SQLite** for lightweight local persistence
- ✅ **MVCS** architecture (Model-View-Controller-Service)
- ✅ **Authorization** using configurable API token
- ✅ **Logging** via `loguru`
- ✅ Built for extensibility and possible future upgrades

---

## 🗂️ Project Structure

```
math_service/
├── app/
│   ├── main.py                 # Entry point
│   ├── api/                    # API endpoints
│   │   ├── routes.py
│   ├── controllers/            # Handles incoming requests
│   │   ├── math_controller.py
│   ├── services/               # Business logic
│   │   ├── mat_service.py
│   ├── models/                 # DB schema/models
│   ├── db/                     # SQLite engine and DB functions
│   │   ├── database.py
│   ├── auth/                   # Token-based authorization
│   │   ├── auth.py
│   ├── logger/                 # Logging setup
│   │   ├── logger.py
│   └── config.py               # Loads .env variables
├── .env                        # Configurable secrets and settings
├── requirements.txt            # Python dependencies
├── logs/                       # Auto-created log file
│   └── app.log
├── math_ops.db                 # The database
└── README.md                   # This file
```

---

## ⚙️ Setup Instructions

### 1. ✅ Clone the Repo

```bash
git clone https://github.com/your-username/math-microservice.git
cd math-microservice
```

### 2. ✅ Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```

### 3. ✅ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ✅ Configure Environment Variables

Create a `.env` file in the root:

```env
API_TOKEN=Ka3nel
DATABASE_URL=sqlite:///./math_ops.db
LOG_FILE=logs/app.log
```

### 5. ✅ Run the App

```bash
uvicorn app.main:app --reload
```

Open in browser:
```
http://localhost:8000/docs
```

---

## 🔐 Authentication

All endpoints require a valid token in the `Authorization` header.

### Example:

```
Authorization: Ka3nel
```

You can configure this value via `.env`.

---

## 📈 API Endpoints

| Method | Endpoint       | Description                      | Example                                 |
|--------|----------------|----------------------------------|-----------------------------------------|
| GET    | `/api/pow`     | Computes exponentiation          | `?base=2&exponent=5` → 32               |
| GET    | `/api/fib`     | Returns the Nth Fibonacci number | `?n=10` → 55                            |
| GET    | `/api/fact`    | Returns factorial of N           | `?n=5` → 120                            |

---

## 🗃️ Data Persistence

- All API calls are logged to the `requests` table in `math_ops.db`.
- View using any SQLite browser like [DB Browser for SQLite](https://sqlitebrowser.org/)

---

## 📄 Logs

All activity is logged to `logs/app.log` with rotation (1MB, 7-day retention).

---

## 🧪 Testing Example with `curl`

```bash
curl -H "Authorization: Ka3nel" "http://localhost:8000/api/fib?n=7"
```

---

## 🧼 Clean Up

- To reset database: delete `math_ops.db`
- To reset logs: delete `logs/app.log`

---

## 📌 Future Enhancements (Optional)

- Redis or in-memory caching
- Docker support
- JWT-based authentication
- Prometheus/Grafana monitoring

---

## 👨‍💻 Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [Loguru](https://github.com/Delgan/loguru)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)