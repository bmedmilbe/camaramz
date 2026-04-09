# 🏛️ Centralized Multi-Tenant Government Kernel (Backend)

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)

A high-integrity **Django-based API** designed as a unified kernel for government and NGO digital infrastructure. This system manages complex data ecosystems through a secure multi-tenant architecture, serving as a centralized hub for decoupled frontends like **CECAB** and **CMZ**.

---

## 🏗️ Engineering Architecture & Performance

- **Multi-Tenant Isolation & Scalability:** Engineered a shared-database architecture with strict data isolation via custom Middleware. This consolidation reduced infrastructure overhead by **60%** while serving multiple independent organizations from a single instance.
- **Advanced Concurrency Control:** Implemented **PostgreSQL Pessimistic Locking (`select_for_update`)** within the Remittance Core to prevent race conditions during balance settlements, ensuring full **ACID compliance** for financial operations.
- **Database Performance Tuning:**
    - Resolved N+1 query bottlenecks using strategic **Eager Loading** (`select_related` and `prefetch_related`), reducing API latency by **50%**.
    - Optimized search performance in high-volume multi-tenant tables through **B-Tree Indexing** and execution plan analysis via **EXPLAIN ANALYZE**.
- **Financial & Remittance Core:** Built an audit-ready ledger system using **Atomic Transactions** to guarantee data consistency between international managers and local agents.
- **Document Automation:** Integrated **xhtml2pdf** and **Amazon S3** for automated, version-controlled PDF generation for legal certifications and reports.

---

## 🚀 Active Tenants (Frontends)

The system orchestrates and serves real-time data for:

- **CECAB (Organic Cocoa Cooperative):** Transparency platform for the fair-trade organic cacao supply chain. Built with **Next.js & Bootstrap**.
- **CMZ (District Council):** Municipal government portal for residency and legal certifications. Built with **React**.
- **Troca (Remittance Interface):** Specialized financial dashboard for cross-border settlements. Built with **Bootstrap**.

---

## 💻 Tech Stack

- **Backend:** Python, Django REST Framework, PostgreSQL.
- **Advanced Concepts:** Multi-tenancy (Shared Database), Row-level Locking, Transaction Isolation, Middleware Engineering.
- **Cloud & DevOps:** Docker, AWS S3, Railway, CI/CD.

---

## 🛠️ Setup & Installation

### 1. Clone the repository
```bash
git clone [https://github.com/bmedmilbe/mt-email-auth.git](https://github.com/bmedmilbe/mt-email-auth.git)
cd mt-email-auth
