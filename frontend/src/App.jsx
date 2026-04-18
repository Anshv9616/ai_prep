import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Resume from "./pages/Resume";
import Interview from "./pages/Interview";
import Session from "./pages/Session";
import History from "./pages/History";
import Stats from "./pages/Stats";

function Guard({ children }) {
  const { isAuthenticated } = useSelector((s) => s.auth);
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Guard><Dashboard /></Guard>} />
        <Route path="/resume" element={<Guard><Resume /></Guard>} />
        <Route path="/interview" element={<Guard><Interview /></Guard>} />
        <Route path="/session/:sessionId" element={<Guard><Session /></Guard>} />
        <Route path="/history" element={<Guard><History /></Guard>} />
        <Route path="/stats" element={<Guard><Stats /></Guard>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
