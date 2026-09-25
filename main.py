from flask import Flask, request, jsonify
from scipy.signal import butter, lfilter
import numpy as np

app = Flask(__name__)

# دالة الفلترة (تنقية التشويش)
def filter_signal(data):
    # مثال على فلتر بسيط لتنقية الإشارة الخام وحذف التشويش العشوائي
    # (يمكنكِ تعديل الترددات حسب نوع الإشارات لاحقاً)
    return np.array(data) * 0.95  # نموذج مبسط للتنقية والتقييس

@app.route('/predict', methods=['POST'])
def predict():
    req_data = request.get_json()
    raw_signal = req_data.get('features', [])
    
    # 1. تنقية الإشارة من التشويش أولاً
    cleaned_signal = filter_signal(raw_signal)
    
    # 2. إدخال الإشارة المنقية إلى نموذج الذكاء الاصطناعي للتنبؤ
    # (هنا يتم وضع كود الموديل الخاص بكِ)
    prediction_result = 0  # مثال: Left Hand
    label_text = "Left Hand (Cleaned)"
    
    return jsonify({
        "prediction": prediction_result,
        "label": label_text,
        "cleaned_features": cleaned_signal.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)
