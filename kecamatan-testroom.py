# Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os


def main():
    # Setting up the driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Url
    url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52'
    driver.get(url)

    # Create a directory to store images
    os.makedirs("images", exist_ok=True)

    try:
        # Wait for table to be present (using time.sleep instead of EC)
        time.sleep(5)  # Wait for 5 seconds
        table = driver.find_element(By.TAG_NAME, "table")

        # Find kabkots links within the table
        kabkots = table.find_elements(By.TAG_NAME, "a")

        kabkots_list = []

        if not kabkots:
            print("No kabkots found")
        else:
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

                # Navigate to kabkot_href
                driver.get(kabkot_href)

                # Find kecs links within the page
                kecs = driver.find_elements(By.TAG_NAME, "a")
                kecs_list = []
                for kec in kecs:
                    kec_href = kec.get_attribute('href')
                    kec_text = kec.text
                    kecs_list.append({'kec_text': kec_text, 'kec_href': kec_href})
                print(kecs_list)  # Print kecs_list for debugging
                # You can append kecs_list to kabkots_list or perform any other actions here

        print(kabkots_list)



    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()







