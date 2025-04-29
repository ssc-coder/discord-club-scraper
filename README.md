# Discord Clubs Scraper

This script scrapes student club information from a university's [Discord Student Hub](https://support.discord.com/hc/en-us/articles/10113895440983-Student-Hubs). It automates the process of collecting data from each tab — including **Home**, **Clubs**, **Classes & Subjects**, **Social & Study**, and **Miscellaneous** — and compiles it into a clean CSV file.

## 🔧 Features

- Logs into Discord manually via browser.
- Scrolls and scrapes data from each visible card.
- Collects:
  - Club name
  - Club description
  - Total number of members (not just online)
  - Category (e.g., Clubs, Social & Study)
- Identifies clubs **only listed in Home** but **not categorized**, and tags them as `Uncategorized`.
- Skips "Add Server" and other non-club entries.
- Saves everything to a structured CSV file.

## 🖥️ Requirements

- Python 3.7+
- Google Chrome (latest)
- Matching `chromedriver` for your Chrome version

Install dependencies:
```bash
pip install selenium
```

## ⚙️ Setup

1. Download chromedriver for your version of Chrome from: https://googlechromelabs.github.io/chrome-for-testing/
2. Unzip and copy the path to the chromedriver binary.
3. Clone or download this repo, then run:
   ```bash
   python3 scrape_discord_clubs.py
   ```
4. When prompted:
   - Enter the full path to your chromedriver file.
   - Log into Discord in the new window.
   - Manually scroll to load all entries in the Home tab, then press Enter.

## 📁 Output

The results are saved to:
```bash
discord_clubs.csv
```
It includes:
Club Name | Club Description | No. of members | Club Category | …

Clubs that are only visible in Home but not under any category tab are marked with:
```bash
Club Category: Uncategorized
```

## 💡 Why Use This?

Manually copying club info from Discord Student Hubs is slow and painful — especially if you’re gathering contacts, doing outreach, or tracking engagement. This script makes it instant.

## 👥 Contributions Welcome

Feel free to fork, file issues, or make pull requests if you’d like to enhance functionality (e.g. auto-login, headless mode, or category-specific filters).
