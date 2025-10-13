# Help2Study - System Architecture

This document explains how Help2Study works under the hood, with diagrams showing how data flows through the system.

> **📊 Note on Diagrams:** The diagrams in this document use Mermaid syntax, which **automatically renders as visual diagrams on GitHub**. No extension needed! If you're viewing locally in a text editor, you'll see the code - view this file on GitHub to see the rendered diagrams.

---

## System Overview

```mermaid
graph TB
    subgraph "Client Side - Browser"
        A[User Interface<br/>React Components]
        B[HTTP Client<br/>Axios]
    end

    subgraph "Server Side - Django"
        C[URL Router<br/>urls.py]
        D[API Views<br/>views.py]
        E[Serializers<br/>Data Conversion]
        F[Models<br/>ORM]
    end

    subgraph "Data Layer"
        G[(Database<br/>SQLite)]
        H[External API<br/>Gemini AI]
    end

    A -->|User clicks| B
    B -->|HTTP Request| C
    C -->|Routes to| D
    D -->|Validates data| E
    E -->|Query/Save| F
    F -->|SQL| G
    D -->|Process file| H
    H -->|AI response| D
    D -->|JSON| B
    B -->|Updates| A
```

---

## The Complete Request Journey

Let's trace what happens when a user uploads a document to create flashcards.

### Step 1: User Action (Frontend)

**File:** `frontend/src/components/FileUploadForm.jsx`

```mermaid
sequenceDiagram
    participant User
    participant React
    participant EventHandler

    User->>React: Clicks "Create Flashcards"
    React->>EventHandler: Triggers handleSubmit()
    EventHandler->>EventHandler: Collect form data
    Note over EventHandler: File + Topic name
```

**What happens:**
- User fills form and clicks submit
- React event handler captures the click
- Form data (file + topic name) is collected
- Ready to send to backend

**Key concepts:** Event Handling, Form Data, User Interface

---

### Step 2: The API Request

**File:** `frontend/src/api.js`

```mermaid
sequenceDiagram
    participant Frontend
    participant Axios
    participant Network

    Frontend->>Axios: api.post('/api/flashcards/', data)
    Axios->>Axios: Add JWT token to headers
    Axios->>Network: HTTP POST request
    Note over Network: Traveling to backend...
```

**What happens:**
- Axios prepares an HTTP POST request
- JWT token added to Authorization header
- Request body contains file and topic name
- Sent to `http://localhost:8000/api/flashcards/`

**Key concepts:** HTTP Request, HTTP Method (POST), Authentication (JWT), Endpoint

---

### Step 3: Backend Routing

**Files:** `backend/backend/urls.py` → `backend/api/urls.py`

```mermaid
graph LR
    A[Request arrives<br/>:8000/api/flashcards/] --> B[Main urls.py]
    B --> C[API urls.py]
    C --> D[TopicListCreate View]

    style D fill:#90EE90
```

**What happens:**
- Django receives request on port 8000
- Main `urls.py` routes `/api/` to the api app
- API `urls.py` matches `/flashcards/` pattern
- Request directed to `TopicListCreate` view

**Key concepts:** Routing, URL Patterns, Server

---

### Step 4: View Processing

**File:** `backend/api/views.py:20-36`

```mermaid
sequenceDiagram
    participant View
    participant Serializer
    participant Model
    participant AI

    View->>View: Check authentication
    View->>Serializer: Validate data
    Serializer->>Model: Create Topic object
    Model->>Model: Save to database
    View->>AI: Process file with Gemini
    AI-->>View: Return flashcard data
    View->>Model: Create Flashcard objects
    Model->>Model: Save flashcards
```

**What happens:**
1. View checks if user is authenticated (JWT token)
2. Serializer validates the incoming data
3. Topic model instance created and saved
4. File extracted and sent to Gemini AI
5. AI returns flashcard questions/answers
6. Multiple Flashcard objects created and saved
7. Response prepared

**Key concepts:** View, Permissions, Validation, ORM, CRUD Operations

---

### Step 5: Database Operations

**File:** `backend/api/models.py`

```mermaid
erDiagram
    User ||--o{ Topic : creates
    User ||--o{ Flashcard : owns
    Topic ||--o{ Flashcard : contains

    User {
        int id
        string username
        string email
    }

    Topic {
        int id
        string name
        datetime created_at
        int user_id
    }

    Flashcard {
        int id
        text question
        text answer
        datetime created_at
        int topic_id
        int user_id
    }
```

**What happens:**
- Django ORM translates Python to SQL
- `Topic.objects.create()` → `INSERT INTO topics...`
- `Flashcard.objects.filter()` → `SELECT * FROM flashcards WHERE...`
- No raw SQL needed

**Key concepts:** Models, ORM, Foreign Keys, Database Relationships

---

### Step 6: Response Returned

**File:** `backend/api/serializers.py`

```mermaid
sequenceDiagram
    participant Django
    participant Serializer
    participant Network
    participant Frontend

    Django->>Serializer: Convert Topic object
    Serializer->>Serializer: Python → JSON
    Serializer->>Network: HTTP 201 Created
    Note over Network: Response travels back
    Network->>Frontend: JSON data received
```

**What happens:**
- Serializer converts Python objects to JSON
- HTTP response created with status code 201 (Created)
- Response includes the new topic data
- Sent back through the network

**Key concepts:** Serialization, HTTP Response, Status Codes, JSON

---

### Step 7: UI Update

**File:** `frontend/src/components/FileUploadForm.jsx`

```mermaid
sequenceDiagram
    participant Axios
    participant React
    participant DOM
    participant User

    Axios->>React: Response received
    React->>React: Update state
    React->>DOM: Re-render component
    DOM->>User: Show success message
```

**What happens:**
- Axios receives the response
- React component state updated
- Component re-renders automatically
- User sees confirmation message
- New flashcards appear in the UI

**Key concepts:** Asynchronous JavaScript, State Management, Component Re-rendering

---

## Request/Response Summary

```mermaid
graph LR
    A[User Clicks] -->|1. Event| B[React]
    B -->|2. HTTP POST| C[Django]
    C -->|3. Route| D[View]
    D -->|4. Save| E[Database]
    D -->|5. Process| F[AI]
    F -->|6. Data| D
    D -->|7. JSON| B
    B -->|8. Update| A

    style A fill:#87CEEB
    style B fill:#90EE90
    style C fill:#FFD700
    style E fill:#DDA0DD
```

**The full cycle:**
1. User action triggers event
2. HTTP request sent
3. Backend routes to handler
4. Data saved to database
5. External API called (optional)
6. Response prepared
7. JSON sent back
8. UI updates

---

## Technology Layers

### Frontend Stack
```
User Interface
      ↓
React Components (JSX)
      ↓
React Router (Navigation)
      ↓
Axios (HTTP Client)
      ↓
HTTP Request → Backend
```

### Backend Stack
```
HTTP Request arrives
      ↓
Django URL Router
      ↓
View (Request Handler)
      ↓
Serializer (Validation)
      ↓
Model (ORM)
      ↓
Database (SQL)
```

---

## Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant DB

    Note over User,DB: Registration
    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /api/user/register/
    Backend->>DB: Create user
    Backend-->>Frontend: Success

    Note over User,DB: Login
    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /api/token/
    Backend->>DB: Verify credentials
    Backend-->>Frontend: Access + Refresh tokens
    Frontend->>Frontend: Store tokens

    Note over User,DB: Authenticated Request
    Frontend->>Backend: Request + JWT token
    Backend->>Backend: Validate token
    Backend-->>Frontend: Protected data
```

**How JWT works:**
1. User logs in with username/password
2. Backend validates and returns JWT tokens
3. Frontend stores tokens (localStorage)
4. Every request includes token in Authorization header
5. Backend validates token before processing

---

## File References

Here's where to find each piece in the codebase:

**Frontend:**
- Entry point: `frontend/src/main.jsx`
- Routing: `frontend/src/App.jsx`
- File upload: `frontend/src/components/FileUploadForm.jsx`
- API client: `frontend/src/api.js`

**Backend:**
- Main settings: `backend/backend/settings.py`
- URL routing: `backend/backend/urls.py` → `backend/api/urls.py`
- Request handlers: `backend/api/views.py`
- Database models: `backend/api/models.py`
- Data serialization: `backend/api/serializers.py`
- AI integration: `backend/api/geminiapi.py`

---

## Key Takeaways

✅ **Separation of concerns:** Frontend, backend, and database each have clear responsibilities

✅ **Request/response cycle:** All web interactions follow this pattern

✅ **RESTful design:** Endpoints use standard HTTP methods (GET, POST, DELETE)

✅ **Authentication:** JWT tokens secure API endpoints

✅ **ORM abstraction:** Django handles database operations without SQL

✅ **State management:** React automatically updates UI when data changes

---

## Next Steps

**To understand the code:**
1. Read through `views.py` to see request handlers
2. Check `models.py` to see database structure
3. Look at `FileUploadForm.jsx` to see how requests start
4. Trace a request through the system using browser DevTools

**To modify the system:**
1. Add new model → Run migrations
2. Create new view → Add URL route
3. Build frontend component → Connect to API
4. Test with browser Network tab

**See [CONCEPTS_GUIDE.md](CONCEPTS_GUIDE.md) for term definitions and learning resources**
