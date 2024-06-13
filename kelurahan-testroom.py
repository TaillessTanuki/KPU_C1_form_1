from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os


# Function to download image
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


def main():
    # Initialize WebDriver
    driver = webdriver.Chrome()

    # Navigate to the page
    url = 'https://pemilu2024.kpu.go.id/pilpres/hitung-suara/52/5206/520602/5206022007'
    driver.get(url)

    # Collect hrefs and span texts from the page
    href_span_pairs = [(element.get_attribute("href"), element.text) for element in
                       driver.find_elements(By.XPATH, "//a[@href]")]

    # Create a directory to store images
    os.makedirs("images", exist_ok=True)

    # Iterate over href-span pairs
    for href, span_text in href_span_pairs:
        # Navigate to the page
        driver.get(href)

        # Find the img tag with alt="Form C1 image"
        img_elements = driver.find_elements(By.XPATH, "//img[@alt='Form C1 image']")

        print(span_text)

        # # Iterate over img elements
        # for i, img_element in enumerate(img_elements, start=1):
        #     # Extract source URL of the image
        #     img_src = img_element.get_attribute("src")
        #
        #     # Construct filename based on span texts combined
        #     filename = os.path.join("images", f"{span_text}_image_{i}.jpg")
        #
        #     # Download the image
        #     download_image(img_src, filename)
        #     print(f"Downloaded image {i}: {filename}")

    # Close the WebDriver
    driver.quit()


if __name__ == "__main__":
    main()
