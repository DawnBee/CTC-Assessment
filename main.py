from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Setup WebDriver with ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://bizfileonline.sos.ca.gov/search/business")

# Create a WebDriverWait instance with an increased wait time
wait = WebDriverWait(driver, 20)

# Wait for the table to be loaded
try:
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "div-table-heading")))
except TimeoutException:
    print("Timeout: Table header not found within the specified time.")

# Extract table rows (excluding header)
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")  # Adjust XPath to match your table's structure
extracted_data = []

# Extracting the data from each row
for row in rows:
    try:
        entity_info = row.find_element(By.XPATH, ".//td[1]").text
        initial_filing_date = row.find_element(By.XPATH, ".//td[2]").text
        status = row.find_element(By.XPATH, ".//td[3]").text
        entity_type = row.find_element(By.XPATH, ".//td[4]").text
        formed_in = row.find_element(By.XPATH, ".//td[5]").text
        agent = row.find_element(By.XPATH, ".//td[6]").text
        
        # Append extracted data to the list
        extracted_data.append([entity_info, initial_filing_date, status, entity_type, formed_in, agent])
    except Exception as e:
        print(f"Error extracting data from row: {e}")

# Save the extracted data to a CSV file
with open("outputs.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Writing headers
    writer.writerow([
        "Entity Information", "Initial Filing Date", "Status", 
        "Entity Type", "Formed In", "Agent"
    ])
    
    # Writing the extracted data
    writer.writerows(extracted_data)

# Close the driver when done
driver.quit()
