import React from 'react';
import { useNavigate } from 'react-router-dom';
import './payment-canceled.css';

interface PaymentCanceledProps {
  token: string;
}

const PaymentCancel: React.FC<PaymentCanceledProps> = ({ token }) => {
  const navigate = useNavigate();

  return (
    <div className="payment-cancel">
        <div>
          <p>There was an error processing your payment.</p>
          <button onClick={() => navigate('/profile')}>Return to Profile</button>
        </div>  
    </div>
  );
};

export default PaymentCancel;