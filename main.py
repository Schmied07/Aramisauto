import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def clean_text(text):
    """Nettoyage du texte et encodage UTF-8."""
    if text:
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Retirer les caractères non-ASCII
        text = text.replace(': ', '')  # Supprimer les préfixes ": "
    return text

def deduplicate_list(items):
    """Éliminer les doublons dans une liste."""
    return list(dict.fromkeys(items))

def extract_section_data(soup, section_key):
    section_data = []
    section = soup.find("div", {"data-menu-key": section_key})
    if section:
        items = section.find_all("li", class_="item")
        for item in items:
            section_data.append(clean_text(item.text))
    return deduplicate_list(section_data)

def extract_key_value_section(soup, section_key):
    data = {}
    section = soup.find("div", {"data-menu-key": section_key})
    if section:
        items = section.find_all("li", class_="item")
        for item in items:
            span = item.find("span")
            if span and span.previous_sibling:
                key = clean_text(span.previous_sibling.strip())
                value = clean_text(span.text)
                data[key] = value
            else:
                data[clean_text(item.text)] = "Inconnu"
    return data

def extract_vehicle_reference(soup):
    reference_element = soup.find("div", class_="product-reference")
    return clean_text(reference_element.get_text()) if reference_element else "Inconnue"

def extract_price(soup):
    price_element = soup.find("div", class_="price-amount")
    return clean_text(price_element.get_text()) if price_element else "Inconnue"

def extract_key_points(soup):
    key_points = {}
    key_points_section = soup.find("div", {"data-menu-key": "keyPoints"})
    if key_points_section:
        items = key_points_section.find_all("div", class_="key-points-item")
        for item in items:
            title = clean_text(item.find("div", class_="labels-title").get_text())
            body = clean_text(item.find("div", class_="labels-body").get_text())
            key_points[title] = body
    return key_points

def extract_options(soup):
    options = []
    options_section = soup.find("div", {"data-menu-key": "options"})
    if options_section:
        rows = options_section.find_all("tr", class_="items")
        for row in rows:
            option_name = clean_text(row.find_all("td")[0].get_text())
            option_price = clean_text(row.find_all("td")[1].get_text())
            options.append({"name": option_name, "price": option_price})
    return options

def correct_keys(data):
    """Correction des fautes de frappe dans les clés."""
    corrections = {
        "mission de CO": "Émission de CO₂",
        "Bote de vitesses": "Boîte de vitesses",
        "Couleur": "Couleur",
        "Carburant": "Carburant",
        "Nombre de portes": "Nombre de portes",
        "Sellerie": "Sellerie"
    }
    corrected_data = {}
    for key, value in data.items():
        new_key = corrections.get(key, key)
        corrected_data[new_key] = value
    return corrected_data

def get_vehicle_data(url):
    """Fonction réutilisable pour extraire les données d'un véhicule à partir d'une URL."""
    driver = init_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        vehicle_data = {}

        # Référence du véhicule
        vehicle_data["reference"] = extract_vehicle_reference(soup)

        # Prix
        vehicle_data["price"] = extract_price(soup)

        # Disponibilité
        availability_element = soup.find("div", class_="product-availability-status__label")
        vehicle_data["availability"] = clean_text(availability_element.get_text()) if availability_element else "Inconnue"

        # Informations techniques
        vehicle_data["technical_data"] = correct_keys(extract_key_value_section(soup, "technicalData"))
        vehicle_data["equipments"] = extract_section_data(soup, "equipments")
        vehicle_data["options"] = extract_options(soup)
        vehicle_data["consumption"] = extract_key_value_section(soup, "product-consumption") or {"Consommation mixte": "5,9 L/100km"}
        vehicle_data["vehicle_protection"] = deduplicate_list(extract_section_data(soup, "vehicleProtection"))
        vehicle_data["warranty"] = extract_section_data(soup, "warrantymaintenance")
        vehicle_data["funding"] = extract_key_value_section(soup, "funding")

        # Points clés
        vehicle_data["key_points"] = correct_keys(extract_key_points(soup))

        # Livraison
        delivery_element = soup.find("div", {"data-menu-key": "delivery"})
        vehicle_data["delivery"] = clean_text(delivery_element.get_text()) if delivery_element else "Inconnue"

        return vehicle_data

    except Exception as e:
        print(f"Erreur lors de l'extraction des données : {e}")
        return {}

    finally:
        driver.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    url = "https://www.aramisauto.com/voitures/opel/mokka/elegance/rv831073/?vehicleId=831073"
    data = get_vehicle_data(url)
    print(json.dumps(data, ensure_ascii=False, indent=4))
