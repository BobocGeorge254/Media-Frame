import React from 'react';
import './contact.css';

const Contact: React.FC = () => {
    return (
        <div className="contact-page">
            <div className="contact-thankyou">
                <h2>Thank You for Using Media Frame</h2>
                <p>We appreciate your support and feedback.</p>

                <div className="team-info">
                    <h3>Team Members:</h3>
                    <ul>
                        <li><strong>Albei Liviu-Andrei</strong> - Product Owner</li>
                        <li><strong>Codreanu Radu-Stefan</strong> - Scrum Master & Developer</li>
                        <li><strong>Boboc George</strong> - Developer</li>
                        <li><strong>Dirva Nicolae</strong> - Developer</li>
                    </ul>
                </div>

                <div className="feedback-info">
                    <p>If you would like to provide feedback or report bugs, please email us at:</p>
                    <a href="mailto:mediaframesupport@gmail.com">mediaframesupport@gmail.com</a>
                </div>
            </div>
        </div>
    );
};

export default Contact;
