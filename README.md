# CIBIL Score Predictor (LoanWise)

A web application to predict CIBIL (credit) scores and recommend suitable banks for loans, using a machine learning model and a modern Django-based UI.

## Features
- **CIBIL Score Prediction:** Predicts a user's CIBIL score based on age, income, loan amount, and existing loans using a trained ML model.
- **Bank Recommendations:** Suggests banks and eligible loan amounts based on predicted score and user profile.
- **Modern UI:** Responsive, visually appealing interface for input and results.
- **Admin Dashboard:** Manage predictions and bank data via Django admin.
- **Persistent Storage:** Stores predictions in a SQLite database.

## Demo Screenshots
- **Home Page:** User inputs details (name, age, income, loan amount, existing loans).
- **Result Page:** Shows predicted CIBIL score, score category, and recommended banks with eligible amounts and interest rates.

## Tech Stack
- **Backend:** Python 3, Django 4.2
- **ML Model:** scikit-learn (RandomForestRegressor), numpy
- **Frontend:** Django templates, HTML5, CSS3
- **Database:** SQLite (default, easy to switch to Postgres/MySQL)

## Project Structure
```
cibil_prediction/
├── cibil_prediction/        # Django project settings, URLs
├── predictor/              # Main app: ML model, views, models, admin
│   ├── ml_model.py         # ML logic (RandomForestRegressor)
│   ├── cibil_model.pkl     # Trained model (auto-generated)
│   ├── views.py            # Web views (predict, recommend)
│   ├── models.py           # CibilPrediction, Bank models
│   ├── admin.py            # Django admin registration
│   ├── urls.py             # App URL patterns
│   └── migrations/         # DB migrations
├── templates/
│   ├── base.html           # Base template
│   └── predictor/
│       ├── home.html       # Input form
│       └── result.html     # Results & recommendations
├── static/
│   ├── requirements.txt    # Python dependencies
│   └── ...                 # Images, static assets
├── db.sqlite3              # Default database
└── manage.py               # Django entry point
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd cibil_prediction
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv cibil_env
   source cibil_env/bin/activate  # On Windows: cibil_env\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r static/requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- Fill in your details on the home page and submit.
- View your predicted CIBIL score and recommended banks.
- Use the "Check Another Score" button to try again.

## Machine Learning Model
- The model is a `RandomForestRegressor` trained on synthetic data simulating real-world CIBIL scoring logic.
- Model file: `predictor/cibil_model.pkl` (auto-generated if missing).
- Features used: Age, Monthly Income, Loan Amount, Existing Loans.
- Model code: [`predictor/ml_model.py`](predictor/ml_model.py)

## Django Admin
- Access at `/admin/` (create a superuser with `python manage.py createsuperuser`).
- Manage predictions and banks.

## Customization
- **Bank logic:** Edit `get_suitable_banks` in `predictor/views.py`.
- **ML logic:** Edit `predictor/ml_model.py`.
- **UI:** Edit templates in `templates/predictor/` and styles in `style.css`.

## Requirements
- Python 3.8+
- Django 4.2.7
- numpy 1.24.3
- scikit-learn 1.3.0

## Contributing
Pull requests and suggestions are welcome! Please open an issue or PR for improvements.

## License
This project is for educational/demo purposes. Add a LICENSE file for production use.

---
**Made with Django, ML, and ❤️ for financial literacy.** 
