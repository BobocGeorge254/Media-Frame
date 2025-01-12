import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import "./profile.css";

interface UserProfile {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string | null;
  tier: string;
  date_joined: string;
}

interface ProfileProps {
  token: string;
}

const Profile: React.FC<ProfileProps> = ({ token }) => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const { handleLogout } = useAuth();
  const navigate = useNavigate();

  const tiers = [
    {
      name: 'Free',
      price: '$0/month',
      features: [
        '2 audio/video processing tasks per day',
        'Access to bassboost and noisecancel',
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
      name: 'Premium',
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

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/auth/user/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch profile data");
        }

        const data = await response.json();
        setProfile(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token]);

  if (loading) {
    return <div className="Profile">Loading...</div>;
  }

  if (error) {
    return <div className="Profile">Error: {error}</div>;
  }

  if (!profile) {
    return <div className="Profile">No profile data available</div>;
  }

  const handlePayment = async (priceId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/payments/stripe-checkout/${priceId}/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Payment initiation failed');
      }

      // Get the redirect URL from response
      const data = await response.json();
      // Redirect to Stripe checkout
      window.location.href = data.url;

    } catch (error) {
      console.error('Payment error:', error);
      setError('Payment initialization failed');
    }
  };

  const handleAccountDeletion = async () => {
    try {
      handleLogout();
      const response = await fetch(`http://localhost:8000/api/auth/delete-account/`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) throw new Error("Failed to delete account");
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "Account deletion failed");
    } finally {
      setShowModal(false);
    }
  };

  return (
    <div className="Profile">
      <h1>User Profile</h1>
      <div className="button-container">
        <button onClick={() => navigate('/profile/processor-usage')}>Usage</button>
        <button onClick={() => navigate('/profile/processor-payments')}>Payments</button>
      </div>

      <div className="profile-details">
        <p><strong>Username:</strong> {profile.username}</p>
        <p><strong>Email:</strong> {profile.email}</p>
        <p><strong>Name:</strong> {profile.first_name} {profile.last_name}</p>
        <p><strong>Phone:</strong> {profile.phone_number || 'N/A'}</p>
        <p><strong>Tier:</strong> {profile.tier}</p>
        <p><strong>Joined:</strong> {new Date(profile.date_joined).toLocaleDateString()}</p>
      </div>

      <button className="delete-account-button" onClick={() => setShowModal(true)}>
        Delete Account
      </button>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>Confirm Account Deletion</h2>
            <p>Are you sure you want to delete your account? This action cannot be undone.</p>
            <div className="modal-actions">
              <button className="confirm-button" onClick={() => handleAccountDeletion()}>Yes, Delete</button>
              <button className="cancel-button" onClick={() => setShowModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      <div className="tier-cards-container">
        {tiers.map((tier, i) => (
          <div
            className={`tier-card ${profile.tier.toLowerCase() === tier.name.toLowerCase() || tier.name === 'Free' ? 'disabled' : ''}`}
            key={i}
          >
            <h2>{tier.name}</h2>
            <p className="price">{tier.price}</p>
            <ul className="features">
              {tier.features.map((feature, j) => (
                <li key={j}>{feature}</li>
              ))}
            </ul>
            {tier.name !== 'Free' ? (
              <button 
                className="select-plan-button"
                disabled={profile.tier.toLowerCase() === tier.name.toLowerCase()}
                onClick={() => tier.priceId && handlePayment(tier.priceId)}
              >
                {profile.tier.toLowerCase() === tier.name.toLowerCase() ? 'Your Current Plan' : 'Select Plan'}
              </button>
            ) : (
              <button
                className="select-plan-button"
                disabled={true}
              >
                You can't choose to join free tier
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Profile;
