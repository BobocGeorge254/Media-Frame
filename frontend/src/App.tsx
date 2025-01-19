import React from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Home from './components/home/home';
import Login from './components/authentication/login';
import Processor from './components/processor/processor';
import Register from './components/authentication/register';
import Profile from './components/profile/profile';
import ProcessorUsageList from './components/profile/processor-usage/processor-usage';
import ProcessorPayments from './components/profile/processor-payments/processor-payments';
import PaymentSuccess from './components/profile/payment-success';
import './App.css'
import ForgotPassword from './components/authentication/forgot-password';
import ResetPassword from './components/authentication/reset-password';
import EmailConfirmation from './components/authentication/email-confirmation';
import logo from './logo.png';
import { useAuth } from './hooks/useAuth';
import PublicRoute from './components/routes/public-route';
import ProtectedRoute from './components/routes/protected-route';
import PaymentCancel from './components/profile/payment-canceled';
import Contact from './components/contact/contact';

const App: React.FC = () => {
  const { token, refreshToken, isLoggedIn, isInitializing, handleLogin, handleLogout } = useAuth();
  const navigate = useNavigate();

  if (isInitializing) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <header className="navbar">
        <div className="navbar-left" onClick={() => navigate(isLoggedIn ? '/processor' : '/')}>
          <img src={logo} alt="Media Frame Logo" className="logo-icon" />
          <h1 className="navbar-title">Media Frame</h1>
        </div>

        <div className="navbar-right">
          {isLoggedIn && (
            <>
              <button onClick={() => navigate('/profile')} className="navbar-button profile-button">
                Profile
              </button>
              <button onClick={() => navigate('/contact')} className="navbar-button contact-button">
                Contact
              </button>
              <button onClick={() => handleLogout()} className="navbar-button logout-button">
                Logout
              </button>
            </>
          )}

        </div>
      </header>

      <Routes>
        {/* Public Routes */}
        <Route
          path="/"
          element={
            <PublicRoute isLoggedIn={isLoggedIn}>
              <Home />
            </PublicRoute>
          }
        />
        <Route
          path="/login"
          element={
            <PublicRoute isLoggedIn={isLoggedIn}>
              <Login onLogin={handleLogin} />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute isLoggedIn={isLoggedIn}>
              <Register onRegister={() => navigate('/login')} />
            </PublicRoute>
          }
        />
        <Route
          path="/forgot-password"
          element={
            <PublicRoute isLoggedIn={isLoggedIn}>
              <ForgotPassword />
            </PublicRoute>
          }
        />
        <Route
          path="/reset-password/:uid/:token"
          element={
            <PublicRoute isLoggedIn={isLoggedIn}>
              <ResetPassword />
            </PublicRoute>
          }
        />
        <Route
          path="/confirm-email/:uid/:token"
          element={
            <PublicRoute isLoggedIn={isLoggedIn}>
              <EmailConfirmation />
            </PublicRoute>
          }
        />
        <Route
          path="/payment-success"
          element={<PaymentSuccess token={token} />}
        />

        <Route
          path="/payment-canceled"
          element={
            <PaymentCancel token={token} />
          }
        />

        {/* Protected Routes */}
        <Route
          path="/processor"
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <Processor token={token} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <Profile token={token} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile/processor-usage"
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <ProcessorUsageList token={token} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile/processor-payments"
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <ProcessorPayments token={token} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/contact"
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <Contact />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
};

export default App;