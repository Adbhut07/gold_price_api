from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

app = Flask(__name__)

def get_gold_price():
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    try:
        url = 'https://www.goodreturns.in/gold-rates/'
        driver.get(url)
        element = driver.find_element(By.XPATH, '//*[@id="moneyweb-leftPanel"]/setion/div/div[2]/div[2]/p')
        gold_price = element.text
    except Exception as e:
        gold_price = None
        print(f"Error: {e}")
    finally:
        driver.quit()

    return gold_price

@app.route('/get-gold-price', methods=['GET'])
def gold_price_api():
    price = get_gold_price()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Capture current timestamp
    
    if price:
        return jsonify({
            "gold_price": price,
            "timestamp": timestamp
        })
    else:
        return jsonify({
            "error": "Unable to fetch the gold price",
            "timestamp": timestamp
        }), 500

@app.route('/')
def index():
    return jsonify({"message": "Use the /get-gold-price route to get gold price."})

# Remove app.run() since Gunicorn will manage the app in production.
