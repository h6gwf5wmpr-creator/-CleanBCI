from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data.get('features', [])
        
        if not features:
            return jsonify({'error': 'المصفوفة فارغة'}), 400
        
        # تحويل البيانات إلى مصفوفة رقمية وتنقية الإشارة
        arr = np.array(features, dtype=float)
        denoised = arr * 0.95 # محاكاة عملية التنقية
        
        # حساب متوسط القيمة للإشارة المنقية
        mean_val = float(np.mean(denoised))
        
        # نظام تصنيف ذكي ومتوازن بناءً على متوسط الإشارة
        if mean_val > 1.0:
            label = "Right Hand"
        elif mean_val < -1.0:
            label = "Left Hand"
        else:
            label = "Rest"
            
        return jsonify({
            'label': label,
            'mean_signal_value': round(mean_val, 4),
            'denoised_features': denoised.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
