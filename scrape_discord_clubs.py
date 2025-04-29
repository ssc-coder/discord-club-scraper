from selenium.webdriver.common.by import By
import time, csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup
chromedriver_path = input("🔧 Enter the full path to your chromedriver executable: ").strip()
options = Options()
options.add_argument("--start-maximized")
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://discord.com/login")
input("🔓 Log into Discord manually if needed...\n⚠️ Make sure you're on the Home tab and it’s fully visible, then press Enter...")

# =====================
# SCROLL FUNCTION
# =====================
scroll_container = driver.find_element(By.XPATH, "//div[contains(@class,'scrollerBase_')]")
for _ in range(40):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
    time.sleep(0.3)

# =====================
# SCRAPE FUNCTION
# =====================
def scrape_cards(category_label):
    scroll_container = driver.find_element(By.XPATH, "//div[contains(@class,'scrollerBase_')]")
    for _ in range(40):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        time.sleep(0.3)

    results = []
    cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'card_')]")
    for card in cards:
        # skip the "Add Server" card
        if "Add Server" in card.text:
            continue
        try:
            name = card.find_element(By.XPATH, ".//div[contains(@class, 'guildName')]").text.strip()
        except:
            name = ""
        try:
            desc = card.find_element(By.XPATH, ".//div[contains(@class, 'description')]").text.strip()
        except:
            desc = ""
        try:
            member_divs = card.find_elements(By.XPATH, ".//div[contains(@class, 'memberCount')]")
            members = ""
            for div in member_divs:
                text = div.text.strip()
                if "Member" in text and "Online" not in text:
                    members = text.split()[0]
                    break
        except:
            members = ""

        results.append([name, desc, members, category_label, "", "", "", "", "", "", ""])
    return results

# =====================
# STEP 1: SCRAPE HOME
# =====================
print("🏠 Scraping: Home tab...")
home_clubs = scrape_cards("Home")
home_names = set(row[0].strip().lower() for row in home_clubs if row[0].strip())

# =====================
# STEP 2: SCRAPE CATEGORIES
# =====================
categories = {
    "Clubs": "Clubs",
    "Classes & Subjects": "Classes & Subjects",
    "Social & Study": "Social & Study",
    "Miscellaneous": "Miscellaneous"
}

categorized_clubs = []

for tab_text, category_label in categories.items():
    print(f"📂 Scraping category: {category_label}...")
    try:
        tab = driver.find_element(By.XPATH, f"//div[contains(text(), '{tab_text}')]")
        tab.click()
        time.sleep(2)
        categorized_clubs += scrape_cards(category_label)
    except Exception as e:
        print(f"❌ Couldn’t click tab '{tab_text}': {e}")
        continue

driver.quit()

# =====================
# STEP 3: FIND UNCATEGORIZED
# =====================
categorized_names = set(c[0].strip().lower() for c in categorized_clubs if c[0].strip())
home_names_clean = set(h[0].strip().lower() for h in home_clubs if h[0].strip())

uncategorized_names = home_names_clean - categorized_names

uncategorized_clubs = []
for row in home_clubs:
    normalized_name = row[0].strip().lower()
    if normalized_name in uncategorized_names:
        updated_row = row[:]
        updated_row[3] = "Uncategorized"
        uncategorized_clubs.append(updated_row)

# =====================
# STEP 4: COMBINE + SAVE
# =====================
final_data = categorized_clubs + uncategorized_clubs

with open("discord_clubs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Club Name", "Club Description", "No. of members", "Club Category",
        "Message Sent?", "Admins Replied?", "Admins Response", "Meeting planned",
        "Admins Discord Handle", "Admin Type (Admin/President/Moderator)", "Notes"
    ])
    writer.writerows(final_data)

print(f"✅ Final CSV saved as 'discord_clubs.csv' with {len(final_data)} entries.")
print(f"🧩 {len(uncategorized_clubs)} clubs were only in Home tab and marked as 'Uncategorized'.")