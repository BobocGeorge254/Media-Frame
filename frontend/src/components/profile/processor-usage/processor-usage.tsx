import React, { useEffect, useState } from "react";
import "./processor-usage.css";

interface ProcessorUsage {
  id: number;
  processor_type: string;
  file: string;
  timestamp: string;
}

interface ProcessorUsageListProps {
  token: string;
}

const ProcessorUsageList: React.FC<ProcessorUsageListProps> = ({ token }) => {
  const [processorUsages, setProcessorUsages] = useState<ProcessorUsage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProcessorUsages = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/processor/processor-usage/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch processor usage data");
        }

        const data = await response.json();
        setProcessorUsages(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchProcessorUsages();
  }, [token]);

  if (loading) {
    return <div className="processor-usage loading">Loading...</div>;
  }

  if (error) {
    return <div className="processor-usage"><div className="error">Error: {error}</div></div>;
  }

  if (processorUsages.length === 0) {
    return <div className="processor-usage empty">No processor usage data available</div>;
  }

  return (
    <div className="processor-usage">
      <div className="container">
        <h1>Processor Usage</h1>
        
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Processor Type</th>
                <th>File</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {processorUsages.map((usage) => (
                <tr key={usage.id}>
                  <td>
                    <span className="processor-type">{usage.processor_type}</span>
                  </td>
                  <td>{usage.file.replace(/^.*[\\/]/, '')}</td>
                  <td>{new Date(usage.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ProcessorUsageList;