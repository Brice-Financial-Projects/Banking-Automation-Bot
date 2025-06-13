personal-finance-sync-bot/
│
├── .env.example                # Sample environment variables (never commit .env!)
├── .gitignore
├── README.md
├── requirements.txt
│
├── config/                     # Optional: YAML or Python config files (if needed)
│   └── settings.yaml
│
├── manage.py                   # Django entrypoint
├── django_app/                 # Django project root
│   ├── django_app/             # Django settings, wsgi/asgi, urls
│   │   ├── __init__.py
│   │   ├── settings.py         # DB, secret keys, installed apps
│   │   ├── urls.py
│   │   └── ...
│   ├── finance/                # Django app for financial logic
│   │   ├── __init__.py
│   │   ├── models.py           # Django ORM models
│   │   ├── views.py
│   │   ├── admin.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   └── ...
│   └── ...
│
├── streamlit_app/              # Streamlit MVP
│   ├── __init__.py
│   ├── app.py
│   ├── utils.py
│   └── ...
│
├── backend/                    # Shared backend logic
│   ├── __init__.py
│   ├── plaid_client.py         # Plaid API integration
│   ├── categorizer.py          # Expense categorization logic
│   ├── reporting.py            # Reporting, PDF generation, etc.
│   ├── db.py                   # DB helper functions (for Streamlit or other scripts)
│   └── ...
│
├── scripts/                    # One-off utility scripts
│   ├── __init__.py
│   └── ...
│
├── tests/                      # Tests for all major modules
│   ├── __init__.py
│   ├── test_backend.py
│   └── ...
│
└── docs/                       # Docs, diagrams, API references
    └── architecture.md
