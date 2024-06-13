# Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from kelurahan import main_kelurahan
from kelurahan import href_list
from kabupaten import main_kabupaten

import time
import os


# Record the start time
start_time = time.time()


def main(url_provinsi):
    # Setting up the driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Url
    # provinsi PARADO
    # url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52/5206/520616'
    driver.get(url_provinsi)
    time.sleep(2)


    try:
        # Wait for table to be present (using time.sleep instead of EC)
        table = driver.find_element(By.TAG_NAME, "table")

        # Find provinsi links within the table
        provinsis = table.find_elements(By.TAG_NAME, "a")
        print(provinsis)
        provinsi_href_list = href_list(provinsis)
        print(provinsi_href_list)

        for provinsi in provinsi_href_list:
            main_kabupaten(provinsi)
            print(f'putaran ke: {provinsi}')
            # time.sleep(7)



    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()


# Provinsi DKI Jakarta
url_provinsi = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/31'

if __name__ == "__main__":
    main(url_provinsi)



# Record the end time
end_time = time.time()

# Calculate the duration in seconds
duration = end_time - start_time

# Convert the duration to hours, minutes, and seconds
hours = int(duration // 3600)
minutes = int((duration % 3600) // 60)
seconds = int(duration % 60)

# Print the duration
print(f"Script execution time: {hours} hours, {minutes} minutes, {seconds} seconds")





