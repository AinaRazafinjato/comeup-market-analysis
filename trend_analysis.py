import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_trends(csv_file):
    """Analyse les tendances du marché Comeup"""
    df = pd.read_csv(csv_file)
    
    # 1. Analyse par catégorie
    category_stats = df.groupby('categorie').agg({
        'prix': ['mean', 'median', 'count'],
        'note': 'mean',
        'nombre_vente_total': 'sum'
    }).round(2)
    
    print("=== ANALYSE PAR CATÉGORIE ===")
    print(category_stats)
    
    # 2. Top vendeurs
    top_sellers = df.groupby('nom_vendeur').agg({
        'nombre_vente_total': 'sum',
        'note': 'mean',
        'prix': 'mean'
    }).sort_values('nombre_vente_total', ascending=False).head(10)
    
    print("\n=== TOP 10 VENDEURS ===")
    print(top_sellers)
    
    # 3. Analyse des prix
    print(f"\n=== ANALYSE DES PRIX ===")
    print(f"Prix moyen: {df['prix'].mean():.2f}€")
    print(f"Prix médian: {df['prix'].median():.2f}€")
    print(f"Prix min: {df['prix'].min():.2f}€")
    print(f"Prix max: {df['prix'].max():.2f}€")
    
    # 4. Graphiques
    plt.figure(figsize=(15, 10))
    
    # Prix par catégorie
    plt.subplot(2, 2, 1)
    sns.boxplot(data=df, x='categorie', y='prix')
    plt.xticks(rotation=45)
    plt.title('Distribution des prix par catégorie')
    
    # Notes par catégorie
    plt.subplot(2, 2, 2)
    sns.barplot(data=df, x='categorie', y='note')
    plt.xticks(rotation=45)
    plt.title('Note moyenne par catégorie')
    
    # Nombre de services par catégorie
    plt.subplot(2, 2, 3)
    df['categorie'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Répartition des services par catégorie')
    
    # Corrélation prix/note
    plt.subplot(2, 2, 4)
    plt.scatter(df['prix'], df['note'])
    plt.xlabel('Prix (€)')
    plt.ylabel('Note')
    plt.title('Corrélation Prix vs Note')
    
    plt.tight_layout()
    plt.savefig('comeup_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    analyze_trends("comeup_analysis.csv")