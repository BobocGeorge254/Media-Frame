import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Home from './components/home/home';
import Login from './components/authentication/login';
import Processor from './processor/processor';
import Register from './components/authentication/register';
import './App.css'
import ForgotPassword from './components/authentication/forgot-password';
import ResetPassword from './components/authentication/reset-password';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [token, setToken] = useState<string>(''); // Access token
  const [refreshToken, setRefreshToken] = useState<string>(''); // Refresh token
  const navigate = useNavigate();

  // Check if the user is logged in on component mount
  useEffect(() => {
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    if (storedAccessToken && storedRefreshToken) {
      setIsLoggedIn(true);
      setToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
    }
  }, []);

  const handleLogin = (accessToken: string, refreshToken: string) => {
    setIsLoggedIn(true);
    setToken(accessToken);
    setRefreshToken(refreshToken);
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    navigate('/processor'); // Redirect to processor page after login
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          refresh_token: refreshToken,
        }),
      });

      if (response.ok) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setIsLoggedIn(false);
        setToken('');
        setRefreshToken('');
        navigate('/'); // Redirect to Home page after logout
      } else {
        console.error('Logout failed');
      }
    } catch (err) {
      console.error('Logout failed', err);
    }
  };

  return (
    <div className="App">
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register onRegister={() => navigate('/login')} />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
        {/* Protected Route with Navbar */}
        <Route
          path="/processor"
          element={
            isLoggedIn ? (
              <div>
                {/* Navbar */}
                <header className="navbar">
                  <div className="navbar-left">
                    <div className="logo-icon">MF</div>
                    <h1 className="navbar-title">MediaFrame</h1>
                  </div>
                  <div className="navbar-right">
                    <button onClick={() => alert('Profile')} className="navbar-button profile-button">
                      Profile
                    </button>
                    <button onClick={handleLogout} className="navbar-button logout-button">
                      Logout
                    </button>
                  </div>
                </header>

                {/* Processor Content */}
                <Processor token={token} />
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
      </Routes>
    </div>
  );
};

export default App;
