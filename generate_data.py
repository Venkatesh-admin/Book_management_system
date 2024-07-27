# generate_data.py

import pandas as pd
import numpy as np
import faker

def generate_synthetic_books(num_books=1000):
    fake = faker.Faker()
    genres = ['Science Fiction', 'Fantasy', 'Mystery', 'Non-Fiction', 'Romance']
    
    data = {
        'id': range(1, num_books + 1),
        'title': [fake.catch_phrase() for _ in range(num_books)],
        'author': [fake.name() for _ in range(num_books)],
        'genre': [np.random.choice(genres) for _ in range(num_books)],
        'year_published': [np.random.randint(1900, 2023) for _ in range(num_books)],
        'average_rating': [round(np.random.uniform(1, 5), 1) for _ in range(num_books)],
    }
    
    df = pd.DataFrame(data)
    df.to_csv('synthetic_books.csv', index=False)
    print("Synthetic data generated and saved to 'synthetic_books.csv'.")

if __name__ == '__main__':
    generate_synthetic_books()
