import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from urllib.parse import urljoin
import json

class ComeupScraper:
    def __init__(self):
        self.base_url = "https://comeup.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def extract_service_data(self, service_url):
        """Extrait les données d'un service spécifique"""
        try:
            response = self.session.get(service_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction des données de base
            data = {
                'nom_vendeur': self.extract_seller_name(soup),
                'titre_service': self.extract_service_title(soup),
                'categorie': self.extract_category(soup),
                'prix': self.extract_price(soup),
                'note': self.extract_rating(soup),
                'nombre_vente_total': self.extract_sales_count(soup),
                'avis_positifs': self.extract_positive_reviews(soup),
                'avis_negatifs': self.extract_negative_reviews(soup),
                'commandes_en_cours': self.extract_pending_orders(soup),
                'vendeur_depuis': self.extract_seller_since(soup)
            }
            
            return data
            
        except Exception as e:
            print(f"Erreur lors de l'extraction de {service_url}: {e}")
            return None
    
    def extract_seller_name(self, soup):
        """Extrait le nom du vendeur"""
        # Plusieurs sélecteurs possibles selon la structure de Comeup
        selectors = [
            '.seller-name',
            '.username',
            '[data-testid="seller-name"]',
            '.profile-username'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return "N/A"
    
    def extract_service_title(self, soup):
        """Extrait le titre du service"""
        selectors = [
            'h1',
            '.service-title',
            '[data-testid="service-title"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return "N/A"
    
    def extract_category(self, soup):
        """Extrait la catégorie du service"""
        # Recherche de breadcrumb ou catégorie
        selectors = [
            '.breadcrumb li:last-child',
            '.category-name',
            '[data-testid="category"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Si pas trouvé, essayer de déduire de la description
        title = self.extract_service_title(soup)
        return self.categorize_by_keywords(title)
    
    def categorize_by_keywords(self, text):
        """Catégorise un service basé sur des mots-clés"""
        categories = {
            'Marketing Digital': ['email', 'marketing', 'publicité', 'ads', 'seo', 'social media'],
            'Rédaction': ['rédiger', 'écrire', 'contenu', 'article', 'blog'],
            'Design': ['logo', 'design', 'graphique', 'bannière', 'visuel'],
            'Développement': ['site web', 'application', 'développement', 'code'],
            'Vidéo': ['montage', 'vidéo', 'animation', 'motion'],
            'Audio': ['voix off', 'musique', 'audio', 'podcast'],
            'Traduction': ['traduction', 'traduire', 'langue'],
            'Business': ['business plan', 'stratégie', 'conseil']
        }
        
        text_lower = text.lower()
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'Autre'
    
    def extract_price(self, soup):
        """Extrait le prix du service"""
        selectors = [
            '.price',
            '.service-price',
            '[data-testid="price"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Extraire le nombre du prix
                price_match = re.search(r'(\d+(?:[,\.]\d+)?)', price_text.replace('€', '').replace(',', '.'))
                if price_match:
                    return float(price_match.group(1))
        return 0.0
    
    def extract_rating(self, soup):
        """Extrait la note moyenne"""
        selectors = [
            '.rating',
            '.stars',
            '[data-testid="rating"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                rating_text = element.get_text(strip=True)
                rating_match = re.search(r'(\d+(?:[,\.]\d+)?)', rating_text)
                if rating_match:
                    return float(rating_match.group(1).replace(',', '.'))
        return 0.0
    
    def extract_sales_count(self, soup):
        """Extrait le nombre total de ventes"""
        selectors = [
            '.sales-count',
            '.orders-completed',
            '[data-testid="sales"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                sales_text = element.get_text(strip=True)
                sales_match = re.search(r'(\d+)', sales_text)
                if sales_match:
                    return int(sales_match.group(1))
        return 0
    
    def extract_reviews(self, soup):
        """Extrait les avis (positifs et négatifs)"""
        reviews = {'positifs': 0, 'negatifs': 0}
        
        # Chercher les avis
        review_elements = soup.select('.review, .comment, .feedback')
        
        for review in review_elements:
            review_text = review.get_text(strip=True).lower()
            
            # Mots-clés pour identifier les avis positifs/négatifs
            positive_keywords = ['excellent', 'parfait', 'recommande', 'super', 'génial', 'satisfait']
            negative_keywords = ['décevant', 'mauvais', 'problème', 'insatisfait', 'nul']
            
            if any(keyword in review_text for keyword in positive_keywords):
                reviews['positifs'] += 1
            elif any(keyword in review_text for keyword in negative_keywords):
                reviews['negatifs'] += 1
        
        return reviews
    
    def extract_positive_reviews(self, soup):
        reviews = self.extract_reviews(soup)
        return reviews['positifs']
    
    def extract_negative_reviews(self, soup):
        reviews = self.extract_reviews(soup)
        return reviews['negatifs']
    
    def extract_pending_orders(self, soup):
        """Extrait le nombre de commandes en cours"""
        selectors = [
            '.pending-orders',
            '.queue',
            '[data-testid="pending"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                pending_text = element.get_text(strip=True)
                pending_match = re.search(r'(\d+)', pending_text)
                if pending_match:
                    return int(pending_match.group(1))
        return 0
    
    def extract_seller_since(self, soup):
        """Extrait depuis quand le vendeur est inscrit"""
        selectors = [
            '.member-since',
            '.seller-since',
            '[data-testid="member-since"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return "N/A"
    
    def scrape_services_list(self, category_url, max_pages=5):
        """Scrape une liste de services depuis une catégorie"""
        services_urls = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{category_url}?page={page}"
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Sélecteurs pour les liens de services
                service_links = soup.select('a[href*="/service/"]')
                
                for link in service_links:
                    service_url = urljoin(self.base_url, link['href'])
                    if service_url not in services_urls:
                        services_urls.append(service_url)
                
                time.sleep(1)  # Pause entre les requêtes
                
            except Exception as e:
                print(f"Erreur page {page}: {e}")
                continue
        
        return services_urls
    
    def scrape_to_csv(self, category_urls, output_file="comeup_services.csv"):
        """Scrape les données et les sauvegarde en CSV"""
        all_data = []
        
        for category_url in category_urls:
            print(f"Scraping catégorie: {category_url}")
            service_urls = self.scrape_services_list(category_url)
            
            for i, service_url in enumerate(service_urls):
                print(f"Service {i+1}/{len(service_urls)}: {service_url}")
                
                service_data = self.extract_service_data(service_url)
                if service_data:
                    all_data.append(service_data)
                
                time.sleep(2)  # Pause entre les requêtes
        
        # Créer le DataFrame et sauvegarder
        df = pd.DataFrame(all_data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Données sauvegardées dans {output_file}")
        
        return df

# Utilisation
if __name__ == "__main__":
    scraper = ComeupScraper()
    
    # URLs des catégories à scraper
    categories = [
        "https://comeup.com/fr/best-services",
        "https://comeup.com/fr/category/site-developpement",
    ]
    
    # Lancer le scraping
    df = scraper.scrape_to_csv(categories, "comeup_analysis.csv")
    
    # Afficher un aperçu
    print("\nAperçu des données:")
    print(df.head())
    
    # Statistiques rapides
    print(f"\nNombre total de services: {len(df)}")
    print(f"Catégories trouvées: {df['categorie'].unique()}")