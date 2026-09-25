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
        
        # 1. محاكاة معالجة الإشارات المتقدمة (Advanced Denoising & Feature Extraction)
        mean_val = np.mean(arr)
        std_val = np.std(arr)
        # إزالة التشويش الحاد (Artifact Removal) عبر تقييد القيم ضمن النطاق الطبيعي للإشارات العصبية
        denoised = np.clip(arr, mean_val - (2.5 * std_val), mean_val + (2.5 * std_val))
        
        # حساب المؤشرات الحيوية للإشارة المنقية
        final_mean = float(np.mean(denoised))
        signal_energy = float(np.sum(np.square(denoised))) # طاقة الإشارة
        peak_amplitude = float(np.max(np.abs(denoised)))   # ذروة النشاط العصبي
        
        # 2. نظام تصنيف عصبي ذكي يحاكي دماغ شخص بالغ صاحي
        if final_mean > 2.5 and peak_amplitude > 6.0:
            label = "Right Hand Movement (حركة نشطة باليد اليمنى)"
            description = "نشاط عالي في القشرة الحركية للجانب الأيسر من الدماغ، يمثل نية تنفيذ حركة إرادية باليد اليمنى."
        elif final_mean < -2.5 and peak_amplitude > 6.0:
            label = "Left Hand Movement (حركة نشطة باليد اليسرى)"
            description = "نشاط عالي في القشرة الحركية للجانب الأيمن من الدماغ، يمثل نية تنفيذ حركة إرادية باليد اليسرى."
        elif signal_energy > 150.0 and abs(final_mean) <= 1.5:
            label = "Autonomous / Micro-Movements (حركات عفوية أو حك الجسم)"
            description = "نمط متقطع وعشوائي يرافق الحركات الجسدية التلقائية وردود الفعل الحسية الجلدية."
        elif 1.0 <= peak_amplitude <= 4.0 and std_val < 1.0:
            label = "Cognitive Focus & Intention (تركيز ذهني ونيّة واعية)"
            description = "حالة استقرار مع يقظة عالية، تمثل تفكير الشخص البالغ الواعي في مهمة محددة دون حركة فعلية."
        elif -1.0 <= final_mean <= 1.0 and peak_amplitude < 3.0:
            label = "Deep Relaxation / Baseline Rest (استرخاء وعطالة دماغية طبيعية)"
            description = "إشارات مستقرة وهادئة تمثل حالة الراحة العصبية وانعدام التحفيز الحركي النشط."
        else:
            label = "General Motor Preparation (تأهب حركي عام)"
            description = "حالة إكلينيكية انتقالية تظهر قبل اتخاذ القرار الحركي أو الاستجابة لمؤثر خارجي."
            
        return jsonify({
            'label': label,
            'mean_signal_value': round(final_mean, 4),
            'signal_energy': round(signal_energy, 2),
            'description': description,
            'denoised_features': denoised.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
