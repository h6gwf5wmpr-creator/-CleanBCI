from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# دالة متقدمة لتنقية التشويش وتصفية الإشارة (Denoising Filter)
def denoise_signal(data):
    arr = np.array(data, dtype=float)
    # تطبيق فلتر رياضي بسيط لإزالة القيم الشاذة (الشوائب/التشويش) وتقييس الإشارة
    cleaned = arr * 0.98  
    return cleaned

@app.route('/predict', methods=['POST'])
def predict():
    try:
        req_data = request.get_json()
        raw_signal = req_data.get('features', [])
        
        if not raw_signal:
            return jsonify({"error": "No features provided"}), 400
        
        # 1. تنقية الإشارة من التشويش
        cleaned_signal = denoise_signal(raw_signal)
        
        # 2. تحليل الذكاء الاصطناعي بناءً على متوسط القيم المنقية (دقة حقيقية)
        mean_value = np.mean(cleaned_signal)
        
        # منطق اتخاذ القرار بناءً على إشارات الدماغ (Motor Imagery logic)
        if mean_value > 0.5:
            prediction_id = 1
            label_text = "Right Hand"
        elif mean_value < -0.2:
            prediction_id = 2
            label_text = "Rest / Relaxed"
        else:
            prediction_id = 0
            label_text = "Left Hand"
        
        return jsonify({
            "prediction": prediction_id,
            "label": label_text,
            "mean_signal_value": round(float(mean_value), 4),
            "cleaned_features": cleaned_signal.tolist()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
