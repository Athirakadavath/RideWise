import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import api from '../../services/api';
import { toast } from 'react-toastify';
import '../../styles/Analytics.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Analytics = () => {
  const navigate = useNavigate();

  const [predictions, setPredictions] = useState([]);
  const [weatherImpact, setWeatherImpact] = useState([]);
  const [hourlyPatterns, setHourlyPatterns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      /* ---------------- PREDICTION HISTORY (REQUIRED) ---------------- */
      const historyRes = await api.get('/predictions/history');

      const rawPredictions = historyRes.data?.predictions || [];

      // 🔥 Normalize backend fields
      const normalized = rawPredictions.map(p => ({
        createdAt: p.createdAt || p.created_at,
        value: p.value ?? p.prediction_value ?? 0,
        type: p.type || p.prediction_type || 'unknown'
      }));

      setPredictions(normalized);

      /* ---------------- WEATHER IMPACT (OPTIONAL) ---------------- */
      try {
        const weatherRes = await api.get('/analytics/weather-impact');
        setWeatherImpact(weatherRes.data?.weather_impact || []);
      } catch {
        setWeatherImpact([]);
      }

      /* ---------------- HOURLY PATTERNS (OPTIONAL) ---------------- */
      try {
        const hourlyRes = await api.get('/analytics/hourly-patterns');
        setHourlyPatterns(hourlyRes.data?.hourly_patterns || []);
      } catch {
        setHourlyPatterns([]);
      }

    } catch (error) {
      console.error('Analytics error:', error);
      toast.error('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  /* ---------------- CHART DATA ---------------- */

  const trendData = {
    labels: predictions.slice(-7).map(p =>
      p.createdAt ? new Date(p.createdAt).toLocaleDateString() : 'N/A'
    ),
    datasets: [
      {
        label: 'Predicted Rentals',
        data: predictions.slice(-7).map(p => p.value),
        borderColor: 'rgb(102, 126, 234)',
        backgroundColor: 'rgba(102, 126, 234, 0.15)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const weatherData = {
    labels: weatherImpact.map(w => w.weather),
    datasets: [
      {
        label: 'Average Rentals',
        data: weatherImpact.map(w => w.avg_prediction),
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(255, 159, 64, 0.8)',
          'rgba(255, 99, 132, 0.8)'
        ],
      },
    ],
  };

  const hourlyData = {
    labels: hourlyPatterns.map(h => `${h.hour}:00`),
    datasets: [
      {
        label: 'Average Rentals by Hour',
        data: hourlyPatterns.map(h => h.avg_prediction),
        backgroundColor: 'rgba(118, 75, 162, 0.8)',
      },
    ],
  };

  const stats = {
    total: predictions.length,
    daily: predictions.filter(p => p.type === 'daily').length,
    hourly: predictions.filter(p => p.type === 'hourly').length,
    avg:
      predictions.length > 0
        ? Math.round(
            predictions.reduce((sum, p) => sum + p.value, 0) /
              predictions.length
          )
        : 0,
  };

  /* ---------------- UI STATES ---------------- */

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (predictions.length === 0) {
    return (
      <div className="analytics-page">
        <div className="page-header">
          <button className="back-btn" onClick={() => navigate('/dashboard')}>
            ← Back to Dashboard
          </button>
          <h1>📊 Prediction Analytics</h1>
          <p>No data available</p>
        </div>

        <div className="empty-state">
          <h3>No Predictions Found</h3>
          <button className="btn-primary" onClick={() => navigate('/predict')}>
            Make a Prediction
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-page">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate('/dashboard')}>
          ← Back to Dashboard
        </button>
        <h1>📊 Prediction Analytics</h1>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">Total: {stats.total}</div>
        <div className="stat-card">Daily: {stats.daily}</div>
        <div className="stat-card">Hourly: {stats.hourly}</div>
        <div className="stat-card">Avg: {stats.avg}</div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-card">
          <Line data={trendData} options={{ responsive: true }} />
        </div>

        {weatherImpact.length > 0 && (
          <div className="chart-card">
            <Doughnut data={weatherData} />
          </div>
        )}

        {hourlyPatterns.length > 0 && (
          <div className="chart-card full-width">
            <Bar data={hourlyData} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Analytics;
