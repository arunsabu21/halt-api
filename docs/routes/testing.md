# Routes API Testing

## Get Available Routes

### Test Case 1 - Get all active routes

**Method**

```
http GET
```

**Endpoint**

```text
/api/routes/
```

**Headers**

None.

**Expected Status**

```text
200 OK
```

**Expected Result**

- Returns a list of active routes.
- Routes are ordered by creation date.
- Each route contains:
  - id
  - route_code
  - route_name
  - source_city
  - is_active
  - created_at
  - updated_at

---

### Test Case 2 - No active routes

**Expected Status**

```text
404 Not Found
```

**Expected Result**

```json
{
    "detail": "No routes found."
}
```

---

## Get Route Details

### Test Case 1 - Get route details by valid ID

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/<route_id>/
```

**Headers**

None.

**Expected Status**

```text
200 OK
```

**Excepted Result**

- Returns the requested active route.
- Response Contains:
  - id
  - route_code
  - route_name
  - source_city
  - is_active
  - created_at
  - updated_at

---

### Test Case 2 - Route does not exist

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/<non_existing_route_by_id>/
```

**Headers**

None.

**Expected Status**

```text
404 Not Found
```

**Expected Result**

```json
{
  "detail": "Route not found."
}
```

---

### Test Case 3 - Invalid Route ID

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/invalid-uuid/
```

**Headers**

None.

**Expected Status**

```text
404 Not Found
```

**Expected Result**

- Request is rejected because the route ID is not a valid UUID.
- The request does not reach the view.

## Get Route Stops

### Test Case 1 - Route has stops

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/<route_id>/stops/
```

**Headers**

None.

**Expected Status**

```text
200 OK
```

**Expected Result**

- Returns all stops for the requested route.
- Stops are ordered by `stop_order`.
- Each stop contains:
  - id
  - city_id
  - city
  - state
  - stop_order

---

### Test Case 2 - Route has no stops

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/<route_id>/stops/
```

**Headers**

None.

**Expected Status**

```text
200 OK
```

**Expected Result**

```json
[]
```

---

### Test Case 3 - Route does not exist

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/<non_existing_route_id>/stops/
```

**Headers**

None.

**Expected Status**

```text
404 Not Found
```

**Expected Result**

```json
{
  "detail": "Route not found."
}
```

---

### Test Case 4 - Invalid Route UUID

**Method**

```http
GET
```

**Endpoint**

```text
/api/routes/invalid-uuid/stops/
```

**Headers**

None.

**Expected Status**

```text
404 Not Found
```

**Expected Result**

- The request is rejected because the route ID is not a valid UUId.
- The request does not reach the view.