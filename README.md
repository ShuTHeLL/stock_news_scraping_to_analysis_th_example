# Stock News Scraper and Sentiment Analysis

A Python script that scrapes financial news articles from HoonVision, performs sentiment analysis using AI4Thai's API, and stores the results in CSV files.

## Features

- Web scraping of Thai financial news articles
- Automatic duplicate detection
- Text cleaning and normalization
- Sentiment analysis using AI4Thai's API
- Data export to CSV with timestamp
- Database-like functionality for tracking processed articles

Installation
Clone this repository

Install dependencies:

    pip install -r requirements.txt
Download ChromeDriver (matching your Chrome version) and place it in your PATH:
https://chromedriver.chromium.org/downloads

Configuration
Obtain an API key from AI4Thai (free tier available):
https://aiforthai.in.th/service.php

Replace the empty Apikey in the script:

python
Copy
headers = {
    'Apikey': "YOUR_API_KEY_HERE"  # Replace with your actual API key
}

Usage
Run the script:

    python stock_news_scraper.py
