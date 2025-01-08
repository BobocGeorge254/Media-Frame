import React, { useState, FormEvent } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './reset-password.css';

const ResetPassword: React.FC = () => {
    const { uid, token } = useParams();
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/auth/reset-password/${uid}/${token}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password }),
            });

            if (response.ok) {
                setMessage('Password reset successfully. You can now log in.');
                setError('');
                setTimeout(() => navigate('/login'), 3000);
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
        <div className="reset-password-container">
            <div className="reset-password-form">
                <h1>Reset Password</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>New Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter new password"
                        />
                    </div>
                    <button type="submit">Reset Password</button>
                </form>
                {message && <p className="success-text">{message}</p>}
                {error && <p className="error-text">{error}</p>}
            </div>
        </div>
    );
};

export default ResetPassword;
