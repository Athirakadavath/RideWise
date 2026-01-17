import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Home from './Home';
import Login from './components/auth/Login';
import Signup from './components/auth/Signup';
import Predict from './components/prediction/Predict';
import Dashboard from './components/Dashboard/dashboard';  // ✅ Capital D folder, lowercase d file
import Analytics from './components/analytics/Analytics';
import BikeStations from './components/stations/Bikestations';
import Feedback from './components/common/Feedback';
import PrivateRoute from './components/common/PrivateRoute';

function App() {
  return (
    <Router>
      <ToastContainer position="top-right" autoClose={3000} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected Routes */}
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />

        <Route path="/predict" element={
          <PrivateRoute>
            <Predict />
          </PrivateRoute>
        } />

        <Route path="/analytics" element={
          <PrivateRoute>
            <Analytics />
          </PrivateRoute>
        } />

        <Route path="/stations" element={
          <PrivateRoute>
            <BikeStations />
          </PrivateRoute>
        } />

        <Route path="/feedback" element={
          <PrivateRoute>
            <Feedback />
          </PrivateRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;

