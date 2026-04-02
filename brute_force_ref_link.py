import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import random
import time
import os
from datetime import datetime

# --- CONFIG ---
TARGET_URL = "https://claude.ai/referral/"
CHARSET = string.ascii_letters + string.digits

class UltimateBypass:
    def __init__(self):
        self.success_count = 0
        self.tested_count = 0
        self.options = uc.ChromeOptions()
        # On peut ajouter un proxy ici si nécessaire :
        # self.options.add_argument('--proxy-server=http://user:pass@ip:port')

    def log(self, msg, level="INFO"):
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"[{ts}] [{level}] {msg}")

    def run(self, limit=100):
        self.log("Lancement de Undetected Chromedriver (Le 'Vrai' Ghost)...")
        
        # Initialisation du driver (ça peut prendre 5-10s la première fois)
        driver = uc.Chrome(options=self.options, headless=False, version_main=146)
        
        try:
            for i in range(limit):
                self.tested_count += 1
                code = ''.join(random.choices(CHARSET, k=10))
                url = f"{TARGET_URL}{code}"
                
                self.log(f"Test #{self.tested_count}: {code}")
                
                try:
                    driver.get(url)
                    
                    # On attend que la page se stabilise (Cloudflare Turnstile)
                    # On laisse 5 à 8 secondes pour que le check se fasse tout seul
                    time.sleep(random.uniform(6, 9))

                    # VERIFICATION : On cherche le texte "Accept Invitation"
                    # Si c'est présent, c'est que le lien est valide ET le captcha passé
                    page_text = driver.page_source
                    
                    if "Accept Invitation" in page_text:
                        self.log(f"!!! SUCCÈS RÉEL : {code} !!!", "SUCCESS")
                        with open("valides_v15.txt", "a") as f:
                            f.write(f"{datetime.now()} | {url}\n")
                        self.success_count += 1
                    else:
                        print(f" -> Invalide ou Captcha bloqué (Code: {code})")

                except Exception as e:
                    self.log(f"Erreur durant le test : {e}", "ERROR")
                    continue

                # Pause pour simuler un humain qui réfléchit
                time.sleep(random.uniform(2, 4))

        except KeyboardInterrupt:
            self.log("Arrêt demandé.")
        finally:
            driver.quit()
            self.log(f"Terminé. Trouvés : {self.success_count}")

if __name__ == "__main__":
    print("=== ENGINE V15 (UNDETECTED CHROMEDRIVER) ===")
    limit = input("Nombre de tests : ")
    limit = int(limit) if limit.isdigit() else 10
    
    bot = UltimateBypass()
    bot.run(limit=limit)