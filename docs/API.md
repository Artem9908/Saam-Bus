# API Documentation

## Base URL
`http://localhost:8000`

## Authentication
No authentication required for development. Production endpoints should be secured.

## Endpoints

### Documents

#### Generate Document

```bash
POST /generate-document
```


Request body:

```json
{
  "name": "string",
  "date": "yyyy-mm-dd",
  "amount": "number",
"template_type": "receipt|invoice|contract"
}
```

Response:

```json
{
    "status": "success",
    "data": {
    "id": "number",
    "name": "string",
    "date": "YYYY-MM-DD",
    "amount": "number",
    "content": "string",
    "doc_url": "string",
    "doc_id": "string",
    "google_doc_id": "string",
    "created_at": "string"
    },
    "message": "Document generated successfully"
}
```

#### List Documents

```bash
GET /documents
```


Query parameters:
- `name` (optional): Filter by document name
- `date` (optional): Filter by date (YYYY-MM-DD)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `sortBy` (optional): Sort field (name|date)
- `sortOrder` (optional): Sort direction (asc|desc)

#### Get Document

```bash
GET /documents/{document_id}
```
Response:

```json
{
    "status": "success",
    "data": Document
}
```

## Error Responses
All endpoints return error responses in the following format:

```json
{
  "error": "string",
  "message": "Error description",
  "type": "ValidationError|DatabaseError|GoogleAPIError"
}
```
```


## Validation Rules
- Name: Minimum 2 characters
- Date: Must not be in the future
- Amount: Between 0 and 1,000,000
- Template Type: Must be one of: receipt, invoice, contract