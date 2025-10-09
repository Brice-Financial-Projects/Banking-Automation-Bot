banking_automation_bot/
│
├── .env
├── .env.example              # Example environment variables (never commit the real .env!)
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── pytest.ini
│
├── .github
│   └── workflows/
│       ├── ci-cd.yml
│       └── deploy.yml
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
│   ├── admin.py              # Admin configuration for backend
│   ├── models.py             # Custom User model for banking automation application.
│   ├── serializers.py        # Serializers for user authentication and management.
│   ├── urls.py               # URL configuration for backend
│   ├── views.py              # Authentication and user management views.
│   ├── plaid_client.py       # Plaid API integration
│   ├── categorizer.py        # Categorization logic
│   ├── reporting.py          # Report/PDF generation
│   └── db.py                 # DB helpers for non-Django code
│
├── scripts/                  # One-off utility scripts
│   └── ...
│
├── tests/                    # Project-wide tests (if not in each app)
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_backend.py
│   ├── test_utils.py
│   ├── test_financial.py
│   └── ...
│
└── docs/                     # Extra documentation, architecture, diagrams
    ├── auth_implementation_roadmap.md
    ├── security_best_practices.md
    ├── scope_overview.md
    └── architecture.md
