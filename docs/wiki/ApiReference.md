# API Reference

Base URL: `http://127.0.0.1:8000`

## `GET /`
Returns:
```json
{"message":"Hello, World!"}
```

## `GET /health`
Returns:
```json
{"status":"ok"}
```

## `GET /greet`
Query params:
- Required: `name`, `surname`
- Optional: `phone`, `city`

### Example: required params only
Request:
```bash
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi"
```
Response:
```json
{"message":"Hello, Arash Karimi!"}
```

### Example: with phone
Request:
```bash
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi&phone=555-0101"
```
Response:
```json
{"message":"Hello, Arash Karimi!","phone":"555-0101"}
```

### Example: with city and successful weather lookup
Request:
```bash
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi&city=Tehran"
```
Response shape:
```json
{"message":"Hello, Arash Karimi!","city":"Tehran","weather":{"description":"...","temperature_c":...}}
```

### Example: with city and weather lookup failure
Response shape:
```json
{"message":"Hello, Arash Karimi!","city":"Tehran","weather_error":"..."}
```

### Validation behavior
Missing required params return HTTP `422`.
