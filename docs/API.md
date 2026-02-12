# API Documentation

Complete reference for the Order Processing System REST API.

## Base URL

```
http://localhost:8000/api
```

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Authentication

**Current Version**: No authentication required

**Future Versions**: Will support JWT tokens or API keys

```http
Authorization: Bearer <token>
```

## Endpoints

### 1. Upload Files

Process one or multiple order files.

**Endpoint**: `POST /api/upload`

**Content-Type**: `multipart/form-data`

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| files | File[] | Yes | One or more text files to process |

**Request Example**:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "files=@orders1.txt" \
  -F "files=@orders2.txt"
```

**Response**: `200 OK`

```json
{
  "id": "a93f9cda-6f67-40d9-888c-881599b1b52a",
  "timestamp": "2024-03-15T14:30:45.123456",
  "files": [
    {
      "id": "ca799abd-1251-4749-b7c3-412a7154f2e0",
      "filename": "orders1.txt",
      "output_file": "ca799abd-1251-4749-b7c3-412a7154f2e0_output.txt",
      "error_file": "ca799abd-1251-4749-b7c3-412a7154f2e0_error.txt"
    },
    {
      "id": "7bd264ff-ae55-46f2-aab2-346af5650084",
      "filename": "orders2.txt",
      "output_file": "7bd264ff-ae55-46f2-aab2-346af5650084_output.txt",
      "error_file": "7bd264ff-ae55-46f2-aab2-346af5650084_error.txt"
    }
  ]
}
```

**Error Responses**:

- `422 Unprocessable Entity`: Invalid file format or missing files
- `500 Internal Server Error`: Processing failure

---

### 2. Get History

Retrieve all processed submissions.

**Endpoint**: `GET /api/history`

**Request Example**:

```bash
curl http://localhost:8000/api/history
```

**Response**: `200 OK`

```json
[
  {
    "id": "a93f9cda-6f67-40d9-888c-881599b1b52a",
    "timestamp": "2024-03-15T14:30:45.123456",
    "files": [
      {
        "id": "ca799abd-1251-4749-b7c3-412a7154f2e0",
        "filename": "orders.txt",
        "output_file": "ca799abd-1251-4749-b7c3-412a7154f2e0_output.txt",
        "error_file": "ca799abd-1251-4749-b7c3-412a7154f2e0_error.txt"
      }
    ]
  },
  {
    "id": "b3331f05-a13f-49e6-90f5-c10a6f17d0dc",
    "timestamp": "2024-03-15T10:15:30.987654",
    "files": [...]
  }
]
```

**Notes**:
- Submissions are ordered by timestamp (newest first)
- Empty array returned if no history exists

---

### 3. Get Output Report

Retrieve the processed output report for a specific file.

**Endpoint**: `GET /api/file/{file_id}/output`

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_id | string (UUID) | Yes | Unique identifier for the file |

**Request Example**:

```bash
curl http://localhost:8000/api/file/ca799abd-1251-4749-b7c3-412a7154f2e0/output
```

**Response**: `200 OK`

```
Content-Type: text/plain

+-----------------+----------+---------+---------------+------------+-------------+
|   Customer Name |   Orders |   Items |   Gross Total |   Discount |   Net Total |
+=================+==========+=========+===============+============+=============+
|      John Smith |        3 |       4 |     $2,529.97 |    $200.00 |   $2,329.97 |
+-----------------+----------+---------+---------------+------------+-------------+
|   Sarah Johnson |        3 |       6 |       $236.47 |      $0.00 |     $236.47 |
+-----------------+----------+---------+---------------+------------+-------------+
|     GRAND TOTAL |          |         |     $7,881.37 |    $589.89 |   $7,291.48 |
+-----------------+----------+---------+---------------+------------+-------------+
```

**Error Responses**:

- `404 Not Found`: File ID doesn't exist

---

### 4. Get Error Log

Retrieve validation errors for a specific file.

**Endpoint**: `GET /api/file/{file_id}/error`

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_id | string (UUID) | Yes | Unique identifier for the file |

**Request Example**:

```bash
curl http://localhost:8000/api/file/ca799abd-1251-4749-b7c3-412a7154f2e0/error
```

**Response**: `200 OK`

```
Content-Type: text/plain

Invalid quantity: -1. Must be non-negative. Line: ORD017|Test Customer|Invalid Quantity|-1|50.00|2024-03-23
Invalid format: Expected 6 fields, got 5. Line: ORD018|Test Customer|Missing Field|3|75.00
Invalid date format: 23-03-2024. Expected YYYY-MM-DD. Line: ORD021|Test Customer|Invalid Date|1|40.00|23-03-2024
```

**Error Responses**:

- `404 Not Found`: File ID doesn't exist

**Notes**:
- Empty file if no errors occurred during processing
- Each error includes the problematic line for easy debugging

---

### 5. Delete Submission

Remove a submission and all associated files.

**Endpoint**: `DELETE /api/history/{submission_id}`

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| submission_id | string (UUID) | Yes | Unique identifier for the submission |

**Request Example**:

```bash
curl -X DELETE http://localhost:8000/api/history/a93f9cda-6f67-40d9-888c-881599b1b52a
```

**Response**: `200 OK`

```json
{
  "message": "Submission deleted successfully"
}
```

**Error Responses**:

- `404 Not Found`: Submission ID doesn't exist

**Side Effects**:
- Deletes uploaded file from `uploads/` directory
- Deletes output report from `outputs/` directory
- Deletes error log from `errors/` directory
- Removes submission record from `history.json`

---

### 6. Download File

Download a specific output or error file.

**Endpoint**: `GET /api/download/{file_id}/{type}`

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_id | string (UUID) | Yes | Unique identifier for the file |
| type | string | Yes | Either "output" or "error" |

**Request Example**:

```bash
curl -O http://localhost:8000/api/download/ca799abd-1251-4749-b7c3-412a7154f2e0/output
```

**Response**: `200 OK`

```
Content-Type: text/plain
Content-Disposition: attachment; filename="ca799abd-1251-4749-b7c3-412a7154f2e0_output.txt"

[File contents]
```

**Error Responses**:

- `400 Bad Request`: Invalid file type (not "output" or "error")
- `404 Not Found`: File ID doesn't exist

---

### 7. Health Check

Check if the API is running.

**Endpoint**: `GET /`

**Request Example**:

```bash
curl http://localhost:8000/
```

**Response**: `200 OK`

```json
{
  "message": "Order Processing API is running"
}
```

---

## Data Models

### Submission Record

```typescript
interface Submission {
  id: string;              // UUID v4
  timestamp: string;       // ISO 8601 format
  files: FileRecord[];     // Array of processed files
}
```

### File Record

```typescript
interface FileRecord {
  id: string;              // UUID v4
  filename: string;        // Original filename
  output_file: string;     // Generated output filename
  error_file: string;      // Generated error filename
}
```

### Order (Internal)

```python
class Order(BaseModel):
    order_id: str
    customer_name: str
    product_name: str
    quantity: int
    unit_price: float
    order_date: date
```

### Customer Summary (Internal)

```python
class CustomerSummary(BaseModel):
    customer_name: str
    order_count: int
    total_items: int
    gross_total: float
    total_discount: float
    net_total: float
```

## Error Handling

### Standard Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Description | Common Causes |
|------|-------------|---------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation failure |
| 500 | Internal Server Error | Server-side error |

### Validation Errors

File processing errors are not HTTP errors. They're captured in the error log:

- Invalid line format (wrong number of fields)
- Negative quantities or prices
- Invalid date formats
- Missing required fields

These don't cause the API to return an error status; instead, they're logged in the error file.

## Rate Limiting

**Current Implementation**: None

**Recommended for Production**:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1679068800
```

Consider implementing:
- 100 requests per minute per IP
- 1000 requests per hour per API key

## Examples

### Complete Workflow Example

```bash
# 1. Upload files
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "files=@orders.txt")

# 2. Extract submission ID
SUBMISSION_ID=$(echo $RESPONSE | jq -r '.id')
FILE_ID=$(echo $RESPONSE | jq -r '.files[0].id')

# 3. Get output report
curl http://localhost:8000/api/file/$FILE_ID/output

# 4. Get error log
curl http://localhost:8000/api/file/$FILE_ID/error

# 5. Download output file
curl -O http://localhost:8000/api/download/$FILE_ID/output

# 6. List all history
curl http://localhost:8000/api/history

# 7. Delete submission
curl -X DELETE http://localhost:8000/api/history/$SUBMISSION_ID
```

### Python Client Example

```python
import requests

API_URL = "http://localhost:8000/api"

# Upload files
with open("orders.txt", "rb") as f:
    files = {"files": ("orders.txt", f, "text/plain")}
    response = requests.post(f"{API_URL}/upload", files=files)
    submission = response.json()

# Get output
file_id = submission["files"][0]["id"]
output = requests.get(f"{API_URL}/file/{file_id}/output")
print(output.text)

# Get errors
errors = requests.get(f"{API_URL}/file/{file_id}/error")
print(errors.text)

# List history
history = requests.get(f"{API_URL}/history")
print(history.json())

# Delete submission
delete_response = requests.delete(
    f"{API_URL}/history/{submission['id']}"
)
print(delete_response.json())
```

### JavaScript/Node.js Client Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const API_URL = 'http://localhost:8000/api';

async function uploadFile() {
  const form = new FormData();
  form.append('files', fs.createReadStream('orders.txt'));
  
  const response = await axios.post(`${API_URL}/upload`, form, {
    headers: form.getHeaders()
  });
  
  return response.data;
}

async function getOutput(fileId) {
  const response = await axios.get(`${API_URL}/file/${fileId}/output`);
  return response.data;
}

// Usage
(async () => {
  const submission = await uploadFile();
  const fileId = submission.files[0].id;
  const output = await getOutput(fileId);
  console.log(output);
})();
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

**Swagger UI**: http://localhost:8000/docs
- Test endpoints directly in the browser
- View request/response schemas
- See example values

**ReDoc**: http://localhost:8000/redoc
- Alternative documentation interface
- Better for reading and reference

## CORS Configuration

**Current Settings** (Development):
```python
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

**Production Settings** (Recommended):
```python
allow_origins=["https://yourdomain.com"]
allow_methods=["GET", "POST", "DELETE"]
allow_headers=["Content-Type", "Authorization"]
allow_credentials=True
```

## Versioning

**Current Version**: v1 (implicit)

**Future Versioning Strategy**:
```
/api/v1/upload
/api/v2/upload
```

## Support

For API-related questions:
- Check interactive docs at `/docs`
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for implementation details
- Open an issue on GitHub

---

**Last Updated**: February 2024
