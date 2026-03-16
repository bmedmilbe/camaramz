# 🏛️ Centralized Multi-Tenant Government Kernel (Backend)

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust **Django-based API** designed as a unified kernel for government and NGO digital infrastructure. This system manages complex data ecosystems through a secure multi-tenant architecture, serving as a centralized hub for multiple decoupled frontends.

---

## 🚀 Active Tenants

The system currently orchestrates and serves data for:

- **Câmara Mé-Zóchi (CMZ):** The municipal government council for the Mé-Zóchi district of São Tomé and Príncipe.
- **CECAB-STP:** The Organic Cocoa Export Cooperative, a leading fair-trade organization for organic cocoa farmers.

---

## 🏗️ Technical Architecture & Features

- **Multi-Tenant Isolation:** Implemented a centralized database approach with **PostgreSQL**, ensuring 100% data isolation between government districts and NGOs while sharing a single application instance.
- **Domain-Based Routing:** Automatically identifies tenants via subdomains/headers to serve correct branding, site titles, and dedicated SMTP configurations.
- **Financial & Remittance Core:** Engineered an audit-ready ledger using **Django Atomic Transactions** to guarantee 100% consistency for international money transfers.
- **Document Automation:** Integrated **xhtml2pdf** and **Amazon S3** for automated, legally compliant PDF generation and secure cloud storage.
- **Security:** Stateless authentication using **JWT (JSON Web Tokens)** and hardened CORS/CSRF configurations for multi-domain production environments.
- **Infrastructure Impact:** Optimized architecture that reduced infrastructure overhead by **60%**.

---

## 💻 Tech Stack

**Backend:** Python, Django REST Framework, PostgreSQL.
**DevOps:** Docker, AWS S3, Railway.

---

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Virtualenv

### 1. Clone the repository

```bash
git clone [https://github.com/bmedmilbe/mt-email-auth.git](https://github.com/bmedmilbe/mt-email-auth.git)
cd mt-email-auth
```
