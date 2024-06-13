# Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time
import os
import csv


# Function to download image
def download_image(tps):

    print('entering def donwload_image')
    # Set up driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(tps)

    time.sleep(4)

    # Find the img tag with alt="Form C1 image"
    img_elements = driver.find_elements(By.XPATH, "//img[@alt='Form C1 image']")
    print(f'img_elements: {img_elements}')

    # Locate span tags 3 to 7
    span_tags = driver.find_elements(By.TAG_NAME, "span")

    # Extract text from each span tag
    span_texts = [span.text.strip() for span in span_tags]
    print(f'span_texts: {span_texts}')

    # Iterate over img elements
    for i, img_element in enumerate(img_elements, start=1):

        # time.sleep(3)  # Wait for 3 seconds

        # Extract source URL of the image
        img_src = img_element.get_attribute("src")

        # Construct filename based on span texts combined
        filename = os.path.join("images", f"{span_texts}_image_{i}.jpg")

        # Download the image
        response = requests.get(img_src)
        print(f"Downloading image {i}: {filename}")
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded image {i}: {filename}")


def href_list(elements):
    href_listr = []  # Create an empty list to store href values
    for element in elements:
        # Get tps href
        href = element.get_attribute('href')
        print(f'href: {href}')
        href_listr.append(href)  # Append href to href_listr, not href_list

    return href_listr


def main_kelurahan(url_kelurahan):
    # Setting up the driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Url
    # url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52/5206/520602/5206022007'
    driver.get(url_kelurahan)

    try:
        # Wait for table to be present (using time.sleep instead of EC)
        time.sleep(3)  # Wait for 5 seconds
        table = driver.find_element(By.TAG_NAME, "table")

        # Find href links within the table
        tpss = table.find_elements(By.TAG_NAME, "a")
        print(tpss)
        tps_href_list = href_list(tpss)

        # Create a directory to store images
        os.makedirs("images", exist_ok=True)

        print('Lets Start')

        for tps in tps_href_list:
            download_image(tps)
            print(f'putaran ke: {tps}')
            # time.sleep(7)

        print('done')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()


url_kelurahan = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52/5206/520602/5206022007'

if __name__ == "__main__":
    main_kelurahan(url_kelurahan)
