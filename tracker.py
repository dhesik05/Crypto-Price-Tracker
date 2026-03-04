import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --------------------------------
# Setup Chrome
# --------------------------------
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment if you want no browser window

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# --------------------------------
# Open Website
# --------------------------------
url = "https://coinmarketcap.com/"
driver.get(url)

# Wait until table loads properly
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))

# --------------------------------
# Scrape Top 10 Coins
# --------------------------------
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")

data = []

for row in rows[:10]:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) >= 8:
        name = cols[2].text
        price = cols[3].text
        change_24h = cols[4].text
        market_cap = cols[7].text

        data.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Coin": name,
            "Price": price,
            "24h Change": change_24h,
            "Market Cap": market_cap
        })

driver.quit()

# --------------------------------
# Convert to DataFrame
# --------------------------------
df = pd.DataFrame(data)

print("Total coins scraped:", len(df))
print(df)

# --------------------------------
# Save Files Only If Data Exists
# --------------------------------
if not df.empty:
    df.to_csv("crypto_prices.csv", index=False)
    df.to_excel("crypto_prices.xlsx", index=False)
    print("Crypto data saved successfully!")
else:
    print("No data scraped. File not created.")
