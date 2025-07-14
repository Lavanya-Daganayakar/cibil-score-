import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

class CibilScorePredictor:
    def __init__(self):
        self.model = None
        self.load_or_train_model()
    
    def load_or_train_model(self):
        model_path = 'predictor/cibil_model.pkl'
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.train_model()
    
    def train_model(self):
        # Synthetic training data for demonstration
        # In real project, use actual CIBIL dataset
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic features
        age = np.random.randint(18, 70, n_samples)
        income = np.random.randint(20000, 200000, n_samples)
        loan_amount = np.random.randint(100000, 5000000, n_samples)
        existing_loans = np.random.randint(0, 5, n_samples)
        
        # Create synthetic CIBIL scores based on realistic rules
        scores = []
        for i in range(n_samples):
            base_score = 500
            
            # Income factor (higher income = better score)
            if income[i] > 100000:
                base_score += 150
            elif income[i] > 50000:
                base_score += 100
            elif income[i] > 30000:
                base_score += 50
            
            # Age factor (stable age = better score)
            if 25 <= age[i] <= 50:
                base_score += 100
            elif age[i] > 50:
                base_score += 80
            
            # Loan burden factor
            loan_to_income_ratio = loan_amount[i] / (income[i] * 12)
            if loan_to_income_ratio < 3:
                base_score += 80
            elif loan_to_income_ratio < 5:
                base_score += 40
            else:
                base_score -= 50
            
            # Existing loans factor
            base_score -= existing_loans[i] * 30
            
            # Add some randomness
            base_score += np.random.randint(-50, 50)
            
            # Ensure score is within CIBIL range
            base_score = max(300, min(900, base_score))
            scores.append(base_score)
        
        # Prepare training data
        X = np.column_stack([age, income, loan_amount, existing_loans])
        y = np.array(scores)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Save model
        with open('predictor/cibil_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
    
    def predict_score(self, age, income, loan_amount, existing_loans):
        if self.model is None:
            return 650  # Default score
        
        features = np.array([[age, income, loan_amount, existing_loans]])
        predicted_score = self.model.predict(features)[0]
        
        # Ensure score is within valid range
        return max(300, min(900, int(predicted_score)))