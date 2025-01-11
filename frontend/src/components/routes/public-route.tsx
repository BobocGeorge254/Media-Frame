// src/components/routes/PublicRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';

interface PublicRouteProps {
  isLoggedIn: boolean;
  children: React.ReactNode;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ isLoggedIn, children }) => {
  return isLoggedIn ? <Navigate to="/processor" /> : <>{children}</>;
};

export default PublicRoute;
