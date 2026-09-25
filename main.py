// دالة "المايند" الذكية لتصنيف جميع الأوامر والنشاطات بناءً على المصفوفة المدخلة
function processBrainMind(signalArray) {
    if (!Array.isArray(signalArray) || signalArray.length === 0) {
        return { action: "خامل / لا توجد إشارة", description: "الدماغ في حالة راحة تامة." };
    }

    // 1. استخراج المؤشرات الأساسية من المصفوفة المدخلة
    const maxVal = Math.max(...signalArray); // أعلى قيمة شحنة
    const minVal = Math.min(...signalArray); // أقل قيمة
    const sum = signalArray.reduce((a, b) => a + b, 0);
    const avg = sum / signalArray.length;     // المتوسط
    const length = signalArray.length;        // طول المصفوفة (عدد القنوات)

    // 2. شبكة اتخاذ القرار وتصنيف الأوامر (تغطية كافة الأطراف والاحتياجات)
    let classification = "";
    let analysisText = "";

    // شروط ديناميكية تعتمد على نمط الأرقام المدخلة
    if (maxVal > 1.9) {
        classification = "Right Hand (اليد اليمنى)";
        analysisText = "تم رصد إشارة حركية حادة في القشرة المخية اليسرى؛ أمر بتحريك اليد اليمنى.";
    } 
    else if (maxVal > 1.7 && maxVal <= 1.9) {
        classification = "Left Hand (اليد اليسرى)";
        analysisText = "تم رصد إشارة في القشرة المخية اليمنى؛ أمر بتحريك اليد اليسرى.";
    } 
    else if (avg > 1.5 && length > 5) {
        classification = "Walking (المشي / حركة الأطراف السفلية)";
        analysisText = "إشارات متزامنة عالية التردد تدل على الرغبة في تحريك الأرجل أو المشي العفوي.";
    } 
    else if (avg > 1.4 && avg <= 1.5) {
        classification = "Reading & Focus (القراءة والتركيز)";
        analysisText = "ارتفاع في موجات (Beta) تدل على التركيز الذهني العالي ومعالجة النصوص والقراءة.";
    } 
    else if (minVal < 1.3 && maxVal > 1.6) {
        classification = "Gaming (اللعب والتفاعل السريع)";
        analysisText = "تذبذب سريع وحاد في الإشارات يتوافق مع استجابات ردود الفعل السريعة أثناء اللعب.";
    } 
    else if (avg >= 1.0 && avg <= 1.3) {
        classification = "Biological Need (قضاء الحاجة)";
        analysisText = "إشارات مرسلة من الجهاز العصبي الذاتي تحاكي الرغبة في قضاء الحاجة البيولوجية.";
    } 
    else {
        classification = "Spontaneous Movement (حركة عفوية)";
        analysisText = "نشاط دماغي عام غير موجه، يتوافق مع الحركات الارتدادية أو العفوية للجسم.";
    }

    // إرجاع النتائج بالكامل للمنصة
    return {
        action: classification,
        description: analysisText,
        averageSignal: avg.toFixed(2),
        spectralPower: (sum * avg).toFixed(2) // معادلة تقريبية للطاقة الطيفية
    };
}

// === طريقة ربط الكود بزر التحليل في المنصة ===
// داخل دالة الضغط على الزر (onclick) الخاصة بك، استدعي المايند هكذا:
/*
   let result = processBrainMind(signalArray);
   
   // تحديث واجهتك بناءً على النتيجة الذكية
   document.getElementById('neuro-classification').innerText = result.action; 
   document.getElementById('clinical-analysis').innerText = result.description;
   document.getElementById('avg-signal').innerText = result.averageSignal + " µV";
   document.getElementById('power-signal').innerText = result.spectralPower + " dB";
*/
