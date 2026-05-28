import pandas as pd
#1 task
# 1. Excel немесе CSV файлын жүктеу
file_path = '../data/retail_customer_loyalty_realistic.csv'

with open(file_path, 'r', encoding='utf-8') as f:
    df = pd.read_csv(f)

# 2. Алғашқы 10 жолды шығару
print("1. Деректердің алғашқы 10 жолы ")
print(df.head(10))

# 3. Жолдар мен бағандар санын анықтау
rows, cols = df.shape
print(f"\n--- 2. Кесте өлшемі ---\nЖолдар саны: {rows}\nБағандар саны: {cols}")

# 4. Деректер типтерін шығару
print("3. Бағандардың деректер типтері ")
print(df.dtypes)

# 5. customer_id бойынша дубликаттарды тексеру
duplicates = df.duplicated(subset=['customer_id']).sum()
print(f"4. Қайталанатын ID-лер саны: {duplicates}")

# 6. Пропускілерді (NaN) есептеу
print(" 5. Бос орындар (Missing values) саны ")
print(df.isnull().sum())

# 7. Теріс мәндерді іздеу (total_spent және avg_purchase_value)
# Саудада шығын мен орташа чек теріс сан болмауы керек
problematic_data = df[(df['total_spent'] < 0) | (df['avg_purchase_value'] < 0)]
print(f"6. Теріс мәні бар жолдар саны: {len(problematic_data)}")

# 8. Проблемалы жолдардың пайыздық үлесін шығару
percent_bad = (len(problematic_data) / rows) * 100
print(f"7. Қате деректердің үлесі: {percent_bad:.2f}%")

#2task
print("task2")
cities = df['city'].unique().tolist()
income_levels = df['income_level'].unique().tolist()
city_set = set(cities)
print(df['preferred_category'].value_counts())
top_cat = df['preferred_category'].mode()[0]
print(f"Ең танымал категория: {top_cat}")

#task3
print('task3')
upper_ids = [str(cid).upper() for cid in df['customer_id']]
id_lengths = [len(str(cid)) for cid in df['customer_id']]
avg_len = sum(id_lengths)/len(id_lengths)
df['customer_numeric_id'] =df['customer_id'].str.extract(r'(\d+)').astype(float)
print(df.nlargest(10, ['customer_numeric_id']))

#task4
print('task4')
avg_spent = df['total_spent'].mean()
median_freq = df['purchase_frequency'].median()
high_value_clients = df[
    (df['total_spent'] > avg_spent) &
    (df['purchase_frequency'] > median_freq) &
    (df['loyalty_score'] >70)
]
print(high_value_clients[['customer_id' , 'total_spent', 'loyalty_score']].head(10))

#task5
print('task5')
df['spend_per_purchase'] = df['total_spent'] / df['purchase_frequency']  +1
df['return_ratio'] = df.apply(lambda x: x['returns_count'] / x['purchase_frequency'] +1, axis=1)
df['engagement_score_custom'] = (df['app_sessions_per_month'] + df['website_visits_per_month']) /2

#task6
print('task6')
df['client_score'] = (df['total_spent'] * 0.5) + (df['loyalty_score'] * 0.3) - (df['returns_count']* 0.2)
top_20_clients = df.sort_values(by='client_score', ascending=False).head(20)
print(top_20_clients)

#task7
print('task7')
def active_online_shoppers(dataframe):
    for _, row in dataframe.iterrows():
        if row['online_shopper'] == True and row['loyalty_score'] > 60:
            yield row

gen = active_online_shoppers(df)
for i in range(20):
    print(next(gen)['customer_id'])

#task8
print('task8')
city_spend = {}
city_count = {}

for _, row in df.iterrows():
    city = row['city']
    spend = row['total_spent']
    city_spend[city] = city_spend.get(city, 0) + spend
    city_count[city] = city_count.get(city, 0) + 1

for city in city_spend:
    avg = city_spend[city] / city_count[city]
    print(f"{city}: {avg:.2f}")

#task9
print('task9')
top_5 = []

for _, row in df.iterrows():
    val = row['total_spent']
    top_5.append(val)
    top_5.sort(reverse=True)
    if len(top_5) > 5:
        top_5.pop()

print(f"Топ-5 шығын: {top_5}")

#task10
print('task10')
# Барлық жаңа бағандармен сақтау
df.to_csv('refined_customer_data.csv', index=False)

# Тек топ-100 клиентті бөлек сақтау
df.nlargest(100, 'client_score').to_csv('top_100_clients.csv', index=False)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------- STYLE ----------------------
sns.set_theme(style="whitegrid")

plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11

# =========================================================
# 1. Missing Values Heatmap
# =========================================================
plt.figure(figsize=(12, 5))

sns.heatmap(
    df.isnull(),
    cbar=True,
    yticklabels=False,
    cmap='mako'
)

plt.title("Missing Values Heatmap", fontsize=18, weight='bold')
plt.xlabel("Columns")
plt.tight_layout()
plt.show()

# =========================================================
# 2. Preferred Categories Bar Chart
# =========================================================
plt.figure(figsize=(12, 6))

category_counts = df['preferred_category'].value_counts()

ax = sns.barplot(
    x=category_counts.values,
    y=category_counts.index,
    hue=category_counts.index,
    palette='viridis',
    legend=False
)

# Сандарды шығару
for i, value in enumerate(category_counts.values):
    ax.text(value + 1, i, str(value), va='center', fontsize=10)

plt.title("Most Popular Product Categories", fontsize=18, weight='bold')
plt.xlabel("Number of Customers")
plt.ylabel("Category")

plt.tight_layout()
plt.show()

# =========================================================
# 3. Purchase Frequency vs Total Spent
# =========================================================
plt.figure(figsize=(12, 7))

scatter = plt.scatter(
    df['purchase_frequency'],
    df['total_spent'],
    c=df['loyalty_score'],
    cmap='coolwarm',
    s=80,
    alpha=0.7,
    edgecolors='black'
)

plt.axhline(
    avg_spent,
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'Average Spent = {avg_spent:.1f}'
)

plt.axvline(
    median_freq,
    color='green',
    linestyle='--',
    linewidth=2,
    label=f'Median Frequency = {median_freq:.1f}'
)

plt.title(
    "Customer Spending vs Purchase Frequency",
    fontsize=18,
    weight='bold'
)

plt.xlabel("Purchase Frequency")
plt.ylabel("Total Spent")

cbar = plt.colorbar(scatter)
cbar.set_label("Loyalty Score")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# =========================================================
# 4. Top 20 Clients
# =========================================================
plt.figure(figsize=(14, 8))

top20 = top_20_clients.sort_values(by='client_score')

ax = sns.barplot(
    x=top20['client_score'],
    y=top20['customer_id'],
    hue=top20['customer_id'],
    palette='magma',
    legend=False
)

for i, value in enumerate(top20['client_score']):
    ax.text(value + 5, i, f"{value:.1f}", va='center')

plt.title("Top 20 Customers by Client Score", fontsize=18, weight='bold')
plt.xlabel("Client Score")
plt.ylabel("Customer ID")

plt.tight_layout()
plt.show()

# =========================================================
# 5. Average Spending by City
# =========================================================
cities_avg_spend = {
    city: city_spend[city] / city_count[city]
    for city in city_spend
}

cities_df = pd.Series(cities_avg_spend).sort_values(ascending=False)

plt.figure(figsize=(13, 7))

ax = sns.barplot(
    x=cities_df.values,
    y=cities_df.index,
    hue=cities_df.index,
    palette='crest',
    legend=False
)

for i, value in enumerate(cities_df.values):
    ax.text(value + 5, i, f"{value:.1f}", va='center')

plt.title(
    "Average Customer Spending by City",
    fontsize=18,
    weight='bold'
)

plt.xlabel("Average Spending")
plt.ylabel("City")

plt.tight_layout()
plt.show()

# =========================================================
# 6. Loyalty Score Distribution
# =========================================================
plt.figure(figsize=(11, 6))

sns.histplot(
    df['loyalty_score'],
    bins=20,
    kde=True,
    color='purple'
)

plt.title("Distribution of Loyalty Scores", fontsize=18, weight='bold')
plt.xlabel("Loyalty Score")
plt.ylabel("Count")

plt.tight_layout()
plt.show()

# =========================================================
# 7. Online Shopper Distribution
# =========================================================
plt.figure(figsize=(7, 7))

online_counts = df['online_shopper'].value_counts()

plt.pie(
    online_counts,
    labels=['Online Shopper', 'Offline Shopper'],
    autopct='%1.1f%%',
    startangle=90
)

plt.title("Online Shopper Distribution", fontsize=18, weight='bold')

plt.tight_layout()
plt.show()