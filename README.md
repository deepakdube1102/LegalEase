# LegalEase - NLP Legal Simplifier

LegalEase is an AI-powered system designed to translate complex legal text into simple, easy-to-understand English. It uses a combination of dictionary-based rules, linguistic parsing with spaCy, and transformer models from Hugging Face.

## Features
- **Rule-Based Engine**: Replaces archaic legal terms (e.g., "hereinafter") with modern equivalents.
- **AI Paraphrasing**: Utilizes the T5 transformer model to rewrite complex sentences.
- **Premium UI**: High-fidelity glassmorphic interface with real-time stats and animations.
- **Split-View Editor**: Compare original and simplified text side-by-side.

## Tech Stack
- **Frontend**: React, Vite, Framer Motion, Lucide Icons, Vanilla CSS.
- **Backend**: FastAPI, Python, spaCy, Transformers (PyTorch).

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

### Setup
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python main.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Design Aesthetics
The UI follows an "Obsidian & Emerald" theme, emphasizing trust, clarity, and modern technology.
