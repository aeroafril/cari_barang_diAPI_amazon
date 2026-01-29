from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_amazon(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # hapus ini kalau mau lihat browser
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hasil = []

    produk_list = soup.select("div.s-main-slot div.s-result-item")
    for produk in produk_list:
        nama = produk.select_one("h2 span")
        harga_whole = produk.select_one("span.a-price-whole")
        harga_frac = produk.select_one("span.a-price-fraction")

        if nama and harga_whole:
            harga = harga_whole.get_text(strip=True)
            if harga_frac:
                harga += "," + harga_frac.get_text(strip=True)

            hasil.append({
                "nama": nama.get_text(strip=True),
                "harga": "$" + harga
            })

    driver.quit()
    return hasil