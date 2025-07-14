from django.db import models

class CibilPrediction(models.Model):
    age = models.IntegerField()
    service_years = models.IntegerField(default=0)  # type: ignore
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    desired_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    existing_loans = models.IntegerField()
    predicted_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # This method always returns a string, not a CharField (linter clarification)
        created_str = self.created_at.strftime('%Y-%m-%d') if self.created_at else ''  # type: ignore
        return f"CIBIL Score: {self.predicted_score} (Created: {created_str})"  # type: ignore[override]

class Bank(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    min_cibil_score = models.IntegerField()
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField()
    logo_url = models.URLField(blank=True)
    
    def __str__(self):
        return str(self.name)  # type: ignore[override]

# ============================================================================
# 6. predictor/ml_model.py (MACHINE LEARNING MODEL)
# ============================================================================

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import os
from django.conf import settings

class CibilScorePredictor:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(settings.BASE_DIR, 'predictor', 'cibil_model.pkl')
        self.load_or_train_model()
    
    def load_or_train_model(self):
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("Model loaded successfully!")
            except:
                print("Error loading model, training new one...")
                self.train_model()
        else:
            print("No existing model found, training new one...")
            self.train_model()
    
    def train_model(self):
        """Train a realistic CIBIL score prediction model"""
        print("Training CIBIL prediction model...")
        
        # Generate synthetic but realistic training data
        np.random.seed(42)
        n_samples = 5000
        
        # Generate realistic feature distributions
        age = np.random.normal(35, 10, n_samples).clip(18, 70).astype(int)
        service_years = (60 - age).clip(1, 47)  # Assume retirement age is 60
        monthly_income = np.random.lognormal(10.5, 0.8, n_samples).clip(15000, 500000)
        loan_amount = np.random.lognormal(13, 1, n_samples).clip(50000, 10000000)
        existing_loans = np.random.poisson(1.5, n_samples).clip(0, 8)
        
        # Create realistic CIBIL scores based on financial logic
        scores = []
        for i in range(n_samples):
            base_score = 600  # Starting point
            
            # Income factor (30% weight)
            income_score = 0
            if monthly_income[i] >= 100000:
                income_score = 120
            elif monthly_income[i] >= 75000:
                income_score = 100
            elif monthly_income[i] >= 50000:
                income_score = 80
            elif monthly_income[i] >= 30000:
                income_score = 60
            elif monthly_income[i] >= 20000:
                income_score = 40
            else:
                income_score = 20
            
            # Service years factor (replaces age stability, 15% weight)
            service_score = 0
            if service_years[i] >= 30:
                service_score = 60  # Many years left, very stable
            elif 15 <= service_years[i] < 30:
                service_score = 50  # Good stability
            elif 5 <= service_years[i] < 15:
                service_score = 40  # Nearing retirement
            else:
                service_score = 25  # Very close to retirement
            
            # Debt-to-income ratio (35% weight)
            annual_income = monthly_income[i] * 12
            debt_ratio = loan_amount[i] / annual_income if annual_income > 0 else 10
            
            debt_score = 0
            if debt_ratio <= 2:
                debt_score = 100  # Excellent
            elif debt_ratio <= 3:
                debt_score = 80   # Good
            elif debt_ratio <= 5:
                debt_score = 60   # Fair
            elif debt_ratio <= 8:
                debt_score = 40   # Poor
            else:
                debt_score = 20   # Very poor
            
            # Existing loans factor (20% weight)
            loan_penalty = existing_loans[i] * 25
            
            # Calculate final score
            final_score = base_score + (income_score * 0.3) + (service_score * 0.15) + (debt_score * 0.35) - loan_penalty
            
            # Add some randomness to make it realistic
            final_score += np.random.normal(0, 30)
            
            # Ensure score is within CIBIL range (300-900)
            final_score = max(300, min(900, int(final_score)))
            scores.append(final_score)
        
        # Prepare training data
        X = np.column_stack([age, service_years, monthly_income, loan_amount, existing_loans])
        y = np.array(scores)
        
        # Train the model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model.fit(X, y)
        
        # Save the trained model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"Model trained and saved to {self.model_path}")
        
        # Print model performance
        from sklearn.metrics import mean_absolute_error, r2_score
        predictions = self.model.predict(X)
        mae = mean_absolute_error(y, predictions)
        r2 = r2_score(y, predictions)
        print(f"Model Performance - MAE: {mae:.2f}, R²: {r2:.3f}")
    
    def predict_score(self, age, service_years, monthly_income, loan_amount, existing_loans):
        """Predict CIBIL score for given features"""
        if self.model is None:
            print("Model not available, returning default score")
            return 650
        
        try:
            features = np.array([[age, service_years, monthly_income, loan_amount, existing_loans]])
            predicted_score = self.model.predict(features)[0]
            
            # Ensure score is within valid CIBIL range
            final_score = max(300, min(900, int(predicted_score)))
            return final_score
        except Exception as e:
            print(f"Prediction error: {e}")
            return 650