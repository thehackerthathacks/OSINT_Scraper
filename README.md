# OSINT Scraper

A Python tool to search usernames on multiple platforms and check email information without any API keys.

## Features

- Check username existence on GitHub, Twitter, Reddit, Instagram, TikTok, Facebook, LinkedIn, Medium, StackOverflow, Pinterest, YouTube, Steam, Twitch, Keybase.
- Check email for:
  - Syntax validity
  - Gravatar profile
  - MX record / domain existence
- Output in terminal or JSON format
- No API keys required

## Installation

```bash
git clone https://github.com/thehackerthathacks/osint-scraper.git
cd osint-scraper
pip install -r requirements.txt

## Usage

# Check a username on all platforms
python osint_scraper.py --username hacker123

# Check an email for Gravatar, MX records, and validity
python osint_scraper.py --email test@example.com

# Combine email + username checks
python osint_scraper.py --username hacker123 --email test@example.com

# Output results in JSON format
python osint_scraper.py --username hacker123 --json
