# 🏛️ CamaraMZ: Centralized Multi-Tenant Government Kernel

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)
[![Pipenv](https://img.shields.io/badge/managed%20by-pipenv-yellow.svg)](https://pipenv.pypa.io/)

A production-grade **Django REST Framework API** acting as a unified kernel for government and NGO digital infrastructure. This system powers multiple organizations (Tenants) through a high-performance **Shared-Database Multi-tenant architecture**.

---

## 🎯 Project Scope: The Unified Ecosystem

**CamaraMZ** is a **SaaS Kernel** built on a custom multi-tenant authentication logic originally developed in the [camaramz](https://github.com/bmedmilbe/camaramz) project.

### 🏛️ Institutional Engine (CECAB & CMZ)

These tenants share a core infrastructure with 100% data segregation:

- **Unified CMS Module:** A centralized engine for institutional content, news, and media, filtered dynamically by tenant.
- **Administrative Backoffice (Certificates App):** A specialized layer for official workflows.
  - **CMZ (Municipality):** Automates the issuance of residency certifications and municipal declarations.
  - **CECAB (NGO):** Tracks supply chain transparency and documentation.
  - **Workflow:** Full document lifecycle from application to secure PDF generation.

### 💸 Financial Settlement (Troca)

A high-security module for cross-border remittances.

- **Data Integrity:** Implements **Pessimistic Locking** to ensure atomicity.
- **Auditability:** Full ledger tracking for agents and financial authorities.

---

## 🏗️ Core Engineering Principles

- **Custom Multi-Tenant Auth:** Integration of the identity logic from [camaramz](https://github.com/bmedmilbe/camaramz), enabling users to belong to specific tenants with email-based authentication.
- **Row-Level Isolation:** Enforced via custom Middleware that identifies the organization by subdomain.
- **Hybrid Configuration:** Environment-based settings for Dev/Prod managed via Docker.
- **Cloud-Ready Storage:** AWS S3 integration for certificates and institutional media.

---

## 📚 Technical Documentation

1.  **[ARCHITECTURE.md](ARCHITECTURE.md)** | 2. **[SETUP.md](SETUP.md)** | 3. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | 4. **[APP_STRUCTURE.md](APP_STRUCTURE.md)** | 5. **[DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 🚀 Infrastructure Roadmap

- [ ] **Nginx Reverse Proxy** | [ ] **Pytest Suite** | [ ] **Redis Caching**

---

## 👥 Authorship & Contact

- **Lead Engineer:** [Edmilbe Ramos](https://www.linkedin.com/in/edmilbe-ramos/)
- **Core Auth Logic:** Developed in [camaramz](https://github.com/bmedmilbe/camaramz)
- **Email:** bm.edmilbe@gmail.com
