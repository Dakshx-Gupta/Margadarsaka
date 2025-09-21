// Built with Deno
/**
 * Rating Component for Streamlit
 * A Streamlit custom component for interactive star ratings
 */

// The Streamlit component library
import Streamlit from 'streamlit-component-lib';

// Initialize communication with Streamlit
Streamlit.setComponentReady();

// Get the component's initial args
const { initialValue, maxStars } = Streamlit.getInitialArgs();

// Create the main component container
const container = document.createElement('div');
container.className = 'rating-component';
document.body.appendChild(container);

// CSS for the rating component
const style = document.createElement('style');
style.textContent = `
  .rating-component {
    font-family: 'Inter', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
  }
  
  .stars-container {
    display: flex;
    gap: 5px;
  }
  
  .star {
    font-size: 28px;
    cursor: pointer;
    transition: transform 0.2s ease;
  }
  
  .star:hover {
    transform: scale(1.2);
  }
  
  .star.filled {
    color: #FFAC33;
  }
  
  .star.empty {
    color: #E0E0E0;
  }
  
  .rating-label {
    margin-top: 8px;
    font-size: 14px;
    color: #666;
  }
`;
document.head.appendChild(style);

// Create stars container
const starsContainer = document.createElement('div');
starsContainer.className = 'stars-container';
container.appendChild(starsContainer);

// Create rating label
const ratingLabel = document.createElement('div');
ratingLabel.className = 'rating-label';
container.appendChild(ratingLabel);

// Set initial value or default to 0
let currentRating = initialValue || 0;
const numStars = maxStars || 5;

// Update label text
function updateLabel(rating) {
  const labels = [
    'Not rated',
    'Poor',
    'Below average',
    'Average',
    'Good',
    'Excellent'
  ];
  ratingLabel.textContent = rating > 0 ? labels[rating] : labels[0];
}

// Create the stars
for (let i = 1; i <= numStars; i++) {
  const star = document.createElement('span');
  star.className = `star ${i <= currentRating ? 'filled' : 'empty'}`;
  star.textContent = '★';
  star.dataset.value = i;
  
  star.addEventListener('click', (e) => {
    const rating = parseInt(e.target.dataset.value);
    currentRating = rating;
    
    // Update star appearance
    document.querySelectorAll('.star').forEach((s, index) => {
      s.className = `star ${index < rating ? 'filled' : 'empty'}`;
    });
    
    updateLabel(rating);
    
    // Send data to Streamlit
    Streamlit.setComponentValue(rating);
  });
  
  starsContainer.appendChild(star);
}

// Initialize the label
updateLabel(currentRating);

// Handle iframe resize
window.addEventListener('resize', () => {
  Streamlit.setFrameHeight();
});

// Set initial height once the component has loaded
Streamlit.setFrameHeight();