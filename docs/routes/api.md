# Routes API

## Get Available Routes

**Base URL**

```
api/routes/
```

---

## Get Routes

Returns a list of all active routes ordered by creation date.

### Endpoint

```
GET /api/routes/
```
### Authentication

None

### Permission

AllowAny

### Success Response (200 OK)

```json
[
  {
    "id": "93303d1b-f7c3-4db6-95a0-bb5368c21ea8",
    "route_code": "R001",
    "route_name": "Chennai → Bengaluru",
    "source_city": "d89362eb-612d-48a0-9c52-97d7506cbd37",
    "is_active": true,
    "created_at": "2026-07-05T20:53:37.227250+05:30",
    "updated_at": "2026-07-05T20:53:37.227287+05:30"
  }
]
```

---

## Get Route Details

Returns details of a single active route.

### Endpoint

```
GET /api/routes/{route_id}/
```

### Authentication

None

### Permission

AllowAny

### Success Response (200 OK)

```json
{
  "id": "93303d1b-f7c3-4db6-95a0-bb5368c21ea8",
  "route_code": "R001",
  "route_name": "Chennai → Bengaluru",
  "source_city": "d89362eb-612d-48a0-9c52-97d7506cbd37",
  "is_active": true,
  "created_at": "2026-07-05T20:53:37.227250+05:30",
  "updated_at": "2026-07-05T20:53:37.227287+05:30"
}
```

### Error Response (404 Not Found)

```json
{
  "detail": "Route not found."
}
```

---

## Get Route Stops

**Endpoint**

```http
GET /api/routes/<route_id>/stops/
```

**Description**

Returns all stops for the specified active route in stop order.

**Authentication**

- No authentication required

**Permission**

- AllowAny

**Request Body**

None.

**Success Response (200 OK)**

```json
[
  {
    "id": "bfc9e508-8dea-4a89-a8c0-3fb424c50b99",
    "city_id": "d89362eb-612d-48a0-9c52-97d7506cbd37",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "stop_order": 1
  },
  {
    "id": "ad314a8f-db22-4e51-9651-278091a92de7",
    "city_id": "efd69b35-170e-4df4-aed3-a3033637111b",
    "city": "Vellore",
    "state": "Tamil Nadu",
    "stop_order": 2
  },
  {
    "id": "c3656f5e-ca43-4363-b01c-b39d36e5fbc8",
    "city_id": "094e9092-3e01-40b6-b971-d9abfa1ed443",
    "city": "Krishnagiri",
    "state": "Tamil Nadu",
    "stop_order": 3
  },
  {
    "id": "107d7d62-8798-4fee-afda-4155d46db538",
    "city_id": "db16dace-e0c6-4e24-9ce5-7a4780b9de4d",
    "city": "Hosur",
    "state": "Tamil Nadu",
    "stop_order": 4
  }
]
```

**Success Response (No Stops)**

**Status Code:** `200 OK`

```json
[]
```

**Error Response**

**Status Code:** `404 Not Found`

```json
{
  "detail": "Route not found."
}
```



