# System Architecture

This document provides a comprehensive overview of the Order Processing System's architecture, design decisions, and technical implementation.

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [System Components](#system-components)
- [Data Flow](#data-flow)
- [Directory Structure](#directory-structure)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Data Models](#data-models)
- [API Design](#api-design)
- [Storage Architecture](#storage-architecture)
- [Security Considerations](#security-considerations)
- [Scalability & Performance](#scalability--performance)

## High-Level Overview

The Order Processing System implements a **client-server architecture** with clear separation between presentation, business logic, and data layers.

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT TIER                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Streamlit Web Application                 │    │
│  │  - File Upload UI                                   │    │
│  │  - Results Visualization                            │    │
│  │  - History Management                               │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTP/REST API
                            │ (JSON)
┌───────────────────────────▼──────────────────────────────────┐
│                      APPLICATION TIER                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              FastAPI Backend                        │    │
│  │                                                     │    │
│  │  ┌──────────────┐      ┌────────────────────┐     │    │
│  │  │ API Routes   │─────►│  Core Processor    │     │    │
│  │  │  - Upload    │      │  - Parse           │     │    │
│  │  │  - History   │      │  - Validate        │     │    │
│  │  │  - Download  │      │  - Calculate       │     │    │
│  │  └──────────────┘      │  - Report          │     │    │
│  │                        └────────────────────┘     │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            │ File I/O
┌───────────────────────────▼──────────────────────────────────┐
│                        DATA TIER                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Uploads    │  │   Outputs    │  │    Errors    │     │
│  │  (Raw Files) │  │  (Reports)   │  │   (Logs)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │         history.json (Metadata)                   │      │
│  │  - Submission records                             │      │
│  │  - File associations                              │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## System Components

### 1. Frontend (Streamlit Application)

**Location**: `frontend/app.py`

**Responsibilities**:
- User interface rendering
- File upload handling
- API communication
- State management
- Results visualization

**Key Features**:
- Session state management for navigation
- Real-time file processing feedback
- Toggle between output reports and error logs
- Download functionality
- Historical submission browsing

**Technology**: Streamlit 1.28+

### 2. Backend (FastAPI Application)

**Location**: `backend/`

**Responsibilities**:
- REST API endpoints
- Business logic orchestration
- File processing coordination
- Data persistence management

**Components**:

#### API Layer (`backend/api/routes.py`)
- Handles HTTP requests/responses
- Request validation
- File upload management
- History CRUD operations
- Error handling and HTTP status codes

#### Core Business Logic (`backend/core/`)

**Models** (`models.py`):
- `Order`: Raw order data model
- `ProcessedOrder`: Order with calculated fields
- `CustomerSummary`: Aggregated customer data
- `ProcessingResult`: Complete processing outcome

**Processor** (`processor.py`):
- `parse_order_line()`: Parses pipe-delimited lines
- `calculate_totals()`: Applies business rules (discounts)
- `generate_report()`: Aggregates by customer
- `process_file_content()`: Orchestrates full processing pipeline

### 3. Data Storage

**File System Storage**:
```
backend/data/
├── uploads/     # Original uploaded files
├── outputs/     # Generated reports
├── errors/      # Validation error logs
└── history.json # Submission metadata
```

## Data Flow

### File Upload and Processing Flow

```
1. User uploads file(s) via Streamlit UI
         ↓
2. Streamlit sends multipart/form-data POST to /api/upload
         ↓
3. FastAPI receives file(s)
         ↓
4. For each file:
   a. Generate unique file ID (UUID)
   b. Save to uploads/ directory
   c. Read file content
   d. Pass to processor.process_file_content()
         ↓
5. Processor pipeline:
   a. Split content into lines
   b. Parse each line (parse_order_line)
   c. Validate data
   d. Calculate totals (calculate_totals)
   e. Aggregate by customer (generate_report)
   f. Format as table (tabulate)
         ↓
6. Save results:
   a. Write report to outputs/
   b. Write errors to errors/
         ↓
7. Create submission record:
   a. Generate submission ID
   b. Record timestamp
   c. Associate file IDs
   d. Save to history.json
         ↓
8. Return submission metadata to frontend
         ↓
9. Frontend updates UI and displays results
```

### Data Retrieval Flow

```
1. User selects submission from history
         ↓
2. Frontend requests file content via /api/file/{id}/{type}
         ↓
3. Backend locates file by ID prefix
         ↓
4. Read file content from disk
         ↓
5. Return as PlainTextResponse
         ↓
6. Frontend displays in code block
```

## Directory Structure

```
order-processing-system/
│
├── backend/                    # Backend application
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization
│   │
│   ├── api/                   # API layer
│   │   ├── __init__.py
│   │   └── routes.py          # Route handlers
│   │
│   ├── core/                  # Business logic
│   │   ├── __init__.py
│   │   ├── models.py          # Pydantic models
│   │   └── processor.py       # Processing logic
│   │
│   └── data/                  # Data storage
│       ├── uploads/           # Uploaded files
│       ├── outputs/           # Generated reports
│       ├── errors/            # Error logs
│       └── history.json       # Metadata database
│
├── frontend/                  # Frontend application
│   └── app.py                 # Streamlit app
│
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_processor.py      # Unit tests
│
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # This file
│   ├── QUICKSTART.md
│   ├── API.md
│   ├── DEVELOPMENT.md
│   └── USER_GUIDE.md
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
└── run_app.bat               # Windows launch script
```

## Technology Stack

### Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | FastAPI | 0.100+ | REST API implementation |
| Validation | Pydantic | 2.0+ | Data modeling and validation |
| ASGI Server | Uvicorn | 0.20+ | Production server |
| Table Formatting | Tabulate | 0.9+ | Report generation |
| Testing | Pytest | 7.0+ | Unit testing framework |

**Why FastAPI?**
- Modern async support
- Automatic API documentation (OpenAPI/Swagger)
- Built-in validation with Pydantic
- High performance (comparable to Node.js)
- Type hints throughout

### Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| UI Framework | Streamlit | 1.28+ | Rapid web app development |
| HTTP Client | Requests | 2.31+ | API communication |
| Data Handling | Pandas | 2.0+ | Data manipulation |

**Why Streamlit?**
- Rapid prototyping
- Python-native (no JavaScript required)
- Built-in state management
- Automatic reactive updates
- File upload widgets out-of-the-box

## Design Patterns

### 1. Separation of Concerns

- **Presentation Layer**: Streamlit UI (frontend)
- **Business Logic Layer**: Core processor (backend/core)
- **Data Access Layer**: File I/O and JSON storage (backend/api)

### 2. Repository Pattern

The `history.json` file acts as a simple repository with:
- `load_history()`: Read operation
- `save_history()`: Write operation
- Atomic file operations

### 3. Pipeline Pattern

Order processing follows a pipeline:
```
Raw Text → Parse → Validate → Calculate → Aggregate → Format
```

Each stage is a pure function with single responsibility.

### 4. Error Accumulation Pattern

Rather than failing on first error:
- Collect all validation errors
- Process all valid orders
- Return both results and errors

This allows partial processing and complete error reporting.

### 5. UUID-Based Identification

- Submission IDs: Unique per upload session
- File IDs: Unique per file processed
- Prevents naming collisions
- Enables file association

## Data Models

### Order (Input Model)

```python
class Order(BaseModel):
    order_id: str          # ORD001
    customer_name: str     # John Smith
    product_name: str      # Laptop
    quantity: int          # 2
    unit_price: float      # 999.99
    order_date: date       # 2024-03-15
```

### ProcessedOrder (Enhanced Model)

```python
class ProcessedOrder(Order):
    line_total: float      # quantity × unit_price
    discount_amount: float # 10% if line_total > 500
    net_total: float       # line_total - discount_amount
```

### CustomerSummary (Aggregated Model)

```python
class CustomerSummary(BaseModel):
    customer_name: str     # John Smith
    order_count: int       # 3
    total_items: int       # 4
    gross_total: float     # Sum of line_totals
    total_discount: float  # Sum of discounts
    net_total: float       # gross_total - total_discount
```

### ProcessingResult (Output Model)

```python
class ProcessingResult(BaseModel):
    summary_report: List[CustomerSummary]
    grand_total_gross: float
    grand_total_discount: float
    grand_total_net: float
```

## API Design

### RESTful Endpoints

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| POST | `/api/upload` | Upload and process files | multipart/form-data | Submission record |
| GET | `/api/history` | List all submissions | - | Array of submissions |
| GET | `/api/file/{id}/output` | Get output report | - | Plain text |
| GET | `/api/file/{id}/error` | Get error log | - | Plain text |
| DELETE | `/api/history/{id}` | Delete submission | - | Success message |

### Request/Response Examples

**Upload Request**:
```http
POST /api/upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="files"; filename="orders.txt"
Content-Type: text/plain

ORD001|John Smith|Laptop|2|999.99|2024-03-15
------WebKitFormBoundary--
```

**Upload Response**:
```json
{
  "id": "uuid-submission-id",
  "timestamp": "2024-03-15T10:30:00",
  "files": [
    {
      "id": "uuid-file-id",
      "filename": "orders.txt",
      "output_file": "uuid-file-id_output.txt",
      "error_file": "uuid-file-id_error.txt"
    }
  ]
}
```

## Storage Architecture

### File Naming Convention

```
{file_id}_{original_filename}

Examples:
a36ed576-124a-48b1-93dc-cd4e6f00c5de_orders.txt         # Upload
a36ed576-124a-48b1-93dc-cd4e6f00c5de_output.txt         # Report
a36ed576-124a-48b1-93dc-cd4e6f00c5de_error.txt          # Errors
```

### History Record Structure

```json
{
  "id": "submission-uuid",
  "timestamp": "ISO-8601-datetime",
  "files": [
    {
      "id": "file-uuid",
      "filename": "original-name.txt",
      "output_file": "file-uuid_output.txt",
      "error_file": "file-uuid_error.txt"
    }
  ]
}
```

### Data Persistence Strategy

**Current Implementation**: File-based JSON storage

**Pros**:
- Zero external dependencies
- Simple deployment
- Human-readable
- Git-friendly for development

**Cons**:
- Not suitable for high concurrency
- No ACID guarantees
- Limited querying capabilities

**Migration Path**: For production scale, consider:
- SQLite for single-instance deployments
- PostgreSQL for multi-instance/cloud deployments
- Redis for caching frequently accessed history

## Security Considerations

### Current Implementation

1. **CORS Configuration**: Allows all origins (development mode)
   ```python
   allow_origins=["*"]  # ⚠️ Should be restricted in production
   ```

2. **File Upload Validation**: 
   - File type restriction (`.txt` only)
   - No size limits (potential DoS vector)
   - No virus scanning

3. **Data Validation**:
   - Pydantic models enforce types
   - Business rule validation (non-negative values)
   - Date format validation

### Production Recommendations

1. **CORS**: Restrict to specific domains
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. **File Upload Security**:
   - Implement file size limits (e.g., 10MB max)
   - Scan for malicious content
   - Sanitize filenames (remove path traversal attempts)

3. **Rate Limiting**: Prevent abuse
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

4. **Authentication**: Add user authentication
   - JWT tokens
   - API keys
   - OAuth2

5. **Input Sanitization**: Already partially implemented via Pydantic

6. **HTTPS**: Use TLS certificates in production

## Scalability & Performance

### Current Limitations

- **Synchronous Processing**: Blocks during file processing
- **Single-Threaded**: No parallel processing
- **Local Storage**: Not suitable for distributed systems
- **No Caching**: Repeated reads from disk

### Optimization Strategies

#### Short-Term (Current Architecture)

1. **Async Processing**:
   ```python
   async def process_file_content(content: str) -> Tuple[str, str]:
       # Async I/O operations
   ```

2. **Streaming Large Files**:
   ```python
   async for line in file_stream:
       process_line(line)
   ```

3. **Response Compression**: Enable gzip
   ```python
   app.add_middleware(GZipMiddleware, minimum_size=1000)
   ```

#### Long-Term (Architectural Changes)

1. **Background Task Queue**:
   ```
   User → Upload → Queue Job → Background Worker → Results
   ```
   - Tools: Celery, RQ, or FastAPI BackgroundTasks
   - Benefits: Non-blocking uploads, progress tracking

2. **Database Migration**:
   - PostgreSQL with connection pooling
   - Indexed queries for history lookup
   - JSONB columns for flexible metadata

3. **Caching Layer**:
   ```
   Redis → Recent results, history
   Disk  → Long-term storage
   ```

4. **Horizontal Scaling**:
   ```
   Load Balancer → [API Server 1, API Server 2, ...]
                  ↓
            Shared Storage (S3/MinIO)
                  ↓
            Shared Database
   ```

5. **CDN for Static Assets**: Serve reports via CDN

### Performance Benchmarks

**Current Performance** (Single file, 1000 orders):
- Parse: ~50ms
- Calculate: ~30ms
- Generate Report: ~20ms
- Total: ~100ms

**Bottlenecks**:
- Disk I/O: File writes
- Tabulate formatting: Complex table generation

**Optimization Targets**:
- Parse: Use compiled parser (e.g., polars)
- Report: Cache templates, batch writes
- Overall: Async I/O, connection pooling

## Future Enhancements

### Planned Features

1. **Real-Time Processing**: WebSocket updates
2. **Batch Operations**: Process multiple submissions at once
3. **Export Formats**: CSV, Excel, PDF outputs
4. **Data Validation Rules**: Configurable validation logic
5. **Audit Trail**: Track all changes
6. **Multi-Tenancy**: User accounts and permissions
7. **Analytics Dashboard**: Visualize trends over time

### Technology Considerations

- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis broker
- **Storage**: S3-compatible object storage
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logs with ELK stack

---

## Conclusion

The Order Processing System demonstrates a clean, maintainable architecture suitable for MVP deployment. The modular design allows for incremental improvements and scaling as requirements grow.

For questions about architectural decisions, consult the development team or open an issue on GitHub.
