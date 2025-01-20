import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './email-confirmation.css';

const EmailConfirmation: React.FC = () => {
    const { uid, token } = useParams();
    const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [redirectCountdown, setRedirectCountdown] = useState(3);
    const navigate = useNavigate();

    useEffect(() => {
        const confirmEmail = async () => {
            try {
                // Clear any existing auth tokens first
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');

                const response = await fetch(`http://127.0.0.1:8000/api/auth/confirm-email/${uid}/${token}/`, {
                    method: 'GET',
                });

                if (response.ok) {
                    setMessage('Email confirmed successfully. Redirecting to login...');
                    setError('');
                    setStatus('success');

                    const countdownInterval = setInterval(() => {
                        setRedirectCountdown((prev) => {
                            if (prev <= 1) {
                                clearInterval(countdownInterval);
                                // Force a clean state before redirect
                                localStorage.clear();
                                window.location.href = '/login';
                                return 0;
                            }
                            return prev - 1;
                        });
                    }, 1000);

                    return () => clearInterval(countdownInterval);
                } else {
                    const result = await response.json();
                    setError(result.error || 'Invalid or expired confirmation link.');
                    setMessage('');
                    setStatus('error');
                }
            } catch (err) {
                setError('Failed to connect to the server. Please try again later.');
                setMessage('');
                setStatus('error');
            }
        };

        confirmEmail();
    }, [uid, token]);

    return (
        <div className="email-confirmation-container">
            <div className="email-confirmation-box">
                <h1>Email Confirmation</h1>
                {status === 'loading' && <p>Processing your request...</p>}
                {status === 'success' && (
                    <>
                        <p className="success-text">{message}</p>
                        <p>Redirecting in {redirectCountdown} seconds...</p>
                    </>
                )}
                {status === 'error' && <p className="error-text">{error}</p>}
            </div>
        </div>
    );
};

export default EmailConfirmation;