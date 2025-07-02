import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import re
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

url = 'https://www.esjzone.cc/forum/1748654870/add.html'
folder_path = r"D:\成為黑暗大海的燈光"

# Set up Firefox options
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Initialize the WebDriver
driver = webdriver.Firefox(options=options)
driver.get('https://www.esjzone.cc/my/login')

# --- File Filtering and Data Extraction ---
def get_matching_files(folder_path):
    """
    Filters files ending with _MMDD HHMI.txt and returns a sorted list of their details.
    Returns a list of tuples: (full_file_path, month, day, hour, minute).
    """
    pattern = re.compile(r'_(\d{2})(\d{2}) (\d{2})(\d{2})\.txt$')
    matching_files_details = []

    for filename in os.listdir(folder_path):
        match = pattern.search(filename)
        if match:
            full_file_path = os.path.join(folder_path, filename)
            month_str, day_str, hour_str, minute_str = match.groups()
            matching_files_details.append((full_file_path, int(month_str), int(day_str), int(hour_str), int(minute_str)))

    # Sort files by their full path (which includes MMDD HHMI) to ensure consistent order
    matching_files_details.sort()
    return matching_files_details

def extract_data_from_single_file(file_path, month, day, hour, minute):
    """
    Extracts subject and content from a given file path.
    Returns subject, content, or None if an error occurs.
    """
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                print(f"File {os.path.basename(file_path)} is empty.")
                return None, None

            subject = lines[0].strip()
            content = "".join(lines[1:]).strip() # Content is everything after the first line

            return subject, content

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None, None

# --- Selenium Automation ---

def fill_and_submit_form(driver, subject, content, month, day, hour, minute):
    """
    Fills out the form on the provided HTML page using Selenium and JavaScript.
    """
    try:
        # Navigate to the form page for each submission
        driver.get(url)
        print(f"Navigated to {url}")

        # 1. Subject
        subject_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "subject"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", subject_input, subject)
        print("Subject filled.")

        # 2. Content (Froala Editor)
        content_editor_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#artEditor .fr-element.fr-view"))
        )

        escaped_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html_content = escaped_content.replace('\n', '<br>')
        
        driver.execute_script("arguments[0].innerHTML = arguments[1];", content_editor_div, html_content)
        print("Content filled in editor with all newlines converted to <br>.")

        # Also update the hidden input 'content'
        # This hidden input is usually updated by the Froala editor's own JavaScript
        # but explicitly setting it can be a good fallback if the editor doesn't immediately sync.
        hidden_content_input = driver.find_element(By.NAME, "content")
        driver.execute_script("arguments[0].value = arguments[1];", hidden_content_input, html_content)
        print("Hidden content input updated with HTML content.")
    
        # 3. Select "符號轉換:" to "否" (value="0")
        marks_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "marks"))
        )
        driver.execute_script("arguments[0].value = '0';", marks_select)
        print("'符號轉換:' set to '否'.")

        # 4. Set "預約發文:" date (reserve)
        current_year = datetime.now().year
        reserve_date_str = f"{current_year}-{month:02d}-{day:02d}"

        reserve_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "reserve"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", reserve_input, reserve_date_str)
        driver.execute_script("$(arguments[0]).trigger('change');", reserve_input) # Trigger change event for datepicker
        print(f"'預約發文:' date set to {reserve_date_str}.")

        # 5. Set "預約發文:" hour
        hour_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hour"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", hour_select, f"{hour:02d}")
        print(f"'預約發文:' hour set to {hour:02d}.")

        # 6. Set "預約發文:" minute
        min_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "min"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", min_select, f"{minute:02d}")
        print(f"'預約發文:' minute set to {minute:02d}.")

        # 7. Submit the form
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-send[data-form='artEditor']"))
        )
        driver.execute_script("arguments[0].click();", submit_button)
        print("Form submitted.")

        # Add a small delay to observe the submission or wait for a success message
        time.sleep(10) # Shorter sleep after each submission
        print(f"Finished processing and submitting form for: {subject[:30]}...")
        return True

    except Exception as e:
        print(f"An error occurred during form filling/submission for file: {subject[:30]}... Error: {e}")
        # Optionally, take a screenshot on error
        # driver.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        return False


# --- Main Execution ---
if __name__ == "__main__":
    if driver is None:
        print("WebDriver was not initialized. Exiting.")
        exit()

    all_files_details = get_matching_files(folder_path)

    if not all_files_details:
        print(f"No files matching the pattern '_MMDD HHMI.txt' found in {folder_path}")
    else:
        print(f"Found {len(all_files_details)} matching files.")
        for i, (file_path, month, day, hour, minute) in enumerate(all_files_details):
            print(f"\n--- Processing file {i+1}/{len(all_files_details)}: {os.path.basename(file_path)} ---")
            subject, content = extract_data_from_single_file(file_path, month, day, hour, minute)

            if all([subject, content, month is not None, day is not None, hour is not None, minute is not None]):
                print("Data extracted successfully:")
                print(f"Subject: {subject[:50]}...")
                print(f"Content length: {len(content)}")
                print(f"Schedule: {month:02d}/{day:02d}, {hour:02d}:{minute:02d}")
            
                success = fill_and_submit_form(driver, subject, content, month, day, hour, minute)
                if success:
                    print(f"Successfully processed {os.path.basename(file_path)}")
                else:
                    print(f"Failed to process {os.path.basename(file_path)}")
                
                # Add a pause between submissions if needed, e.g., to avoid overwhelming the server
                time.sleep(5) 
            else:
                print(f"Could not extract all necessary data from {os.path.basename(file_path)}. Skipping form submission for this file.")

    print("\nAll files processed or skipped.")
    # Ensure the browser is closed after all processing is done
    if driver:
        driver.quit()
        print("WebDriver closed.")
