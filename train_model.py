import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
import pickle

def train_recommendation_model(data_path='synthetic_books.csv'):
    df = pd.read_csv(data_path)
    
    # Encode genres
    label_encoder = LabelEncoder()
    df['genre_code'] = label_encoder.fit_transform(df['genre'])
    X = df[['genre_code', 'average_rating']]
    
    # Train a Nearest Neighbors model
    model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
    model.fit(X)
    
    # Save the model to a pickle file
    with open('/train_dataset/recommendation_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    # Save the dataframe for later use
    df.to_pickle('/train_dataset/books_df.pkl')
    with open('/train_dataset/label_encoder.pkl', 'wb') as encoder_file:
        pickle.dump(label_encoder, encoder_file)
    
    print("Model and data saved to 'recommendation_model.pkl' and 'books_data.pkl'.")
    
if __name__ == '__main__':
    train_recommendation_model()
