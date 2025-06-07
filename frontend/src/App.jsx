// App.jsx
import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [thumbnails, setThumbnails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: ''
  });
  const [stats, setStats] = useState({
    totalGenerated: 0,
    avgGenerationTime: 2.3
  });

  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    // Load saved thumbnails from localStorage on component mount
    const savedThumbnails = localStorage.getItem('thumbnails');
    if (savedThumbnails) {
      setThumbnails(JSON.parse(savedThumbnails));
    }
  }, []);

  const saveThumbnailsToStorage = (newThumbnails) => {
    localStorage.setItem('thumbnails', JSON.stringify(newThumbnails));
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const generateThumbnail = async () => {
    if (!formData.title.trim()) {
      alert('Please enter a video title');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/generate-thumbnail`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description || ''
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const newThumbnail = {
          id: Date.now(),
          title: formData.title,
          imageUrl: data.image_url,
          downloadUrl: data.download_url,
          thumbnailUrl: data.thumbnail_url,
          generationTime: data.generation_time,
          createdAt: new Date().toISOString()
        };

        const updatedThumbnails = [newThumbnail, ...thumbnails];
        setThumbnails(updatedThumbnails);
        saveThumbnailsToStorage(updatedThumbnails);
        
        setStats(prev => ({
          totalGenerated: prev.totalGenerated + 1,
          avgGenerationTime: data.generation_time
        }));

        // Clear form
        setFormData({ title: '', description: '' });
      } else {
        alert('Failed to generate thumbnail. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating thumbnail. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const downloadThumbnail = (thumbnail) => {
    const link = document.createElement('a');
    link.href = thumbnail.downloadUrl || thumbnail.imageUrl;
    link.download = `${thumbnail.title.substring(0, 50)}-thumbnail.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all thumbnails?')) {
      setThumbnails([]);
      localStorage.removeItem('thumbnails');
    }
  };

  const HomePage = () => (
    <div className="home-page">
      <header className="hero-section">
        <div className="hero-content">
          <div className="logo-container">
            <div className="logo">🎬</div>
            <h1 className="brand-title">ThumbNailer</h1>
            <p className="brand-subtitle">Secret of Viral Videos</p>
          </div>
          
          <h2 className="hero-title">
            Create <span className="highlight">Viral</span> YouTube Thumbnails with AI
          </h2>
          
          <p className="hero-description">
            Generate eye-catching, professional thumbnails in seconds. 
            Our AI understands what makes viewers click and creates 
            thumbnails optimized for maximum engagement.
          </p>
          
          <button 
            className="cta-button"
            onClick={() => setCurrentPage('app')}
          >
            <span>✨ Enter App</span>
            <div className="button-glow"></div>
          </button>
        </div>
        
        <div className="hero-visual">
          <div className="thumbnail-preview">
            <div className="preview-item">🖼️</div>
            <div className="preview-item">🎨</div>
            <div className="preview-item">⚡</div>
          </div>
        </div>
      </header>

      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Why Choose ThumbnailGuru?</h2>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Design</h3>
              <p>Advanced AI analyzes your content and creates thumbnails that convert viewers into clicks</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Lightning Fast</h3>
              <p>Generate professional thumbnails in under 30 seconds. No more hours in design software</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Optimized for CTR</h3>
              <p>Every thumbnail is designed using proven psychological triggers that increase click-through rates</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>Mobile Optimized</h3>
              <p>Thumbnails look perfect on all devices - from phones to 4K displays</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h3>Multiple Styles</h3>
              <p>From educational to entertainment - AI adapts to your content genre automatically</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">💾</div>
              <h3>Instant Download</h3>
              <p>High-quality PNG files ready for upload. Perfect 1280x720 YouTube dimensions</p>
            </div>
          </div>
        </div>
      </section>

      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">50,000+</div>
              <div className="stat-label">Thumbnails Generated</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">98%</div>
              <div className="stat-label">Satisfaction Rate</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">2.3s</div>
              <div className="stat-label">Average Generation Time</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">AI Availability</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );

  const AppPage = () => (
    <div className="app-page">
      <nav className="app-nav">
        <div className="nav-content">
          <div className="nav-logo" onClick={() => setCurrentPage('home')}>
            <span className="logo-icon">🎬</span>
            <span className="logo-text">ThumbnailGuru</span>
          </div>
          
          <div className="nav-stats">
            <div className="stat">
              <span className="stat-value">{stats.totalGenerated}</span>
              <span className="stat-label">Generated</span>
            </div>
            <div className="stat">
              <span className="stat-value">{stats.avgGenerationTime}s</span>
              <span className="stat-label">Avg Time</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="app-container">
        <div className="generator-section">
          <div className="generator-card">
            <h2 className="generator-title">
              <span className="title-icon">✨</span>
              Generate Your Thumbnail
            </h2>
            
            <div className="form-group">
              <label className="form-label">Video Title *</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Enter your video title..."
                className="form-input"
                maxLength="100"
              />
              <div className="char-count">{formData.title.length}/100</div>
            </div>
            
            <div className="form-group">
              <label className="form-label">Description (Optional)</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Brief description to help AI understand your content better..."
                className="form-textarea"
                rows="3"
                maxLength="500"
              />
              <div className="char-count">{formData.description.length}/500</div>
            </div>
            
            <button 
              className={`generate-button ${loading ? 'loading' : ''}`}
              onClick={generateThumbnail}
              disabled={loading || !formData.title.trim()}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  <span>Generating Magic...</span>
                </>
              ) : (
                <>
                  <span>🎨 Generate Thumbnail</span>
                </>
              )}
            </button>
            
            {loading && (
              <div className="loading-info">
                <div className="loading-bar">
                  <div className="loading-progress"></div>
                </div>
                <p className="loading-text">AI is crafting your perfect thumbnail...</p>
              </div>
            )}
          </div>
        </div>

        <div className="gallery-section">
          <div className="gallery-header">
            <h3 className="gallery-title">
              <span className="gallery-icon">🖼️</span>
              Your Thumbnails ({thumbnails.length})
            </h3>
            {thumbnails.length > 0 && (
              <button className="clear-button" onClick={clearHistory}>
                🗑️ Clear All
              </button>
            )}
          </div>
          
          {thumbnails.length === 0 ? (
            <div className="empty-gallery">
              <div className="empty-icon">📭</div>
              <p className="empty-text">No thumbnails yet. Generate your first one!</p>
            </div>
          ) : (
            <div className="thumbnails-grid">
              {thumbnails.map((thumbnail) => (
                <div key={thumbnail.id} className="thumbnail-tile">
                  <div 
                    className="thumbnail-image"
                    onClick={() => setSelectedImage(thumbnail)}
                  >
                    <img 
                      src={thumbnail.thumbnailUrl || thumbnail.imageUrl} 
                      alt={thumbnail.title}
                      loading="lazy"
                    />
                    <div className="thumbnail-overlay">
                      <button className="overlay-button">👁️ View</button>
                      <button 
                        className="overlay-button"
                        onClick={(e) => {
                          e.stopPropagation();
                          downloadThumbnail(thumbnail);
                        }}
                      >
                        💾 Save
                      </button>
                    </div>
                  </div>
                  
                  <div className="thumbnail-info">
                    <h4 className="thumbnail-title">{thumbnail.title}</h4>
                    <div className="thumbnail-meta">
                      <span className="meta-item">
                        ⏱️ {thumbnail.generationTime}s
                      </span>
                      <span className="meta-item">
                        📅 {new Date(thumbnail.createdAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {selectedImage && (
        <div className="modal-overlay" onClick={() => setSelectedImage(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button 
              className="modal-close"
              onClick={() => setSelectedImage(null)}
            >
              ✕
            </button>
            
            <div className="modal-image-container">
              <img 
                src={selectedImage.imageUrl} 
                alt={selectedImage.title}
                className="modal-image"
              />
            </div>
            
            <div className="modal-info">
              <h3 className="modal-title">{selectedImage.title}</h3>
              <div className="modal-actions">
                <button 
                  className="modal-button primary"
                  onClick={() => downloadThumbnail(selectedImage)}
                >
                  💾 Download HD
                </button>
                <button 
                  className="modal-button secondary"
                  onClick={() => setSelectedImage(null)}
                >
                  👁️ Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="App">
      {currentPage === 'home' ? <HomePage /> : <AppPage />}
    </div>
  );
};

export default App;