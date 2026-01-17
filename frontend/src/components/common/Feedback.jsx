import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../../services/api';
import '../../styles/Feedback.css';

const Feedback = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    rating: 5,
    category: 'general',
    feedback: '',
    email: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target. name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.feedback. trim()) {
      toast.error('Please provide your feedback');
      return;
    }

    setLoading(true);

    try {
      await api.post('/feedback', formData);
      toast.success('Thank you for your feedback! ');
      setFormData({
        rating: 5,
        category: 'general',
        feedback: '',
        email:  ''
      });

      // Redirect back to dashboard after 2 seconds
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (error) {
      console.error('Feedback error:', error);
      toast.error('Failed to submit feedback.  Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feedback-container">
      <div className="feedback-card">
        <button
          className="back-btn"
          onClick={() => navigate('/dashboard')}
        >
          ← Back to Dashboard
        </button>

        <div className="feedback-header">
          <h1>💬 We Value Your Feedback</h1>
          <p>Help us improve RideWise by sharing your thoughts</p>
        </div>

        <form onSubmit={handleSubmit} className="feedback-form">
          {/* Rating */}
          <div className="form-group">
            <label htmlFor="rating">How would you rate your experience?</label>
            <div className="rating-stars">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  className={`star ${formData.rating >= star ? 'active' : ''}`}
                  onClick={() => setFormData({ ...formData, rating: star })}
                >
                  ★
                </button>
              ))}
            </div>
            <p className="rating-text">
              {formData.rating === 5 && 'Excellent! 🎉'}
              {formData. rating === 4 && 'Great! 😊'}
              {formData. rating === 3 && 'Good 👍'}
              {formData.rating === 2 && 'Needs Improvement 😐'}
              {formData.rating === 1 && 'Poor 😞'}
            </p>
          </div>

          {/* Category */}
          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              name="category"
              value={formData. category}
              onChange={handleChange}
              className="form-select"
            >
              <option value="general">General Feedback</option>
              <option value="prediction">Prediction Accuracy</option>
              <option value="ui">User Interface</option>
              <option value="features">Feature Request</option>
              <option value="bug">Bug Report</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Feedback Text */}
          <div className="form-group">
            <label htmlFor="feedback">Your Feedback *</label>
            <textarea
              id="feedback"
              name="feedback"
              value={formData.feedback}
              onChange={handleChange}
              required
              rows="6"
              placeholder="Tell us what you think..."
              className="form-textarea"
            />
          </div>

          {/* Email (Optional) */}
          <div className="form-group">
            <label htmlFor="email">Email (Optional)</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your.email@example.com"
              className="form-input"
            />
            <small>We'll only use this if we need to follow up</small>
          </div>

          <button
            type="submit"
            className="btn btn-primary submit-btn"
            disabled={loading}
          >
            {loading ? 'Submitting...' : 'Submit Feedback'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Feedback;