import React from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const tier = {
    name: 'Free',
    price: '$0/month',
    features: [
      '2 audio/video processing tasks per day',
      'Access to transcribe and noisecancel',
      'Basic processing speed',
    ],
  };

  return (
    <div className="homepage-container">
      <div className="card-container">
        <header className="card-header">
          <div className="app-title">
            <div className="logo-icon">MF</div>
            <h1>Media Frame</h1>
          </div>
          <p>Transform your audio and video like a pro, without the cost.</p>
        </header>

        <div className="auth-buttons">
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

        <div className="tier-card">
          <h2>{tier.name}</h2>
          <p className="price">{tier.price}</p>
          <ul className="features">
            {tier.features.map((feature, i) => (
              <li key={i}>{feature}</li>
            ))}
          </ul>
          <button
            className="select-plan-button"
            onClick={() => navigate('/processor')}
          >
            Start for Free
          </button>
        </div>

        <p className="login-message">
          To see all the price plans, please <strong>log in</strong> to the app.
        </p>
      </div>
    </div>
  );
};

export default Home;
