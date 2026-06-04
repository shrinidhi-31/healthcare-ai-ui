# MedVerify API Contracts

## Base URL

```
https://api.medverify.io/v1
```

---

## Authentication

All endpoints (except `/health`) require an `X-API-Key` header.

```
X-API-Key: <your_api_key>
```

---

## Endpoints

---

### 1. Health Check

**`GET /health`**

Returns service status. No authentication required.

**Response `200 OK`**

```json
{
  "status": "ok",
  "version": "1.0.0",
  "redis": "connected"
}
```

---

### 2. WhatsApp Webhook

---

#### 2.1 Verify Webhook

**`GET /webhook/whatsapp`**

Used by WhatsApp to verify the webhook endpoint during setup.

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hub.mode` | string | Yes | Always `subscribe` |
| `hub.verify_token` | string | Yes | Your configured verify token |
| `hub.challenge` | string | Yes | Challenge string to echo back |

**Response `200 OK`**

Returns the `hub.challenge` value as plain text.

---

#### 2.2 Receive Message

**`POST /webhook/whatsapp`**

Receives incoming messages from WhatsApp Cloud API.

**Request Body**

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "919876543210",
              "phone_number_id": "PHONE_ID"
            },
            "messages": [
              {
                "from": "919876543210",
                "id": "wamid.xxx",
                "timestamp": "1700000000",
                "type": "text",
                "text": {
                  "body": "1"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

**Response `200 OK`**

```json
{
  "status": "processed",
  "message_id": "wamid.xxx",
  "reply": "Welcome to MedVerify! Please choose an option:\n1. Symptom Assessment\n2. Upload Report\n3. Find Doctor"
}
```

**Response `422 Unprocessable Entity`**

```json
{
  "detail": [
    {
      "loc": ["body", "entry"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 3. Alerts

---

#### 3.1 List Alerts

**`GET /alerts`**

Returns all active emergency alerts for the admin dashboard.

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | `open` | Filter by status: `open`, `acknowledged`, `resolved` |
| `severity` | string | No | — | Filter by severity: `HIGH`, `MEDIUM`, `LOW` |
| `limit` | integer | No | `50` | Max results to return (1–200) |
| `offset` | integer | No | `0` | Pagination offset |

**Response `200 OK`**

```json
{
  "total": 2,
  "alerts": [
    {
      "alert_id": "alert_01HXK2J4",
      "user_id": "919876543210",
      "severity": "HIGH",
      "reason": "Chest pain detected",
      "status": "open",
      "created_at": "2024-11-15T10:30:00Z",
      "updated_at": "2024-11-15T10:30:00Z"
    },
    {
      "alert_id": "alert_01HXK3M5",
      "user_id": "919812345678",
      "severity": "HIGH",
      "reason": "Breathing difficulty reported",
      "status": "acknowledged",
      "created_at": "2024-11-15T09:15:00Z",
      "updated_at": "2024-11-15T09:45:00Z"
    }
  ]
}
```

---

#### 3.2 Get Alert

**`GET /alerts/{alert_id}`**

Returns a single alert by ID.

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `alert_id` | string | Yes | Alert identifier |

**Response `200 OK`**

```json
{
  "alert_id": "alert_01HXK2J4",
  "user_id": "919876543210",
  "severity": "HIGH",
  "reason": "Chest pain detected",
  "status": "open",
  "symptoms": ["chest pain", "shortness of breath"],
  "session_snapshot": {
    "flow": "emergency",
    "step": 1,
    "language": "en"
  },
  "created_at": "2024-11-15T10:30:00Z",
  "updated_at": "2024-11-15T10:30:00Z"
}
```

**Response `404 Not Found`**

```json
{
  "detail": "Alert not found"
}
```

---

#### 3.3 Update Alert Status

**`PATCH /alerts/{alert_id}`**

Update the status of an alert (e.g. acknowledge or resolve).

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `alert_id` | string | Yes | Alert identifier |

**Request Body**

```json
{
  "status": "acknowledged"
}
```

| Field | Type | Required | Allowed Values |
|-------|------|----------|----------------|
| `status` | string | Yes | `open`, `acknowledged`, `resolved` |

**Response `200 OK`**

```json
{
  "alert_id": "alert_01HXK2J4",
  "status": "acknowledged",
  "updated_at": "2024-11-15T11:00:00Z"
}
```

---

#### 3.4 Create Alert (Internal)

**`POST /alerts`**

Internal endpoint called by the Emergency Flow to create new alerts. Should not be exposed publicly.

**Request Body**

```json
{
  "user_id": "919876543210",
  "severity": "HIGH",
  "reason": "Chest pain detected",
  "symptoms": ["chest pain", "shortness of breath"],
  "session_snapshot": {
    "flow": "emergency",
    "step": 1,
    "language": "en"
  }
}
```

**Response `201 Created`**

```json
{
  "alert_id": "alert_01HXK2J4",
  "user_id": "919876543210",
  "severity": "HIGH",
  "reason": "Chest pain detected",
  "status": "open",
  "created_at": "2024-11-15T10:30:00Z"
}
```

---

### 4. Sessions (Debug / Admin)

---

#### 4.1 Get Session

**`GET /sessions/{user_id}`**

Retrieve the current session state for a user.

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User phone number (e.g. `919876543210`) |

**Response `200 OK`**

```json
{
  "user_id": "919876543210",
  "flow": "symptoms",
  "step": 2,
  "language": "en",
  "intent": null,
  "data": {
    "main_symptom": "headache",
    "duration": "2 days"
  },
  "ttl_seconds": 3542
}
```

**Response `404 Not Found`**

```json
{
  "detail": "Session not found"
}
```

---

#### 4.2 Delete Session

**`DELETE /sessions/{user_id}`**

Clear a user's session (resets conversation to start).

**Response `204 No Content`**

No body returned.

---

## Error Responses

All error responses follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

| Status Code | Meaning |
|-------------|---------|
| `400` | Bad Request — invalid input |
| `401` | Unauthorized — missing or invalid API key |
| `404` | Not Found — resource does not exist |
| `422` | Unprocessable Entity — validation error |
| `500` | Internal Server Error |

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `POST /webhook/whatsapp` | 1000 req/min |
| `GET /alerts` | 100 req/min |
| All others | 60 req/min |

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1700000060
```
