# Streamlit Custom Components for Margadarsaka

This directory contains custom Streamlit components used in the Margadarsaka application. These components are built using JavaScript/React and integrated into the Python Streamlit app.

## Available Components

### Rating Component

A star-based rating component that allows users to provide feedback or view ratings with an interactive interface.

**Usage:**

```python
from margadarsaka.ui.components.custom_components import rating_component

# Display a rating component with default 5 stars
rating = rating_component(key="my_rating")

# Display with a preset value and custom number of stars
rating = rating_component(key="custom_rating", initial_value=3, max_stars=10)

# Get the user's selected rating
st.write(f"Selected rating: {rating}")
```

## Development

### Prerequisites

- Node.js (v16+)
- npm

### Building Components

To build all custom components:

#### Windows

```powershell
.\build_components.ps1
```

#### Linux/macOS

```bash
./build_components.sh
```

### Development Mode

To run the development server for live-reloading during development:

#### Windows

```powershell
.\build_components.ps1 dev
```

#### Linux/macOS

```bash
./build_components.sh dev
```

This will start a development server at http://localhost:5173/ where you can see the component in isolation.

### Adding New Components

1. Create a new JavaScript file in `starter-for-js/src/`
2. Create a corresponding HTML file in `starter-for-js/`
3. Create a Vite config file in `starter-for-js/` (see `vite.config.rating_component.js` as an example)
4. Create a Python wrapper in `src/margadarsaka/ui/components/custom_components/your_component_name/`
5. Update the build scripts to include your new component

## Architecture

The custom components are built using the following architecture:

- **JavaScript**: Component UI and logic (`starter-for-js/src/`)
- **HTML**: Component mounting point (`starter-for-js/*.html`)
- **Vite**: Build tool for JavaScript bundling
- **Python**: Wrapper around the JavaScript component using Streamlit's component API

## Production Deployment

For production use, set `_RELEASE = True` in the Python wrapper and ensure all components are properly built and bundled.