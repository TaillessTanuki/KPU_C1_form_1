# Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os

# Setting up the driver
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Url
url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52'
driver.get(url)

# Folder path
base_dir = r'C:\Users\prata\PycharmProjects\KPU_C1_form\C1_form1'

# Table kabupaten/kota NTB
table = driver.find_element(By.TAG_NAME, "table")
kabkots = table.find_elements(By.TAG_NAME, "a")

# kabkots = WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "a")))

kabkots_list = []


for kabkot in kabkots:
    # Kabupaten dan Kota
    print('WENZ BENZ')
    kabkot_href = kabkot.get_attribute('href')
    print(f'href: {kabkot_href}')

    kabkot_text = kabkot.text
    print(f'kabupaten/kota: {kabkot_text}')
    # print(f"Text: {text}, Href: {href}")

    kabkots_list.append({'kabkot_text': kabkot_text, 'kabkot_href': kabkot_href})

    # Make folders based on kabupaten and kota
    print('Is he Ill Sludge')
    folder_name = kabkot_text.strip().replace(' ', '_')  # Replace spaces with underscores
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


print(kabkots_list)



# print(kabkots_list)

# Exit the chrome
time.sleep(10)
driver.quit()