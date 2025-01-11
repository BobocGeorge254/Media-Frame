import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

interface UseAuthResult {
  token: string;
  refreshToken: string;
  isLoggedIn: boolean;
  isInitializing: boolean;
  handleLogin: (accessToken: string, refreshToken: string) => void;
  handleLogout: () => Promise<void>;
}

export const useAuth = (): UseAuthResult => {
  const [token, setToken] = useState<string>('');
  const [refreshToken, setRefreshToken] = useState<string>('');
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [isInitializing, setIsInitializing] = useState<boolean>(true);
  const navigate = useNavigate();

  const refreshAccessToken = async (currentRefreshToken: string): Promise<{ access: string; refresh?: string } | null> => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh: currentRefreshToken,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        return { access: data.access, refresh: data.refresh };
      }
      return null;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return null;
    }
  };

  const refreshThreshold = 3 * 60 * 1000;

  const shouldRefresh = (token: string): boolean => {
    if (!token) return false;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expirationTime = payload.exp * 1000; 
      const currentTime = Date.now();

      return currentTime >= expirationTime - refreshThreshold;
    } catch (error) {
      return false;
    }
  };

  useEffect(() => {
    const refreshInterval = setInterval(async () => {
      if (isLoggedIn && refreshToken) {
        if (shouldRefresh(token)) {
          const result = await refreshAccessToken(refreshToken);
          if (result) {
            const { access, refresh } = result;
            setToken(access);
            localStorage.setItem('accessToken', access);
  
            if (refresh) {
              setRefreshToken(refresh);
              localStorage.setItem('refreshToken', refresh);
            }
          } else {
            await handleLogout(); // Logout if refresh fails
          }
        }
      }
    }, 3 * 60 * 1000); 

    return () => clearInterval(refreshInterval);
  }, [token, refreshToken, isLoggedIn]);

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    
    if (storedAccessToken && storedRefreshToken) {
      setToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      setIsLoggedIn(true);
    }
    setIsInitializing(false);
  }, []);

  const handleLogin = useCallback((accessToken: string, refreshToken: string) => {
    setToken(accessToken);
    setRefreshToken(refreshToken);
    setIsLoggedIn(true);
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    navigate('/processor');
  }, []);

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

      if (!response.ok) {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      setToken('');
      setRefreshToken('');
      setIsLoggedIn(false);
    }
  };

  return {
    token,
    refreshToken,
    isLoggedIn,
    isInitializing,
    handleLogin,
    handleLogout,
  };
};