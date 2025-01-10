import React, { useEffect, useState } from "react";
import "./processor-payments.css";

interface Payment {
  id: number;
  stripe_session_id: string;
  amount: string;
  status: string;
  created_at: string;
  price_id: string;
  user: number;
}

interface PaymentListProps {
  token: string;
}

const ProcessorPayments: React.FC<PaymentListProps> = ({ token }) => {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [filteredPayments, setFilteredPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>("completed");

  useEffect(() => {
    const fetchPayments = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/payments/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch payment data");
        }

        const data = await response.json();
        setPayments(data);
        setFilteredPayments(data.filter((payment: Payment) => payment.status === statusFilter));
      } catch (err) {
        setError(err instanceof Error ? err.message : "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchPayments();
  }, [token, statusFilter]);

  const handleStatusChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newStatus = event.target.value;
    setStatusFilter(newStatus);
  };

  if (loading) {
    return <div className="payment-list loading">Loading...</div>;
  }

  if (error) {
    return <div className="payment-list"><div className="error">Error: {error}</div></div>;
  }

  if (filteredPayments.length === 0) {
    return <div className="payment-list empty">No payments available</div>;
  }

  return (
    <div className="payment-list">
      <div className="container">
        <h1>Payments</h1>

        {/* Filter Dropdown */}
        <div className="filter-container">
          <label htmlFor="status-filter">Filter by Status: </label>
          <select id="status-filter" value={statusFilter} onChange={handleStatusChange}>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
        </div>
        
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Stripe Session ID</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {filteredPayments.map((payment) => (
                <tr key={payment.id}>
                  <td>{payment.stripe_session_id}</td>
                  <td>${payment.amount}</td>
                  <td>{payment.status}</td>
                  <td>{new Date(payment.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ProcessorPayments;
