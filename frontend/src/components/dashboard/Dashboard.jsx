import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Chatbot from '../chatbot/Chatbot';
import api from '../../services/api';
import '../../styles/Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({
    total_predictions: 0,
    daily_predictions: 0,
    hourly_predictions: 0,
    last_prediction: '--',
    feedback_count: 0,
    accuracy_rate: 95
  });
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (! token) {
      navigate('/');
      return;
    }

    fetchUserData();
    fetchDashboardStats();
  }, [token, navigate]);

  const fetchUserData = async () => {
    try {
      const username = localStorage.getItem('username') || 'User';
      setUser({ name: username });
    } catch (error) {
      console.error('Error fetching user data:', error);
      const username = localStorage.getItem('username') || 'User';
      setUser({ name: username });
    }
  };

  const fetchDashboardStats = async () => {
    try {
      const { data } = await api.get('/dashboard/stats');
      if (data.success) {
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Failed to load dashboard stats:', error);
      // Keep default values if fetch fails
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
    navigate('/');
  };

  if (!user || loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Welcome Header */}
      <section className="dashboard-header">
        <div className="welcome-content">
          <div className="welcome-text">
            <h1>Welcome back, <span className="username-highlight">{user. name}!</span></h1>
            <p>Ready to make data-driven predictions for bike-sharing demand? </p>
          </div>
          <button onClick={handleLogout} className="logout-btn">
            <span>Logout</span>
            <span className="logout-icon">🚪</span>
          </button>
        </div>
      </section>

      {/* Quick Access Cards */}
      <section className="quick-actions-section">
        <h2 className="section-title">Quick Actions</h2>
        <div className="quick-actions-grid">
          <button onClick={() => navigate('/predict')} className="action-card predict-card">
            <div className="action-icon">🔮</div>
            <h3>Predict Demand</h3>
            <p>Make new bike demand predictions</p>
            <div className="action-arrow">→</div>
          </button>
          <button onClick={() => navigate('/stations')} className="action-card stations-card">
            <div className="action-icon">🗺️</div>
            <h3>Bike Stations</h3>
            <p>Explore station map</p>
            <div className="action-arrow">→</div>
          </button>

          <button onClick={() => navigate('/feedback')} className="action-card feedback-card">
            <div className="action-icon">💬</div>
            <h3>Feedback</h3>
            <p>Share your thoughts</p>
            <div className="action-arrow">→</div>
          </button>
        </div>
      </section>

      {/* Stats Section - Now Dynamic!  */}
      <section className="stats-section">
        <h2 className="section-title">Your Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3>Total Predictions</h3>
              <p className="stat-number">{stats.total_predictions}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-content">
              <h3>Accuracy Rate</h3>
              <p className="stat-number">{stats.accuracy_rate}%</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🕒</div>
            <div className="stat-content">
              <h3>Last Prediction</h3>
              <p className="stat-number">{stats.last_prediction}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⭐</div>
            <div className="stat-content">
              <h3>Feedback Given</h3>
              <p className="stat-number">{stats.feedback_count}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Activity */}
      <section className="recent-activity-section">
        <h2 className="section-title">Recent Activity</h2>
        <div className="activity-card">
          {stats.total_predictions === 0 ? (
            <>
              <p className="no-activity">No recent activity yet.  Start by making your first prediction!</p>
              <button onClick={() => navigate('/predict')} className="start-prediction-btn">
                Make Your First Prediction
              </button>
            </>
          ) : (
            <>
              <div className="activity-summary">
                <p className="activity-text">
                  🎉 You've made <strong>{stats.total_predictions}</strong> prediction{stats.total_predictions > 1 ? 's' : ''} so far!
                </p>
                <div className="activity-breakdown">
                  <span className="activity-badge">📅 Daily: {stats.daily_predictions}</span>
                  <span className="activity-badge">⏰ Hourly: {stats.hourly_predictions}</span>
                </div>
              </div>
              <button onClick={() => navigate('/predict')} className="start-prediction-btn">
                Make Another Prediction
              </button>
            </>
          )}
        </div>
      </section>

      {/* Chatbot */}
      <Chatbot />
    </div>
  );
};

export default Dashboard;