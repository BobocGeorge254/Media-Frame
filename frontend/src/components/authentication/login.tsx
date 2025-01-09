import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';

interface LoginProps {
  onLogin: (accessToken: string, refreshToken: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const { access, refresh } = data;

        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        onLogin(access, refresh);
      } else {
        const result = await response.json();
        setError(result.error || 'Invalid credentials');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h1>Login</h1>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />
          </div>
          <button type="submit">Login</button>
        </form>
        {error && <p className="error-text">{error}</p>}

        <button type="submit" onClick={() => navigate('/register')}>Register</button>

        <p className="forgot-password">
          <a onClick={() => navigate('/forgot-password')} className="forgot-password-link">
            Forgot Password?
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;
