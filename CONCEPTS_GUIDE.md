# Help2Study - Technical Concepts Guide

A glossary of all technical terms used in this project, organized by topic.

---

## Frontend Concepts

### UI (User Interface)
**Definition:** The visual layout of an application that a user interacts with, composed of elements like buttons, forms, and text.

**In Help2Study:** React components in `frontend/src/components/` and `frontend/src/pages/`

**Learn more:** [MDN - User Interface](https://developer.mozilla.org/en-US/docs/Glossary/UI)

---

### DOM (Document Object Model)
**Definition:** A tree-like representation of the HTML document created by the browser. JavaScript can interact with the DOM to change the page's structure, style, and content dynamically.

**In Help2Study:** React manages DOM updates automatically when state changes

**Learn more:** [MDN - DOM Introduction](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)

---

### Event Handling
**Definition:** The process of listening for and reacting to user actions (events) like clicks, key presses, or mouse movements. In React, this is often done with attributes like `onClick`.

**In Help2Study:** See `onClick` handlers in components like `FileUploadForm.jsx`

**Learn more:** [React - Responding to Events](https://react.dev/learn/responding-to-events)

---

### State Management
**Definition:** The practice of managing the data that an application's UI depends on. In React, when a component's state changes, React automatically re-renders the component to reflect the new data.

**In Help2Study:** `useState` hooks throughout React components

**Learn more:** [React - State: A Component's Memory](https://react.dev/learn/state-a-components-memory)

---

### Asynchronous JavaScript
**Definition:** Code that allows the browser to perform long-running tasks (like waiting for an API response) in the background without freezing the user interface. This is managed using `async/await` or `.then()`.

**In Help2Study:** All API calls use `async/await` pattern

**Learn more:** [MDN - Async JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous)

---

## API & Network Concepts

### API (Application Programming Interface)
**Definition:** A set of rules and definitions that allows two separate software systems (like a React frontend and a Django backend) to communicate with each other. It's the "menu" the frontend orders from.

**In Help2Study:** REST API endpoints in `backend/api/urls.py`

**Learn more:** [MDN - Web APIs](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction)

---

### HTTP Request
**Definition:** A formal message sent from the client to the server to request an action or resource.

**In Help2Study:** Axios sends requests from `frontend/src/api.js`

**Learn more:** [MDN - HTTP Messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)

---

### Endpoint (URL)
**Definition:** The specific address on the server where the request is sent (e.g., `/api/tasks`). It identifies the resource you want to interact with.

**In Help2Study:** Defined in `backend/api/urls.py` (e.g., `/api/flashcards/`)

**Learn more:** [REST API - Endpoints](https://restfulapi.net/resource-naming/)

---

### HTTP Method
**Definition:** A verb that specifies the intended action of the request. The most common are:
- **GET** - Read data
- **POST** - Create data
- **PUT/PATCH** - Update data
- **DELETE** - Remove data

**In Help2Study:** Views in `views.py` handle different HTTP methods

**Learn more:** [MDN - HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

---

### Payload (Request Body)
**Definition:** The data sent to the server with the request, typically used with POST or PUT methods.

**In Help2Study:** File and topic data sent in POST requests

**Learn more:** [MDN - HTTP Request Body](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages#body)

---

### JSON (JavaScript Object Notation)
**Definition:** A lightweight, text-based format for structuring and transmitting data. It's the standard language for APIs on the web.

**In Help2Study:** All API responses are in JSON format

**Learn more:** [MDN - Working with JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON)

---

## Backend Concepts

### Server
**Definition:** A program that runs on a computer, continuously listening for incoming network requests on a specific port.

**In Help2Study:** Django server runs on port 8000

**Learn more:** [MDN - What is a Web Server?](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_web_server)

---

### Routing
**Definition:** The mechanism that directs an incoming request to the correct piece of code that should handle it, based on the request's URL and HTTP method. In Django, this is managed in `urls.py`.

**In Help2Study:** `backend/backend/urls.py` → `backend/api/urls.py`

**Learn more:** [Django - URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)

---

### View (Django)
**Definition:** A function or class in `views.py` that processes a web request and returns a web response. It contains the core logic for what to do when a specific endpoint is hit.

**In Help2Study:** Class-based views in `backend/api/views.py`

**Learn more:** [Django - Views](https://docs.djangoproject.com/en/stable/topics/http/views/)

---

### HTTP Response
**Definition:** The message a server sends back to the client after receiving and processing its request.

**In Help2Study:** Django views return Response objects

**Learn more:** [MDN - HTTP Responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages#http_responses)

---

### Status Codes
**Definition:** Three-digit codes that indicate the outcome of a request. Key examples:
- **200 OK** - Success
- **201 Created** - Success, new resource made
- **404 Not Found** - Resource doesn't exist
- **500 Internal Server Error** - Server crash

**In Help2Study:** Views return appropriate status codes

**Learn more:** [MDN - HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

### Serializer (Django REST Framework)
**Definition:** A tool that converts complex data types, like Django model instances (QuerySets), into native Python datatypes that can then be easily rendered into JSON for the API response. It also handles data validation.

**In Help2Study:** `backend/api/serializers.py`

**Learn more:** [DRF - Serializers](https://www.django-rest-framework.org/api-guide/serializers/)

---

## Database Concepts

### CRUD (Create, Read, Update, Delete)
**Definition:** The four fundamental operations of persistent storage.

**In Help2Study:**
- Create: `POST /api/flashcards/`
- Read: `GET /api/topics/`
- Update: Not implemented yet
- Delete: `DELETE /api/topics/<id>/`

**Learn more:** [Wikipedia - CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)

---

### Model (Django)
**Definition:** A Python class in `models.py` that defines the structure and behavior of your application's data. Each model maps to a single database table.

**In Help2Study:** `Topic` and `Flashcard` models in `backend/api/models.py`

**Learn more:** [Django - Models](https://docs.djangoproject.com/en/stable/topics/db/models/)

---

### ORM (Object-Relational Mapper)
**Definition:** A programming technique that allows you to interact with your database (like writing queries and creating records) using an object-oriented programming language (like Python) instead of raw SQL. Django's built-in ORM is one of its most powerful features.

**In Help2Study:** `Topic.objects.filter(user=user)` instead of `SELECT * FROM topics WHERE user_id = ?`

**Learn more:** [Django - Making Queries](https://docs.djangoproject.com/en/stable/topics/db/queries/)

---

## Architecture Concepts

### Full-Stack Development
**Definition:** The practice of building and maintaining all three parts of a web application: the frontend (client-side), the backend (server-side), and the database.

**In Help2Study:** React frontend + Django backend + SQLite database

**Learn more:** [freeCodeCamp - What is Full Stack?](https://www.freecodecamp.org/news/what-is-a-full-stack-developer-full-stack-engineer-guide/)

---

### Client-Server Model
**Definition:** The fundamental architecture of the web where a Client (like your browser) requests information from a central Server, which processes the request and returns a response.

**In Help2Study:** React app (client) requests data from Django API (server)

**Learn more:** [MDN - Client-Server Overview](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview)

---

### Request/Response Cycle
**Definition:** The complete, two-way communication process where a client sends a Request for data, and the server sends back a Response. This cycle is the foundation of all web interactions.

**In Help2Study:** See detailed breakdown in [ARCHITECTURE.md](ARCHITECTURE.md)

**Learn more:** [MDN - HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

---

## Development Tools

### Version Control (Git)
**Definition:** A system that tracks changes to files over time, allowing you to recall specific versions later. It's essential for collaboration and managing code history. `clone` copies a repository locally, while `fork` creates a personal copy on your GitHub account.

**In Help2Study:** Project uses Git for version control

**Learn more:** [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

### Package Management
**Definition:** Tools that automate the process of installing, updating, and managing the external libraries (dependencies) a project uses. `npm` is used for the React frontend, and `pip` is used for the Django backend.

**In Help2Study:**
- Frontend: `npm install` reads `package.json`
- Backend: `pip install -r requirements.txt`

**Learn more:**
- [npm Docs](https://docs.npmjs.com/)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)

---

### Environment Variables (.env)
**Definition:** A system for storing configuration values and secrets (like API keys or database passwords) outside of your source code for better security and portability.

**In Help2Study:** `.env` file stores `API_KEY` and `VITE_API_URL`

**Learn more:** [The Twelve-Factor App - Config](https://12factor.net/config)

---

## Additional Resources

### Official Documentation
- [React Documentation](https://react.dev) - Complete React guide
- [Django Documentation](https://docs.djangoproject.com/) - Django framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API building
- [Vite Documentation](https://vitejs.dev/) - Build tool
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Axios Documentation](https://axios-http.com/) - HTTP client

### Learning Platforms
- [MDN Web Docs](https://developer.mozilla.org/) - Web technologies reference
- [freeCodeCamp](https://www.freecodecamp.org/) - Free coding courses
- [Real Python](https://realpython.com/) - Python tutorials
- [JavaScript.info](https://javascript.info/) - Modern JavaScript tutorial

### Specific Topics
- [REST API Tutorial](https://restfulapi.net/) - RESTful design principles
- [JWT.io](https://jwt.io/introduction) - JSON Web Token guide
- [SQL vs ORM](https://www.djangoproject.com/start/overview/#write-your-api) - Why use an ORM

---

## Quick Reference

| Concept | What It Does | Where to Find It |
|---------|-------------|------------------|
| **React Component** | Reusable UI piece | `frontend/src/components/` |
| **API Endpoint** | URL that handles requests | `backend/api/urls.py` |
| **View** | Request handler | `backend/api/views.py` |
| **Model** | Database table | `backend/api/models.py` |
| **Serializer** | Data converter | `backend/api/serializers.py` |
| **State** | Component data | `useState` in components |
| **HTTP Request** | Client → Server | Axios in `api.js` |
| **HTTP Response** | Server → Client | Django Response object |
| **JWT Token** | Authentication | localStorage + headers |
| **ORM Query** | Database operation | `.objects.filter()` etc. |

---

**For system architecture and request flow diagrams, see [ARCHITECTURE.md](ARCHITECTURE.md)**

**For setup instructions, see [README.md](README.md)**
