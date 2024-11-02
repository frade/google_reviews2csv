from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
from datetime import datetime
import re

def initialize_driver():
    """Initialize Chrome driver with necessary options"""
    options = webdriver.ChromeOptions()
    # Comment out headless mode for debugging
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)

def get_place_url(place_name):
    """Convert place name to Google Maps search URL format"""
    return f"https://www.google.com/maps/search/{place_name.replace(' ', '+')}/"

def scroll_reviews(driver, wait, total_reviews):
    """Scroll through all reviews to load them"""
    try:
        # Wait for the reviews container - this is the scrollable reviews panel
        reviews_container = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[class*="dS8AEf"]')))  # Updated selector for the reviews panel
        
        print(f"Total reviews to load: {total_reviews}")
        
        # Keep scrolling until we find all reviews or hit a limit
        max_attempts = 20
        attempt = 0
        last_height = 0
        
        while attempt < max_attempts:
            # Get current number of loaded reviews
            current_reviews = len(driver.find_elements(By.CSS_SELECTOR, 'div[class*="jftiEf"]'))
            print(f"Currently loaded reviews: {current_reviews}")
            
            if current_reviews >= total_reviews:
                print("All reviews loaded successfully")
                break
            
            # Scroll the reviews panel
            current_height = driver.execute_script(
                'return arguments[0].scrollHeight', reviews_container)
            
            if current_height == last_height:
                attempt += 1
            else:
                attempt = 0
                last_height = current_height
            
            # Scroll down the reviews panel
            driver.execute_script(
                'arguments[0].scrollTo(0, arguments[0].scrollHeight);', 
                reviews_container)
            
            time.sleep(2)
            
        if attempt >= max_attempts:
            print("Warning: Could not load all reviews after maximum attempts")
            
    except Exception as e:
        print(f"Error while scrolling: {str(e)}")

def extract_reviews(driver):
    """Extract all review information"""
    reviews = []
    review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="section-review ripple"]')
    
    for review in review_elements:
        try:
            # Extract review data
            author = review.find_element(By.CSS_SELECTOR, 'div[class*="section-review-title"]').text
            
            try:
                rating = len(review.find_elements(By.CSS_SELECTOR, 'span[class*="section-review-stars"] span'))
            except:
                rating = "N/A"
                
            try:
                relative_time = review.find_element(By.CSS_SELECTOR, 'span[class*="section-review-publish-date"]').text
            except:
                relative_time = "N/A"
                
            try:
                text = review.find_element(By.CSS_SELECTOR, 'span[class*="section-review-text"]').text
            except:
                text = ""
            
            reviews.append({
                'author_name': author,
                'rating': rating,
                'relative_time': relative_time,
                'text': text.replace('\n', ' ')
            })
            
        except Exception as e:
            print(f"Error extracting review: {e}")
            continue
            
    return reviews

def save_reviews_to_csv(place_name, reviews):
    """Save reviews to CSV file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{place_name}_reviews_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['author_name', 'rating', 'relative_time', 'text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for review in reviews:
                writer.writerow(review)
        print(f"Reviews successfully saved to {filename}")
        print(f"Total reviews saved: {len(reviews)}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def get_all_reviews(place_name):
    driver = initialize_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        # Navigate to search results
        driver.get(get_place_url(place_name))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        
        # Click first result (using existing selectors)
        result_selectors = [
            'a[class*="place-result"]',
            'div[class*="place-result"]',
            'div[role="article"]',
            'a[href*="/place/"]'
        ]
        
        for selector in result_selectors:
            try:
                first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                first_result.click()
                print("Successfully clicked search result")
                time.sleep(3)
                break
            except:
                continue

        total_reviews = 0
        more_reviews_element = None
        
        # Try to find "More reviews" button and get total count
        more_reviews_selectors = [
            'span.wNNZR.fontTitleSmall',
            'button[aria-label*="More reviews"]',
            'button[aria-label*="reviews"]',
            'span[class*="fontTitleSmall"]',
            '//span[contains(text(), "More reviews")]',
            '//button[contains(., "More reviews")]'
        ]

        for selector in more_reviews_selectors:
            try:
                if selector.startswith('//'):
                    element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                else:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                
                more_reviews_text = element.text
                match = re.search(r'\((\d+)\)', more_reviews_text)
                if match:
                    total_reviews = int(match.group(1))
                    more_reviews_element = element
                    print(f"Found reviews button with {total_reviews} total reviews")
                    break
            except Exception as e:
                continue

        if total_reviews == 0:
            print("Could not determine total number of reviews")
            return

        # Click the found element
        try:
            more_reviews_element.click()
        except:
            driver.execute_script("arguments[0].click();", more_reviews_element)

        print("Successfully clicked More reviews button")
        time.sleep(3)

        # Now scroll through all reviews
        scroll_reviews(driver, wait, total_reviews)

        # Rest of your code remains the same
        reviews = []
        review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="jftiEf"]')
        
        for review in review_elements:
            try:
                author = review.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                rating = len(review.find_elements(By.CSS_SELECTOR, 'span[aria-label*="stars"]'))
                time_element = review.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
                
                # Try to find and click "More" button if it exists
                try:
                    more_button = review.find_element(By.CSS_SELECTOR, 'button.w8nwRe.kyuRq')
                    driver.execute_script("arguments[0].click();", more_button)
                    time.sleep(0.5)  # Short wait for text to expand
                except:
                    pass  # No "More" button found, review is already fully expanded
                
                # Get the full text after potentially expanding it
                try:
                    text = review.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                except:
                    text = "No comment provided"  # Default text for reviews without comments
                
                reviews.append({
                    'author_name': author,
                    'rating': rating,
                    'relative_time': time_element,
                    'text': text.replace('\n', ' ')
                })
            except Exception as e:
                print(f"Error extracting review: {str(e)}")
                continue

        if reviews:
            save_reviews_to_csv(place_name, reviews)
        else:
            print("No reviews were found in the current view")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def main():
    place_name = input("Enter place name to search: ") or "Xsolla"
    get_all_reviews(place_name)

if __name__ == "__main__":
    main() 