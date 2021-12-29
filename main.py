from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
import requests
import time

CHROME_DRIVER_PATH = r"/Users/caleb/Documents/chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdqCi7GIzCdixPFcmKvEcCrD1i7uA-8-XM2zaqVrgidt7jyUA/viewform?usp=sf_link"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8"
}

response = requests.get("https://www.zillow.com/buffalo-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Buffalo%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-79.03696752539064%2C%22east%22%3A-78.74582983007814%2C%22south%22%3A42.90544399210973%2C%22north%22%3A43.01875552479061%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A17222%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
                        headers=header)

data = response.text
soup = BeautifulSoup(data, "html.parser")

all_link_elements = soup.select(".list-card-top a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

all_price_elements = soup.select(".list-card-heading")
all_prices = []
for element in all_price_elements:
    #retrieve prices. single/multi lists have different tag/class structures
    try:
        #price w/ only one listing
        price = element.select(".list-card-price")[0].contents[0]
    except IndexError:
        #multi
        print("Multiple listings for the card")
        price = element.select(".list-card-details li")[0].contents[0]
        continue
    finally:
        all_prices.append(price)
    try:
        for n in range(len(all_links)):
            driver.get(FORM)
            time.sleep(2)
            address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

            address.send_keys(all_addresses[n])
            price.send_keys(all_prices[n])
            link.send_keys(all_links[n])
            submit.click()

    except UnexpectedAlertPresentException:
        continue
    except IndexError:
        continue
