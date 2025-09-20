# 🧠 Margadarsaka - AI Career Advisor

**Margadarsaka** is an intelligent, AI-powered career advisor specializing in psychological assessment, mental skills evaluation, and culturally-aware career guidance. Designed for the Indian context with support for both Hindi and English, it provides comprehensive career recommendations based on psychological profiling and RIASEC model assessment.

---

## ✨ Features

### 🎯 Core Capabilities
- **AI-Powered Career Guidance**: Google Gemini integration for intelligent recommendations
- **Psychological Assessment**: RIASEC model-based career profiling with mental skills evaluation
- **Cultural Awareness**: Indian job market insights with Hindi language support
- **Resume Analysis**: ATS scoring with detailed feedback and improvement suggestions
- **Interactive Roadmaps**: PDF/image generation with gamification elements
- **Multi-Language Support**: Hindi and English with intelligent translation

### 🧪 Psychological Testing Framework
- **Mental Skills Assessment**: Analytical, deductive, and problem-solving capabilities
- **RIASEC Profiling**: Realistic, Investigative, Artistic, Social, Enterprising, Conventional
- **Personality Insights**: Career compatibility analysis
- **Skill Gap Analysis**: Personalized learning recommendations

### 🎨 User Experience
- **Minimalist UI**: Clean Streamlit interface with Indian cultural elements
- **Interactive Charts**: Data visualization with Plotly and Matplotlib
- **Downloadable Reports**: PDF career roadmaps with visual elements
- **Progress Tracking**: Career development milestones and achievements

---

## 🛠️ Tech Stack

### Core Technologies
- **Language**: Python 3.12+
- **Package Manager**: [UV](https://docs.astral.sh/uv/) for fast dependency management
- **Backend**: FastAPI with Pydantic models
- **Frontend**: Streamlit with custom components
- **AI/ML**: Google Generative AI (Gemini), Transformers, PyTorch
- **Data Processing**: Polars, Pandas, NumPy, SciPy

### Development & Deployment
- **Secrets Management**: Doppler SDK with environment fallback
- **Testing**: pytest with integration and unit tests
- **Code Quality**: Black, Ruff for formatting and linting
- **Translation**: Deep Translator, Google Translate
- **PDF Generation**: ReportLab with custom styling

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+**
- **[UV Package Manager](https://docs.astral.sh/uv/getting-started/installation/)**
- **[Doppler CLI](https://docs.doppler.com/docs/install-cli)** (optional for secrets management)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dakshx-Gupta/Margadarsaka.git
   cd Margadarsaka
   ```

2. **Install dependencies with UV:**
   ```bash
   uv sync
   ```

3. **Set up secrets management (optional):**
   ```bash
   # Install Doppler CLI first, then run:
   uv run python setup_doppler.py
   
   # Or use environment variables by creating .env file:
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Application

#### Option 1: Full Application (Recommended)
```bash
uv run margadarsaka
```
This starts both API (port 8000) and UI (port 8501) with interactive launcher.

#### Option 2: Individual Services
```bash
# API only:
uv run uvicorn src.margadarsaka.api:app --host 0.0.0.0 --port 8000

# UI only:
uv run streamlit run src/margadarsaka/ui.py --server.port 8501
```

#### Option 3: With Doppler Secrets
```bash
# If you have Doppler configured:
doppler run --project margadarsaka --config dev -- uv run margadarsaka
```

---

## 🧪 Testing

### Quick Test
```bash
# Run basic tests
uv run python -m pytest tests/ -v

# Run with integration tests
uv run python -m pytest tests/ --integration -v
```

### Comprehensive Testing
```bash
# Windows (PowerShell)
.\test.ps1 -TestType full

# Linux/Mac
./test.sh full
```

### Test Categories
- **Unit Tests**: Core functionality and components
- **Integration Tests**: Doppler, API, and external services
- **Code Quality**: Black formatting and Ruff linting
- **Startup Tests**: Import validation and basic functionality

---

## 🔐 Secrets Management

Margadarsaka uses a **hybrid secrets management approach** for maximum flexibility:

### 🔄 **How It Works**
The application automatically follows this priority order:
1. **Doppler** (if configured and available)
2. **Environment variables** from `.env` file
3. **System environment variables**
4. **Sensible defaults** (where applicable)

This ensures the app works in any environment while providing enterprise-grade security when needed.

### Method 1: Doppler (Recommended for Production)

**Best for**: Production deployments, team collaboration, security compliance

1. **Install Doppler CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://cli.doppler.com/install.ps1 -useb | iex
   
   # macOS
   brew install dopplerhq/cli/doppler
   
   # Linux
   curl -Ls https://cli.doppler.com/install.sh | sh
   ```

2. **Set up Doppler:**
   ```bash
   # Run automated setup
   uv run python setup_doppler.py
   
   # Update your API keys
   doppler secrets set GEMINI_API_KEY=your_actual_key --project margadarsaka --config dev
   ```

3. **Run with Doppler:**
   ```bash
   doppler run --project margadarsaka --config dev -- uv run margadarsaka
   ```

### Method 2: Environment Variables (.env file)

**Best for**: Local development, quick setup, new contributors, offline work

1. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your keys:**
   ```env
   ENVIRONMENT=development
   DEBUG=true
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///margadarsaka.db
   ```

3. **Run normally:**
   ```bash
   uv run margadarsaka
   ```

### 🎯 **Which Method Should I Use?**

| Scenario | Recommended Method | Why |
|----------|-------------------|-----|
| **New contributor** | `.env` file | Fastest setup, no external dependencies |
| **Local development** | Either | Personal preference |
| **Team collaboration** | Doppler | Centralized, secure, easy sharing |
| **Production deployment** | Doppler | Enterprise security, audit trails |
| **CI/CD pipelines** | Either | Depends on your infrastructure |
| **Offline development** | `.env` file | No internet dependency |

### 🔧 **Switching Between Methods**

The application **automatically detects** which method is available:
- If Doppler is configured → uses Doppler
- If `.env` file exists → uses `.env` file  
- Otherwise → uses system environment variables

No code changes needed! 🎉

---

## 📖 API Documentation

### Interactive API Docs
Once the API is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Psychological Assessment
```bash
POST /api/v1/assessment/riasec
# Submit RIASEC assessment responses

GET /api/v1/assessment/results/{session_id}
# Get assessment results and recommendations
```

#### Career Recommendations
```bash
POST /api/v1/career/recommendations
# Get AI-powered career recommendations

POST /api/v1/career/roadmap
# Generate career roadmap with resources
```

#### Resume Analysis
```bash
POST /api/v1/resume/analyze
# Upload and analyze resume for ATS scoring

GET /api/v1/resume/suggestions/{analysis_id}
# Get improvement suggestions
```

#### Health Check
```bash
GET /health
# API health status
```

---

## 🎯 Usage Guide

### 1. Take Psychological Assessment
1. Launch the application
2. Navigate to "Psychological Assessment"
3. Complete the RIASEC questionnaire (15-20 questions)
4. Review your personality profile and mental skills assessment

### 2. Get Career Recommendations
1. Based on your assessment, view recommended career paths
2. Explore detailed job descriptions and requirements
3. Get skill gap analysis and learning recommendations
4. Access curated resources from roadmap.sh integration

### 3. Analyze Your Resume
1. Upload your resume (PDF/DOC format)
2. Get ATS compatibility score
3. Review detailed feedback and suggestions
4. Download improved resume template

### 4. Generate Career Roadmap
1. Select your target career path
2. Customize your learning preferences
3. Generate PDF roadmap with milestones
4. Track your progress and achievements

### 5. Explore Resources
1. Browse 70+ career roadmaps from roadmap.sh
2. Access curated learning materials
3. Find relevant courses and certifications
4. Connect with career opportunities

---

## 🌐 Multi-Language Support

### Supported Languages
- **English**: Full support for all features
- **Hindi**: UI translation and AI responses in Hindi

### Language Features
- Automatic language detection
- Real-time translation of career advice
- Culturally appropriate job recommendations
- Hindi-English code-mixing support

---

## 🧑‍💻 Development

### Project Structure
```
Margadarsaka/
├── src/margadarsaka/           # Main application source
│   ├── api.py                  # FastAPI application
│   ├── ui.py                   # Streamlit interface
│   ├── secrets.py              # Secrets management
│   ├── core/                   # Core business logic
│   ├── models/                 # Data models
│   └── utils/                  # Utility functions
├── tests/                      # Test suite
├── deploy/                     # Deployment configurations
├── setup_doppler.py           # Doppler setup automation
├── test.sh / test.ps1          # Test runners
└── pyproject.toml              # Project configuration
```

### Development Commands
```bash
# Install dev dependencies
uv sync --dev

# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking (if mypy is installed)
uv run mypy src/

# Run specific tests
uv run python -m pytest tests/test_doppler.py -v

# Start development server with auto-reload
uv run uvicorn src.margadarsaka.api:app --reload
```

### Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on:

- Setting up the development environment
- Code style and conventions  
- Testing guidelines
- Pull request process
- Areas where we need help

Quick start for contributors:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Run tests: `uv run python -m pytest tests/ -v`
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

---

## 📋 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Environment (development/staging/production) | `development` | No |
| `DEBUG` | Enable debug mode | `true` | No |
| `GEMINI_API_KEY` | Google Gemini API key | - | Yes |
| `SECRET_KEY` | Application secret key | Auto-generated | No |
| `DATABASE_URL` | Database connection string | `sqlite:///margadarsaka.db` | No |
| `API_BASE_URL` | API server URL | `http://localhost:8000` | No |
| `UI_BASE_URL` | UI server URL | `http://localhost:8501` | No |

### Doppler Configuration
If using Doppler, secrets are automatically managed across environments:
- **dev**: Development environment
- **stg**: Staging environment  
- **prd**: Production environment
- **dev_local**: Local development override

---

## 🔧 Troubleshooting

### Common Issues

#### 1. UV Installation Issues
```bash
# Windows: Install via PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac: Install via curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Doppler Setup Issues
```bash
# Check Doppler authentication
doppler auth status

# Re-login if needed
doppler auth login

# Verify project setup
doppler projects list
```

#### 3. Import Errors
```bash
# Ensure you're in the project directory
cd Margadarsaka

# Reinstall dependencies
uv sync --force

# Check Python path
uv run python -c "import sys; print(sys.path)"
```

#### 4. Port Conflicts
```bash
# Check if ports are in use
netstat -an | findstr :8000
netstat -an | findstr :8501

# Kill processes if needed (Windows)
taskkill /F /PID <process_id>
```

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/Dakshx-Gupta/Margadarsaka/issues)
- **Discussions**: [Community discussions](https://github.com/Dakshx-Gupta/Margadarsaka/discussions)
- **Documentation**: Check inline documentation in source code

---

## 📄 Legal & Disclaimers

### Important Notice
Margadarsaka provides **educational guidance only**. Career decisions should be made considering multiple factors including personal circumstances, market conditions, and professional advice.

### Disclaimer
- Results are based on psychological models and AI analysis
- Career recommendations are suggestions, not guarantees
- Users should verify job market information independently
- The application is for informational purposes only

### Third-Party Resources
- Roadmap.sh integration: All roadmaps are used with attribution
- Google Gemini: Subject to Google's terms of service
- External resources: Check individual licensing terms

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Roadmap.sh** for comprehensive learning roadmaps
- **Google Gemini** for AI-powered recommendations
- **UV Team** for the excellent package manager
- **Doppler** for secure secrets management
- **Streamlit Community** for the amazing UI framework

---

## 📊 Project Status

![Version](https://img.shields.io/badge/version-0.2.0-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-beta-orange)

**Latest Update**: September 2025 - Full UV integration, Doppler secrets management, comprehensive testing suite

---

<div align="center">

**Made with ❤️ for career seekers everywhere**

[🌟 Star this repo](https://github.com/Dakshx-Gupta/Margadarsaka) | [🐛 Report Bug](https://github.com/Dakshx-Gupta/Margadarsaka/issues) | [💡 Request Feature](https://github.com/Dakshx-Gupta/Margadarsaka/issues)

</div>