# Authentication Implementation Roadmap
## Automated Personal Finance Sync Bot

---

## Current State Analysis

**Project Setup:**
- Django 5.2.3 with default configuration
- Empty app modules: `backend/`, `finance/`, `streamlit_app/`
- Using SQLite (temporary - will migrate to PostgreSQL)
- Plaid Python SDK installed
- No custom authentication implemented yet

**Immediate Security Issues to Address:**
- ⚠️ Hardcoded SECRET_KEY in settings.py:23
- ⚠️ DEBUG mode enabled
- ⚠️ No environment-based configuration
- ⚠️ Default ALLOWED_HOSTS = []

---

## 1. Authentication Architecture Options

### Option A: Django REST Framework (DRF) + JWT (Recommended)
**Best for:** API-first architecture, mobile/SPA support, microservices-ready

**Stack:**
- `djangorestframework` - RESTful API framework
- `djangorestframework-simplejwt` - JWT authentication
- `drf-spectacular` - OpenAPI/Swagger documentation
- `django-cors-headers` - CORS management for frontend

**Pros:**
- Stateless authentication (scalable)
- Perfect for React/Vue frontends + Streamlit integration
- Industry-standard for fintech APIs
- Token refresh mechanism built-in
- Easy to add rate limiting and throttling

**Cons:**
- More complex initial setup
- Token management requires careful handling
- Need to implement token blacklisting for logout

### Option B: Django Session-Based Auth + django-allauth
**Best for:** Traditional web app, simpler deployment, server-side rendering

**Stack:**
- Built-in Django auth system
- `django-allauth` - Comprehensive auth with social login
- Session-based authentication

**Pros:**
- Simpler to implement initially
- Built-in CSRF protection
- Better for traditional Django templates
- Easy password reset flows

**Cons:**
- Session state requires sticky sessions or shared session storage
- Less flexible for API consumption
- Not ideal for mobile apps or separate frontend

### Recommendation: **Option A (DRF + JWT)**
Aligns with your phased approach (Streamlit MVP → Django Production) and provides the flexibility needed for a modern fintech application.

---

## 2. Custom User Model Design

**Why Custom User Model?**
Django recommends creating a custom user model at the start of every project, even if you don't need customization initially. This is especially critical for fintech apps where you'll likely need additional user fields.

### Proposed User Model (`backend/models.py` or `finance/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom user model for banking automation app.
    """
    # Use UUID as primary key for better security
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Additional fields for fintech use case
    email = models.EmailField(unique=True)  # Override to make required and unique
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Plaid-specific fields
    plaid_access_token = models.TextField(blank=True, null=True)  # Encrypted
    plaid_item_id = models.CharField(max_length=255, blank=True, null=True)

    # Account management
    email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_plaid_sync = models.DateTimeField(null=True, blank=True)

    # Preferences
    notification_preferences = models.JSONField(default=dict)
    timezone = models.CharField(max_length=50, default='UTC')

    USERNAME_FIELD = 'email'  # Use email for login
    REQUIRED_FIELDS = ['username']  # Required for createsuperuser

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
```

**Important:** Custom user model must be created BEFORE first migration.

---

## 3. Authentication Endpoints Structure

### Core Auth Endpoints

```
POST   /api/auth/register/              - User registration
POST   /api/auth/login/                 - Login (returns JWT tokens)
POST   /api/auth/logout/                - Logout (blacklist token)
POST   /api/auth/token/refresh/         - Refresh access token
POST   /api/auth/password/reset/        - Request password reset
POST   /api/auth/password/reset/confirm/ - Confirm password reset
POST   /api/auth/email/verify/          - Send verification email
GET    /api/auth/email/verify/:token/   - Confirm email verification
GET    /api/auth/me/                    - Get current user profile
PATCH  /api/auth/me/                    - Update user profile
POST   /api/auth/2fa/enable/            - Enable 2FA (future)
POST   /api/auth/2fa/verify/            - Verify 2FA code (future)
```

### Plaid Integration Endpoints

```
POST   /api/plaid/create-link-token/    - Get Plaid Link token (authenticated)
POST   /api/plaid/exchange-token/       - Exchange public_token for access_token
GET    /api/plaid/accounts/             - Get linked accounts
POST   /api/plaid/sync/                 - Trigger manual sync
DELETE /api/plaid/unlink/               - Remove Plaid connection
```

### Protected Resource Endpoints

```
GET    /api/transactions/               - List transactions
GET    /api/transactions/:id/           - Transaction detail
GET    /api/accounts/                   - List connected accounts
GET    /api/reports/                    - List available reports
GET    /api/reports/:id/download/       - Download report PDF
```

---

## 4. Security Implementation Checklist

### Phase 1: Foundation Security (MVP)
- [ ] Move SECRET_KEY to environment variable
- [ ] Install and configure `python-dotenv` for env management
- [ ] Set DEBUG = False for production
- [ ] Configure ALLOWED_HOSTS appropriately
- [ ] Set up CORS headers for API access
- [ ] Implement HTTPS in production (enforce SECURE_SSL_REDIRECT)
- [ ] Configure secure cookie settings (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- [ ] Set up password validators (already in settings)
- [ ] Implement rate limiting on auth endpoints

### Phase 2: Data Security
- [ ] Install django-environ for robust env management
- [ ] Implement field-level encryption for Plaid tokens (django-encrypted-model-fields)
- [ ] Set up database encryption at rest (PostgreSQL)
- [ ] Implement secure token storage (avoid localStorage, use httpOnly cookies)
- [ ] Add request logging and audit trails
- [ ] Set up HSTS headers
- [ ] Configure Content Security Policy (CSP)

### Phase 3: Advanced Security (Production)
- [ ] Implement two-factor authentication (django-otp or pyotp)
- [ ] Add anomaly detection for unusual login patterns
- [ ] Set up automated security scanning (Bandit, Safety)
- [ ] Implement token refresh rotation
- [ ] Add webhook signature verification for Plaid callbacks
- [ ] Configure rate limiting per user
- [ ] Set up DDoS protection (Cloudflare or AWS Shield)
- [ ] Implement account lockout after failed attempts

---

## 5. Token Management Strategy

### JWT Token Design

**Access Token:**
- Short-lived (15 minutes)
- Contains: user_id, email, permissions
- Used for API authentication

**Refresh Token:**
- Longer-lived (7 days)
- Stored in httpOnly cookie (not accessible via JavaScript)
- Used to obtain new access tokens
- Rotates on each use
- Can be revoked/blacklisted

### Token Storage Options

**Option 1: Access Token in Memory + Refresh Token in httpOnly Cookie (Recommended)**
- Most secure for web applications
- Access token stored in application state (React/Vue)
- Refresh token in httpOnly cookie prevents XSS attacks

**Option 2: Both Tokens in httpOnly Cookies**
- Simpler implementation
- Automatic cookie management
- Requires CSRF protection

**Option 3: localStorage (NOT RECOMMENDED)**
- Vulnerable to XSS attacks
- Common but not suitable for fintech apps

---

## 6. Plaid Integration with Auth Flow

### Initial Link Flow

```
1. User logs in → Receives JWT tokens
2. User clicks "Connect Bank"
3. Frontend calls POST /api/plaid/create-link-token/ (authenticated)
4. Backend creates Plaid Link token with user context
5. Frontend opens Plaid Link UI
6. User completes bank login in Plaid modal
7. Plaid returns public_token to frontend
8. Frontend calls POST /api/plaid/exchange-token/ with public_token
9. Backend exchanges for access_token and stores encrypted in database
10. Backend triggers initial transaction sync
```

### Security Considerations for Plaid Integration

- Never expose Plaid access_tokens to frontend
- Encrypt Plaid tokens in database using field-level encryption
- Store Plaid client_id and secret in environment variables
- Validate webhook signatures for Plaid updates
- Implement token refresh for expired Plaid items
- Log all Plaid API calls for audit

---

## 7. Implementation Phases

### Phase 1: MVP Setup (Week 1-2)
**Goal:** Basic authentication with email verification and Streamlit integration

**Tasks:**
1. Create custom User model
2. Install and configure DRF + SimpleJWT
3. Move sensitive config to .env
4. Create user registration endpoint
5. Create login endpoint (returns JWT in httpOnly cookies)
6. Create logout endpoint (clears cookies and blacklists token)
7. Implement email verification flow (required for account activation)
8. Implement basic password reset flow
9. Create "Get Current User" endpoint
10. Set up basic CORS for Streamlit integration
11. Configure cookie-based token storage (both tokens in httpOnly cookies)
12. Write tests for auth endpoints

**Deliverable:** Working auth API with email verification that Streamlit can call

### Phase 2: Plaid Integration (Week 3-4)
**Goal:** Secure Plaid connection flow

**Tasks:**
1. Create Plaid Link token endpoint
2. Create token exchange endpoint
3. Implement encrypted storage for access tokens
4. Create account sync endpoints
5. Set up Plaid webhook handling
6. Implement error handling for Plaid API
7. Create transaction retrieval endpoints
8. Write tests for Plaid integration
9. Document Plaid flow in README

**Deliverable:** Users can connect banks and sync transactions

### Phase 3: Security Hardening (Week 5-6)
**Goal:** Production-ready security

**Tasks:**
1. Implement token refresh rotation
2. Add rate limiting (django-ratelimit or throttling)
3. Set up token blacklisting for logout
4. Configure all security headers (CSP, HSTS, etc.)
5. Implement field-level encryption for sensitive data
6. Set up audit logging
7. Add email verification flow
8. Implement account lockout mechanism
9. Security audit and penetration testing
10. Document security measures

**Deliverable:** Production-ready secure authentication

### Phase 4: Advanced Features (Week 7+)
**Goal:** Enhanced security and UX

**Tasks:**
1. Implement 2FA with TOTP
2. Add social login (Google, Apple) via django-allauth
3. Implement "Remember this device" functionality
4. Add session management UI
5. Create admin dashboard for user management
6. Set up automated security scanning in CI/CD
7. Implement anomaly detection
8. Add comprehensive monitoring and alerting

**Deliverable:** Enterprise-grade authentication system

---

## 8. Environment Configuration Template

### `.env` file structure

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here-use-strong-random-string
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (PostgreSQL for production)
DB_NAME=banking_automation
DB_USER=dbuser
DB_PASSWORD=strong-db-password
DB_HOST=localhost
DB_PORT=5432

# Plaid Configuration
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret-sandbox
PLAID_ENVIRONMENT=sandbox  # sandbox, development, or production

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=15  # minutes
JWT_REFRESH_TOKEN_LIFETIME=7  # days
JWT_ALGORITHM=HS256

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Encryption Keys
FIELD_ENCRYPTION_KEY=your-field-encryption-key-base64

# Frontend Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8501

# Security
SECURE_SSL_REDIRECT=True  # Only in production
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 9. Testing Strategy

### Unit Tests
- User model creation and validation
- JWT token generation and validation
- Password hashing and verification
- Email verification logic
- Plaid token encryption/decryption

### Integration Tests
- Full registration flow
- Login and token refresh flow
- Password reset flow
- Plaid Link and token exchange
- Transaction sync process

### Security Tests
- SQL injection attempts
- XSS attack vectors
- CSRF protection validation
- Rate limiting enforcement
- Token expiration handling
- Unauthorized access attempts

---

## 10. Migration from SQLite to PostgreSQL

**Before First Migration:**
1. Set up PostgreSQL database (local or cloud)
2. Update settings.py with PostgreSQL config
3. Install psycopg2-binary: `pip install psycopg2-binary`

**Database Configuration:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

---

## 11. Recommended Package Additions

```
# Add to requirements.txt

# REST Framework
djangorestframework==3.15.1
djangorestframework-simplejwt==5.3.1
drf-spectacular==0.27.2  # API documentation

# Security
django-cors-headers==4.4.0
django-ratelimit==4.2.0
django-encrypted-model-fields==0.6.5
cryptography==44.0.0

# Environment Management
django-environ==0.12.0

# PostgreSQL
psycopg2-binary==2.9.10

# Email
django-ses==4.3.0  # If using AWS SES

# Testing
pytest-django==4.9.0
factory-boy==3.3.1
faker==33.2.0
```

---

## 12. Next Steps

### Immediate Actions (This Week):
1. **Review and approve this roadmap**
2. **Choose authentication approach** (DRF + JWT recommended)
3. **Set up environment variables** (.env file)
4. **Create custom User model** (BEFORE any migrations!)
5. **Install core dependencies** (DRF, SimpleJWT, etc.)

### Week 1 Tasks:
1. Create `backend` app for authentication
2. Implement custom User model
3. Configure settings for JWT and DRF
4. Create registration and login endpoints
5. Write basic tests
6. Document API endpoints in README

### Questions to Discuss:
- Do you want to support social login (Google/Apple) initially?
- Should we implement email verification from the start or defer to Phase 3?
- Do you want 2FA in MVP or production phase?
- Preference for access token storage: memory + httpOnly cookie or both in cookies?
- Timeline expectations for each phase?

---

## Resources

**Django REST Framework:**
- https://www.django-rest-framework.org/
- https://django-rest-framework-simplejwt.readthedocs.io/

**Plaid API:**
- https://plaid.com/docs/
- https://plaid.com/docs/link/

**Security Best Practices:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Django Security: https://docs.djangoproject.com/en/5.2/topics/security/

**Testing:**
- pytest-django: https://pytest-django.readthedocs.io/
