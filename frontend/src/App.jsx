import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Wand2, Brain, Languages, BarChart, Zap, Copy, Shield, Download, Scale, Info } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '/_/backend' : 'http://localhost:8000');

// --- Shared Components ---

const Navbar = () => (
  <header className="header">
    <Link to="/" className="label-text-pixel" style={{ fontSize: '18px', textDecoration: 'none' }}>
      LegalEase
    </Link>
  </header>
);

const Footer = () => (
  <footer className="container">
    <div className="footer">
      <div>
        <div className="label-text-pixel" style={{ fontSize: '16px', marginBottom: '8px' }}>LegalEase</div>
        <div className="copy-text">© 2024 LegalEase AI. Secured by Digital Vault technology.</div>
      </div>
      <div className="footer-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
        <a href="#">Security Disclosure</a>
        <a href="#">Contact</a>
      </div>
    </div>
  </footer>
);

// --- Page Components ---

const LandingPage = () => {
  const navigate = useNavigate();
  return (
    <div className="page-transition">
      <div className="video-background-container">
        <video autoPlay loop muted playsInline>
          <source src="/1.mp4" type="video/mp4" />
        </video>
      </div>
      <div className="video-overlay"></div>
      <div className="grid-overlay"></div>
      <div className="data-stream"></div>
      <div className="data-stream" style={{ right: '20%', animationDelay: '-4s' }}></div>
      <section className="container hero">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="glitch-text">
            Understand Legal Language <span style={{ color: '#00D28E' }}>Instantly</span>
          </h1>
          <p>
            Convert complex legal text into plain English using AI. No more fine print confusion, just clarity.
          </p>
          <button className="btn-large" onClick={() => navigate('/app')}>
            Start Simplifying
          </button>
        </motion.div>
      </section>

      {/* Features Preview */}
      <section id="features" className="container features-section">
        <h2 className="features-title glitch-text">Advanced Intelligence Architecture</h2>
        <div className="features-grid">
          <div className="feature-card robotic-corner">
            <div className="feature-icon"><Brain size={24} /></div>
            <h3 className="glitch-text">AI Rewriting</h3>
            <p>Neural networks trained on thousands of legal precedents for contextual accuracy.</p>
          </div>
          <div className="feature-card robotic-corner">
            <div className="feature-icon"><Languages size={24} /></div>
            <h3 className="glitch-text">Term Simplification</h3>
            <p>Instant translation of Latin phrases and archaic legalese into modern vernacular.</p>
          </div>
          <div className="feature-card robotic-corner">
            <div className="feature-icon"><BarChart size={24} /></div>
            <h3 className="glitch-text">Readability Score</h3>
            <p>Flesch-Kincaid based metrics applied in real-time to every text segment.</p>
          </div>
          <div className="feature-card robotic-corner">
            <div className="feature-icon"><Zap size={24} /></div>
            <h3 className="glitch-text">Fast Processing</h3>
            <p>Proprietary LLM infrastructure ensures sub-second simplification for lengthy documents.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

const SimplifierApp = () => {
  const [inputText, setInputText] = useState('');
  const [simplifiedText, setSimplifiedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState({ readability: 84, reduction: 42, complexity: 'Normal' });

  const calculateDiagnostics = (original, simplified) => {
    const getWordCount = (str) => str.trim().split(/\s+/).length;
    const getSentenceCount = (str) => str.split(/[.!?]+/).filter(s => s.trim().length > 0).length || 1;
    const getAvgWordLength = (str) => {
      const words = str.trim().split(/\s+/);
      return words.reduce((acc, word) => acc + word.length, 0) / words.length || 0;
    };

    const origWords = getWordCount(original);
    const simpWords = getWordCount(simplified);
    
    // Word Reduction
    const reduction = Math.max(0, Math.round(((origWords - simpWords) / origWords) * 100));
    
    // Simplified Readability (Approx Flesch-Kincaid)
    const avgSentLen = simpWords / getSentenceCount(simplified);
    const avgWordLen = getAvgWordLength(simplified);
    // Rough syllable estimate: length / 3
    const readability = Math.min(100, Math.max(0, Math.round(206.835 - (1.015 * avgSentLen) - (84.6 * (avgWordLen / 3)))));
    
    let complexity = 'Normal';
    if (readability > 80) complexity = 'Simple';
    else if (readability < 40) complexity = 'Professional';
    
    return { readability, reduction, complexity };
  };

  const handleSimplify = async () => {
    if (!inputText.trim()) return;
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/simplify`, { text: inputText });
      const simplified = response.data.simplified_text;
      setSimplifiedText(simplified);
      
      const newStats = calculateDiagnostics(inputText, simplified);
      setStats(newStats);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = () => {
    if (!simplifiedText) return;
    const element = document.createElement("a");
    // Using application/msword for .doc format compatibility
    const file = new Blob([simplifiedText], { type: 'application/msword' });
    element.href = URL.createObjectURL(file);
    element.download = "SIMPLIFIED_LEGAL.doc";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="container page-transition" style={{ height: '100vh', display: 'flex', flexFlow: 'column', padding: '20px 24px 0' }}>
      <section className="tool-section-wrapper flex-1 flex flex-col min-h-0">
        <div className="tool-header-new">
          <div className="label-text-pixel">Original Legal Text</div>
          <div className="label-text-pixel">Simplified Version</div>
        </div>

        <section className="tool-section-new flex-grow min-h-0">
          {isLoading && <div className="scanning-bar" />}
          
          {/* Original Text Pane */}
          <div className="relative flex-1 min-h-0">
            <textarea
              className="text-area-new w-full h-full"
              placeholder="Paste legal text here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
          </div>

          {/* Action Button */}
          <button className="magic-button" onClick={handleSimplify} disabled={isLoading}>
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
            ) : (
              <Wand2 size={20} color="#000" />
            )}
          </button>

          {/* Converted Text Pane */}
          <div className="text-area-new result-area relative flex-1 min-h-0 w-full" style={{ fontStyle: simplifiedText ? 'normal' : 'italic', color: simplifiedText ? '#fff' : '#444' }}>
            {simplifiedText && (
              <div className="flex gap-3 z-10" style={{ position: 'absolute', top: '16px', right: '16px' }}>
                <Download 
                  size={14} 
                  className="text-emerald-500 cursor-pointer hover:text-white transition-all" 
                  onClick={handleExport}
                  title="Download as .doc"
                />
                <Copy 
                  size={14} 
                  className="text-emerald-500 cursor-pointer hover:text-white transition-all" 
                  onClick={() => {
                    navigator.clipboard.writeText(simplifiedText);
                    alert('Copied to clipboard!');
                  }} 
                  title="Copy to clipboard"
                />
              </div>
            )}
            <div className="w-full h-full overflow-y-auto">
              {simplifiedText || "// AWAITING_INITIALIZATION..."}
            </div>
          </div>
        </section>
      </section>

      <motion.div 
        className="stats-grid-compact"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div className="stat-card-compact">
          <div className="stat-label-pixel">Readability</div>
          <div className="stat-value-pixel">{stats.readability}%</div>
          <div className="progress-container-mini">
            <motion.div 
              className="progress-bar" 
              initial={{ width: 0 }}
              animate={{ width: `${stats.readability}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
        </div>
        <div className="stat-card-compact">
          <div className="stat-label-pixel">Reduction</div>
          <div className="stat-value-pixel">{stats.reduction}%</div>
          <div className="progress-container-mini">
            <motion.div 
              className="progress-bar" 
              initial={{ width: 0 }}
              animate={{ width: `${stats.reduction}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
        </div>
        <div className="stat-card-compact">
          <div className="stat-label-pixel">Complexity</div>
          <div className="stat-value-pixel normal">{stats.complexity}</div>
          <div className="text-slate-600 text-[10px] mt-2 font-mono">STATUS: STABLE</div>
        </div>
      </motion.div>
    </div>
  );
};

// --- Main App Component ---

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#0A0A0A] text-white">
        <Navbar />
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/app" element={<SimplifierApp />} />
          </Routes>
        </AnimatePresence>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
