# 🔌 API Reference Guide: CamaraMZ Kernel

This API is the centralized engine for Municipal Management and NGO Services. It uses **OpenAPI 3.0** (OAS) and is fully documented via Swagger.

## 🔐 Authentication (JWT)

The system uses `djoser` for identity management. All protected resources require a Bearer Token.

| Action                   | Method | Endpoint             |
| :----------------------- | :----- | :------------------- |
| **Login / Create Token** | `POST` | `/auth/jwt/create/`  |
| **Refresh Token**        | `POST` | `/auth/jwt/refresh/` |
| **User Registration**    | `POST` | `/auth/users/`       |
| **My Profile**           | `GET`  | `/auth/users/me/`    |

---

## 🏛️ Domain-Specific Modules

### 1. Certificates & Governance (`/certificates/`)

Manages official documentation and institutional registers.

- `GET /certificates/documents/` - List all certificates.
- `GET /certificates/institutions/` - List registered government bodies.
- `GET /certificates/countries/` & `cities/` - Geographical registers.

### 2. Financial Remittance (`/troca/`)

Secure transaction kernel for currency exchange and transfers.

- `POST /troca/transactions/` - Execute new financial settlement.
- `GET /troca/customers/` - Manage authorized financial agents.
- **Note:** Implements _Pessimistic Locking_ for balance integrity.

### 3. Operations & Logistics (`/ground/` & `/fly/`)

Inventory management and travel inquiries.

- `GET /ground/products/` - Stock and inventory tracking.
- `GET /ground/sells/` - Sales records.
- `GET /fly/airlines/` - Aviation partners and flight inquiries.

### 4. Specialized Services (`/bespoketour/`)

- `GET /bespoketour/customer/` - Specialized profile management.

---

## 🛠️ Integration Tools

Since the backend uses `drf-spectacular`, you can interact with the API in real-time:

- **Interactive Swagger UI:** `http://localhost:8000/api/swagger/`
- **Technical ReDoc:** `http://localhost:8000/api/redoc/`
- **JSON Schema:** `http://localhost:8000/api/schema/`

---

## 📐 Implementation Details

- **Multi-Tenancy:** Each request is scoped to a `Tenant` via the subdomain/middleware.
- **Response Format:** Standard JSON.
- **Pagination:** Uses `LimitOffsetPagination` for large datasets (e.g., `?limit=20&offset=0`).
