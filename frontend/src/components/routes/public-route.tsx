import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

interface PublicRouteProps {
  isLoggedIn: boolean;
  children: React.ReactNode;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ isLoggedIn, children }) => {
  const location = useLocation();

  // Routes that should always be accessible, even when logged in
  const alwaysPublicRoutes = ['/confirm-email'];

  // Check if the current route starts with one of the always-public routes
  const isAlwaysPublic = alwaysPublicRoutes.some((route) =>
    location.pathname.startsWith(route)
  );

  // Redirect to /processor if logged in and not on an always-public route
  if (isLoggedIn && !isAlwaysPublic) {
    return <Navigate to="/processor" />;
  }

  return <>{children}</>;
};

export default PublicRoute;
