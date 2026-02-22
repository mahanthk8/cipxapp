# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# import random
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Set random seeds for reproducibility
# np.random.seed(42)
# random.seed(42)

# # Constants
# N_ROWS = 8000
# START_DATE = datetime(2020, 1, 1)
# END_DATE = datetime(2024, 12, 31)

# # Categories
# COMPLAINT_CATEGORIES = ['garbage', 'drainage', 'mosquito', 'water_shortage', 'electricity', 'road_damage']
# REGIONS = ['North', 'South', 'East', 'West', 'Central', 'Suburban', 'Industrial', 'Coastal']
# SEASONS = ['Summer', 'Rainy', 'Winter']

# # Emergency and health keywords
# EMERGENCY_WORDS = ['urgent', 'emergency', 'critical', 'immediate', 'dangerous', 'hazardous']
# HEALTH_WORDS = ['health', 'medical', 'disease', 'infection', 'contamination', 'toxic']

# def generate_synthetic_data(n_rows=8000):
#     """Generate synthetic complaint management dataset"""

#     # Initialize lists to store data
#     data = []

#     # Generate base dates
#     date_range = pd.date_range(START_DATE, END_DATE, freq='D')

#     for i in range(n_rows):
#         # Identity & Time
#         created_date = pd.Timestamp(np.random.choice(date_range)) # Fix: Convert numpy.datetime64 to pd.Timestamp
#         year = created_date.year
#         month = created_date.month
#         week_of_year = created_date.isocalendar()[1]
#         day_of_week = created_date.weekday()
#         is_weekend = 1 if day_of_week >= 5 else 0

#         # Season based on month (simplified for India)
#         if month in [12, 1, 2]:
#             season = 'Winter'
#         elif month in [6, 7, 8, 9]:
#             season = 'Rainy'
#         else:
#             season = 'Summer'

#         # Complaint Features
#         complaint_category = np.random.choice(COMPLAINT_CATEGORIES)
#         region = np.random.choice(REGIONS)

#         # Population density and urban index based on region
#         region_factors = {
#             'North': (8000, 0.85),
#             'South': (7500, 0.80),
#             'East': (7000, 0.75),
#             'West': (8500, 0.90),
#             'Central': (10000, 0.95),
#             'Suburban': (5000, 0.60),
#             'Industrial': (6000, 0.70),
#             'Coastal': (4000, 0.50)
#         }

#         base_density, base_urban = region_factors[region]
#         population_density = max(1000, np.random.normal(base_density, 1000))
#         urban_index = np.clip(np.random.normal(base_urban, 0.1), 0, 1)

#         # Environmental Context - correlated with season
#         if season == 'Summer':
#             avg_temperature = np.random.normal(35, 3)
#             rainfall_level = np.random.normal(10, 5)
#             humidity = np.random.normal(45, 10)
#         elif season == 'Rainy':
#             avg_temperature = np.random.normal(28, 2)
#             rainfall_level = np.random.normal(200, 50)
#             humidity = np.random.normal(80, 10)
#         else:  # Winter
#             avg_temperature = np.random.normal(20, 3)
#             rainfall_level = np.random.normal(30, 15)
#             humidity = np.random.normal(60, 10)

#         air_quality_index = np.random.normal(150, 30) + (50 if region in ['Industrial', 'Central'] else 0)

#         # Operational Context
#         active_officers = np.random.randint(5, 20)
#         avg_officer_star = np.clip(np.random.normal(4.2, 0.5), 1, 5)
#         avg_workload = np.random.normal(25, 5)

#         # Complaint history (will be calculated later, placeholder for now)
#         complaints_last_7_days_region = np.random.randint(0, 50)
#         complaints_last_30_days_region = np.random.randint(0, 200)
#         complaints_same_category_last_30_days = np.random.randint(0, 100)

#         # Description and keywords
#         contains_emergency_word = np.random.choice([0, 1], p=[0.85, 0.15])
#         contains_health_word = np.random.choice([0, 1], p=[0.90, 0.10])

#         # Adjust probability based on category
#         if complaint_category in ['mosquito', 'water_shortage']:
#             contains_health_word = max(contains_health_word, np.random.choice([0, 1], p=[0.7, 0.3]))

#         # Generate description
#         category_descriptions = {
#             'garbage': ['Garbage collection missed', 'Waste pileup', 'Dustbin overflow', 'Illegal dumping'],
#             'drainage': ['Drainage blockage', 'Water stagnation', 'Sewage overflow', 'Drainage repair needed'],
#             'mosquito': ['Mosquito menace', 'Breeding site', 'Fogging required', 'Malaria outbreak'],
#             'water_shortage': ['Water supply issue', 'Low pressure', 'Pipeline burst', 'Water contamination'],
#             'electricity': ['Power outage', 'Voltage fluctuation', 'Transformer issue', 'Street light not working'],
#             'road_damage': ['Pothole', 'Road damage', 'Street repair', 'Footpath broken']
#         }

#         base_desc = np.random.choice(category_descriptions[complaint_category])

#         if contains_emergency_word:
#             base_desc = f"URGENT: {base_desc} - immediate attention required"
#         if contains_health_word:
#             base_desc = f"{base_desc} - health hazard reported"

#         description = base_desc

#         # Priority based on multiple factors
#         priority_score = 0

#         # Category weights
#         category_weights = {
#             'electricity': 0.3,
#             'water_shortage': 0.4,
#             'mosquito': 0.2,
#             'drainage': 0.1,
#             'garbage': 0.05,
#             'road_damage': 0.05
#         }

#         priority_score += category_weights[complaint_category]

#         # Environmental factors
#         if avg_temperature > 38: priority_score += 0.1
#         if rainfall_level > 150: priority_score += 0.05
#         if air_quality_index > 200: priority_score += 0.1

#         # Operational factors
#         if avg_workload > 30: priority_score += 0.05
#         if complaints_last_7_days_region > 30: priority_score += 0.05

#         # Emergency/health keywords
#         if contains_emergency_word: priority_score += 0.2
#         if contains_health_word: priority_score += 0.15

#         # Weekend effect
#         if is_weekend: priority_score += 0.05

#         # Determine priority
#         if priority_score > 0.4:
#             priority = 'High'
#         elif priority_score > 0.2:
#             priority = 'Medium'
#         else:
#             priority = 'Low'

#         # Resolution days based on priority and context
#         base_resolution = {'High': 3, 'Medium': 7, 'Low': 14}[priority]

#         # Add noise and context-based adjustments
#         resolution_days = base_resolution + np.random.normal(0, 2)

#         # Seasonal adjustment
#         if season == 'Rainy':
#             resolution_days += np.random.normal(2, 1)

#         # Workload impact
#         resolution_days += max(0, (avg_workload - 25) * 0.2)

#         # Officer quality impact
#         resolution_days -= (avg_officer_star - 3) * 0.5

#         # Ensure positive resolution days
#         resolution_days = max(1, int(resolution_days))

#         # Create row
#         row = {
#             'complaint_id': i + 1,
#             'created_date': created_date,
#             'year': year,
#             'month': month,
#             'week_of_year': week_of_year,
#             'day_of_week': day_of_week,
#             'is_weekend': is_weekend,
#             'season': season,
#             'description': description,
#             'complaint_category': complaint_category,
#             'region': region,
#             'population_density': round(population_density, 0),
#             'urban_index': round(urban_index, 2),
#             'avg_temperature': round(avg_temperature, 1),
#             'rainfall_level': round(rainfall_level, 1),
#             'humidity': round(humidity, 1),
#             'air_quality_index': round(air_quality_index, 0),
#             'active_officers': active_officers,
#             'avg_officer_star': round(avg_officer_star, 1),
#             'avg_workload': round(avg_workload, 1),
#             'complaints_last_7_days_region': complaints_last_7_days_region,
#             'complaints_last_30_days_region': complaints_last_30_days_region,
#             'complaints_same_category_last_30_days': complaints_same_category_last_30_days,
#             'priority': priority,
#             'resolution_days': resolution_days
#         }

#         data.append(row)

#     # Create DataFrame
#     df = pd.DataFrame(data)

#     # Calculate proper rolling statistics
#     df = df.sort_values(['region', 'created_date']).reset_index(drop=True)

#     for region in REGIONS:
#         region_mask = df['region'] == region
#         region_indices = df[region_mask].index

#         for idx in region_indices:
#             current_date = df.loc[idx, 'created_date']

#             # Calculate actual rolling statistics
#             region_complaints = df[(df['region'] == region) & (df['created_date'] < current_date)]

#             last_7_days = region_complaints[region_complaints['created_date'] >= (current_date - timedelta(days=7))]
#             last_30_days = region_complaints[region_complaints['created_date'] >= (current_date - timedelta(days=30))]

#             current_category = df.loc[idx, 'complaint_category']
#             same_category_30_days = last_30_days[last_30_days['complaint_category'] == current_category]

#             df.loc[idx, 'complaints_last_7_days_region'] = len(last_7_days)
#             df.loc[idx, 'complaints_last_30_days_region'] = len(last_30_days)
#             df.loc[idx, 'complaints_same_category_last_30_days'] = len(same_category_30_days)

#     # Add derived features
#     df['contains_emergency_word'] = df['description'].str.contains('|'.join(EMERGENCY_WORDS), case=False).astype(int)
#     df['contains_health_word'] = df['description'].str.contains('|'.join(HEALTH_WORDS), case=False).astype(int)

#     return df

# # Generate the dataset
# df = generate_synthetic_data(20000)

# # Display summary statistics
# print("Dataset Shape:", df.shape)
# print("\nFirst few rows:")
# print(df.head())
# print("\nDataset Info:")
# print(df.info())
# print("\nPriority Distribution:")
# print(df['priority'].value_counts())
# print("\nCategory Distribution:")
# print(df['complaint_category'].value_counts())
# print("\nRegion Distribution:")
# print(df['region'].value_counts())

# # Save to CSV
# df.to_csv('complaint_management_synthetic_dataset20k.csv', index=False)
# print("\nDataset saved as 'complaint_management_synthetic_dataset.csv'")

# # Display basic statistics for numeric columns
# print("\nNumeric columns summary:")
# numeric_cols = df.select_dtypes(include=[np.number]).columns
# print(df[numeric_cols].describe())