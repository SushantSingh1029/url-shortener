import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";

function App() {

  const token = localStorage.getItem("token");

  return (
    <Routes>

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/"
        element={
          token
            ? <Navigate to="/dashboard" />
            : <Navigate to="/login" />
        }
      />

    </Routes>
  );
}

export default App;