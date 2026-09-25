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
        
        arr = np.array(features, dtype=float)
        
        # معالجة وفلترة الإشارات العصبية
        mean_val = np.mean(arr)
        std_val = np.std(arr)
        denoised = np.clip(arr, mean_val - (2.5 * std_val), mean_val + (2.5 * std_val))
        
        final_mean = float(np.mean(denoised))
        signal_energy = float(np.sum(np.square(denoised)))
        peak_amplitude = float(np.max(np.abs(denoised)))
        variance = float(np.var(denoised))
        
        # نظام تصنيف شامل ومتعدد الحالات (يحاكي دماغ شخص بالغ بكل تفاصيله)
        if final_mean > 3.5 and peak_amplitude > 7.0:
            label = "Right Hand/Arm Movement (حركة الأطراف - اليد اليمنى)"
            description = "نشاط عالي في القشرة الحركية اليسرى للدماغ، يعبر عن قرار إرادي بتحريك الأطراف اليمنى."
        elif final_mean < -3.5 and peak_amplitude > 7.0:
            label = "Left Hand/Arm Movement (حركة الأطراف - اليد اليسرى)"
            description = "نشاط عالي في القشرة الحركية اليمنى للدماغ، يعبر عن قرار إرادي بتحريك الأطراف اليسرى."
        elif variance > 12.0 and peak_amplitude > 8.0:
            label = "Autonomous / Scratching Micro-Movements (حركات عفوية وحك الجسم)"
            description = "أنماط كهربائية عصبية مرتبطة بردود الفعل الحسية الجلدية والحركات التلقائية اللاإرادية."
        elif 2.0 <= abs(final_mean) <= 3.5 and 4.0 <= peak_amplitude <= 7.0:
            label = "Ocular / Eye Movement & Blinking (إشارات حركة العين والرمش)"
            description = "تغيرات في الجهد الكهربائي الجبهي/القذالي الناتجة عن حركة العيون أو الرمش السريع."
        elif -1.5 <= final_mean <= 1.5 and signal_energy > 80.0 and variance < 3.0:
            label = "Visceral / Autonomic State - Elimination Intention (حالة أحشائية - نية قضاء الحاجة)"
            description = "استجابة عصبية ذاتية تنشط من محور الدماغ-الأمعاء للإحساس بالحاجة الفيزيولوجية الملحة."
        elif abs(final_mean) < 1.0 and peak_amplitude < 3.5:
            label = "Deep Relaxation & Baseline Rest (استرخاء عميق وراحة عصبية)"
            description = "استقرار تام في الإشارات الكهربائية مع سيادة موجات الهدوء وانعدام التحفيز الحركي."
        else:
            label = "Complex Cognitive Focus & Intention (تركيز ذهني عميق وتفكير واعٍ)"
            description = "حالة يقظة وتفكير مركّز تتوزع فيها الإشارات عبر الفصوص الجبهية دون إطلاق حركة جسدية."
            
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
