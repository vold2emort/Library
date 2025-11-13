import React, { useState } from "react";

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password1: "",
    email: "",
    password2: "",
  });

  // Handle input change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();

    const endpoint = isLogin
      ? "http://127.0.0.1:8000/api/v1/rest-auth/login/"
      : "http://127.0.0.1:8000/api/v1/rest-auth/registration/";

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      console.log(data);

      if (res.ok) {
        alert(isLogin ? "Login successful!" : "Signup successful!");
      } else {
        alert(data.detail || "Something went wrong");
        console.log()
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Network error");
    }
  };

  return (
    <div className="d-flex vh-100 justify-content-center align-items-center bg-light">
      <div className="card shadow p-4" style={{ width: "400px" }}>
        <h3 className="text-center mb-3 fw-bold">
          {isLogin ? "Login" : "Sign Up"}
        </h3>

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-floating mb-3">
              <input
                type="email"
                name="email"
                className="form-control"
                id="floatingEmail"
                placeholder="name@example.com"
                required
                value={formData.email}
                onChange={handleChange}
              />
              <label htmlFor="floatingEmail">Email</label>
            </div>
          )}

          <div className="form-floating mb-3">
            <input
              type="text"
              name="username"
              className="form-control"
              id="floatingUsername"
              placeholder="Username"
              required
              value={formData.username}
              onChange={handleChange}
            />
            <label htmlFor="floatingUsername">Username</label>
          </div>

          <div className="form-floating mb-3">
            <input
              type="password"
              name="password1"
              className="form-control"
              id="floatingPassword"
              placeholder="Password"
              required
              value={formData.password}
              onChange={handleChange}
            />
            <label htmlFor="floatingPassword">Password</label>
          </div>

          {!isLogin && (
            <div className="form-floating mb-3">
              <input
                type="password"
                name="password2"
                className="form-control"
                id="floatingCPassword"
                placeholder="Confirm Password"
                required
                value={formData.c_password}
                onChange={handleChange}
              />
              <label htmlFor="floatingCPassword">Confirm Password</label>
            </div>
          )}

          <div className="text-center">
            <button type="submit" className="btn btn-primary w-100">
              {isLogin ? "Login" : "Sign Up"}
            </button>
          </div>
        </form>

        <p className="text-center mt-3">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            className="btn btn-link p-0"
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin ? "Sign up here" : "Login here"}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthForm;
