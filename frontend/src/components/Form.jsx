import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Form({ route, method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const name = method === "login" ? "Login" : "Register";

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(route, { username, password });
      if (method === "login") {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-lg">
      <fieldset className="fieldset w-full bg-base-200 border border-base-300 p-6 rounded-box shadow-lg">
        <legend className="fieldset-legend text-xl font-semibold">
          {name}
        </legend>

        <label className="fieldset-label text-lg mt-2">Username</label>
        <input
          type="text"
          className="input input-lg w-full p-3"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />

        <label className="fieldset-label text-lg mt-4">Password</label>
        <input
          type="password"
          className="input input-lg w-full p-3"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />

        <button className="btn btn-neutral btn-lg mt-6 w-full" type="submit">
          {name}
        </button>
      </fieldset>
    </form>
  );
}

export default Form;
