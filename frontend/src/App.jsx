import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import Home from "./pages/Home";
import ProtectedRoute from "./components/ProtectedRoutes";
import Topics from "./pages/Topics";
import Flashcards from "./pages/Flashcards";
import Logout from "./pages/Logout";

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route
          path="/topics"
          element={
            <ProtectedRoute>
              <Topics></Topics>
            </ProtectedRoute>
          }
        />
        <Route
          path="topics/flashcards/:id"
          element={
            <ProtectedRoute>
              <Flashcards></Flashcards>
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
