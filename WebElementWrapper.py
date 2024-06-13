from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import os
import time

class WebElementWrapper:
    def __init__(self, driver, by, value):
        self.driver = driver
        self.by = by
        self.value = value
        self.element = None

    def find(self):
        try:
            self.element = self.driver.find_element(self.by, self.value)
            return self.element
        except:
            print("Element not found")
            return None

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
        time.sleep(5)  # Wait for 5 seconds to ensure the table is loaded
        table_wrapper = WebElementWrapper(driver, By.TAG_NAME, "table")
        table = table_wrapper.find()

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

                # Wait for the page to load (you can adjust the sleep time accordingly)
                time.sleep(5)  # Wait for 5 seconds to ensure the page is loaded

                # Find kecs links within the page
                kecs_wrapper = WebElementWrapper(driver, By.TAG_NAME, "a")
                kecs = kecs_wrapper.find()
                if kecs:
                    kecs_list = []
                    kecs = [kecs] if not isinstance(kecs, list) else kecs  # Ensure kecs is a list
                    for kec in kecs:
                        kec_href = kec.get_attribute('href')
                        kec_text = kec.text
                        kecs_list.append({'kec_text': kec_text, 'kec_href': kec_href})
                    print(kecs_list)  # Print kecs_list for debugging
                    # You can append kecs_list to kabkots_list or perform any other actions here
                else:
                    print("No kecs found")

                break

        print(kabkots_list)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
