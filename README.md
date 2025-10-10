# Banking Automation Bot

🚀 **Banking Automation Bot** is a Django + Docker based automation tool designed to streamline financial workflows.  
Currently in **early development** — this repo serves as the foundation for one of my top 5 backend projects over the next year.

---

## 📌 Project Vision
The Banking Automation Bot will:
- Automate repetitive banking tasks
- Provide secure API integrations with financial data sources
- Offer a modular design for expansion (e.g., budgeting, reconciliation, reporting)

---

## 🛠️ Tech Stack
- **Backend:** Django
- **Containerization:** Docker + Docker Compose
- **Database:** PostgreSQL (planned)
- **Auth:** JWT / Django auth (planned)
- **CI/CD:** GitHub Actions (planned)

---

## 📂 Repo Status
This is an **early-stage skeleton repo**. Core development begins later in 2025.  
In the meantime:
- [ ] Scaffold Django app
- [ ] Set up Docker + Compose
- [ ] Integrate PostgreSQL
- [ ] Define automation modules

---

## 🔮 Roadmap
- **Phase 1:** Project scaffolding & Docker setup
- **Phase 2:** Core banking automation engine
- **Phase 3:** API integrations (bank feeds, transaction exports)
- **Phase 4:** Security hardening & CI/CD pipelines
- **Phase 5:** Documentation & deployment

---

## 🚀 Phase 1 Complete — Authentication + Plaid Integration Stub

![Status](https://img.shields.io/badge/Phase%201%20Complete-✅%20Auth%20%2B%20Plaid%20Stub-brightgreen)
![Tests](https://img.shields.io/badge/pytest-passing-success)
![Framework](https://img.shields.io/badge/Django-5.2.3-blue)
![API](https://img.shields.io/badge/DRF-SimpleJWT-lightblue)
![Integration](https://img.shields.io/badge/Plaid-Mock%20Sandbox-yellow)

### ✅ Summary

Phase 1 establishes the foundation for the **Automated Personal Finance Sync Bot**, delivering:
- 🔐 Full JWT-based user authentication (register, login, logout).
- 🧩 A **Mock Plaid Client** simulating link token creation, token exchange, and account retrieval.
- ⚙️ Verified endpoints under `/api/plaid/` for authenticated users.
- 🧪 Passing end-to-end tests confirming integration flow.
- 🧱 CI-ready code structure for future Plaid Sandbox upgrade.

This milestone completes the **MVP authentication layer** and sets the stage for Phase 2:  
**→ Plaid Sandbox Integration and Transaction Sync.**

---

## 👨‍💻 Author
Brice Nelson — Python Developer (Backend/FinTech)  
[LinkedIn](https://www.linkedin.com/in/brice-a-nelson-p-e-mba-36b28b15/) • [Portfolio](https://www.devbybrice.com)
