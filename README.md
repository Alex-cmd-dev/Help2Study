# Help2Study - AI Flashcard Generator

A full-stack application that uses AI to automatically generate flashcards from your documents. Upload a PDF, DOCX, or TXT file and let Google Gemini create study materials for you.

Built with React, Django, and modern web technologies to demonstrate real-world full-stack development.

---
## What You'll Learn

By exploring and modifying this project, you'll understand:
- ✅ How data flows from user action → frontend → backend → database and back
- ✅ How authentication works in real applications (JWT tokens)
- ✅ How to integrate third-party APIs (Google Gemini)
- ✅ How to structure a production-ready full-stack app
- ✅ Common patterns you'll see in professional codebases
- ✅ Why certain architectural decisions are made

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
- SQLite - Database (built-in, no installation needed)
- Google Gemini - AI processing

---

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

**New to installation or running Windows?** Check [INSTALLATION.md](INSTALLATION.md) for easy setup using package managers (Homebrew for macOS, Winget for Windows).

### Automated Setup (Recommended)

Run the setup script for your operating system:

**macOS/Linux:**
```bash
./setup.sh
```

**Windows:**
```batch
setup.bat
```

The script will:
- Check that Python and Node.js are installed
- Create your `.env` file from `.env.example`
- Install all dependencies
- Set up the database
- Guide you through any required steps

Then start the app:
```bash
make dev
```

Visit http://localhost:5173 to use the app!

---

## Next Steps After Setup

Once the app is running, here's your learning path:

1. **⏱️ 5 mins** - Create your first flashcard set: Upload a document and see the AI in action
2. **⏱️ 30 mins** - Follow a request through the code: Open browser DevTools (Network tab), make a request, trace it through the codebase using the flow diagram above
3. **⏱️ 1 hour** - Read [CONCEPTS_GUIDE.md](CONCEPTS_GUIDE.md): Learn the terminology you'll see in the code
4. **⏱️ 2-3 hours** - Explore the codebase: Read through the files in the Project Structure below, see how they connect
5. **⏱️ Variable** - Try the challenges: See "Challenges" section below to start building!

---

### Manual Setup (Alternative)

**1. Clone and configure**
```bash
git clone https://github.com/Alex-cmd-dev/Help2Study.git
cd Help2Study
cp .env.example .env
```

**Get your Gemini API key:**
1. Go to https://aistudio.google.com and sign in with your Google account
2. Click on "Get API Key" in the dashboard
3. Click "Create API Key"
4. Create a new project (or select an existing one)
5. Select the project you want to use
6. Click "Generate API Key"
7. Copy the generated API key
8. Open `.env` file and paste your API key: `GEMINI_API_KEY=your_key_here`

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
│   │   ├── geminiapi.py       # AI integration
│   │   └── utils/             # Utility functions
│   │       └── text_extractors.py
│   └── backend/
│       └── settings.py        # Configuration
│
├── frontend/                   # React (Client)
│   └── src/
│       ├── components/        # UI components
│       ├── pages/             # Page views
│       ├── services/          # API service layer
│       │   ├── topicService.js
│       │   └── flashcardService.js
│       └── api.js             # HTTP client
│
├── ARCHITECTURE.md            # System design details
├── ADVANCED_PATTERNS.md       # Professional patterns guide
├── CONCEPTS_GUIDE.md          # Technical glossary
├── INSTALLATION.md            # Beginner installation guide
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

## Challenges: Apply What You've Learned

### Challenge 1: Make It Yours (Beginner - 30-60 mins)
**Goal:** Get comfortable modifying the existing codebase

Pick ONE to try:
- Add a "Favorite" button to flashcards (frontend + backend + database)
- Change the flashcard flip animation to a slide transition
- Add a flashcard counter showing "Card 3 of 10"
- Modify the AI prompt in `geminiapi.py` to generate more/fewer questions per document
- Add a "dark mode" toggle to the UI

**Why this helps:** You'll trace code from UI → API → database, understanding the full flow.

---

### Challenge 2: Add a New Feature (Intermediate - 2-4 hours)
**Goal:** Build something new using the existing patterns

Pick ONE feature to add:
- **Study Mode:** Track which cards you got right/wrong, show statistics
- **Search:** Filter flashcards by keyword
- **Edit Mode:** Let users edit generated flashcards before saving
- **Export:** Download flashcard set as CSV or JSON
- **Quiz Mode:** Multiple choice version of flashcards with scoring

**Why this helps:** You'll apply the patterns you learned to solve new problems.

---

### Challenge 3: Build Your Own Project (The Real Challenge)
**Goal:** Start YOUR project TODAY

Don't wait to feel "ready." Pick an idea and START:

**Ideas based on Help2Study's structure:**
- **Recipe Saver** - Upload photos, AI extracts ingredients/steps
- **Code Snippet Manager** - Save and organize code with AI-generated tags
- **Interview Prep** - Upload job description, generate practice questions
- **Budget Tracker** - Scan receipts, auto-categorize expenses
- **Habit Tracker** - Log daily habits with streak visualization

**Or adapt Help2Study directly:**
- Change it to quiz generation instead of flashcards
- Make it for a different subject (vocabulary, math problems, etc.)
- Add multiplayer study groups

**The Rule:** Commit your first code TODAY. Even if it's just the project setup and a README. Starting is the hardest part.

**Remember:** You learned by doing, not by waiting. Your next project will be easier because you'll recognize the patterns.

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

**Without Make:**

*Windows:*
```batch
# Start backend
cd backend && python manage.py runserver

# Start frontend (in a new terminal)
cd frontend && npm run dev
```

*macOS/Linux:*
```bash
# Start backend
cd backend && python3 manage.py runserver

# Start frontend (in a new terminal)
cd frontend && npm run dev
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
- [INSTALLATION.md](INSTALLATION.md) - Fast setup using package managers
- [ARCHITECTURE.md](ARCHITECTURE.md) - Request flow diagrams
- [CONCEPTS_GUIDE.md](CONCEPTS_GUIDE.md) - Technical terms explained
- [ADVANCED_PATTERNS.md](ADVANCED_PATTERNS.md) - Professional patterns & refactoring guide

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
→ Create `.env` file with your Gemini API key:
   1. Visit https://aistudio.google.com
   2. Sign in and click "Get API Key" in the dashboard
   3. Create a new project or select an existing one
   4. Generate the API key and copy it
   5. Paste it in your `.env` file: `GEMINI_API_KEY=your_key_here`

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
