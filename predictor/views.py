from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CibilPrediction
from .ml_model import CibilScorePredictor
import logging

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    """Display the home page with input form"""
    return render(request, 'predictor/home.html')

def predict_cibil(request):
    """Handle CIBIL score prediction"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')  # Extract name from form
            age = int(request.POST.get('age', 0))
            monthly_income = float(request.POST.get('monthly_income', 0))
            desired_loan_amount = float(request.POST.get('desired_loan_amount', 0))
            existing_loans = int(request.POST.get('existing_loans', 0))
            
            # Basic validation
            if not (18 <= age <= 100):
                raise ValueError("Age must be between 18 and 100")
            if monthly_income < 1000:
                raise ValueError("Monthly income must be at least ₹1,000")
            if desired_loan_amount < 10000:
                raise ValueError("Loan amount must be at least ₹10,000")
            if existing_loans < 0:
                raise ValueError("Number of existing loans cannot be negative")
            
            # Calculate service years internally
            retirement_age = 60
            service_years = max(1, retirement_age - age)
            
            # Predict CIBIL score
            predictor = CibilScorePredictor()
            predicted_score = predictor.predict_score(
                age, monthly_income, desired_loan_amount, existing_loans
            )
            
            # Save prediction to database
            try:
                prediction = CibilPrediction.objects.create(  # type: ignore
                    age=age,
                    service_years=service_years,
                    monthly_income=monthly_income,
                    desired_loan_amount=desired_loan_amount,
                    existing_loans=existing_loans,
                    predicted_score=predicted_score
                )
                logger.info(f"Prediction saved: Score {predicted_score} for user data")
            except Exception as db_error:
                logger.error(f"Database save error: {db_error}")
                # Continue even if DB save fails
            
            # Get suitable banks
            suitable_banks = get_suitable_banks(predicted_score, desired_loan_amount, monthly_income)
            
            # Prepare context for result page
            context = {
                'name': name,
                'age': age,
                'monthly_income': monthly_income,
                'desired_amount': desired_loan_amount,
                'existing_loans': existing_loans,
                'predicted_score': predicted_score,
                'score_category': get_score_category(predicted_score),
                'banks': suitable_banks,
            }
            
            return render(request, 'predictor/result.html', context)
            
        except ValueError as ve:
            messages.error(request, f"Input Error: {str(ve)}")
            return render(request, 'predictor/home.html')
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            messages.error(request, "An error occurred while processing your request. Please try again.")
            return render(request, 'predictor/home.html')
    
    return redirect('home')

def get_score_category(score):
    """Return score category based on CIBIL score"""
    if score >= 750:
        return "Excellent"
    elif score >= 700:
        return "Very good"
    elif score >= 650:
        return "Good"
    elif score >= 600:
        return "Fair"
    else:
        return "Poor"

def get_suitable_banks(cibil_score, loan_amount, monthly_income):
    """Get list of suitable banks based on CIBIL score and other factors"""
    
    # Comprehensive bank data with realistic criteria
    banks_data = [
        {
            'name': 'State Bank of India',
            'short_name': 'SBI',
            'min_score': 650,
            'max_amount': 15000000,
            'interest_rate': 8.50,
            'priority': 1,
            'income_multiplier': 60  # Max loan = 60x monthly income
        },
        {
            'name': 'HDFC Bank',
            'short_name': 'HDFC',
            'min_score': 720,
            'max_amount': 20000000,
            'interest_rate': 8.65,
            'priority': 2,
            'income_multiplier': 80
        },
        {
            'name': 'ICICI Bank',
            'short_name': 'ICICI',
            'min_score': 700,
            'max_amount': 18000000,
            'interest_rate': 8.75,
            'priority': 3,
            'income_multiplier': 75
        },
        {
            'name': 'Axis Bank',
            'short_name': 'AXIS',
            'min_score': 680,
            'max_amount': 12000000,
            'interest_rate': 9.00,
            'priority': 4,
            'income_multiplier': 65
        },
        {
            'name': 'Cooperative Bank',
            'short_name': 'COOP',
            'min_score': 600,
            'max_amount': 5000000,
            'interest_rate': 9.50,
            'priority': 5,
            'income_multiplier': 40
        }
    ]
    
    suitable_banks = []
    annual_income = monthly_income * 12
    
    for bank in banks_data:
        if cibil_score >= bank['min_score']:
            # Calculate maximum eligible amount based on multiple factors
            
            # Factor 1: Income-based calculation
            income_based_limit = monthly_income * bank['income_multiplier']
            
            # Factor 2: CIBIL score based multiplier
            score_multiplier = 1.0
            if cibil_score >= 800:
                score_multiplier = 1.3
            elif cibil_score >= 750:
                score_multiplier = 1.2
            elif cibil_score >= 700:
                score_multiplier = 1.1
            elif cibil_score >= 650:
                score_multiplier = 1.0
            else:
                score_multiplier = 0.8
            
            # Factor 3: Bank's policy limit
            policy_limit = bank['max_amount']
            
            # Calculate final eligible amount
            base_eligible = min(income_based_limit * score_multiplier, policy_limit)
            
            # Ensure it's reasonable compared to desired amount
            if loan_amount <= base_eligible:
                eligible_amount = int(min(loan_amount * 1.1, base_eligible))  # 10% buffer
            else:
                eligible_amount = int(base_eligible)
            
            # Only include banks that can offer reasonable amounts
            if eligible_amount >= 50000:  # Minimum viable loan
                suitable_banks.append({
                    'name': bank['name'],
                    'short_name': bank['short_name'],
                    'eligible_amount': eligible_amount,
                    'interest_rate': bank['interest_rate'],
                    'priority': bank['priority'],
                    'approval_chance': min(95, 60 + (cibil_score - bank['min_score']) // 10)
                })
    
    # Sort by priority (best banks first) and then by eligible amount
    suitable_banks.sort(key=lambda x: (x['priority'], -x['eligible_amount']))
    
    return suitable_banks[:5]  # Return top 5 banks
