import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver

def extract_bama_cars():
    options = webdriver.ChromeOptions()
    
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print("Chrome WebDriver error. Make sure Google Chrome is installed.")
        return []

    url = "https://bama.ir/car/samand/all-models/all-trims?year=1386-0"
    driver.get(url)
    time.sleep(7) 

    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(2.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    results = []
    seen_texts = set()

    links = soup.find_all('a')
    for link in links:
        text = link.get_text(separator='|', strip=True)
        if 'سمند' in text and ('تومان' in text or 'توافقی' in text):
            if text in seen_texts:
                continue
            seen_texts.add(text)
            
            parts = text.split('|')
            price = "N/A"
            mileage = "N/A"
            year = "1386"
            desc = parts[0]
            
            for part in parts:
                if 'تومان' in part or 'توافقی' in part:
                    price = part
                elif 'کیلومتر' in part:
                    mileage = part
                elif part.isdigit() and len(part) == 4:
                    year = part
                    
            results.append({
                'Price': price,
                'Mileage': mileage,
                'Production Year': year,
                'Color': "Check Ad",
                'Transmission': "Manual",
                'Description': desc
            })
            
            if len(results) >= 50:
                break

    return results

if __name__ == "__main__":
    print("Launching automated browser...")
    data = extract_bama_cars()
    if data:
        df = pd.DataFrame(data)
        df.to_excel('samand_data.xlsx', index=False)
        print(f"Extracted {len(df)} cars and saved to samand_data.xlsx")
    else:
        print("Extraction failed. Check your internet connection or run again.")