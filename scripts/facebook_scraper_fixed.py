import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import csv
import os

class FacebookScraper:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Scraper")
        self.root.geometry("800x600")

        # Variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.target_profile = tk.StringVar()
        self.driver = None
        self.scraped_data = []
        self.log_messages = []

        self.setup_ui()

    def setup_ui(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Login Credentials")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(input_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.username).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(input_frame, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.password, show="*").grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(input_frame, text="Target Profile:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.target_profile).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        input_frame.columnconfigure(1, weight=1)

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(button_frame, text="Start", command=self.start_scraping).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Export", command=self.export_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Export Log", command=self.export_log).pack(side="left", padx=5)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=5)

        # Text Area for Logs
        log_frame = ttk.LabelFrame(self.root, text="Logs")
        log_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_text = tk.Text(log_frame, height=15, wrap="word")
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def log(self, message):
        self.log_messages.append(message)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_scraping(self):
        if not self.username.get() or not self.password.get() or not self.target_profile.get():
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.log("Starting scraping process...")
        self.progress["value"] = 0

        # Run in separate thread to avoid freezing UI
        threading.Thread(target=self.scrape_thread, daemon=True).start()

    def scrape_thread(self):
        try:
            self.setup_driver()
            self.login()
            self.navigate_to_profile()
            self.scrape_followers()
            self.scrape_posts()
            self.log("Scraping completed successfully!")
        except Exception as e:
            self.log(f"Error during scraping: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
            self.progress["value"] = 100

    def setup_driver(self):
        self.log("Setting up Chrome driver...")
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--headless")  # Run in headless mode

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def login(self):
        self.log("Logging into Facebook...")
        self.driver.get("https://www.facebook.com")
        time.sleep(3)

        # Updated selectors (may need adjustment based on current Facebook layout)
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(self.username.get())

            password_field = self.driver.find_element(By.ID, "pass")
            password_field.send_keys(self.password.get())

            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()

            time.sleep(5)  # Wait for login to complete
            self.log("Login successful")
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")

    def navigate_to_profile(self):
        self.log(f"Navigating to profile: {self.target_profile.get()}")
        self.driver.get(f"https://www.facebook.com/{self.target_profile.get()}")
        time.sleep(3)

    def scrape_followers(self):
        self.log("Scraping followers...")
        try:
            # Updated selector - this may need to be adjusted
            followers_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
            )
            followers_link.click()
            time.sleep(3)

            # Scroll to load more followers
            for _ in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Updated selector for followers
            followers = self.driver.find_elements(By.XPATH, "//div[@data-visualcompletion='ignore-dynamic']//span[@dir='auto']")
            for follower in followers[:50]:  # Limit to first 50
                self.scraped_data.append({
                    "type": "follower",
                    "name": follower.text,
                    "url": follower.find_element(By.XPATH, "..").get_attribute("href") if follower.find_elements(By.XPATH, "..") else ""
                })
            self.log(f"Scraped {len(followers)} followers")
        except Exception as e:
            self.log(f"Error scraping followers: {str(e)}")

    def scrape_posts(self):
        self.log("Scraping posts...")
        try:
            # Updated selector for posts
            posts = self.driver.find_elements(By.XPATH, "//div[@data-ad-preview='message']")
            for post in posts[:20]:  # Limit to first 20
                self.scraped_data.append({
                    "type": "post",
                    "content": post.text,
                    "timestamp": ""  # Would need to find timestamp selector
                })
            self.log(f"Scraped {len(posts)} posts")
        except Exception as e:
            self.log(f"Error scraping posts: {str(e)}")

    def refresh_data(self):
        self.scraped_data = []
        self.log("Data refreshed")

    def export_data(self):
        if not self.scraped_data:
            messagebox.showwarning("Warning", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if file_path:
            if file_path.endswith(".json"):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            else:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    if self.scraped_data:
                        writer = csv.DictWriter(f, fieldnames=self.scraped_data[0].keys())
                        writer.writeheader()
                        writer.writerows(self.scraped_data)
            self.log(f"Data exported to {file_path}")

    def export_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.log_messages))
            self.log(f"Log exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookScraper(root)
    root.mainloop()
