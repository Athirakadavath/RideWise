import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './styles/Home.css';

const Home = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    // Redirect to dashboard if already logged in and trying to access home
    if (token) {
      navigate('/dashboard');
      return;
    }

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver(
      (entries) => {
        entries. forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      },
      { threshold: 0.1 }
    );

    // Fixed:  Removed space before 'animate-on-scroll'
    document.querySelectorAll('.animate-on-scroll').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, [token, navigate]);

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
        </div>
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-icon">⚡</span>
            <span>95% Prediction Accuracy</span>
          </div>
          <h1 className="hero-title">
            <span className="gradient-text">🚴 Welcome to RideWise</span>
          </h1>
          <p className="hero-description">
            Predicting Bike-Sharing Demand Based on Weather and Urban Events.
            Make data-driven decisions with our advanced ML-powered prediction system.
          </p>
          <div className="hero-buttons">
            <Link to="/signup" className="hero-btn hero-btn-primary pulse">
              <span>Get Started</span>
              <span className="btn-arrow">→</span>
            </Link>
            <Link to="/login" className="hero-btn hero-btn-secondary">
              <span>Login</span>
              <span className="btn-icon">🔑</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section animate-on-scroll">
        <div className="features-content">
          <div className="features-header">
            <h2 className="section-title">Why Choose RideWise?</h2>
            <p className="section-subtitle">Powerful features for intelligent bike-sharing demand forecasting</p>
          </div>
          <div className="features-grid">
            {[
              {
                icon:  '🤖',
                title: 'ML-Powered Predictions',
                description: 'Advanced XGBoost regression model with 95% accuracy for reliable demand forecasting.',
                delay: '0s'
              },
              {
                icon: '🌦️',
                title: 'Weather Integration',
                description: 'Real-time weather data integration to predict how conditions affect bike-sharing demand.',
                delay: '0.1s'
              },
              {
                icon: '🎉',
                title: 'Urban Events Analysis',
                description: 'Factor in city events, holidays, and activities to forecast demand surges accurately.',
                delay: '0.2s'
              },
              {
                icon: '📊',
                title: 'Interactive Analytics',
                description: 'Visualize demand patterns, trends, and feature importance with comprehensive dashboards.',
                delay: '0.3s'
              },
              {
                icon: '🗺️',
                title: 'Station Insights',
                description: 'View bike stations on an interactive map with predicted demand for optimal fleet management.',
                delay: '0.4s'
              },
              {
                icon: '💬',
                title: 'AI Chatbot Support',
                description: 'Get instant help and insights about predictions and system features through our AI assistant.',
                delay: '0.5s'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="feature-card"
                style={{ animationDelay: feature.delay }}
              >
                <div className="feature-icon-wrapper">
                  <div className="feature-icon">{feature.icon}</div>
                  <div className="icon-glow"></div>
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
                <div className="card-shine"></div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section animate-on-scroll">
        <div className="how-it-works-content">
          <div className="how-it-works-header">
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Get started in four simple steps</p>
          </div>
          <div className="steps-grid">
            {[
              { number: 1, title: 'Sign Up', description: 'Create your account to access the prediction system. ', delay: '0s' },
              { number: 2, title:  'Input Parameters', description: 'Enter date, weather conditions, and event details for prediction.', delay: '0.15s' },
              { number:  3, title: 'Get Predictions', description: 'Receive accurate bike demand forecasts powered by our ML model.', delay: '0.3s' },
              { number:  4, title: 'Analyze & Optimize', description: 'Use insights to optimize fleet distribution and operations.', delay: '0.45s' }
            ].map((step) => (
              <div
                key={step.number}
                className="step-card"
                style={{ animationDelay:  step.delay }}
              >
                <div className="step-number-wrapper">
                  <div className="step-number">{step. number}</div>
                  <div className="step-connector"></div>
                </div>
                <h3>{step. title}</h3>
                <p>{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="features-section use-cases-section animate-on-scroll">
        <div className="features-content">
          <div className="features-header">
            <h2 className="section-title">Key Use Cases</h2>
            <p className="section-subtitle">Empowering urban planning and transit operations</p>
          </div>
          <div className="features-grid use-cases-grid">
            {[
              {
                icon: '🚲',
                title: 'Demand Forecasting',
                description:  'Predict daily and hourly bike rental counts to support fleet management and station stocking decisions.',
                delay: '0s'
              },
              {
                icon: '📈',
                title: 'Feature Impact Analysis',
                description: 'Understand how weather, events, and location characteristics influence ridership patterns.',
                delay: '0.15s'
              },
              {
                icon: '🔄',
                title: 'Fleet Rebalancing',
                description: 'Anticipate demand surges during events or weather changes for optimal bike distribution.',
                delay: '0.3s'
              }
            ].map((useCase, index) => (
              <div
                key={index}
                className="feature-card use-case-card"
                style={{ animationDelay: useCase.delay }}
              >
                <div className="feature-icon-wrapper">
                  <div className="feature-icon">{useCase.icon}</div>
                  <div className="icon-glow"></div>
                </div>
                <h3>{useCase.title}</h3>
                <p>{useCase.description}</p>
                <div className="card-shine"></div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section animate-on-scroll">
        <div className="cta-background">
          <div className="cta-gradient-orb"></div>
        </div>
        <div className="cta-content">
          <h2 className="cta-title">Ready to Optimize Your Bike-Sharing System?</h2>
          <p className="cta-description">
            Join urban planners and transit operators using RideWise for
            data-driven decision making.
          </p>
          <div className="hero-buttons">
            <Link to="/signup" className="hero-btn hero-btn-primary cta-btn pulse">
              <span>Sign Up Now</span>
              <span className="btn-arrow">→</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;