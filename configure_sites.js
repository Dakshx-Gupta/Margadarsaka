#!/usr/bin/env node
/**
 * Configure starter-for-js for Appwrite Sites deployment
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Paths
const ROOT_DIR = path.resolve(__dirname);
const STARTER_DIR = path.join(ROOT_DIR, 'starter-for-js');
const PACKAGE_JSON_PATH = path.join(STARTER_DIR, 'package.json');
const VITE_CONFIG_PATH = path.join(STARTER_DIR, 'vite.config.js');

// Check if starter-for-js exists
if (!fs.existsSync(STARTER_DIR)) {
  console.error('Error: starter-for-js directory not found!');
  process.exit(1);
}

// Update package.json with Appwrite Sites configuration
console.log('Updating package.json with Appwrite Sites configuration...');
const packageJson = JSON.parse(fs.readFileSync(PACKAGE_JSON_PATH, 'utf8'));

// Add Appwrite Sites specific scripts
packageJson.scripts = {
  ...packageJson.scripts,
  'build:sites': 'vite build --config vite.config.sites.js',
  'deploy:sites': 'node ../deploy_sites.js'
};

// Save updated package.json
fs.writeFileSync(PACKAGE_JSON_PATH, JSON.stringify(packageJson, null, 2));

// Create a Sites-specific Vite config
console.log('Creating Appwrite Sites specific Vite config...');
const sitesConfig = `
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  // Base path for assets (empty for relative paths)
  base: '/',
  
  // Build configuration
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    minify: true,
    
    // Add hash to file names for cache busting
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]'
      }
    }
  },
  
  // Server configuration
  server: {
    port: 5173,
    open: true
  }
});
`;

// Save the Sites-specific Vite config
fs.writeFileSync(path.join(STARTER_DIR, 'vite.config.sites.js'), sitesConfig);

// Create a simple index.html that showcases Margadarsaka
console.log('Creating sample landing page for Appwrite Sites...');
const landingPage = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Margadarsaka - AI Career Advisor</title>
  <link rel="stylesheet" href="./style/main.css">
  <script type="module" src="./src/main.js"></script>
  <!-- Add preconnect for better performance -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
</head>
<body>
  <header>
    <div class="container">
      <div class="logo">
        <h1>🚀 Margadarsaka</h1>
      </div>
      <nav>
        <ul>
          <li><a href="#features">Features</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="https://app.margadarsaka.appwrite.io" class="btn">Launch App</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <div class="hero-content">
        <h1>AI-Powered Career Guidance</h1>
        <p>Personalized career recommendations, resume analysis, and skill development plans tailored for your professional journey.</p>
        <a href="https://app.margadarsaka.appwrite.io" class="btn btn-primary">Get Started</a>
      </div>
      <div class="hero-image">
        <!-- Placeholder for hero image -->
        <div class="placeholder"></div>
      </div>
    </div>
  </section>

  <section id="features" class="features">
    <div class="container">
      <h2>Key Features</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">📄</div>
          <h3>Resume Analysis</h3>
          <p>AI-powered resume analysis with ATS optimization suggestions and keyword matching.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🧠</div>
          <h3>Psychological Profiling</h3>
          <p>Understand your personality traits and how they align with different career paths.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Career Recommendations</h3>
          <p>Get personalized career suggestions based on your skills, interests, and market trends.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🚀</div>
          <h3>Skill Development</h3>
          <p>Actionable skill development plans to achieve your career goals.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="about" class="about">
    <div class="container">
      <h2>About Margadarsaka</h2>
      <p>Margadarsaka is an AI-driven career guidance platform designed to help professionals navigate their career journeys. Our mission is to empower individuals with personalized insights and actionable recommendations for career growth.</p>
      <p>Built with cutting-edge technology and hosted on Appwrite Sites, Margadarsaka provides a seamless and secure experience for users worldwide.</p>
    </div>
  </section>

  <footer>
    <div class="container">
      <p>&copy; 2025 Margadarsaka. All rights reserved.</p>
      <div class="social-links">
        <a href="#">Twitter</a>
        <a href="#">LinkedIn</a>
        <a href="#">GitHub</a>
      </div>
    </div>
  </footer>
</body>
</html>
`;

// Save the landing page
fs.writeFileSync(path.join(STARTER_DIR, 'sites_landing.html'), landingPage);

// Create or update CSS file
console.log('Creating CSS for the landing page...');
const css = `
/* Base styles */
:root {
  --primary-color: #6366F1;
  --secondary-color: #8B5CF6;
  --text-color: #1F2937;
  --light-text: #F9FAFB;
  --background: #FFFFFF;
  --light-background: #F3F4F6;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: var(--background);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

a {
  color: var(--primary-color);
  text-decoration: none;
}

/* Header */
header {
  padding: 1.5rem 0;
  background-color: var(--background);
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  font-size: 1.5rem;
  color: var(--primary-color);
}

nav ul {
  display: flex;
  list-style: none;
}

nav ul li {
  margin-left: 2rem;
}

nav ul li a {
  font-weight: 500;
}

.btn {
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: var(--light-text);
  border-radius: 0.25rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: var(--secondary-color);
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
}

/* Hero section */
.hero {
  padding: 6rem 0;
  background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
  color: var(--light-text);
}

.hero .container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-image .placeholder {
  width: 100%;
  height: 400px;
  background-color: rgba(255,255,255,0.2);
  border-radius: 1rem;
}

/* Features section */
.features {
  padding: 6rem 0;
  background-color: var(--light-background);
}

.features h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: var(--background);
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  margin-bottom: 1rem;
}

/* About section */
.about {
  padding: 6rem 0;
}

.about h2 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

.about p {
  font-size: 1.1rem;
  max-width: 800px;
  margin-bottom: 1.5rem;
}

/* Footer */
footer {
  background-color: var(--text-color);
  color: var(--light-text);
  padding: 3rem 0;
}

footer .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.social-links a {
  color: var(--light-text);
  margin-left: 1.5rem;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.social-links a:hover {
  opacity: 1;
}

/* Responsive design */
@media (max-width: 768px) {
  .hero .container {
    grid-template-columns: 1fr;
  }
  
  .hero-content {
    text-align: center;
  }
  
  footer .container {
    flex-direction: column;
    text-align: center;
  }
  
  .social-links {
    margin-top: 1.5rem;
  }
  
  .social-links a {
    margin: 0 0.75rem;
  }
}
`;

// Create style directory if it doesn't exist
const styleDir = path.join(STARTER_DIR, 'style');
if (!fs.existsSync(styleDir)) {
  fs.mkdirSync(styleDir);
}

// Save the CSS file
fs.writeFileSync(path.join(styleDir, 'sites.css'), css);

// Create JavaScript file for the landing page
console.log('Creating JavaScript for the landing page...');
const js = `
/**
 * Main JavaScript for Margadarsaka landing page
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize smooth scrolling for anchor links
  initSmoothScroll();
  
  // Add animation for features
  animateFeatures();
});

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScroll() {
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  
  anchorLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      
      const targetId = link.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

/**
 * Add animation for features when they come into view
 */
function animateFeatures() {
  const featureCards = document.querySelectorAll('.feature-card');
  
  // Simple animation when scrolling to features
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  
  // Set initial styles and observe
  featureCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
}
`;

// Create src directory if it doesn't exist
if (!fs.existsSync(path.join(STARTER_DIR, 'src'))) {
  fs.mkdirSync(path.join(STARTER_DIR, 'src'));
}

// Save the JavaScript file
fs.writeFileSync(path.join(STARTER_DIR, 'src', 'main.js'), js);

console.log('\nConfiguration complete!');
console.log('\nTo build the site for Appwrite Sites deployment:');
console.log('1. cd starter-for-js');
console.log('2. npm run build:sites');
console.log('\nTo deploy to Appwrite Sites:');
console.log('1. cd ..');
console.log('2. python deploy_sites.py --site-id margadarsaka');