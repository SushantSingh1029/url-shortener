import { useState } from "react";
import { useNavigate } from "react-router-dom";

import API from "../api/api";

function Login() {

  const navigate = useNavigate();

  const [username, setUsername] = useState("");

  const [password, setPassword] = useState("");

  const [error, setError] = useState("");

  async function handleLogin(e) {

    e.preventDefault();

    setError("");

    try {

      const formData = new URLSearchParams();

      formData.append("username", username);

      formData.append("password", password);

      const response = await API.post(
        "/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      navigate("/dashboard");

    }

    catch (err) {

      setError("Invalid username or password.");

    }

  }

  return (

    <div
      style={{
        width: "400px",
        margin: "80px auto",
        textAlign: "center",
      }}
    >

      <h1>Login</h1>

      <form onSubmit={handleLogin}>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <br /><br />

        <button type="submit">

          Login

        </button>

      </form>

      <br />

      {error &&

        <p style={{ color: "red" }}>

          {error}

        </p>

      }

    </div>

  );

}

export default Login;