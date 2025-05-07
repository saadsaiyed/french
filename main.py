import pandas as pd

# Lists of 20 words for each subject (without headers)
daily_routine = [
    ("Morning", "Matin"),
    ("Evening", "Soir"),
    ("Night", "Nuit"),
    ("Wake up", "Se réveiller"),
    ("Sleep", "Dormir"),
    ("Breakfast", "Petit-déjeuner"),
    ("Lunch", "Déjeuner"),
    ("Dinner", "Dîner"),
    ("Water", "Eau"),
    ("Coffee", "Café"),
    ("Tea", "Thé"),
    ("Work", "Travailler"),
    ("Job", "Travail / Emploi"),
    ("Study", "Étudier"),
    ("School", "École"),
    ("House", "Maison"),
    ("Travel", "Voyager"),
    ("Walk", "Marcher"),
    ("Come", "Venir"),
    ("Go", "Aller"),
]

vegetables = [
    ("Carrot", "Carotte"),
    ("Potato", "Pomme de terre"),
    ("Tomato", "Tomate"),
    ("Onion", "Oignon"),
    ("Garlic", "Ail"),
    ("Cabbage", "Chou"),
    ("Spinach", "Épinard"),
    ("Broccoli", "Brocoli"),
    ("Peas", "Petits pois"),
    ("Cucumber", "Concombre"),
    ("Cauliflower", "Chou-fleur"),
    ("Chili", "Piment"),
    ("Eggplant", "Aubergine"),
    ("Corn", "Maïs"),
    ("Pumpkin", "Citrouille"),
    ("Beetroot", "Betterave"),
    ("Zucchini", "Courgette"),
    ("Radish", "Radis"),
    ("Celery", "Céleri"),
    ("Lettuce", "Laitue"),
]

family = [
    ("Father", "Père"),
    ("Mother", "Mère"),
    ("Brother", "Frère"),
    ("Sister", "Sœur"),
    ("Grandfather", "Grand-père"),
    ("Grandmother", "Grand-mère"),
    ("Uncle", "Oncle"),
    ("Aunt", "Tante"),
    ("Cousin (male)", "Cousin"),
    ("Cousin (female)", "Cousine"),
    ("Nephew", "Neveu"),
    ("Niece", "Nièce"),
    ("Husband", "Mari"),
    ("Wife", "Femme"),
    ("Son", "Fils"),
    ("Daughter", "Fille"),
    ("Parents", "Parents"),
    ("Children", "Enfants"),
    ("Family", "Famille"),
    ("Relative", "Parent"),
]

city_country = [
    ("City", "Ville"),
    ("Country", "Pays"),
    ("Street", "Rue"),
    ("Road", "Route"),
    ("Airport", "Aéroport"),
    ("Train station", "Gare"),
    ("Hotel", "Hôtel"),
    ("Restaurant", "Restaurant"),
    ("Park", "Parc"),
    ("Hospital", "Hôpital"),
    ("Museum", "Musée"),
    ("Library", "Bibliothèque"),
    ("Market", "Marché"),
    ("Mall", "Centre commercial"),
    ("Bridge", "Pont"),
    ("River", "Rivière"),
    ("Mountain", "Montagne"),
    ("Beach", "Plage"),
    ("Capital city", "Capitale"),
    ("Village", "Village"),
]

clothes = [
    ("Shirt", "Chemise"),
    ("T-shirt", "T-shirt"),
    ("Pants", "Pantalon"),
    ("Jeans", "Jean"),
    ("Dress", "Robe"),
    ("Skirt", "Jupe"),
    ("Shoes", "Chaussures"),
    ("Socks", "Chaussettes"),
    ("Hat", "Chapeau"),
    ("Cap", "Casquette"),
    ("Sweater", "Pull"),
    ("Jacket", "Veste"),
    ("Coat", "Manteau"),
    ("Shorts", "Short"),
    ("Gloves", "Gants"),
    ("Scarf", "Écharpe"),
    ("Belt", "Ceinture"),
    ("Suit", "Costume"),
    ("Boots", "Bottes"),
    ("Pajamas", "Pyjama"),
]

food_items = [
    ("Bread", "Pain"),
    ("Butter", "Beurre"),
    ("Cheese", "Fromage"),
    ("Milk", "Lait"),
    ("Eggs", "Œufs"),
    ("Chicken", "Poulet"),
    ("Meat", "Viande"),
    ("Fish", "Poisson"),
    ("Rice", "Riz"),
    ("Pasta", "Pâtes"),
    ("Salt", "Sel"),
    ("Pepper", "Poivre"),
    ("Sugar", "Sucre"),
    ("Honey", "Miel"),
    ("Soup", "Soupe"),
    ("Salad", "Salade"),
    ("Apple", "Pomme"),
    ("Banana", "Banane"),
    ("Orange", "Orange"),
    ("Cake", "Gâteau"),
]

# Combine all lists
all_words = daily_routine + vegetables + family + city_country + clothes + food_items

# Create DataFrame
df_all_words = pd.DataFrame(all_words)

# Save without header
csv_words_path = "./Daily_Vocabulary_French_Anki_Import.csv"
df_all_words.to_csv(csv_words_path, index=False, header=False)

print(csv_words_path)