import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar  # You'll need to add this to requirements.txt

import numpy as np

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def login_x(target_date, desired_times, retry_interval):
    """
    Try to book fitness slots at the specified times on the target date.

    Args:
        target_date (datetime): Date to book for (time component is ignored)
        desired_times (list): List of times to try booking in order of preference
                            Format: ["09:00", "10:30", "12:00"]
    """
    # Format date for the date picker
    date_str = target_date.strftime("%Y-%m-%d")

    # Load environment variables
    load_dotenv()
    username = os.getenv('TU_USERNAME')
    password = os.getenv('TU_PASSWORD')

    # Initialize Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    # Add headless mode options
    chrome_options.add_argument("--headless=new")  # new headless mode for Chrome v109+
    chrome_options.add_argument("--window-size=1920,1080")  # Set a standard resolution
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")  # Recommended for headless

    # Initialize the webdriver with webdriver-manager
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    while True:
        try:
            # If driver is not responding, restart it
            try:
                driver.current_url
            except:
                print("Browser seems unresponsive, restarting...")
                driver.quit()
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=chrome_options
                )

            # Navigate to the website
            print("Navigating to x.tudelft.nl...")
            driver.get('https://x.tudelft.nl')

            # Wait for and click the TU Delft button
            print("Waiting for TU Delft button...")
            wait = WebDriverWait(driver, 20)
            try:
                tu_delft_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[data-test-id='oidc-login-button']")))
                print("Found TU Delft button")
                tu_delft_button.click()
                print("Clicked TU Delft button")
            except Exception as e:
                print(f"Error with TU Delft button: {str(e)}")
                # Let's try to print the page source to see what's actually there
                print("Current page HTML:")
                # Print first 500 chars of page source
                print(driver.page_source[:500])
                raise  # Re-raise the exception to trigger our retry logic

            # Select "Delft University of Technology" account
            tu_delft_account = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[data-title='Delft University of Technology']")))
            tu_delft_account.click()
            print("Clicked TU Delft account")
            # Wait for login elements and login
            username_field = wait.until(
                EC.presence_of_element_located((By.ID, 'username')))
            password_field = driver.find_element(By.ID, 'password')

            username_field.send_keys(username)
            password_field.send_keys(password)
            print("Sent username and password")
            # Find and click login button
            login_button = driver.find_element(By.ID, 'submit_button')
            login_button.click()
            print("Clicked login button")

            # Wait for date picker to be present and interactable
            date_picker = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input.datepicker-input[type='date']"))
            )
            # Wait until it's not disabled/readonly
            wait.until(lambda d: date_picker.get_attribute("readonly") is None)

            # Set the date value using JavaScript to ensure correct format
            driver.execute_script(
                "arguments[0].value = arguments[1]",
                date_picker,
                date_str
            )
            print(f"Set date to {date_str}")

            # Trigger change event to ensure the page updates
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change', { 'bubbles': true }))",
                date_picker
            )
            print(f"Date change event dispatched")

            # Wait for the page to update with the new date
            time.sleep(1)

            # Type "Fitness" into the filter input
            filter_input = wait.until(
                EC.presence_of_element_located((By.ID, 'tag-filterinput')))
            filter_input.clear()
            filter_input.send_keys("Fitness")
            print("Sent Fitness")

            # Select the Fitness checkbox
            fitness_checkbox = wait.until(
                EC.element_to_be_clickable((By.ID, 'tagCheckbox28')))
            fitness_checkbox.click()
            print("Clicked Fitness checkbox")

            # Press Escape to close the filter popup
            filter_input.send_keys(Keys.ESCAPE)
            print("Pressed Escape to close filter")

            # Wait for fitness slots to load and be interactive
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@data-test-id='bookable-slot-list']")))
            print("Fitness slots loaded")

            # Try to ensure the page is in a stable state
            driver.execute_script("window.scrollTo(0, 0)")  # Scroll to top
            time.sleep(1)  # Let the page settle

            # Look for slots matching desired times in order
            for desired_time in desired_times:
                print(f"Trying to book slot for {desired_time}")
                # Find all slots for this time
                time_slots = driver.find_elements(
                    By.XPATH,
                    f"//p[@data-test-id='bookable-slot-start-time'][.//strong[contains(text(), '{desired_time}')]]"
                )
                print(f"Found {len(time_slots)} slots for {desired_time}")

                # For each time slot, find its parent container and check if it's available
                available_slots = [
                    slot.find_element(
                        By.XPATH, "ancestor::div[@data-test-id='bookable-slot-list']")
                    for slot in time_slots
                    if not (
                        'opacity-50' in slot.find_element(
                            By.XPATH, "ancestor::div[@data-test-id='bookable-slot-list']").get_attribute('class')
                        or slot.find_element(By.XPATH, "ancestor::div[@data-test-id='bookable-slot-list']").find_elements(By.XPATH, ".//div[@data-test-id='bookable-slot-spots-full']")
                    )
                ]
                print(
                    f"Found {len(available_slots)} available slots for {desired_time}")

                if available_slots:
                    try:
                        # Find and click the book button within the slot container
                        book_button = wait.until(EC.element_to_be_clickable(available_slots[0].find_element(
                            By.XPATH,
                            ".//button[@data-test-id='bookable-slot-book-button']"
                        )))
                        print("Found book button")

                        # Try to ensure no overlays are present
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", book_button)
                        time.sleep(1)  # Wait for any overlays to clear

                        # Try clicking via JavaScript if regular click fails
                        try:
                            book_button.click()
                        except:
                            driver.execute_script(
                                "arguments[0].click();", book_button)
                        print("Clicked book button")

                        # Wait for and click the confirm booking button
                        confirm_button = wait.until(EC.element_to_be_clickable(
                            (By.XPATH,
                             "//button[@data-test-id='details-book-button']")
                        ))

                        # Scroll the confirm button to the middle of the viewport
                        driver.execute_script("""
                            var element = arguments[0];
                            var elementRect = element.getBoundingClientRect();
                            var absoluteElementTop = elementRect.top + window.pageYOffset;
                            var middle = absoluteElementTop - (window.innerHeight / 2);
                            window.scrollTo(0, middle);
                        """, confirm_button)

                        confirm_button.click()
                        print("Clicked confirm button")

                        print(
                            f"Successfully booked a slot for {desired_time}!")
                        driver.quit()
                        return True

                    except Exception as e:
                        print(f"Error booking {desired_time}: {str(e)}")
                        continue
                else:
                    print(f"No available slots for {desired_time}")

            print(
                f"No slots available at any of the desired times. Trying again in {retry_interval} minutes...")
            raise NoAvailableSlotsError(
                "No slots available at any of the desired times")

        except Exception as e:
            if isinstance(e, NoAvailableSlotsError):
                print(f"No available slots: {str(e)}")
                driver.quit()
                return False
            else:
                print(f"An error occurred: {str(e)}")
            try:
                driver.quit()
            except:
                pass

            return False


class NoAvailableSlotsError(Exception):
    pass


class BookingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fitness Slot Booking")
        self.root.geometry("500x700")

        # Date Selection
        self.cal = Calendar(self.root,
                          mindate=datetime.now(),
                          maxdate=datetime.now().replace(month=datetime.now().month + 3),
                          date_pattern='y-mm-dd')
        self.cal.pack(pady=20)

        # Add retry interval control
        retry_frame = ttk.LabelFrame(self.root, text="Retry Settings")
        retry_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(retry_frame, text="Retry Interval (minutes):").pack(side=tk.LEFT, padx=5)
        
        # Default retry interval is 5 minutes
        self.retry_interval = tk.StringVar(value="5")
        
        # Entry widget for retry interval with validation
        vcmd = (self.root.register(self.validate_interval), '%P')
        retry_entry = ttk.Entry(retry_frame, textvariable=self.retry_interval, 
                              width=5, validate='key', validatecommand=vcmd)
        retry_entry.pack(side=tk.LEFT, padx=5)

        # Time Selection
        time_frame = ttk.LabelFrame(self.root, text="Select Times")
        time_frame.pack(pady=20, padx=10, fill="x")

        # Available times with priority
        self.times = [
            "07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
            "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
            "19:00", "20:00", "21:00", "22:00", "23:00"
        ]

        # Create a frame for the list of selected times
        self.selected_frame = ttk.LabelFrame(
            self.root, text="Selected Times (Priority Order)")
        self.selected_frame.pack(pady=20, padx=10, fill="x")

        # Create checkboxes for times
        self.time_vars = {}
        for i, time in enumerate(self.times):
            var = tk.BooleanVar()
            self.time_vars[time] = var

            # Create frame for each time slot
            slot_frame = ttk.Frame(time_frame)
            slot_frame.grid(row=i//3, column=i % 3, padx=5, pady=2, sticky="w")

            # Add checkbox
            cb = ttk.Checkbutton(slot_frame, text=time, variable=var,
                                 command=lambda t=time: self.update_selected_times())
            cb.pack(side=tk.LEFT)

        # Selected times will be stored in order
        self.selected_times = []

        # Button frame for Book and Stop buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        # Book Button
        self.book_button = ttk.Button(button_frame, text="Book Selected Slots",
                                    command=self.start_booking)
        self.book_button.pack(side=tk.LEFT, padx=5)

        # Stop Button
        self.stop_button = ttk.Button(button_frame, text="Stop Retrying",
                                    command=self.stop_booking)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        # Add retry timer attribute
        self.retry_timer = None

    def update_selected_times(self):
        # Clear the selected frame
        for widget in self.selected_frame.winfo_children():
            widget.destroy()

        # Get currently selected times
        current_selected = [time for time,
                            var in self.time_vars.items() if var.get()]

        # Add new selections
        for time in current_selected:
            if time not in self.selected_times:
                self.selected_times.append(time)

        # Remove unselected times
        self.selected_times = [
            t for t in self.selected_times if t in current_selected]

        # Display selected times with up/down buttons
        for i, time in enumerate(self.selected_times):
            frame = ttk.Frame(self.selected_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)

            ttk.Label(frame, text=f"{i+1}. {time}").pack(side=tk.LEFT)

            if i > 0:  # Can move up
                ttk.Button(frame, text="↑", width=3,
                           command=lambda t=time: self.move_time_up(t)).pack(side=tk.RIGHT)
            if i < len(self.selected_times) - 1:  # Can move down
                ttk.Button(frame, text="↓", width=3,
                           command=lambda t=time: self.move_time_down(t)).pack(side=tk.RIGHT)

    def move_time_up(self, time):
        idx = self.selected_times.index(time)
        if idx > 0:
            self.selected_times[idx -
                                1], self.selected_times[idx] = self.selected_times[idx], self.selected_times[idx-1]
            self.update_selected_times()

    def move_time_down(self, time):
        idx = self.selected_times.index(time)
        if idx < len(self.selected_times) - 1:
            self.selected_times[idx], self.selected_times[idx +
                                                          1] = self.selected_times[idx+1], self.selected_times[idx]
            self.update_selected_times()

    def validate_interval(self, P):
        """Validate the retry interval input"""
        if P == "":
            return True
        try:
            value = int(P)
            return value > 0
        except ValueError:
            return False

    def start_booking(self):
        selected_date = self.cal.get_date()

        if not self.selected_times:
            self.status_label.config(text="Please select at least one time slot")
            return

        self.status_label.config(text="Starting booking process...")
        
        self.book_button.state(['disabled'])

        # Create date object (time will be ignored)
        target_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Start the booking process with prioritized times
        try:
            if login_x(target_date, self.selected_times, self.retry_interval.get()):
                self.status_label.config(text="Booking completed!")
                self.book_button.state(['!disabled'])
            else:
                # Get retry interval in minutes
                try:
                    interval = int(self.retry_interval.get())
                except ValueError:
                    interval = 5  # Default to 5 minutes if invalid input

                self.status_label.config(
                    text=f"No available slots, retrying in {interval} minutes...")
                
                # Schedule retry using after() with the custom interval
                if self.retry_timer:
                    self.root.after_cancel(self.retry_timer)
                self.retry_timer = self.root.after(interval * 60 * 1000, 
                                                 lambda: self.start_booking())
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.book_button.state(['!disabled'])

    def stop_booking(self):
        if self.retry_timer:
            self.root.after_cancel(self.retry_timer)
            self.retry_timer = None
            self.status_label.config(text="Booking stopped")
            self.book_button.state(['!disabled'])

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = BookingGUI()
    app.run()
