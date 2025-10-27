# House-Price-Prediction
## 📘 Project Overview
A machine learning project that predicts house prices based on features like area, bedrooms, bathrooms, stories, and parking . Built with Python, pandas, and scikit-learn using Linear Regression, it includes data preprocessing, model training, evaluation, and web-based prediction.

## ⚙️ Key Features

* Data preprocessing and feature encoding
* Model comparison:
  
    Linear Regression → 0.6272862376933837 ✅
  
    Lasso Regression → 0.6272862341468444
  
    Decision Tree Regressor → 0.008571514366602306
  
    Random Forest Regressor → 0.5852040592470394
  
* Hyperparameter Tuning using RandomizedSearchCV to find the best-performing model
  
    Best_Model_Score => 0.6407027669595713
  
* Model saved using Pickle for easy prediction
* Simple Flask web app for real-time prediction

## 🧠 Model Deployment

* The best-performing Random Forest model was saved using Pickle for easy deployment and real-time prediction.

## 💻 Web Application (Flask + HTML + CSS + JS)

The trained model is integrated with a Flask web interface, allowing users to:

✅ Log in securely

✅ Access a dashboard with prediction history

✅ Enter house details via an interactive HTML form

✅ Predict house prices 

✅ View all predictions with timestamps (Sri Lanka local time)

## 🧩 Technologies Used

* Python → Core programming language for data analysis and modeling
* pandas, NumPy → Data cleaning, manipulation, and analysis
* scikit-learn → Model training, tuning, and evaluation
* Flask → Backend web framework for user interaction and prediction
* HTML, CSS, JavaScript → Frontend for user interface
* SQLite3 → Lightweight database for user login and prediction storage
* pytz → Handle timestamps in Sri Lanka time zone
* pickle → Save and load the trained model for deployment


 <img width="615" height="609" alt="Capture1" src="https://github.com/user-attachments/assets/724acb4f-bb30-474f-ba33-59b98498f7f0" />
 
<img width="1333" height="640" alt="Capture2" src="https://github.com/user-attachments/assets/ea7020dc-197b-4f60-9dae-4d676454c875" />

<img width="1338" height="616" alt="Capture3" src="https://github.com/user-attachments/assets/c8ad8067-1cd0-46b8-9629-55f6b3bfcb90" />



