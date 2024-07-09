from selenium import webdriver
from selenium.webdriver.common.by import By


browser=webdriver.Firefox()
browser.get("http://localhost:8000")

assert "Congratulations!" in browser.title
print("OK")
