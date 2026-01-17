import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>🚴 RideWise</h3>
            <p>AI-Powered Bike Rental Prediction System</p>
          </div>
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/predict">Predict</a></li>
              <li><a href="/analytics">Analytics</a></li>
              <li><a href="/stations">Stations</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Technology</h4>
            <ul>
              <li>React.js</li>
              <li>Flask</li>
              <li>XGBoost ML</li>
              <li>Google Maps API</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Contact</h4>
            <p>📧 support@ridewise.com</p>
            <p>📞 +1 (555) 123-4567</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 RideWise. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;