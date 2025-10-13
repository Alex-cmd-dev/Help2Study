# Help2Study - AI Flashcard Generator

A full-stack application that uses AI to automatically generate flashcards from your documents. Upload a PDF, DOCX, or TXT file and let Google Gemini create study materials for you.

Built with React, Django, and modern web technologies to demonstrate real-world full-stack development.

## Features

- Upload and process documents (PDF, DOCX, TXT)
- AI-powered flashcard generation
- User authentication
- Organize by topics
- Interactive flashcard viewer

---

## Understanding the Architecture

### The Restaurant Analogy 🍽️

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Dining Area  │  ←────→ │   Kitchen    │  ←────→ │    Pantry    │
│  (Frontend)  │         │  (Backend)   │         │  (Database)  │
│              │         │              │         │              │
│   React      │         │   Django     │         │   SQLite     │
│ What you see │         │ The logic    │         │ Stored data  │
└──────────────┘         └──────────────┘         └──────────────┘
```

**Frontend:** What users see and interact with (the dining area)
**Backend:** Where the logic happens (the kitchen)
**Database:** Where data is stored permanently (the pantry)
**API:** How they talk to each other (the order system)

---

## How a Request Travels Through the System

When you upload a document, here's what happens:

**1. User Action (Frontend)**
```
You click "Create Flashcards" → React captures the event
```
The UI responds to your click using event handling.

**2. The Request (API Call)**
```
Browser sends HTTP POST → Travels to backend
```
An HTTP request with your file is sent to an endpoint like `/api/flashcards/`

**3. Backend Receives (Routing)**
```
Django receives request → Routes to the correct view
```
The server matches the URL and directs it to the right handler.

**4. Processing (Database + AI)**
```
View validates → Saves to database → Processes with AI
```
Django's ORM saves your data, then Gemini AI generates flashcards.

**5. Response Sent Back**
```
Backend sends JSON response → Status code indicates success
```
The server responds with a status code (like 201 Created) and data.

**6. UI Updates**
```
Frontend receives response → Updates the page
```
React's state management triggers a re-render to show your new flashcards.

📚 **See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed diagrams and code references**

---

## Tech Stack

### Frontend (Client-Side)
- React 18 - UI components
- Vite - Fast build tool
- Tailwind CSS - Styling
- Axios - API requests

### Backend (Server-Side)
- Django 5.2.7 - Web framework
- Django REST Framework - API toolkit
- JWT - Authentication
- SQLite - Database
- Google Gemini - AI processing

---

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Setup in 3 Steps

**1. Clone and configure**
```bash
git clone <repository-url>
cd Flashcards
cp .env.example .env
# Edit .env and add your Gemini API key
```

**2. Install dependencies**
```bash
make install
# OR manually: pip install + npm install
```

**3. Run migrations and start**
```bash
make migrate
make dev
```

Visit http://localhost:5173 to use the app!

---

## Project Structure

```
help2study/
├── backend/                    # Django (Server)
│   ├── api/
│   │   ├── models.py          # Database structure
│   │   ├── views.py           # Request handlers
│   │   ├── serializers.py     # Data conversion
│   │   ├── urls.py            # API routing
│   │   └── geminiapi.py       # AI integration
│   └── backend/
│       └── settings.py        # Configuration
│
├── frontend/                   # React (Client)
│   └── src/
│       ├── components/        # UI components
│       ├── pages/             # Page views
│       └── api.js             # HTTP client
│
├── ARCHITECTURE.md            # System design details
├── CONCEPTS_GUIDE.md          # Technical glossary
└── README.md                  # This file
```

---

## API Endpoints

REST API following standard HTTP methods:

**Authentication**
- `POST /api/user/register/` - Create account
- `POST /api/token/` - Login

**Flashcards (CRUD)**
- `GET /api/topics/` - List topics
- `POST /api/topics/` - Create topic + upload file to generate flashcards
- `GET /api/flashcards/<topic_id>/` - Get flashcards for a topic
- `DELETE /api/topic/delete/<id>` - Delete topic

---

## Customizing This Project

Use Help2Study as a starting point for your own ideas:

**Replace the AI logic** → Change `geminiapi.py` to your own processing
**Modify the data model** → Edit `models.py` for different data
**Update the UI** → Customize components with Tailwind
**Add features** → Search, real-time updates, exports, etc.

---

## Make Commands

```bash
make install         # Install all dependencies
make migrate         # Setup database
make dev             # Start both servers
make dev-backend     # Start Django only
make dev-frontend    # Start React only
make lint            # Check code quality
make clean           # Clean temp files
```

---

## Key Concepts

**Full-Stack Development:** Building frontend, backend, and database together
**Client-Server Model:** Browser (client) requests data from server
**Request/Response Cycle:** How clients and servers communicate
**HTTP Methods:** GET (read), POST (create), DELETE (remove)
**ORM:** Work with database using Python objects, not SQL
**State Management:** How React tracks and updates data
**Environment Variables:** Store secrets like API keys safely

📚 **Full glossary with links: [CONCEPTS_GUIDE.md](CONCEPTS_GUIDE.md)**

---

## Learning Resources

**This Project:**
- [ARCHITECTURE.md](ARCHITECTURE.md) - Request flow diagrams
- [CONCEPTS_GUIDE.md](CONCEPTS_GUIDE.md) - Technical terms explained

**Official Docs:**
- [React](https://react.dev) - Frontend
- [Django](https://docs.djangoproject.com/) - Backend
- [Django REST Framework](https://www.django-rest-framework.org/) - API
- [Tailwind CSS](https://tailwindcss.com/) - Styling

**Learning:**
- [MDN Web Docs](https://developer.mozilla.org/) - Web fundamentals
- [freeCodeCamp](https://www.freecodecamp.org/) - Free tutorials

---

## Troubleshooting

**Can't find API_KEY**
→ Create `.env` file with your Gemini API key

**Can't connect to backend**
→ Make sure Django is running: `make dev-backend`

**Database errors**
→ Run migrations: `make migrate`

**Port already in use**
→ Kill process: `lsof -ti:8000 | xargs kill -9`

---

## Development Tips

**Think in systems:** Plan your data model and API endpoints first
**Follow the request:** Use browser DevTools to trace data flow
**Build incrementally:** Start simple, add features one at a time

---

## Security Notes

- Never commit `.env` or API keys
- Change Django `SECRET_KEY` for production
- Set `DEBUG=False` in production
- Use PostgreSQL instead of SQLite in production

---

## Credits

Built with [Django](https://www.djangoproject.com/), [React](https://react.dev/), [Vite](https://vitejs.dev/), [shadcn/ui](https://ui.shadcn.com/), and [Google Gemini](https://deepmind.google/technologies/gemini/)
