# Flashcards - AI-Powered Study Tool

A full-stack application that uses AI (Google Gemini) to automatically generate flashcards from uploaded documents (PDF, DOCX, TXT). Built with React, Django, and the Gemini API.

## Features

- Upload documents (PDF, DOCX, or TXT files)
- AI-powered flashcard generation using Google Gemini
- Organize flashcards by topics
- Interactive flashcard viewer with flip animation
- User authentication with JWT tokens
- Responsive design with Tailwind CSS

## Tech Stack

**Frontend:**
- React 18
- Vite
- React Router
- Tailwind CSS 4.0
- Axios
- shadcn/ui components

**Backend:**
- Django 5.1
- Django REST Framework
- Google Gemini AI API
- JWT Authentication
- SQLite database

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+ (for Django backend)
- Node.js 16+ and npm (for React frontend)
- Make (optional, for using Makefile commands)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Flashcards
```

### 2. Set Up Environment Variables

Copy the `.env.example` file to `.env` and fill in your actual values:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Gemini API key:

```env
# Get your API key from: https://makersuite.google.com/app/apikey
API_KEY=your_gemini_api_key_here

# Backend API URL (default for local development)
VITE_API_URL=http://localhost:8000
```

### 3. Install Dependencies

#### Option A: Using Make (Recommended)

```bash
make install
```

#### Option B: Manual Installation

**Backend:**
```bash
cd backend
python -m pip install -r requirements.txt
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 4. Run Database Migrations

```bash
make migrate
# OR
cd backend && python manage.py migrate
```

### 5. Start the Development Servers

#### Option A: Using Make (Recommended)

Start both servers simultaneously:
```bash
make dev
```

Start servers individually:
```bash
make dev-backend  # Start Django on http://localhost:8000
make dev-frontend # Start Vite on http://localhost:5173
```

#### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Available Make Commands

```bash
make help            # Show all available commands
make install         # Install all dependencies
make install-backend # Install Python dependencies only
make install-frontend # Install Node.js dependencies only
make setup           # Complete setup (install + migrate)
make dev             # Start both dev servers
make dev-backend     # Start Django server only
make dev-frontend    # Start Vite server only
make migrate         # Run Django migrations
make lint            # Run linting checks
make test            # Run backend tests
make clean           # Clean temporary files and caches
```

## Project Structure

```
Flashcards/
├── backend/                 # Django backend
│   ├── api/                # Main API app
│   │   ├── models.py       # Database models
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   ├── geminiapi.py    # Gemini AI integration
│   │   └── urls.py         # API routes
│   ├── backend/            # Django settings
│   │   ├── settings.py     # Project settings
│   │   └── urls.py         # Main URL configuration
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── api.js          # Axios configuration
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── Makefile                # Make commands for easy setup
└── README.md               # This file
```

## Usage

1. **Register/Login**: Create an account or log in
2. **Upload Document**: Go to the home page and upload a PDF, DOCX, or TXT file
3. **Enter Topic**: Provide a topic name for organizing your flashcards
4. **Generate**: The AI will automatically extract content and generate flashcards
5. **Study**: Navigate to Topics to view and study your flashcards

## API Endpoints

### Authentication
- `POST /api/user/register/` - Register new user
- `POST /api/token/` - Login (get JWT tokens)
- `POST /api/token/refresh/` - Refresh access token

### Flashcards
- `GET /api/topics/` - Get all topics
- `POST /api/flashcards/` - Upload file and create flashcards
- `GET /api/flashcards/<topic_id>/` - Get flashcards for a topic
- `DELETE /api/topics/<topic_id>/delete/` - Delete a topic

## Linting

The project includes ESLint configuration for the frontend. Run linting checks:

```bash
make lint
# OR
cd frontend && npm run lint
```

Currently, there is 1 minor warning about exporting both components and constants in the button.jsx file, which is intentional for the shadcn/ui component library.

## Troubleshooting

### Issue: "API_KEY not found"
- Make sure you created the `.env` file in the root directory
- Verify you added your Gemini API key to the `.env` file
- Get an API key from: https://makersuite.google.com/app/apikey

### Issue: "Cannot connect to backend"
- Ensure the backend server is running on port 8000
- Check that `VITE_API_URL` in your `.env` file is set to `http://localhost:8000`
- Verify CORS settings in Django settings.py

### Issue: ESLint errors
- Run `make install-frontend` or `cd frontend && npm install` to ensure all dependencies are installed
- The project has been configured to handle most linting issues

### Issue: Database errors
- Run migrations: `make migrate` or `cd backend && python manage.py migrate`
- Delete `db.sqlite3` and run migrations again if needed

## Security Notes

- The `.env` file contains sensitive information and is excluded from version control
- Never commit your API keys or secrets to the repository
- The Django SECRET_KEY in settings.py should be changed for production use
- Set DEBUG=False and configure ALLOWED_HOSTS properly for production deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run linting checks
5. Submit a pull request

## License

This project is for educational purposes.

## Credits

- Built with [Django](https://www.djangoproject.com/)
- Frontend powered by [React](https://react.dev/) and [Vite](https://vitejs.dev/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- AI powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
