personal-finance-sync-bot/
│
├── .env.example              # Example environment variables (never commit the real .env!)
├── .gitignore
├── README.md
├── requirements.txt
│
├── config/                   # Django project package (settings, URLs, WSGI/ASGI)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py                 # Django project management script
│
├── finance/                  # Your Django app for financial logic
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── ...
│
├── streamlit_app/            # Streamlit MVP app
│   ├── __init__.py
│   ├── app.py
│   └── utils.py
│
├── backend/                  # Shared backend logic (optional, reusable modules)
│   ├── __init__.py
│   ├── plaid_client.py       # Plaid API integration
│   ├── categorizer.py        # Categorization logic
│   ├── reporting.py          # Report/PDF generation
│   └── db.py                 # DB helpers for non-Django code
│
├── scripts/                  # One-off utility scripts
│   └── ...
│
├── tests/                    # Project-wide tests (if not in each app)
│   └── ...
│
└── docs/                     # Extra documentation, architecture, diagrams
    └── architecture.md
