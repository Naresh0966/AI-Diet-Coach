import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle

def load_and_train_model():
    df = pd.read_csv('dataset.csv')
    
    features = ['Age', 'Weight', 'Height', 'BloodSugar', 'ActivityLevel']
    X = df[features].copy()
    y = df['DiabeticRisk'].copy()
    
    le = LabelEncoder()
    if X['ActivityLevel'].dtype == 'object':
        X['ActivityLevel'] = le.fit_transform(X['ActivityLevel'])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Train Accuracy: {train_score:.4f}")
    print(f"Test Accuracy: {test_score:.4f}")
    
    with open('trained_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    
    return model

if __name__ == "__main__":
    model = load_and_train_model()
    print("Model trained and saved successfully!")
