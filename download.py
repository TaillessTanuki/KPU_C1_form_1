def download_image(tps):

    print('entering def donwload_image')
    # Set up driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(tps)

    time.sleep(3)

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






def download_image(tps):

    print('entering def download_image')
    # Set up driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(tps)

    time.sleep(3)

    # Find the img tag with alt="Form C1 image"
    img_elements = driver.find_elements(By.XPATH, "//img[@alt='Form C1 image']")
    print(f'img_elements: {img_elements}')

    # Locate span tags 3 to 7
    span_tags = driver.find_elements(By.TAG_NAME, "span")

    # Extract text from each span tag
    span_texts = [span.text.strip() for span in span_tags]
    print(f'span_texts: {span_texts}')

    # Check if img_elements is empty (no image found)
    if not img_elements:
        # Use the "not found" image from environment
        img_not_found_path = os.getenv("IMG_NOT_FOUND_PATH", "img_not_found.jpg")
        not_found_filename = f"{span_texts[0]}_image_not_found.jpg"  # Using only the first span text for filename
        filename = os.path.join("images", not_found_filename)

        # Copy the "not found" image to the specified filename
        with open(img_not_found_path, 'rb') as src, open(filename, 'wb') as dest:
            dest.write(src.read())

        print(f"No image found. Saved not found image as: {filename}")
    else:
        # Iterate over img elements
        for i, img_element in enumerate(img_elements, start=1):
            # Extract source URL of the image
            img_src = img_element.get_attribute("src")

            # Construct filename based on span texts combined
            filename = os.path.join("images",
                                    f"{span_texts[0]}_image_{i}.jpg")  # Using only the first span text for filename

            # Download the image
            response = requests.get(img_src)
            print(f"Downloading image {i}: {filename}")
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded image {i}: {filename}")



def download_image(tps):

    print('entering def donwload_image')
    # Set up driver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(tps)

    time.sleep(3)

    # Find the img tag with alt="Form C1 image"
    img_elements = driver.find_elements(By.XPATH, "//img[@alt='Form C1 image']")
    print(f'img_elements: {img_elements}')

    # Locate span tags 3 to 7
    span_tags = driver.find_elements(By.TAG_NAME, "span")

    # Extract text from each span tag
    span_texts = [span.text.strip() for span in span_tags]
    print(f'span_texts: {span_texts}')

    if img_elements:
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

    else:
        # Use the "not found" image from environment
        img_not_found_path = os.getenv("IMG_NOT_FOUND_PATH", "img_not_found.jpg")
        not_found_filename = f"{span_texts}_image_not_found.jpg"  # Using only the first span text for filename
        filename = os.path.join("images", not_found_filename)

        # Copy the "not found" image to the specified filename
        print(f"No image found.")
        with open(img_not_found_path, 'rb') as src, open(filename, 'wb') as dest:
            dest.write(src.read())
        print(f"No image found.")