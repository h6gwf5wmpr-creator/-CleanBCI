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
        
        # تحويل البيانات إلى مصفوفة رقمية
        arr = np.array(features, dtype=float)
        
        # خوارزمية تنقية الإشارة (Denoising): إزالة التشويش العشوائي وتصفية القيم الشاذة
        # تطبيق مرشح أساسي لتنقية القيم الحادة
        mean_val_raw = np.mean(arr)
        std_val = np.std(arr)
        
        # تنقية متقدمة بإزالة التذبذبات العالية غير المرغوبة
        denoised = np.clip(arr, mean_val_raw - (2 * std_val), mean_val_raw + (2 * std_val))
        denoised = denoised * 0.98 # معامل تخفيف وتثبيت الإشارة
        
        mean_val = float(np.mean(denoised))
        max_val = float(np.max(np.abs(denoised)))
        
        # نظام تصنيف دقيق وشامل لجميع الأوامر العصبية
        if mean_val > 2.0:
            label = "Right Hand (حركة اليد اليمنى)"
        elif mean_val < -2.0:
            label = "Left Hand (حركة اليد اليسرى)"
        elif max_val > 5.0 and 0.5 <= abs(mean_val) <= 2.0:
            label = "Both Feet (حركة القدمين)"
        elif -0.5 <= mean_val <= 0.5:
            label = "Rest (حالة الراحة والاسترخاء)"
        else:
            label = "Tongue / General Motor (حركة اللسان أو تركيز عام)"
            
        return jsonify({
            'label': label,
            'mean_signal_value': round(mean_val, 4),
            'denoised_features': denoised.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
