import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import './payment-success.css';

interface PaymentSuccessProps {
  token: string;
}

const PaymentSuccess: React.FC<PaymentSuccessProps> = ({ token }) => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');

  useEffect(() => {
    const verifyPayment = async () => {
      const sessionId = searchParams.get('session_id');
      
      if (!sessionId) {
        setStatus('error');
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/api/payments/payment-success/?session_id=${sessionId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });

        if (response.ok) {
          setStatus('success');
          // Refresh user data or redirect
          setTimeout(() => {
            navigate('/profile');
          }, 2000);
        } else {
          setStatus('error');
        }
      } catch (error) {
        setStatus('error');
      }
    };

    verifyPayment();
  }, [searchParams, token, navigate]);

  return (
    <div className="payment-success">
      {status === 'loading' && <p>Verifying payment...</p>}
      {status === 'success' && <p>Payment successful! Redirecting...</p>}
      {status === 'error' && (
        <div>
          <p>There was an error processing your payment.</p>
          <button onClick={() => navigate('/profile')}>Return to Profile</button>
        </div>
      )}
    </div>
  );
};

export default PaymentSuccess;