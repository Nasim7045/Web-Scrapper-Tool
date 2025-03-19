import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Function to extract emails
def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(email_pattern, text)))

# Function to extract phone numbers
def extract_phone_numbers(text):
    phone_pattern = r"\+?\d{1,4}[\s-]?\(?\d{1,4}\)?[\s-]?\d{2,4}[\s-]?\d{2,4}"
    return list(set(re.findall(phone_pattern, text)))

# Function to extract addresses (basic street address pattern)
def extract_addresses(text):
    address_pattern = r"\d{1,5}\s\w+(\s\w+){1,5},?\s\w+,\s\w{2,}\s\d{5}"
    return list(set(re.findall(address_pattern, text)))

# Function to scrape data from website
def scrape_website(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"Website": url, "Status": "Failed", "Error": str(e)}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title = soup.find("title").text.strip() if soup.find("title") else "Unknown"

    # Extract all text from the page
    text_content = soup.get_text(separator=" ", strip=True)

    # Extract emails
    emails = extract_emails(text_content)

    # Extract phone numbers
    phone_numbers = extract_phone_numbers(text_content)

    # Extract addresses
    addresses = extract_addresses(text_content)

    # Extract links from <a> tags
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # Extract possible names from headers
    names = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"]) if len(h.text.strip()) > 2]

    return {
        "Website": url,
        "Title": title,
        "Emails": ", ".join(emails) if emails else "N/A",
        "Phone Numbers": ", ".join(phone_numbers) if phone_numbers else "N/A",
        "Addresses": ", ".join(addresses) if addresses else "N/A",
        "Links": ", ".join(links[:5]) if links else "N/A",  # Limit links to 5 for display
        "Names": ", ".join(names[:5]) if names else "N/A"  # Limit names to 5 for display
    }

# Streamlit UI
st.set_page_config(page_title="Web Scraper", layout="wide")
st.title("🔍 Web Scraper Tool")
st.write("Enter a website URL below to extract useful information.")

# User input
url = st.text_input("Enter Website URL", "https://nasimkhan-portfolio.netlify.app/#home")

if st.button("Scrape"):
    with st.spinner("Scraping... Please wait..."):
        data = scrape_website(url)

    if "Error" in data:
        st.error(f"❌ Error: {data['Error']}")
    else:
        st.success("✅ Scraping Completed!")

        # Display extracted data
        st.write("### Extracted Data")
        st.json(data)

        # Convert to DataFrame for CSV download
        df = pd.DataFrame([data])

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "scraped_data.csv", "text/csv", key="download-csv")
