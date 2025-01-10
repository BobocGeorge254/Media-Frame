import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Home from './components/home/home';
import Login from './components/authentication/login';
import Processor from './components/processor/processor';
import Register from './components/authentication/register';
import Profile from './components/profile/profile';
import './App.css'
import ForgotPassword from './components/authentication/forgot-password';
import ResetPassword from './components/authentication/reset-password';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [token, setToken] = useState<string>(''); // Access token
  const [refreshToken, setRefreshToken] = useState<string>(''); // Refresh token
  const navigate = useNavigate();

  useEffect(() => {
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    if (storedAccessToken && storedRefreshToken) {
      setIsLoggedIn(true);
      setToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      navigate('/processor'); // Redirect to the processor if tokens are valid
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
      <header className="navbar">
        {!isLoggedIn && (
          <div className="navbar-left" onClick={() => navigate('/')}>
            <div className="logo-icon">MF</div>
            <h1 className="navbar-title">Media Frame</h1>
          </div>
        )}

        {isLoggedIn && (
          <div className="navbar-left" onClick={() => navigate('/processor')}>
            <div className="logo-icon">MF</div>
            <h1 className="navbar-title">Media Frame</h1>
          </div>
        )}


        <div className="navbar-right">
          {isLoggedIn && (
            <>
              <button onClick={() => navigate('/profile')} className="navbar-button profile-button">
                Profile
              </button>
              <button onClick={handleLogout} className="navbar-button logout-button">
                Logout
              </button>
            </>
          )}

        </div>
      </header>

      {/* Routes */}
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register onRegister={() => navigate('/login')} />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
        {/* Protected Route with Processor */}
        <Route
          path="/processor"
          element={
            isLoggedIn ? (
              <Processor token={token} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/profile"
          element={
            isLoggedIn ? (
              <Profile token={token} />
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
