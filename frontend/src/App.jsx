// App.jsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import './App.css';

// --- HomePage Component ---
const HomePage = ({ setCurrentPage }) => (
  <div className="home-page">
    <header className="hero-section">
      <div className="hero-content">
        <div className="logo-container">
          <div className="logo">🎬</div>
          <h1 className="brand-title">ThumbnailGuru</h1>
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
          <span>✨ Start Creating</span>
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

    <footer className="footer-section">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <span className="footer-logo-icon">🎬</span>
              <span className="footer-logo-text">ThumbnailGuru</span>
            </div>
            {/* <p className="footer-tagline">Secret of Viral Videos</p>  Removed this if the subtitle serves better */}
            <p className="footer-sub-tagline">Made with ❤️ for creators around the world</p>
          </div>
          
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <ul>
                <li><a href="#features">Features</a></li>
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#api">API</a></li>
              </ul>
            </div>
            <div className="footer-column">
              <h4>Support</h4>
              <ul>
                <li><a href="#help">Help Center</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="#tutorials">Tutorials</a></li>
              </ul>
            </div>
            <div className="footer-column">
              <h4>Community</h4>
              <ul>
                <li><a href="#discord">Discord</a></li>
                <li><a href="#twitter">Twitter</a></li>
                <li><a href="#youtube">YouTube</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>© {new Date().getFullYear()} ThumbnailGuru. Empowering creators worldwide.</p>
        </div>
      </div>
    </footer>
  </div>
);

// --- AppPage Component ---
const AppPage = ({
  setCurrentPage,
  thumbnails,
  loading,
  selectedImage,
  setSelectedImage,
  formData,
  handleInputChange,
  stats,
  generateThumbnail,
  downloadThumbnail,
  clearHistory,
  ThumbnailGridComponent 
}) => (
  <div className="app-page">
    <nav className="app-nav">
      <div className="nav-content">
        <div className="nav-logo" onClick={() => setCurrentPage('home')} role="button" tabIndex={0} 
             onKeyPress={(e) => e.key === 'Enter' && setCurrentPage('home')}>
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

    <div className="new-app-layout">
      <div className="generator-section-centered">
        <div className="generator-card">
          <h2 className="generator-title">
            <span className="title-icon">✨</span>
            Generate Your Thumbnail
          </h2>
          
          <div className="form-row">
            <div className="form-group flex-1">
              <label htmlFor="title" className="form-label">Video Title *</label>
              <input
                id="title"
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
            
            <div className="form-group flex-1">
              <label htmlFor="description" className="form-label">Description (Optional)</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Brief description..."
                className="form-textarea"
                rows="3"
                maxLength="500"
              />
              <div className="char-count">{formData.description.length}/500</div>
            </div>
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

      <div className="gallery-section-new">
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
          <div className="thumbnails-grid-horizontal">
            {ThumbnailGridComponent}
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
            aria-label="Close modal"
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

// --- Main App Component ---
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
    avgGenerationTime: 20 
  });

  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    const savedThumbnails = localStorage.getItem('thumbnails');
    if (savedThumbnails) {
      setThumbnails(JSON.parse(savedThumbnails));
    }
    const savedStats = localStorage.getItem('thumbnailStats');
    if (savedStats) {
      setStats(JSON.parse(savedStats));
    } else {
      localStorage.setItem('thumbnailStats', JSON.stringify(stats));
    }
  }, []); // Initial load for stats

  const saveThumbnailsToStorage = useCallback((newThumbnails) => {
    localStorage.setItem('thumbnails', JSON.stringify(newThumbnails));
  }, []);

  const saveStatsToStorage = useCallback((newStats) => {
    localStorage.setItem('thumbnailStats', JSON.stringify(newStats));
  }, []);

  const handleInputChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  }, []);

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
          generationTime: parseFloat(data.generation_time) || 2.0, // Ensure it's a number
          createdAt: new Date().toISOString()
        };

        const updatedThumbnails = [newThumbnail, ...thumbnails];
        setThumbnails(updatedThumbnails);
        saveThumbnailsToStorage(updatedThumbnails);
        
        setStats(prev => {
          const newTotalGenerated = prev.totalGenerated + 1;
          const currentTotalTime = (prev.avgGenerationTime * prev.totalGenerated);
          const newAvgTime = (currentTotalTime + newThumbnail.generationTime) / newTotalGenerated;
          
          const updatedStats = {
            totalGenerated: newTotalGenerated,
            avgGenerationTime: parseFloat(newAvgTime.toFixed(1)) || prev.avgGenerationTime
          };
          saveStatsToStorage(updatedStats);
          return updatedStats;
        });

        setFormData({ title: '', description: '' });
      } else {
        alert(data.message || 'Failed to generate thumbnail. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating thumbnail. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const downloadThumbnail = useCallback((thumbnail) => {
    const link = document.createElement('a');
    link.href = thumbnail.downloadUrl || thumbnail.imageUrl;
    const safeTitle = (thumbnail.title || 'untitled').replace(/[^a-z0-9]/gi, '_').toLowerCase();
    link.download = `${safeTitle.substring(0, 50)}-thumbnail.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all thumbnails?')) {
      setThumbnails([]);
      localStorage.removeItem('thumbnails');
      // Optionally, you might want to reset parts of stats or keep them global
      // For now, totalGenerated remains, avgGenerationTime might become less accurate
      // or you could reset it if it's meant to be avg of current list
    }
  };
  
  const memoizedThumbnailGrid = useMemo(() => {
    return thumbnails.map((thumbnail) => (
      <div key={thumbnail.id} className="thumbnail-tile">
        <div 
          className="thumbnail-image"
          onClick={() => setSelectedImage(thumbnail)}
          role="button" tabIndex={0}
          onKeyPress={(e) => e.key === 'Enter' && setSelectedImage(thumbnail)}
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
              ⏱️ {thumbnail.generationTime ? thumbnail.generationTime.toFixed(1) : 'N/A'}s
            </span>
            <span className="meta-item">
              📅 {new Date(thumbnail.createdAt).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    ));
  }, [thumbnails, setSelectedImage, downloadThumbnail]);

  return (
    <div className="App">
      {currentPage === 'home' ? (
        <HomePage setCurrentPage={setCurrentPage} />
      ) : (
        <AppPage
          setCurrentPage={setCurrentPage}
          thumbnails={thumbnails}
          loading={loading}
          selectedImage={selectedImage}
          setSelectedImage={setSelectedImage}
          formData={formData}
          handleInputChange={handleInputChange}
          stats={stats}
          generateThumbnail={generateThumbnail}
          downloadThumbnail={downloadThumbnail}
          clearHistory={clearHistory}
          ThumbnailGridComponent={memoizedThumbnailGrid}
        />
      )}
    </div>
  );
};

export default App;