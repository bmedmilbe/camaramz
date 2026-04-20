# 📦 Backend Application Architecture

This document details the modular structure of the CamaraMZ Kernel. The system is divided into 9 specialized applications, following the **Separation of Concerns (SoC)** principle and a **Shared-Database Multi-tenant** pattern.

---

## 1. 🔐 Core Layer (`core`)

**Purpose:** The foundation of the system. It handles global infrastructure, multi-tenancy isolation, and identity management.

### Key Models

- **Tenant:** Represents an organization (e.g., CECAB, CMZ).
- **User:** A custom identity model extending `AbstractUser`. Includes `tenant` scoping to ensure a user belongs to exactly one organization.

### Technical Implementation

- **TenantMiddleware:** Automatically extracts the tenant context from requests to enforce data isolation.
- **Scoped Authentication:** Supports Email/Phone login unique to each tenant environment.

---

## 2. 🏛️ Certifications (`certificates`)

**Purpose:** Manages the lifecycle of official documents and government certifications.

- **Workflow:** Handles the transition of documents from `pending` to `shipped`.
- **Automation:** Integrated with `xhtml2pdf` for dynamic PDF generation and AWS S3 for secure archival.

---

## 3. 💸 Financial & Remittance (`troca`)

**Purpose:** A secure cross-border settlement system.

- **Data Integrity:** Uses **Pessimistic Locking (SELECT FOR UPDATE)** to prevent race conditions during balance transfers.
- **Audit Trail:** Comprehensive tracking of agents, authorities, and transaction history to ensure ACID compliance.

---

## 4. 🚜 Operations Management (`ground`)

**Purpose:** Handles inventory, sales, and expense tracking for tenant organizations.

- **Features:** Client management, product stock tracking, and financial destination categorization for expenses.

---

## 5. ✈️ Logistics & Inquiries (`fly`)

**Purpose:** Manages travel-related data, including country/city registers, airline information, and customer inquiries.

---

## 🏗️ Technical Design Patterns

### Multi-Tenant Isolation Pattern

Every tenant-specific model inherits a pattern where:

1. `tenant = ForeignKey(Tenant)` is mandatory.
2. Database-level constraints ensure that unique fields (like email or SKU) are only unique _within_ that specific tenant's scope.

### Performance Optimization

- **Custom QuerySets:** Most models implement an `.optimized()` method using `select_related` and `prefetch_related` to mitigate the N+1 query problem.
- **Signal Handlers:** Located in `signals/`, used for decoupling logic such as automatic profile creation or notification triggers.

### Project Directory Standard

Each application follows a consistent structure for high maintainability:

```text
app_name/
├── models.py          # Database Schema
├── views.py           # API Logic (REST ViewSets)
├── serializers.py     # Data Validation & Transformation
├── signals/           # Decoupled Event Listeners
├── helpers.py         # Reusable Business Logic
├── management/        # Custom CLI Commands
└── migrations/        # Version-controlled Schema Changes


Maintained by: Edmilbe Ramos
Technical Focus: Multi-tenancy, Database Optimization, and Scalable Backend Architecture.

```
