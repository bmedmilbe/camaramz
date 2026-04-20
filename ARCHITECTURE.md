# 🏗️ System Architecture: CamaraMZ Kernel

## Overview

CamaraMZ is a **multi-tenant Django REST Framework API** designed as a unified backend for government and NGO digital infrastructure. The system employs a **shared-database multi-tenancy model** with row-level isolation enforced via custom middleware and database constraints.

## Core Architecture Principles

### 1. Multi-Tenancy Design

The kernel serves multiple frontends from a single running instance, optimizing resource usage.

```text
┌─────────────────────────────────────────────────┐
│         Django REST API (Single Instance)       │
├─────────────────────────────────────────────────┤
│  CECAB    │    CMZ     │  Troca  │  (Frontends) │
│  (Next.js)│  (React)   │(Mobile)  │  Clients     │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   TenantMiddleware    Row-Level Isolation
     (Auto-detect)     (DB Constraints)
        │                    │
        └──────────┬─────────┘
                   ▼
        ┌──────────────────────┐
        │ Shared PostgreSQL DB │
        │                      │
        │ Tenant: CECAB        │
        │ Tenant: CMZ          │
        │ Tenant: Troca        │
        └──────────────────────┘


Key Engineering Benefits:
Infrastructure Efficiency: Significant cost reduction by consolidating multiple organizations into one instance.
Data Integrity: Strict isolation ensures Tenant A can never access Tenant B's data.
Unified Logic: Security patches and feature updates are deployed once and benefit all tenants simultaneously.
2. Request Isolation Flow
Request Entry: The middleware identifies the tenant via the subdomain (e.g., cecab.api.com).
Context Binding: The tenant_id is attached to the request object.
Query Filtering: All ViewSets automatically filter data based on the active request.tenant.
Validation: Database-level UniqueConstraints (e.g., unique_email_per_tenant) act as the final line of defense.
3. Database Schema Relationships (Core Modules)

Plaintext


Tenant (Root)
  ├── User (Scoped to Tenant)
  │     ├── bespoketour.Customer
  │     ├── certificates.Customer
  │     ├── ground.Customer
  │     └── troca.Customer (Transaction Owner)
  │
  ├── certificates.Country / City / Institution
  ├── ground.Product / Sell / Expense
  └── fly.Airline / Country / City


🛠️ Design Patterns Used
Middleware Pattern: For transparent tenant detection.
Service Layer (Helpers): Business logic is kept out of views to ensure reusability.
Pessimistic Locking: Utilized in the troca app to ensure financial transaction atomicity.
Author: Edmilbe Ramos
Technical Strategy: Scalable Multi-tenancy & High-Integrity Financial Backend.

```
