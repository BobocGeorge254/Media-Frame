import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import './forgot-password.css';

const ForgotPassword: React.FC = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/forgot-password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            if (response.ok) {
                setMessage('If the email exists, a password reset link has been sent.');
                setError('');
            } else {
                const result = await response.json();
                setError(result.error || 'An error occurred.');
                setMessage('');
            }
        } catch (err) {
            setError('Failed to connect to the server.');
            setMessage('');
        }
    };

    return (
        <div className="forgot-password-container">
            <div className="forgot-password-form">
                <h1>Forgot Password</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                        />
                    </div>
                    <button type="submit">Send Reset Link</button>
                </form>
                {message && <p className="success-text">{message}</p>}
                {error && <p className="error-text">{error}</p>}
                <button className="back-button" onClick={() => navigate('/login')}>
                    Back to Login
                </button>
            </div>
        </div>
    );
};

export default ForgotPassword;
