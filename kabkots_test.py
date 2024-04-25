from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os

def create_folder_if_not_exists(folder_path):
    """Create a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def main():
    # Setting up the driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Url
    url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52'
    driver.get(url)

    # Folder path
    base_dir = r'C:\Users\prata\PycharmProjects\KPU_C1_form\C1_form1'

    try:
        # Wait for table to be present
        table = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "table")))

        # Find kabkots links within the table
        kabkots = table.find_elements(By.TAG_NAME, "a")

        kabkots_list = []

        for kabkot in kabkots:
            # Kabupaten dan Kota
            kabkot_href = kabkot.get_attribute('href')
            kabkot_text = kabkot.text
            print(f'href: {kabkot_href}')
            print(f'kabupaten/kota: {kabkot_text}')
            kabkots_list.append({'kabkot_text': kabkot_text, 'kabkot_href': kabkot_href})

            # Create folder based on kabkot_text
            folder_name = kabkot_text.strip().replace(' ', '_')
            folder_path = os.path.join(base_dir, folder_name)
            create_folder_if_not_exists(folder_path)

        print(kabkots_list)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()