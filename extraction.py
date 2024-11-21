import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
import json
from main import get_vehicle_data
def extract_car_data(pages=5):
    # Configuration de Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Mode sans interface graphique
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    all_data = []

    # Parcourir plusieurs pages
    for page in range(1, pages + 1):
        url = f'https://www.aramisauto.com/achat/?page={page}'
        print(f"Scraping URL: {url}")
        driver.get(url)

        # Attendre que les cartes de produit soient chargées
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card'))
            )
        except Exception as e:
            print(f"Erreur de chargement pour la page {page}: {e}")
            continue

        # Récupérer les cartes de produit
        articles = driver.find_elements(By.CLASS_NAME, 'product-card')

        # Extraction des informations pour chaque carte
        for article in articles:
            try:
                # Marque et modèle
                marque = article.get_attribute("makerid")
                modele = article.get_attribute("modelid")

                # Lien cliquable
                relative_link = article.get_attribute("href")
                full_link = f"{relative_link}"
                
        
                # Utilisation d'une expression régulière pour extraire l'ID après "vehicleId="
                match = re.search(r'vehicleId=(\d+)', full_link)
                if match:
                    car_id = match.group(1)
                else:
                    print("ID non trouvé.")

                # Titre de la voiture
                title = article.find_element(By.CLASS_NAME, 'product-card-vehicle-information__title').text

                # Détails de la voiture
                details = article.find_element(By.CLASS_NAME, 'product-card-vehicle-information__details').text

                # Extraction de la motorisation et de la finition
                motorisation_info = article.find_element(By.CLASS_NAME, 'product-card-vehicle-information__details--light').text.split("•")
                motorisation = motorisation_info[0].strip()
                finition = motorisation_info[1].strip() if len(motorisation_info) > 1 else "Inconnue"

                # Extraction du type de carburant et de la transmission
                fuel_transmission_info = article.find_elements(By.CLASS_NAME, 'product-card-vehicle-information__details--light')[1].text.split("•")
                fuel_type = fuel_transmission_info[0].strip()
                transmission = fuel_transmission_info[1].strip() if len(fuel_transmission_info) > 1 else "Inconnue"

                # Année de fabrication et kilométrage
                bottom_info = article.find_element(By.CLASS_NAME, 'product-card-vehicle-information__bottom').text
                year = "Inconnue"
                mileage = "Inconnu"

                # Extraire l'année et le kilométrage si disponibles
                parts = bottom_info.split("•")
                if len(parts) > 0:
                    year = parts[0].strip()
                if len(parts) > 1:
                    mileage = parts[1].strip()

                # Prix de la voiture
                try:
                    price = article.find_element(By.CLASS_NAME, 'heading-l').text
                except:
                    price = article.find_element(By.CLASS_NAME, 'product-card-discount').text

                # Disponibilité
                availability = article.find_element(By.CLASS_NAME, 'product-availability-status__label').text

                # URL de l'image
                image_url = article.find_element(By.TAG_NAME, 'img').get_attribute('src')

                # Ajouter les données au JSON
                car_data = {
                    "id": car_id,
                    "marque": marque,
                    "modele": modele,
                    "title": title,
                    "motorisation": motorisation,
                    "finition": finition,
                    "fuel_type": fuel_type,
                    "transmission": transmission,
                    "year": year,
                    "mileage": mileage,
                    "price": price,
                    "availability": availability,
                    "image_url": image_url,
                    "link": full_link
                }
                all_data.append(car_data)

            except Exception as e:
                print(f"Erreur lors de l'extraction des données : {e}")

    # Fermer le navigateur
    driver.quit()

    # Sauvegarder les données dans un fichier JSON
    with open("detailed_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"Données sauvegardées dans 'detailed_data.json' avec {len(all_data)} voitures.")

if __name__ == "__main__":
    extract_car_data(pages=100)  # Modifier le nombre de pages à scraper
