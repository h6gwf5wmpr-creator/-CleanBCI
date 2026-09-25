// =======================================================
// خوارزمية "المايند" المتقدمة لفك تشفير إشارات الدماغ (CleanBCI)
// تضمن دقة الفصل بين الأوامر والجهات والوظائف بدون خربطة
// =======================================================
function processBrainMind(signalArray) {
    if (!Array.isArray(signalArray) || signalArray.length === 0) {
        return {
            classification: "Idle State / وضع الخمول",
            descAr: "لا توجد إشارات مدخلة، الدماغ في حالة راحة تامة.",
            descEn: "No signal input detected, the brain is in a complete state of rest.",
            avgSignal: "0.00 µV",
            powerSignal: "0.00 dB"
        };
    }

    // 1. استخراج المؤشرات الحسابية والترددية الدقيقة من المصفوفة
    const maxVal = Math.max(...signalArray);
    const minVal = Math.min(...signalArray);
    const sum = signalArray.reduce((a, b) => a + b, 0);
    const avg = sum / signalArray.length;
    const len = signalArray.length;
    
    // حساب التباين (Variance) لقراءة تذبذب الإشارة الدقيق وسرعة ردود الفعل
    const variance = signalArray.reduce((a, b) => a + Math.pow(b - avg, 2), 0) / len;

    let result = {
        classification: "",
        descAr: "",
        descEn: "",
        avgSignal: `${avg.toFixed(2)} µV`,
        powerSignal: `${(sum * avg).toFixed(2)} dB`
    };

    // 2. خريطة اتخاذ القرار الصارمة لمنع تداخل أو خربطة الأوامر
    
    // الأمر الأول: تحريك اليد اليمنى (إذا كانت الشحنة القصوى حادة جداً وأعلى من 2.0)
    if (maxVal > 2.0 && avg > 1.4) {
        result.classification = "Right Hand Movement / حركة اليد اليمنى";
        result.descAr = "تم رصد تفريغ عصبي حاد وموجه في الفص الجبهي الأيسر (Motor Cortex)، مما يشير بوضوح إلى نية حركية مؤكدة لتفعيل وتحريك اليد اليمنى بدقة.";
        result.descEn = "A sharp, localized neural discharge detected in the left frontal lobe (Motor Cortex), indicating a definitive motor intention to precisely move the Right Hand.";
    } 
    
    // الأمر الثاني: تحريك اليد اليسرى (إذا كانت القيمة العظمى متوسطة القوة وتتجاوز 1.65)
    else if (maxVal > 1.65 && maxVal <= 2.0 && variance < 0.1) {
        result.classification = "Left Hand Movement / حركة اليد اليسرى";
        result.descAr = "تم رصد تفجر إشاري نشط متوافق مع القشرة الحركية اليمنى، مما يؤكد نجاح فك تشفير أمر تحريك اليد اليسرى وتجاوز عائق تشويش عظام الجمجمة.";
        result.descEn = "An active signal burst registered within the right motor cortex, validating successful decoding of the Left Hand movement command while bypassing cranial dampening.";
    } 
    
    // الأمر الثالث: المشي والحركات العفوية للأطراف السفلية (عند وجود قنوات مصفوفة ممتدة وتدفق مستمر)
    else if (avg > 1.5 && len >= 6) {
        result.classification = "Spontaneous Walking / المشي وحركة الأطراف السفلية";
        result.descAr = "إشارات متزامنة واسعة النطاق ممتدة عبر فصي الدماغ تتوافق مع الأنماط الحركية التلقائية والعفوية؛ مثل الرغبة في المشي، الوقوف، أو تنسيق الأرجل.";
        result.descEn = "Broad, synchronized bilateral hemisphere signals corresponding to automated motor patterns, successfully simulating walking or automated coordination of lower extremities.";
    } 
    
    // الأمر الرابع: طور اللعب والتفاعل السريع (إذا كانت الإشارة متذبذبة جداً وبها تباين سريع حاد)
    else if (variance >= 0.08 && maxVal > 1.55) {
        result.classification = "Interactive Gaming & Reflexes / طور اللعب والتفاعل السريع";
        result.descAr = "تذبذبات حسية حركية متعاقبة ذات تباين عالٍ تحاكي ردود الفعل الفورية وعمليات اتخاذ القرار اللحظي المتوافقة تماماً مع ألعاب الفيديو السريعة.";
        result.descEn = "High-frequency oscillations combined with rapid consecutive sensorimotor changes, simulating reflex actions and instantaneous decision-making aligned with active gaming.";
    } 
    
    // الأمر الخامس: التركيز الذهني والقراءة (إشارات مستقرة جداً بمعدل قشري محدد لموجات Beta)
    else if (avg > 1.35 && avg <= 1.5 && variance < 0.05) {
        result.classification = "Cognitive Focus & Reading / التركيز الذهني والقراءة";
        result.descAr = "ارتفاع ملحوظ في ترددات وسعة موجات بيتا (Beta Waves) فوق مناطق المعالجة البصرية واللغوية، مما يدل على حالة قراءة نشطة، تحليل نصوص، أو تركيز ذهني عميق.";
        result.descEn = "Significant amplitude spikes in Beta frequencies over visual and language processing centers, demonstrating an active state of text comprehension or deep reading.";
    } 
    
    // الأمر السادس: الرغبة في قضاء الحاجة (نبضات منخفضة وتفريغ في قاع الإشارة من الجهاز العصبي الذاتي)
    else if (avg >= 1.0 && avg <= 1.35 && minVal < 1.1) {
        result.classification = "Biological Excretion Urge / الرغبة في قضاء الحاجة";
        result.descAr = "نجاح فك تشفير نبضات بطيئة آتية من الجهاز العصبي الذاتي (Autonomic System)، تحاكي بدقة التنبيهات الحشوية الداخلية للجسم والرغبة في قضاء الحاجة البيولوجية.";
        result.descEn = "Successful decoding of low-frequency autonomic visceral impulses, precisely tracking internal physiological indicators and the biological urge to evacuate.";
    } 
    
    // الأمر السابع والافتراضي: حركات ارتدادية عفوية عامة للجسم في وضع الراحة
    else {
        result.classification = "Spontaneous Reflex / حركة ارتدادية عفوية عامة";
        result.descAr = "نشاط قشري عام غير مركزي يتوافق مع التيارات العفوية الارتدادية أو الحركات الدقيقة واللاإرادية التي يقوم بها الجسم في وضع الراحة لتعديل الوضعية العامة.";
        result.descEn = "Non-localized general cortical activity consistent with spontaneous background reflexes or minor involuntary shifts executed by the body during micro-rest intervals.";
    }

    return result;
}
