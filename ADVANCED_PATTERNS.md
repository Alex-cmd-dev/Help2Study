# Advanced Patterns & Professional Architecture

This guide explains the architectural patterns used in Help2Study and when to apply them. It's designed for students who understand the basics and are ready to learn professional software engineering practices.

> **Prerequisites:** You should be comfortable with the concepts in [ARCHITECTURE.md](ARCHITECTURE.md) before reading this guide.

---

## Table of Contents

1. [What Changed & Why](#what-changed--why)
2. [Backend Patterns](#backend-patterns)
3. [Frontend Patterns](#frontend-patterns)
4. [When to Refactor](#when-to-refactor)
5. [Testing Strategies](#testing-strategies)
6. [Next Steps](#next-steps)

---

## What Changed & Why

### The Journey So Far

In the original architecture, the code was organized for **learning clarity**:
- All file processing logic in one place (`geminiapi.py`)
- API calls directly in components
- Clear, linear flow through the request cycle

This is perfect for understanding **how** things work. But as projects grow, we need better organization.

### What We Improved

We made **minimal, high-impact** changes:

#### Backend Changes
```
Before:
backend/api/geminiapi.py
├── processfile()
├── pdf_to_text()         ← Text extraction
├── docx_to_text()        ← Text extraction
├── read_text_file()      ← Text extraction
├── text_2flashcards()
└── create_flashcards()

After:
backend/api/
├── geminiapi.py          ← Focus on AI & orchestration
└── utils/
    └── text_extractors.py ← Pure utility functions
```

**Benefits:**
- Text extractors are **reusable** (could be used for file preview feature)
- Text extractors are **testable** (no dependencies on Django or AI)
- Main file is **clearer** (focuses on the workflow, not format details)

#### Frontend Changes
```
Before:
Components call API directly:
→ ListofTopics.jsx: api.get('/api/topics/')
→ FileUploadForm.jsx: api.post('/api/topics/', data)
→ DisplayFlashcards.jsx: api.get('/api/flashcards/:id')

After:
Components use services:
→ ListofTopics.jsx: topicService.getAllTopics()
→ FileUploadForm.jsx: topicService.createTopic(data)
→ DisplayFlashcards.jsx: flashcardService.getFlashcardsByTopic(id)
```

**Benefits:**
- **DRY Principle**: API calls defined once, used everywhere
- **Single Source of Truth**: Change endpoint in one place
- **Easier Testing**: Mock the service instead of API calls
- **Clearer Components**: Components focus on UI, not network logic

---

## Backend Patterns

### 1. Utility Functions Pattern

**What:** Pure functions with no dependencies that perform a specific task.

**Example:** Text extractors in `backend/api/utils/text_extractors.py`

```python
# Pure function - same input always produces same output
def pdf_to_text(file_path):
    # No database access, no API calls, no side effects
    return extracted_text
```

**When to use:**
- ✅ File parsing, data transformation, calculations
- ✅ Functions used in multiple places
- ✅ Functions that don't need Django models or request context
- ❌ Database operations (use models or services instead)
- ❌ API calls (use services instead)

**Benefits:**
- Easy to test (no mocking needed)
- Easy to reuse
- Easy to understand

### 2. Service Layer Pattern (Next Step)

**What:** Classes or modules that encapsulate business logic.

**Example (not yet implemented):**
```python
# backend/api/services/flashcard_service.py

class FlashcardService:
    """
    Handles all flashcard-related business logic
    """

    def create_flashcards_from_file(self, file, topic, user):
        """
        Complete workflow for flashcard creation
        """
        # 1. Validate file
        # 2. Extract text
        # 3. Call AI
        # 4. Save to database
        # 5. Return results

    def get_user_flashcards(self, user, topic_id=None):
        """
        Get flashcards with optional filtering
        """
        pass
```

**When to use:**
- ✅ Complex business logic that spans multiple models
- ✅ Operations that involve external APIs + database
- ✅ When views become too complex (>50 lines)
- ❌ Simple CRUD operations (views are fine)
- ❌ Pure utility functions (use utils instead)

**Benefits:**
- Business logic separated from web framework
- Easier to test (no HTTP requests needed)
- Can be reused in background tasks, CLI commands, etc.

### 3. Repository Pattern (Advanced)

**What:** Abstracts database access behind an interface.

**When to use:**
- ✅ Large applications with complex queries
- ✅ When you might switch databases
- ✅ When testing requires extensive database mocking

**For this project:** Probably overkill! Django's ORM is already a repository pattern.

---

## Frontend Patterns

### 1. Service Layer Pattern ✅ Implemented

**What:** Centralized API calls in separate modules.

**Example:** `frontend/src/services/topicService.js`

```javascript
// Before (in component)
const response = await api.get('/api/topics/');
const topics = response.data;

// After (with service)
const topics = await topicService.getAllTopics();
```

**Why it's better:**
```javascript
// If API endpoint changes:
// Before: Update in 5 different components
// After: Update once in the service

// If you need to add caching:
// Before: Add caching logic to 5 components
// After: Add caching once in the service

// If you need to retry failed requests:
// Before: Add retry logic to 5 components
// After: Add retry logic once in the service
```

### 2. Custom Hooks Pattern (Next Step)

**What:** Reusable React hooks that encapsulate common logic.

**Example (not yet implemented):**
```javascript
// frontend/src/hooks/useTopics.js

export function useTopics() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTopics();
  }, []);

  const loadTopics = async () => {
    try {
      setLoading(true);
      const data = await topicService.getAllTopics();
      setTopics(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteTopic = async (id) => {
    await topicService.deleteTopic(id);
    await loadTopics(); // Refresh list
  };

  return { topics, loading, error, deleteTopic, refresh: loadTopics };
}

// Usage in component
function ListofTopics() {
  const { topics, loading, error, deleteTopic } = useTopics();

  if (loading) return <Loading />;
  if (error) return <Error message={error} />;

  return <div>
    {topics.map(topic => <TopicCard key={topic.id} topic={topic} onDelete={deleteTopic} />)}
  </div>;
}
```

**When to use:**
- ✅ Repeated `useEffect` patterns (data fetching)
- ✅ Complex state management (loading, error, data)
- ✅ Logic used in multiple components
- ❌ Component-specific logic (keep in component)

**Benefits:**
- Eliminates duplicate code
- Components become simpler
- State management logic is testable in isolation

### 3. Context API Pattern (Next Step)

**What:** Share state across components without prop drilling.

**Example (not yet implemented):**
```javascript
// frontend/src/context/AuthContext.jsx

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (credentials) => {
    const userData = await authService.login(credentials);
    setUser(userData);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Usage anywhere in the app
function NavBar() {
  const { user, logout } = useAuth();
  return <div>Hello, {user.username}! <button onClick={logout}>Logout</button></div>;
}
```

**When to use:**
- ✅ User authentication state
- ✅ Theme (dark/light mode)
- ✅ Data needed by many components
- ❌ Frequently changing data (causes re-renders)
- ❌ Component-specific state (use useState)

### 4. React Query / SWR (Advanced)

**What:** Libraries for data fetching, caching, and synchronization.

**When to use:**
- ✅ Apps with lots of data fetching
- ✅ Need automatic refetching
- ✅ Need optimistic updates
- ✅ Complex caching requirements

**For this project:** Good next step after mastering custom hooks!

---

## When to Refactor

### Signs You Need Better Organization

#### Backend
1. **File over 200 lines** → Extract utilities or create services
2. **Copy-pasting code** → Extract to reusable function
3. **View does multiple things** → Create service layer
4. **Hard to test** → Too many dependencies, need better separation

#### Frontend
1. **API calls duplicated** → Create services
2. **Same `useEffect` pattern repeated** → Create custom hook
3. **Props drilling 3+ levels deep** → Use Context API
4. **Component over 200 lines** → Split into smaller components

### The Refactoring Process

**Step 1: Identify Pain Points**
- What's hard to change?
- What's duplicated?
- What's hard to test?

**Step 2: Make Small Changes**
- Don't rewrite everything at once
- Extract one thing at a time
- Test after each change

**Step 3: Document Why**
- Add comments explaining the pattern
- Update architecture documentation
- Share with your team

**Example:**
```python
# Bad: Refactor everything at once (risky!)
# ❌ Move all logic to services
# ❌ Add dependency injection
# ❌ Implement repository pattern
# ❌ Add caching layer
# → Too many changes, hard to debug if something breaks!

# Good: Refactor incrementally (safe!)
# ✅ Week 1: Extract text utilities
# ✅ Week 2: Test the utilities
# ✅ Week 3: Create one service class
# ✅ Week 4: Test the service
# → Each change is small and verifiable
```

---

## Testing Strategies

### Backend Testing

#### Test Pure Utilities (Easy!)
```python
# tests/test_text_extractors.py

def test_pdf_to_text():
    result = pdf_to_text("fixtures/sample.pdf")
    assert "expected text" in result

def test_invalid_pdf():
    with pytest.raises(ValueError):
        pdf_to_text("fixtures/corrupted.pdf")
```

#### Test Services (Medium)
```python
# tests/test_flashcard_service.py

@pytest.fixture
def mock_ai():
    with patch('api.services.flashcard_service.ai_client') as mock:
        mock.generate.return_value = [{"q": "What?", "a": "Answer"}]
        yield mock

def test_create_flashcards(mock_ai):
    service = FlashcardService()
    result = service.create_from_text("text content")
    assert len(result) == 1
    mock_ai.generate.assert_called_once()
```

#### Test Views (Advanced)
```python
# tests/test_views.py

def test_create_topic_endpoint(client, user):
    client.force_authenticate(user=user)

    with open('fixtures/test.pdf', 'rb') as f:
        response = client.post('/api/topics/', {
            'name': 'Test Topic',
            'file': f
        })

    assert response.status_code == 201
    assert Topic.objects.filter(name='Test Topic').exists()
```

### Frontend Testing

#### Test Services (Easy!)
```javascript
// services/__tests__/topicService.test.js

import { getAllTopics } from '../topicService';
import api from '../../api';

jest.mock('../../api');

test('getAllTopics returns data', async () => {
  api.get.mockResolvedValue({ data: [{ id: 1, name: 'Math' }] });

  const topics = await getAllTopics();

  expect(topics).toEqual([{ id: 1, name: 'Math' }]);
  expect(api.get).toHaveBeenCalledWith('/api/topics/');
});
```

#### Test Custom Hooks (Medium)
```javascript
// hooks/__tests__/useTopics.test.js

import { renderHook, act } from '@testing-library/react-hooks';
import { useTopics } from '../useTopics';
import topicService from '../../services/topicService';

jest.mock('../../services/topicService');

test('useTopics loads data', async () => {
  topicService.getAllTopics.mockResolvedValue([{ id: 1 }]);

  const { result, waitForNextUpdate } = renderHook(() => useTopics());

  expect(result.current.loading).toBe(true);

  await waitForNextUpdate();

  expect(result.current.loading).toBe(false);
  expect(result.current.topics).toEqual([{ id: 1 }]);
});
```

#### Test Components (Advanced)
```javascript
// components/__tests__/ListofTopics.test.jsx

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ListofTopics from '../ListofTopics';
import topicService from '../../services/topicService';

jest.mock('../../services/topicService');

test('displays topics and allows deletion', async () => {
  topicService.getAllTopics.mockResolvedValue([
    { id: 1, name: 'Math', created_at: '2024-01-01' }
  ]);

  render(<ListofTopics />);

  await waitFor(() => {
    expect(screen.getByText('Math')).toBeInTheDocument();
  });

  const deleteButton = screen.getByRole('button', { name: /delete/i });

  topicService.deleteTopic.mockResolvedValue();

  userEvent.click(deleteButton);

  await waitFor(() => {
    expect(topicService.deleteTopic).toHaveBeenCalledWith(1);
  });
});
```

---

## Next Steps

### For Beginners → Intermediate

1. **✅ You've completed:** Basic refactoring (utilities + services)
2. **Next:** Write tests for your services
3. **Then:** Create your first custom hook
4. **Finally:** Add error boundaries and loading states

### For Intermediate → Advanced

1. **Learn:** TypeScript for type safety
2. **Learn:** React Query for advanced data fetching
3. **Learn:** End-to-end testing with Playwright or Cypress
4. **Learn:** CI/CD pipelines for automated testing

### For Advanced → Professional

1. **Learn:** Microservices architecture
2. **Learn:** Docker and containerization
3. **Learn:** Kubernetes for orchestration
4. **Learn:** Monitoring and observability (Sentry, DataDog)

---

## Additional Resources

### Books
- **Clean Code** by Robert C. Martin - Principles of clean, maintainable code
- **Design Patterns** by Gang of Four - Classic software patterns
- **Refactoring** by Martin Fowler - How to improve existing code

### Online Courses
- **Test-Driven Development** (FreeCodeCamp)
- **Advanced React Patterns** (Kent C. Dodds)
- **Django Best Practices** (Two Scoops of Django)

### Practice Projects
1. Add user profile management to this app
2. Implement spaced repetition algorithm
3. Add collaborative study groups
4. Build a mobile app using React Native

---

## Questions to Consider

As you build your own projects, ask yourself:

1. **Is this code easy to change?** If not, what's making it hard?
2. **Is this code easy to test?** If not, what dependencies are in the way?
3. **Would a new developer understand this?** If not, add comments or refactor.
4. **Am I repeating myself?** If yes, extract to a reusable function.
5. **Is this the simplest solution?** Don't over-engineer, but don't under-engineer either.

---

## Final Thoughts

**Remember:**
- There's no perfect architecture
- Refactoring is a continuous process
- Simplicity is often better than cleverness
- Code is written once, read many times
- Make it work, make it right, make it fast (in that order!)

Good luck on your learning journey! 🚀
