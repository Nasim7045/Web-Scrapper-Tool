import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Function to extract emails from text
def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Regex for email
    return re.findall(email_pattern, text)

# Function to scrape a website
def scrape_website(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract emails from page
        text_content = soup.get_text()
        emails = extract_emails(text_content)
        
        # Extract company name (from title or header tags)
        title = soup.find("title").text.strip() if soup.find("title") else "Unknown"
        
        return {"Website": url, "Company Name": title, "Emails": ", ".join(set(emails))}
    else:
        return {"Website": url, "Company Name": "Failed to load", "Emails": "N/A"}

# Function to process multiple websites
def scrape_multiple_websites(url_list):
    results = []
    for url in url_list:
        print(f"Scraping: {url}")
        data = scrape_website(url)
        results.append(data)
        time.sleep(2)  # Delay to avoid getting blocked
    return results

# List of websites to scrape
website_list = [
    "https://nasimkhan-portfolio.netlify.app/#home",
]

# Scraping websites
data = scrape_multiple_websites(website_list)

# Save results to CSV
output_df = pd.DataFrame(data)
output_df.to_csv("lead_generation_results.csv", index=False)
print("Scraping completed! Data saved to lead_generation_results.csv")
