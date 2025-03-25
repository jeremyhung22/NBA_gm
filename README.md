# NBA GM Chat Bot

A Streamlit application that assists fantasy basketball players by providing player profiles, statistics, salary cap insights, and recent player updates.

## Overview

This project leverages the **OpenAI API** to provide intelligent, conversational insights for fantasy basketball managers. It pulls data from real-time NBA sources and uses AI-powered responses to help users make informed decisions about their fantasy basketball teams, including player stats, salary cap management, and recent performance updates.

## Technical Implementation

- **Frontend**: Streamlit application for an interactive web interface
- **AI Model**: OpenAI API for text generation, which provides conversational responses and insights
- **Data Source**: Real-time NBA player data (can be fetched using sports APIs such as NBA API, SportsRadar, etc.)
- **Prompting Technique**: Few-shot prompting with curated examples to generate responses based on player data, statistics, salary caps, and recent updates

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- OpenAI API key
- API access for NBA data (e.g., Sports API)
- Internet connection for real-time data fetching and model inference

### Installation

```bash
# Clone the repository
git clone https://github.com/jeremyhung22/nba_gm.git
cd nba_gm

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Usage
1. Open the application in your web browser.
2. Enter player names or specific queries related to NBA stats, salary caps, or player updates.
3. Click "Submit" to generate responses using the OpenAI API.
4. Visualize player data or insights, and receive suggestions for fantasy team management.
