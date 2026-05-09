# Job Application Tracker API 🚀

A production-grade RESTful API designed to help job seekers manage their applications, track status changes, and never miss a follow-up. Built with **Django**, **PostgreSQL**, **Redis**, and **Celery**.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.x + Django REST Framework |
| **Authentication** | JWT (SimpleJWT) + Password Reset Flow |
| **Database** | PostgreSQL 16 |
| **Background Tasks**| Celery + Redis |
| **Infrastructure** | Docker & Docker Compose |
| **Web Server** | Nginx (Reverse Proxy) |
| **Database Management** | Adminer |
| **API Docs** | Swagger / OpenAPI (drf-spectacular) |

---

## ✨ Key Features

### 🔐 Security & Auth
- **JWT Authentication**: Secure stateless login with access and refresh tokens.
- **Interactive Password Reset**: A premium, standalone UI for resetting passwords via email links.
- **Protected Media**: Resumes are obfuscated with UUIDs and can **only** be downloaded by the owner or an admin via a dedicated secure endpoint.

### 💼 Application Tracking
- **CRUD Operations**: Full management of job applications.
- **Automated Timeline**: Every status change (e.g., *Applied* → *Interview*) is automatically logged in a historical timeline.
- **Notes System**: Attach multiple detailed logs and notes to any application.
- **Stats Dashboard**: Get a breakdown of your application success rates.

### 🤖 Automation
- **Async Notifications**: Email notifications are sent in the background when applications are created or updated.
- **Stale Reminders**: A daily background task that warns you about applications that haven't been updated in 7 days.

---

## 🚀 Getting Started

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 2. Launch with Docker
```bash
docker compose up --build -d
```
This will spin up:
- **Django App**: `app.localhost`
- **Postgres DB**
- **Redis Broker**
- **Celery Worker & Beat**
- **Adminer**: `adminer.localhost` (Database GUI)

### 3. Initialize
```bash
docker exec -it learning-project-web-1 python manage.py migrate
docker exec -it learning-project-web-1 python manage.py createsuperuser
```

---

## 📖 API Documentation

Once the app is running, visit:
👉 **[http://app.localhost/api/docs/](http://app.localhost/api/docs/)**

You can interact with all endpoints directly from the browser using the "Authorize" button.

---

## 🌍 Free Deployment Options

If you want to host this for free, here are the best options for this specific stack:

1. **Oracle Cloud (Always Free)**: 
   - **Why**: They give you 4 ARM CPUs and 24GB of RAM for life. 
   - **Best for**: Running this entire Docker stack (Postgres, Redis, Celery, Web) in one place.
   
2. **Koyeb**:
   - **Why**: Excellent support for Docker-based deployments.
   - **Best for**: Simple deployments, though you might need to use their managed Postgres.

3. **Railway**:
   - **Why**: Very easy to setup "one-click" templates for Django + Redis + Postgres.
   - **Best for**: Speed and ease of use.

---

## 👨‍💻 Author
**Mohammed EZ-ZOUAK**
[LinkedIn](https://linkedin.com/in/mohammed-ez-zouak) | [GitHub](https://github.com/mezzouak)