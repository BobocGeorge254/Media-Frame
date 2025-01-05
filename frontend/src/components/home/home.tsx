import React from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const tiers = [
    {
      name: 'Free',
      price: '$0/month',
      features: [
        '2 audio/video processing tasks per day',
        'Access to transcribe and noisecancel',
        'Basic processing speed',
      ],
      priceId: null
    },
    {
      name: 'Basic',
      price: '$15/month',
      features: [
        '10 audio/video processing tasks per day',
        'Access to all operations: transcribe, noisecancel, bassboost, speedup, shift, speechidentifier',
        'Faster processing speed',
        'Priority support',
      ],
      priceId: 'price_1QdwivRZZTayXP3ZAb0BM0ry',
    },
    {
      name: 'Enterprise',
      price: '$100/month',
      features: [
        'Unlimited audio/video processing tasks',
        'Access to all operations',
        'Fastest processing speed',
        'Dedicated support and custom solutions',
      ],
      priceId: 'price_1QdwsJRZZTayXP3ZRTlV52rk',
    },
  ];

  return (
    <div className="homepage-container">
      <header className="homepage-header">
        <h1>Welcome to MediaFrame</h1>
        <p>Choose the plan that best suits your audio and video processing needs.</p>
        <div className="homepage-buttons">
          <button 
            className="action-button register-button"
            onClick={() => navigate('/register')}
          >
            Register
          </button>

          <button
            className="action-button login-button"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        </div>
      </header>

      <div className="tier-cards">
        {tiers.map((tier, index) => (
          <div
            className="tier-card"
            key={index}
          >
            <h2>{tier.name}</h2>
            <p className="price">{tier.price}</p>
            <ul className="features">
              {tier.features.map((feature, i) => (
                <li key={i}>{feature}</li>
              ))}
            </ul>
            {tier.name !== 'Free' ? (
              <form action={`http://localhost:8000/api/payments/stripe-checkout/${tier.priceId}/`} method="POST">
                <button className="select-plan-button">Select Plan</button>
              </form>
            ) : (
              <button
                className="select-plan-button"
                onClick={() => navigate('/processor')}
              >
                Try for Free
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
