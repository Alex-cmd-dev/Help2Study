.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend setup clean lint test

# Default target
help:
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies (backend + frontend)"
	@echo "  make install-backend - Install Python dependencies"
	@echo "  make install-frontend - Install Node.js dependencies"
	@echo "  make setup          - Complete setup including migrations and dependencies"
	@echo "  make dev            - Start both backend and frontend dev servers"
	@echo "  make dev-backend    - Start Django development server"
	@echo "  make dev-frontend   - Start Vite development server"
	@echo "  make lint           - Run linting checks"
	@echo "  make clean          - Clean temporary files and caches"
	@echo "  make migrate        - Run Django migrations"
	@echo "  make test           - Run tests"

# Install all dependencies
install: install-backend install-frontend
	@echo "All dependencies installed successfully!"

# Install backend dependencies
install-backend:
	@echo "Installing backend dependencies..."
	@cd backend && python -m pip install -r requirements.txt

# Install frontend dependencies
install-frontend:
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install

# Complete setup
setup: install
	@echo "Setting up the project..."
	@if [ ! -f .env ]; then \
		echo ".env file not found! Please copy .env.example to .env and fill in your values."; \
		exit 1; \
	fi
	@cd backend && python manage.py migrate
	@echo "Setup complete! Run 'make dev' to start the development servers."

# Run database migrations
migrate:
	@echo "Running database migrations..."
	@cd backend && python manage.py migrate

# Start both servers (in parallel using background processes)
dev:
	@echo "Starting development servers..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:5173"
	@echo ""
	@trap 'kill 0' EXIT; \
	(cd backend && python manage.py runserver) & \
	(cd frontend && npm run dev)

# Start backend server only
dev-backend:
	@echo "Starting Django backend server on http://localhost:8000..."
	@cd backend && python manage.py runserver

# Start frontend server only
dev-frontend:
	@echo "Starting Vite frontend server on http://localhost:5173..."
	@cd frontend && npm run dev

# Run linting
lint:
	@echo "Running linting checks..."
	@cd frontend && npm run lint

# Run tests
test:
	@echo "Running tests..."
	@cd backend && python manage.py test
	@echo "Backend tests complete!"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf backend/temp_files
	@echo "Clean complete!"
