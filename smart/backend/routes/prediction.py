import os
from flask import Blueprint, render_template, request
import pickle
import numpy as np

prediction_bp = Blueprint('prediction', __name__, url_prefix='/prediction')

# Load saved model
# model = pickle.load(open('../backend/models/fine_model.pkl', 'rb'))
model_path = os.path.join('..', 'models', 'fine_model.pkl')
@prediction_bp.route('/')
def fine_prediction_page():
    return render_template('fine_prediction.html')

@prediction_bp.route('/predict', methods=['POST'])
def predict_fine():
    days_late = int(request.form['days_late'])
    fine = model.predict(np.array([[days_late]]))[0]
    return render_template('fine_prediction.html', fine=fine)
