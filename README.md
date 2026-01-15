# TicketApp

A Django web application for managing tickets and reviews.

---

## 🚀 Features

- User authentication
- Create and manage tickets
- Review system
- Dashboard interface

---

## 🛠 Requirements

- Python 3.10+
- pip
- virtualenv (recommended)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/USERNAME/ticketApp.git
cd ticketApp
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 5️⃣ Run migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Start development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 📂 Project Structure

```
ticketApp/
│
├── dashboardApp/
├── userRegister/
├── ticketApp/
├── manage.py
├── requirements.txt
└── .env (not pushed)
```

---

## 🔐 Security Notes

- `.env` is ignored by Git
- Never commit secrets
- Use environment variables in production

---

## 📄 License

This project is for learning purposes.
