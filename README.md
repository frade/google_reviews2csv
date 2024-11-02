# Google Maps Reviews Scraper

A Python script that automatically scrapes reviews from Google Maps for any business or place.

## 📋 Features

- Search for any business/place on Google Maps
- Automatically click through to the business page
- Extract all available reviews including:
  - Author name
  - Rating (0-5 stars)
  - Review date
  - Review text
- Save results to CSV file with timestamp
- Handles dynamic loading of reviews through scrolling
- Headless mode support for background operation

## 🔧 Requirements

- Python 3.7+
- Chrome browser installed
- Required Python packages:
  ```
  selenium==4.15.2
  chromedriver-autoinstaller==0.6.2
  ```

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/google-reviews-scraper.git
   cd google-reviews-scraper
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Run the script:
   ```bash
   python google_reviews.py
   ```

2. Enter the business name when prompted
3. The script will:
   - Search for the business on Google Maps
   - Click through to the business page
   - Load all available reviews
   - Save them to a CSV file named `{business_name}_reviews_{timestamp}.csv`

## ⚙️ Configuration

You can modify the following parameters in the script:
- `initialize_driver()`: Chrome driver options (headless mode, window size, etc.)
- `scroll_reviews()`: Scroll behavior and timing
- Review extraction selectors in `extract_reviews()`

## 📄 Output Format

The script creates a CSV file with the following columns:
- `author_name`: Name of the reviewer
- `rating`: Number of stars (0-5)
- `relative_time`: When the review was posted (e.g., "2 months ago")
- `text`: Full review text

## ⚠️ Limitations

- Depends on Google Maps' HTML structure (may need updates if Google changes their layout)
- Rate limiting may apply
- Some reviews might be truncated if they're too long
- Requires stable internet connection

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This script is for educational purposes only. Make sure to comply with Google's terms of service and robots.txt when using this script.

## 🐛 Troubleshooting

If you encounter any issues:

1. Make sure Chrome browser is installed and up to date
2. Check if chromedriver version matches your Chrome browser version
3. Try running without headless mode for debugging
4. Check your internet connection

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/google-reviews-scraper](https://github.com/yourusername/google-reviews-scraper)