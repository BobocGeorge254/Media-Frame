import React from "react";
import "./processor-payments.css"

interface ProcessorUsageListProps {
    token: string;
  }

const ProcessorPayments : React.FC<ProcessorUsageListProps> = ({token}) => {
    return (
        <div className="processor-payments">
            <h1>payments</h1>
        </div>
    )
}

export default ProcessorPayments