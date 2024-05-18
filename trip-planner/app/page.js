'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './page.module.css';

export default function Home() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [vacationType, setVacationType] = useState('');
  const [tripOptions, setTripOptions] = useState([]);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [loading, setLoading] = useState(false);
  const [minStartDate, setMinStartDate] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [isMuted, setIsMuted] = useState(true);

  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    setMinStartDate(today);
  }, []);

  useEffect(() => {
    if (hasInteracted) {
      const landingMusic = document.getElementById('landing-music');
      const loadingMusic = document.getElementById('loading-music');

      if (loading) {
        landingMusic.pause();
        loadingMusic.play().catch(error => console.error('Failed to play loading music:', error));
      } else {
        loadingMusic.pause();
        if (!selectedTrip) {
          landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
        }
      }
    }
  }, [loading, selectedTrip, hasInteracted]);

  const handleStart = () => {
    setHasInteracted(true);
    setShowForm(true);
    const landingMusic = document.getElementById('landing-music');
    landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/plan_trip', {
        vacation_type: vacationType,
        start_date: startDate,
        end_date: endDate,
        budget: parseFloat(budget),
      });
      setTripOptions(response.data);
      setLoading(false);
      setShowForm(false); // Hide form after receiving trip options
    } catch (error) {
      console.error('Error planning trip:', error);
      setLoading(false);
    }
  };

  const handleSelectTrip = async (index) => {
    setLoading(true);
    try {
      console.log(`Sending choice: ${index + 1}`);
      const response = await axios.post('http://localhost:8000/choose_trip', {
        choice: index + 1,
      });
      console.log('Response received:', response.data);
      setSelectedTrip(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error selecting trip:', error);
      console.error('Error details:', error.response?.data || error.message);
      setLoading(false);
    }
  };

  const toggleMute = () => {
    const landingMusic = document.getElementById('landing-music');
    const loadingMusic = document.getElementById('loading-music');
    if (isMuted) {
      landingMusic.muted = false;
      loadingMusic.muted = false;
      landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
    } else {
      landingMusic.muted = true;
      loadingMusic.muted = true;
    }
    setIsMuted(!isMuted);
  };

  return (
    <main className={styles.mainContent}>
      <audio id="landing-music" src="/music/landing.mp3" loop muted />
      <audio id="loading-music" src="/music/loading.mp3" loop muted />

      <div className={styles.muteIcon} onClick={toggleMute}>
        {isMuted ? '🔇' : '🔊'}
      </div>

      {loading ? (
        <div className={styles.loadingContainer}>
          <video autoPlay loop muted className={styles.loadingVideo}>
            <source src={`/videos/${vacationType}.mp4`} type="video/mp4" />
          </video>
          <div className={styles.loadingText}>
            Loading your perfect trip<span className={styles.loadingDots}>
              <span className={styles.dot}>.</span>
              <span className={styles.dot}>.</span>
              <span className={styles.dot}>.</span>
            </span>
          </div>
        </div>
      ) : !hasInteracted ? (
        <div className={styles.landing}>
          <div className={styles.background}>
            <div className={styles.backgroundImage}></div>
          </div>
          <div className={styles.welcome}>
            <h1>Welcome to Trip Planner</h1>
            <button className={styles.button} onClick={handleStart}>Start</button>
          </div>
        </div>
      ) : showForm ? (
        <div className={styles.formContainer}>
          <div className={styles.background}>
            <div className={styles.backgroundImage}></div>
          </div>
          <h2 className={styles.formTitle}>Let's start finding your vacation!</h2>
          <form className={styles.form} onSubmit={handleSubmit}>
            <div className={styles.horizontalForm}>
              <div className={styles.formGroup}>
                <label className={styles.label}>Start Date:</label>
                <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required className={styles.input} min={minStartDate} />
              </div>
              <div className={styles.formGroup}>
                <label className={styles.label}>End Date:</label>
                <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required className={styles.input} min={startDate} />
              </div>
              <div className={styles.formGroup}>
                <label className={styles.label}>Budget (USD):</label>
                <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} required className={styles.input} />
              </div>
              <div className={styles.formGroup}>
                <label className={styles.label}>Vacation Type:</label>
                <select value={vacationType} onChange={(e) => setVacationType(e.target.value)} required className={styles.select}>
                  <option value="">Select Vacation Type</option>
                  <option value="ski">Ski</option>
                  <option value="beach">Beach</option>
                  <option value="city">City</option>
                </select>
              </div>
              <button className={styles.button} type="submit">Search Trips</button>
            </div>
          </form>
        </div>
      ) : tripOptions.length > 0 && !selectedTrip ? (
        <div className={styles.container}>
          <h1 className={styles.title}>Trip Options</h1>
          <ul className={styles.list}>
            {tripOptions.map((option, index) => (
              <li key={index} className={styles.listItem}>
                <button className={styles.link} onClick={() => handleSelectTrip(index)}>
                  {option.destination} - ${option.total_price}
                </button>
              </li>
            ))}
          </ul>
        </div>
      ) : selectedTrip ? (
        <div className={styles.container}>
          <h1 className={styles.title}>Trip Details</h1>
          <p className={styles.detail}>Destination: {selectedTrip.destination}</p>
          <p className={styles.detail}>Total Cost: ${selectedTrip.total_price}</p>
          <p className={styles.detail}>Flight: {selectedTrip.flight.airline} at ${selectedTrip.flight.price}</p>
          <p className={styles.detail}>Hotel: {selectedTrip.hotel.name} at ${selectedTrip.hotel.price} per night</p>
          <h2 className={styles.subtitle}>Daily Plan</h2>
          <ul className={styles.list}>
            {selectedTrip.daily_plan.split('\n').map((item, index) => (
              <li key={index} className={styles.listItem}>{item}</li>
            ))}
          </ul>
          <h2 className={styles.subtitle}>Images</h2>
          <div className={styles.imageContainer}>
            {selectedTrip.image_urls.map((url, index) => (
              <img key={index} src={url} alt={`Trip image ${index + 1}`} className={styles.image} />
            ))}
          </div>
          <button className={styles.button} onClick={() => { setSelectedTrip(null); setShowForm(false); }}>Back to Options</button>
        </div>
      ) : null}
    </main>
  );
}
