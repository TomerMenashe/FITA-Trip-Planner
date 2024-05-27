'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './page.module.css';

export default function Home() {
  // State variables
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

  // Set minimum start date to today's date
  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    setMinStartDate(today);
  }, []);

  // Handle music playback based on user interaction and loading state
  useEffect(() => {
    const landingMusic = document.getElementById('landing-music');
    const loadingMusic = document.getElementById('loading-music');

    if (hasInteracted) {
      if (loading) {
        landingMusic.pause();
        loadingMusic.play().catch(error => console.error('Failed to play loading music:', error));
      } else {
        loadingMusic.pause();
        landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
      }
    } else {
      landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
    }
  }, [loading, selectedTrip, hasInteracted]);

  // Handle start button click
  const handleStart = () => {
    setHasInteracted(true);
    setShowForm(true);
    const landingMusic = document.getElementById('landing-music');
    landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
  };

  // Handle form submission
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

  // Handle selecting a trip option
  const handleSelectTrip = async (index) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/choose_trip', {
        choice: index + 1,
      });
      setSelectedTrip(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error selecting trip:', error);
      setLoading(false);
    }
  };

  // Handle new search button click
  const handleNewSearch = () => {
    setSelectedTrip(null);
    setTripOptions([]);
    setShowForm(true);
    const landingMusic = document.getElementById('landing-music');
    landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
  };

  // Handle back to options button click
  const handleBackToOptions = () => {
    setSelectedTrip(null);
    const landingMusic = document.getElementById('landing-music');
    landingMusic.play().catch(error => console.error('Failed to play landing music:', error));
  };

  // Toggle mute for music
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
            {selectedTrip ? `Getting your vacation to ${selectedTrip.destination} ready...` : 'Loading your perfect trip'}
            <span className={styles.loadingDots}>
              <span className={styles.dot}>.</span>
              <span className={styles.dot}>.</span>
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
          <div className={styles.background}>
            <div className={styles.backgroundImage}></div>
          </div>
          <h1 className={styles.title}>Trip Options</h1>
          <ul className={styles.list}>
            {tripOptions.map((option, index) => (
              <li key={index} className={styles.listItem}>
                <button className={styles.link} onClick={() => handleSelectTrip(index)}>
                  <div className={styles.tripOptionDestination}>{option.destination}</div>
                  <div className={styles.tripOptionPrice}>${option.total_price}</div>
                  <div className={styles.tripOptionDetails}>
                    <p><strong>Flight:</strong> {option.flight.airline} at ${option.flight.price}</p>
                    <p><strong>Hotel:</strong> {option.hotel.name} at ${option.hotel.price} per night</p>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </div>
      ) : tripOptions.length === 0 && !selectedTrip ? (
        <div className={styles.container}>
          <div className={styles.background}>
            <div className={styles.backgroundImage}></div>
          </div>
          <h1 className={styles.title}>No Trip Options Found</h1>
          <p className={styles.detail}>No suitable trip options found within the given budget.</p>
          <button className={styles.button} onClick={handleNewSearch}>New Search</button>
        </div>
      ) : selectedTrip ? (
        <div className={styles.container}>
          <div className={styles.background}>
            <div className={styles.backgroundImage}></div>
          </div>
          <h1 className={styles.title}>Trip Details</h1>
          <p className={styles.detail}><strong>Destination:</strong> {selectedTrip.destination}</p>
          <p className={styles.detail}><strong>Total Cost:</strong> ${selectedTrip.total_price}</p>
          <p className={styles.detail}><strong>Flight:</strong> {selectedTrip.flight.airline} at ${selectedTrip.flight.price}</p>
          <p className={styles.detail}><strong>Hotel:</strong> {selectedTrip.hotel.name} at ${selectedTrip.hotel.price} per stay</p>
          <h2 className={styles.subtitle}>Daily Plan</h2>
          <ul className={styles.dailyPlanList}>
            {selectedTrip.daily_plan.split('\n').map((item, index) => (
              <li key={index} className={styles.dailyPlanItem}>{item}</li>
            ))}
          </ul>
          <h2 className={styles.subtitle}>Images</h2>
          <div className={styles.imageContainer}>
            {selectedTrip.image_urls.map((url, index) => (
              <img key={index} src={url} alt={`Trip image ${index + 1}`} className={styles.image} />
            ))}
          </div>
          <div className={styles.buttonContainer}>
            <button className={styles.button} onClick={handleBackToOptions}>Back to Options</button>
            <button className={styles.button} onClick={handleNewSearch}>New Search</button>
          </div>
        </div>
      ) : null}
    </main>
  );
}
