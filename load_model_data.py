import pickle

def load_model():
    with open('./train_dataset/recommendation_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('./train_dataset/books_df.pkl', 'rb') as df_file:
        df = pickle.load(df_file)
    
    with open('./train_dataset/label_encoder.pkl', 'rb') as encoder_file:
        label_encoder = pickle.load(encoder_file)

    return model,df,label_encoder
   