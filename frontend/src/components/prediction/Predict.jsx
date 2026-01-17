import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { toast } from 'react-toastify';
import '../../styles/Predict.css';

const Predict = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState('select');
  const [predictionType, setPredictionType] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);

  const today = new Date().toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    date: today,
    weathersit: '1',
    temp: '0.7',
    hum: '0.6',
    windspeed: '0.2',
    workingday: '1',
    holiday: '0',
    hr: '12',
  });

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleTypeSelection = (type) => {
    setPredictionType(type);
    setStep('form');
  };

  const handlePDFSelection = () => {
    setStep('pdf');
  };

  const handleBackToSelection = () => {
    setStep('select');
    setPredictionType(null);
    setPdfFile(null);
    setResult(null);
  };

  const getSeasonFromMonth = (month) => {
    if (month >= 3 && month <= 5) return 2;
    if (month >= 6 && month <= 8) return 3;
    if (month >= 9 && month <= 11) return 4;
    return 1;
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const dateObj = new Date(formData.date);
      const year = dateObj.getFullYear();
      const month = dateObj.getMonth() + 1;
      const weekday = dateObj.getDay();
      const season = getSeasonFromMonth(month);
      const yr = year >= 2012 ? 1 : 0;

      const tempValue = parseFloat(formData.temp);

      const predictionData = {
        date: formData.date,
        season: season,
        yr: yr,
        mnth: month,
        weekday:  weekday,
        holiday: parseInt(formData.holiday),
        workingday: parseInt(formData.workingday),
        weathersit: parseInt(formData. weathersit),
        temp: tempValue,
        atemp: tempValue,  // ✅ Set atemp equal to temp
        hum: parseFloat(formData.hum),
        windspeed: parseFloat(formData. windspeed),
      };

      if (predictionType === 'hourly') {
        predictionData.hr = parseInt(formData.hr);
      }

      const endpoint = predictionType === 'daily' ? '/predictions/daily' :  '/predictions/hourly';
      const { data } = await api. post(endpoint, predictionData);

      setResult(data);
      toast.success('Prediction successful! ');
    } catch (error) {
      console.error('Prediction error:', error);
      toast.error(error.response?.data?.error || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFileInputChange = (e) => {
    const file = e. target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      toast.success(`${file.name} selected`);
    } else {
      toast.error('Please select a valid PDF file');
    }
  };

  const handlePDFSubmit = async (e) => {
    e.preventDefault();

    if (!pdfFile) {
      toast.error('Please select a PDF file');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const formDataObj = new FormData();
      formDataObj.append('file', pdfFile);
      formDataObj.append('type', predictionType || 'daily');

      const { data } = await api.post('/predictions/upload-pdf', formDataObj, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult(data);
      toast.success('PDF processed successfully! ');
    } catch (error) {
      console.error('PDF upload error:', error);
      toast.error(error.response?.data?.error || 'PDF processing failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="predict-page">
      {/* Header */}
      <div className="page-header">
        <div className="container">
          <button className="back-btn" onClick={() => navigate('/dashboard')}>
            ← Back to Dashboard
          </button>
          <h1>Bike Demand Prediction</h1>
          <p>Make accurate predictions using our AI-powered model</p>
        </div>
      </div>

      <div className="container">
        {/* Step 1: Selection Screen */}
        {step === 'select' && (
          <div className="selection-section">
            <h2>Choose Prediction Method</h2>
            <div className="method-cards">
              <div className="method-card" onClick={() => handleTypeSelection('daily')}>
                <div className="method-icon">📅</div>
                <h3>Daily Forecast</h3>
                <p>Predict total daily bike demand</p>
                <button className="method-btn">Select</button>
              </div>

              <div className="method-card" onClick={() => handleTypeSelection('hourly')}>
                <div className="method-icon">⏰</div>
                <h3>Hourly Forecast</h3>
                <p>Predict demand by specific hour</p>
                <button className="method-btn">Select</button>
              </div>

              <div className="method-card" onClick={handlePDFSelection}>
                <div className="method-icon">📄</div>
                <h3>Upload PDF</h3>
                <p>Extract data from document</p>
                <button className="method-btn">Select</button>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Manual Form */}
        {step === 'form' && predictionType && (
          <div className="form-section">
            <div className="section-header">
              <button className="text-btn" onClick={handleBackToSelection}>
                ← Change Method
              </button>
              <h2>{predictionType === 'daily' ? '📅 Daily' : '⏰ Hourly'} Prediction</h2>
            </div>

            <form onSubmit={handleFormSubmit} className="prediction-form">
              {/* Date & Time */}
              <div className="form-card">
                <h3>Date & Time Information</h3>
                <div className="form-grid">
                  <div className="form-group full-width">
                    <label>Select Date *</label>
                    <input
                      type="date"
                      name="date"
                      value={formData. date}
                      onChange={handleInputChange}
                      required
                      className="form-input"
                    />
                  </div>

                  <div className="form-group">
                    <label>Working Day</label>
                    <select
                      name="workingday"
                      value={formData.workingday}
                      onChange={handleInputChange}
                      className="form-input"
                    >
                      <option value="1">Yes</option>
                      <option value="0">No</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Holiday</label>
                    <select
                      name="holiday"
                      value={formData.holiday}
                      onChange={handleInputChange}
                      className="form-input"
                    >
                      <option value="0">No</option>
                      <option value="1">Yes</option>
                    </select>
                  </div>

                  {predictionType === 'hourly' && (
                    <div className="form-group">
                      <label>Hour (0-23) *</label>
                      <input
                        type="number"
                        name="hr"
                        value={formData.hr}
                        onChange={handleInputChange}
                        min="0"
                        max="23"
                        required
                        className="form-input"
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* Weather Conditions */}
              <div className="form-card">
                <h3>Weather Conditions</h3>
                <div className="form-grid">
                  <div className="form-group full-width">
                    <label>Weather Situation *</label>
                    <select
                      name="weathersit"
                      value={formData.weathersit}
                      onChange={handleInputChange}
                      className="form-input"
                    >
                      <option value="1">☀️ Clear / Partly Cloudy</option>
                      <option value="2">🌥️ Mist / Cloudy</option>
                      <option value="3">🌧️ Light Snow / Rain</option>
                      <option value="4">⛈️ Heavy Rain / Snow</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Temperature:  {(parseFloat(formData.temp) * 100).toFixed(0)}%</label>
                    <input
                      type="range"
                      name="temp"
                      value={formData. temp}
                      onChange={handleInputChange}
                      min="0"
                      max="1"
                      step="0.01"
                      className="form-range"
                    />
                  </div>

                  {/* ✅ Removed "Feels Like" input - atemp will equal temp */}

                  <div className="form-group">
                    <label>Humidity: {(parseFloat(formData.hum) * 100).toFixed(0)}%</label>
                    <input
                      type="range"
                      name="hum"
                      value={formData.hum}
                      onChange={handleInputChange}
                      min="0"
                      max="1"
                      step="0.01"
                      className="form-range"
                    />
                  </div>

                  <div className="form-group">
                    <label>Wind Speed: {(parseFloat(formData.windspeed) * 100).toFixed(0)}%</label>
                    <input
                      type="range"
                      name="windspeed"
                      value={formData. windspeed}
                      onChange={handleInputChange}
                      min="0"
                      max="1"
                      step="0.01"
                      className="form-range"
                    />
                  </div>
                </div>
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? 'Generating...' : 'Generate Prediction'}
              </button>
            </form>
          </div>
        )}

        {/* Step 3: PDF Upload */}
        {step === 'pdf' && (
          <div className="pdf-section">
            <div className="section-header">
              <button className="text-btn" onClick={handleBackToSelection}>
                ← Change Method
              </button>
              <h2>📄 Upload PDF Document</h2>
            </div>

            <form onSubmit={handlePDFSubmit}>
              <div className="pdf-upload-area">
                <div className="upload-box">
                  <input
                    type="file"
                    id="pdf-input"
                    accept=".pdf"
                    onChange={handleFileInputChange}
                    className="file-input"
                  />
                  <label htmlFor="pdf-input" className="upload-label">
                    {pdfFile ? (
                      <div className="file-selected">
                        <span className="file-icon">📄</span>
                        <div>
                          <p className="file-name">{pdfFile.name}</p>
                          <p className="file-size">{(pdfFile.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                      </div>
                    ) : (
                      <div className="upload-prompt">
                        <span className="upload-icon">📤</span>
                        <p>Click to select PDF file</p>
                        <span className="upload-hint">or drag and drop here</span>
                      </div>
                    )}
                  </label>
                </div>

                <div className="pdf-info">
                  <h4>Required Data</h4>
                  <ul>
                    <li>Date (YYYY-MM-DD format)</li>
                    <li>Weather situation (1-4)</li>
                    <li>Temperature, humidity, wind speed (0-1)</li>
                    <li>Working day and holiday status</li>
                    <li>Hour (0-23) for hourly predictions</li>
                  </ul>
                </div>

                <div className="pdf-type-select">
                  <label>Prediction Type:  </label>
                  <div className="radio-group">
                    <label className="radio-label">
                      <input
                        type="radio"
                        name="pdfType"
                        value="daily"
                        checked={predictionType === 'daily'}
                        onChange={() => setPredictionType('daily')}
                      />
                      <span>Daily</span>
                    </label>
                    <label className="radio-label">
                      <input
                        type="radio"
                        name="pdfType"
                        value="hourly"
                        checked={predictionType === 'hourly'}
                        onChange={() => setPredictionType('hourly')}
                      />
                      <span>Hourly</span>
                    </label>
                  </div>
                </div>
              </div>

              <button
                type="submit"
                className="submit-btn"
                disabled={loading || !pdfFile || ! predictionType}
              >
                {loading ? 'Processing.. .' : 'Upload & Predict'}
              </button>
            </form>
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="result-section">
            <div className="result-card">
              <div className="result-header">
                <h3>✅ Prediction Result</h3>
                <button className="close-btn" onClick={() => { setResult(null); handleBackToSelection(); }}>
                  ✕
                </button>
              </div>

              <div className="result-body">
                <div className="result-main">
                  <div className="result-number">{Math.round(result.prediction)}</div>
                  <div className="result-label">Bikes Expected</div>
                  <div className="result-type">
                    {result.type === 'daily' ? '📅 Daily Forecast' : '⏰ Hourly Forecast'}
                  </div>
                </div>

                <div className="result-details">
                  <div className="detail-item">
                    <span className="detail-label">Date:</span>
                    <span className="detail-value">
                      {new Date(formData.date).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </span>
                  </div>
                  {result.type === 'hourly' && (
                    <div className="detail-item">
                      <span className="detail-label">Time:</span>
                      <span className="detail-value">{formData.hr}: 00</span>
                    </div>
                  )}
                </div>

                <div className="result-actions">
                  <button className="btn-secondary" onClick={() => { setResult(null); handleBackToSelection(); }}>
                    New Prediction
                  </button>
                  <button className="btn-primary" onClick={() => navigate('/analytics')}>
                    View Analytics
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Predict;