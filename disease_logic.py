import datetime

# Expanded disease database: each entry has symptoms, home_treatment, emergency_signs, and advice
DISEASE_DATABASE = [
    {
        'name': 'Common Cold',
        'symptoms': ['runny nose', 'sneezing', 'cough', 'sore throat', 'congestion', 'mild fever'],
        'home_treatment': 'Rest, fluids, steam inhalation, paracetamol if needed.',
        'emergency_signs': ['high fever > 101°F', 'shortness of breath'],
        'emergency_advice': 'If you have high fever or trouble breathing, see a doctor.',
        'non_emergency_advice': 'This appears to be a non-emergency. Try home treatment. If symptoms persist >3-5 days, consult a doctor.'
    },
    {
        'name': 'Mild Fever',
        'symptoms': ['mild fever', 'low grade fever', 'temperature <100.5°F'],
        'home_treatment': 'Fluids, rest, paracetamol.',
        'emergency_signs': ['fever > 102°F', 'confusion', 'vomiting'],
        'emergency_advice': 'High fever or confusion: see a doctor.',
        'non_emergency_advice': 'Monitor at home. If fever lasts >3 days, consult a doctor.'
    },
    {
        'name': 'Headache',
        'symptoms': ['headache', 'mild headache', 'forehead pain'],
        'home_treatment': 'Sleep, hydration, gentle massage.',
        'emergency_signs': ['sudden severe headache', 'one-sided headache', 'vision loss'],
        'emergency_advice': 'Sudden or severe headache: seek urgent care.',
        'non_emergency_advice': 'Try home remedies. If severe or unusual, see a doctor.'
    },
    {
        'name': 'Constipation',
        'symptoms': ['constipation', 'hard stool', 'no bowel movement'],
        'home_treatment': 'Fiber, warm water, fruits.',
        'emergency_signs': ['no bowel for 5+ days', 'severe abdominal pain'],
        'emergency_advice': 'No bowel for 5+ days or severe pain: see a doctor.',
        'non_emergency_advice': 'Increase fiber and fluids. If persists, consult a doctor.'
    },
    {
        'name': 'Acidity / Indigestion',
        'symptoms': ['acidity', 'indigestion', 'heartburn', 'sour burp'],
        'home_treatment': 'Cold milk, antacids, avoid spicy food.',
        'emergency_signs': ['chest pain', 'vomiting blood'],
        'emergency_advice': 'Chest pain or vomiting blood: emergency care needed.',
        'non_emergency_advice': 'Try home remedies. If persistent, see a doctor.'
    },
    {
        'name': 'Diarrhea (Mild)',
        'symptoms': ['diarrhea', 'loose motion', 'watery stool'],
        'home_treatment': 'ORS, banana, curd.',
        'emergency_signs': ['blood in stool', 'dehydration', 'no urine'],
        'emergency_advice': 'Blood in stool or dehydration: urgent doctor visit.',
        'non_emergency_advice': 'Hydrate well. If persists, see a doctor.'
    },
    {
        'name': 'Cough (Dry or Wet)',
        'symptoms': ['cough', 'dry cough', 'wet cough'],
        'home_treatment': 'Ginger tea, honey, steam inhalation.',
        'emergency_signs': ['cough >1 week', 'breathing difficulty'],
        'emergency_advice': 'Breathing difficulty: emergency care needed.',
        'non_emergency_advice': 'Try home remedies. If cough >1 week, see a doctor.'
    },
    {
        'name': 'Minor Skin Allergy',
        'symptoms': ['skin allergy', 'itching', 'mild rash'],
        'home_treatment': 'Aloe vera, antihistamine.',
        'emergency_signs': ['spreading rash', 'swelling of lips/face'],
        'emergency_advice': 'Swelling or spreading rash: urgent care needed.',
        'non_emergency_advice': 'Monitor at home. If worsens, see a doctor.'
    },
    {
        'name': 'Mild Body Pain',
        'symptoms': ['body pain', 'muscle ache', 'mild pain'],
        'home_treatment': 'Rest, hot compress.',
        'emergency_signs': ['pain not reducing', 'severe pain'],
        'emergency_advice': 'Severe or persistent pain: see a doctor.',
        'non_emergency_advice': 'Try home remedies. If not improving, consult a doctor.'
    },
    # ... (Add 30+ more conditions, including emergencies: heart attack, stroke, jaundice, etc.)
    {
        'name': 'Heart Attack',
        'symptoms': ['chest pain', 'left arm pain', 'sweating', 'shortness of breath'],
        'home_treatment': 'None. Emergency only.',
        'emergency_signs': ['chest pain', 'sweating', 'left arm pain'],
        'emergency_advice': '🆘 Possible heart attack. Call emergency services immediately!',
        'non_emergency_advice': ''
    },
    {
        'name': 'Stroke',
        'symptoms': ['face drooping', 'slurred speech', 'weakness', 'vision loss'],
        'home_treatment': 'None. Emergency only.',
        'emergency_signs': ['face drooping', 'slurred speech', 'weakness'],
        'emergency_advice': '🆘 Possible stroke. Go to hospital immediately!',
        'non_emergency_advice': ''
    },
    {
        'name': 'Jaundice',
        'symptoms': ['yellow eyes', 'dark urine', 'yellow skin'],
        'home_treatment': 'See doctor for tests.',
        'emergency_signs': ['yellow eyes', 'dark urine'],
        'emergency_advice': 'Yellow eyes and dark urine: see a doctor soon.',
        'non_emergency_advice': 'Monitor and consult doctor.'
    },
    {
        'name': 'Migraine',
        'symptoms': ['severe headache', 'nausea', 'sensitivity to light', 'sensitivity to sound', 'aura'],
        'home_treatment': 'Rest in dark room, cold compress, pain relievers.',
        'emergency_signs': ['sudden severe headache', 'vision loss', 'confusion'],
        'emergency_advice': 'Sudden severe headache with confusion: seek urgent care.',
        'non_emergency_advice': 'Try home remedies. If severe or unusual, see a doctor.'
    },
    {
        'name': 'Food Poisoning',
        'symptoms': ['nausea', 'vomiting', 'diarrhea', 'stomach cramps', 'fever'],
        'home_treatment': 'Clear fluids, rest, bland diet, avoid dairy.',
        'emergency_signs': ['blood in vomit', 'severe dehydration', 'high fever'],
        'emergency_advice': 'Blood in vomit or severe dehydration: urgent care needed.',
        'non_emergency_advice': 'Hydrate well. If persists >24 hours, see a doctor.'
    },
    {
        'name': 'Urinary Tract Infection',
        'symptoms': ['frequent urination', 'burning sensation', 'cloudy urine', 'lower back pain'],
        'home_treatment': 'Drink plenty of water, cranberry juice, see doctor for antibiotics.',
        'emergency_signs': ['blood in urine', 'high fever', 'severe pain'],
        'emergency_advice': 'Blood in urine or high fever: see doctor immediately.',
        'non_emergency_advice': 'See doctor for antibiotics treatment.'
    },
    {
        'name': 'Ear Infection',
        'symptoms': ['ear pain', 'hearing loss', 'ear discharge', 'fever'],
        'home_treatment': 'Warm compress, pain relievers, see doctor for antibiotics.',
        'emergency_signs': ['severe ear pain', 'facial paralysis', 'high fever'],
        'emergency_advice': 'Severe pain or facial paralysis: urgent care needed.',
        'non_emergency_advice': 'See doctor for proper treatment.'
    },
    {
        'name': 'Sinusitis',
        'symptoms': ['facial pain', 'nasal congestion', 'headache', 'post-nasal drip'],
        'home_treatment': 'Steam inhalation, saline nasal spray, decongestants.',
        'emergency_signs': ['severe headache', 'vision problems', 'high fever'],
        'emergency_advice': 'Severe headache or vision problems: see doctor.',
        'non_emergency_advice': 'Try home remedies. If persists >10 days, see doctor.'
    },
    {
        'name': 'Bronchitis',
        'symptoms': ['persistent cough', 'mucus production', 'chest discomfort', 'fatigue'],
        'home_treatment': 'Rest, fluids, honey, steam inhalation.',
        'emergency_signs': ['breathing difficulty', 'chest pain', 'high fever'],
        'emergency_advice': 'Breathing difficulty or chest pain: seek medical care.',
        'non_emergency_advice': 'Rest and hydrate. If cough >3 weeks, see doctor.'
    },
    {
        'name': 'Pneumonia',
        'symptoms': ['high fever', 'cough with mucus', 'chest pain', 'breathing difficulty'],
        'home_treatment': 'See doctor immediately for antibiotics.',
        'emergency_signs': ['breathing difficulty', 'chest pain', 'high fever'],
        'emergency_advice': 'Breathing difficulty or chest pain: emergency care needed.',
        'non_emergency_advice': 'See doctor for proper treatment.'
    },
    {
        'name': 'Appendicitis',
        'symptoms': ['severe abdominal pain', 'nausea', 'vomiting', 'fever'],
        'home_treatment': 'None. Emergency surgery required.',
        'emergency_signs': ['severe abdominal pain', 'nausea', 'vomiting'],
        'emergency_advice': '🆘 Possible appendicitis. Go to hospital immediately!',
        'non_emergency_advice': ''
    },
    {
        'name': 'Kidney Stones',
        'symptoms': ['severe back pain', 'painful urination', 'blood in urine', 'nausea'],
        'home_treatment': 'Pain relievers, fluids, see doctor.',
        'emergency_signs': ['severe pain', 'blood in urine', 'fever'],
        'emergency_advice': 'Severe pain or blood in urine: urgent care needed.',
        'non_emergency_advice': 'See doctor for proper treatment.'
    },
    {
        'name': 'Gastritis',
        'symptoms': ['stomach pain', 'nausea', 'vomiting', 'loss of appetite'],
        'home_treatment': 'Avoid spicy food, antacids, small meals.',
        'emergency_signs': ['vomiting blood', 'black stools', 'severe pain'],
        'emergency_advice': 'Vomiting blood or black stools: emergency care needed.',
        'non_emergency_advice': 'Try home remedies. If persists, see doctor.'
    },
    {
        'name': 'Anemia',
        'symptoms': ['fatigue', 'weakness', 'pale skin', 'shortness of breath'],
        'home_treatment': 'Iron-rich foods, vitamin C, see doctor for tests.',
        'emergency_signs': ['severe fatigue', 'chest pain', 'fainting'],
        'emergency_advice': 'Severe fatigue or chest pain: see doctor.',
        'non_emergency_advice': 'See doctor for blood tests and treatment.'
    },
    {
        'name': 'Diabetes',
        'symptoms': ['frequent urination', 'excessive thirst', 'fatigue', 'blurred vision'],
        'home_treatment': 'See doctor for proper diagnosis and treatment.',
        'emergency_signs': ['very high blood sugar', 'confusion', 'fainting'],
        'emergency_advice': 'Very high blood sugar or confusion: emergency care needed.',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    },
    {
        'name': 'Hypertension',
        'symptoms': ['headache', 'dizziness', 'chest pain', 'shortness of breath'],
        'home_treatment': 'Reduce salt, exercise, see doctor for medication.',
        'emergency_signs': ['severe headache', 'chest pain', 'vision problems'],
        'emergency_advice': 'Severe headache or chest pain: emergency care needed.',
        'non_emergency_advice': 'See doctor for proper treatment.'
    },
    {
        'name': 'Asthma',
        'symptoms': ['wheezing', 'shortness of breath', 'chest tightness', 'coughing'],
        'home_treatment': 'Use inhaler, avoid triggers, see doctor.',
        'emergency_signs': ['severe breathing difficulty', 'chest pain', 'blue lips'],
        'emergency_advice': '🆘 Severe breathing difficulty: emergency care needed!',
        'non_emergency_advice': 'Use inhaler and see doctor for proper treatment.'
    },
    {
        'name': 'Allergic Reaction',
        'symptoms': ['itching', 'rash', 'swelling', 'sneezing', 'watery eyes'],
        'home_treatment': 'Antihistamines, avoid allergens, cold compress.',
        'emergency_signs': ['swelling of face/lips', 'breathing difficulty', 'dizziness'],
        'emergency_advice': '🆘 Swelling of face/lips or breathing difficulty: emergency care!',
        'non_emergency_advice': 'Take antihistamines. If worsens, see doctor.'
    },
    {
        'name': 'Conjunctivitis',
        'symptoms': ['red eyes', 'itching', 'watery eyes', 'eye discharge'],
        'home_treatment': 'Warm compress, avoid touching eyes, see doctor.',
        'emergency_signs': ['severe eye pain', 'vision loss', 'light sensitivity'],
        'emergency_advice': 'Severe eye pain or vision loss: urgent care needed.',
        'non_emergency_advice': 'See doctor for proper treatment.'
    },
    {
        'name': 'Dental Abscess',
        'symptoms': ['severe toothache', 'swelling', 'fever', 'bad taste in mouth'],
        'home_treatment': 'Pain relievers, salt water rinse, see dentist.',
        'emergency_signs': ['severe pain', 'swelling of face', 'fever'],
        'emergency_advice': 'Severe pain or facial swelling: urgent dental care needed.',
        'non_emergency_advice': 'See dentist for proper treatment.'
    },
    {
        'name': 'Sprain',
        'symptoms': ['joint pain', 'swelling', 'bruising', 'limited movement'],
        'home_treatment': 'RICE (Rest, Ice, Compression, Elevation).',
        'emergency_signs': ['severe pain', 'inability to move joint', 'numbness'],
        'emergency_advice': 'Severe pain or inability to move: see doctor.',
        'non_emergency_advice': 'Use RICE method. If not improving, see doctor.'
    },
    {
        'name': 'Fracture',
        'symptoms': ['severe pain', 'swelling', 'deformity', 'inability to move'],
        'home_treatment': 'Immobilize, ice, see doctor immediately.',
        'emergency_signs': ['severe pain', 'deformity', 'numbness'],
        'emergency_advice': '🆘 Possible fracture. Go to hospital immediately!',
        'non_emergency_advice': ''
    },
    {
        'name': 'Burns',
        'symptoms': ['red skin', 'blisters', 'pain', 'swelling'],
        'home_treatment': 'Cool water, clean dressing, pain relievers.',
        'emergency_signs': ['large burns', 'burns on face/hands', 'charred skin'],
        'emergency_advice': '🆘 Large burns or burns on face: emergency care needed!',
        'non_emergency_advice': 'Cool with water. If severe, see doctor.'
    },
    {
        'name': 'Heat Stroke',
        'symptoms': ['high body temperature', 'confusion', 'nausea', 'rapid heartbeat'],
        'home_treatment': 'Move to cool place, cool body, fluids.',
        'emergency_signs': ['high temperature', 'confusion', 'unconsciousness'],
        'emergency_advice': '🆘 Heat stroke: emergency care needed immediately!',
        'non_emergency_advice': ''
    },
    {
        'name': 'Hypothermia',
        'symptoms': ['shivering', 'confusion', 'slurred speech', 'weakness'],
        'home_treatment': 'Warm clothing, warm drinks, see doctor.',
        'emergency_signs': ['severe shivering', 'confusion', 'unconsciousness'],
        'emergency_advice': '🆘 Severe hypothermia: emergency care needed!',
        'non_emergency_advice': 'Warm up gradually. If severe, see doctor.'
    },
    {
        'name': 'Dehydration',
        'symptoms': ['thirst', 'dry mouth', 'dark urine', 'fatigue'],
        'home_treatment': 'Drink fluids, ORS, rest.',
        'emergency_signs': ['no urine', 'dizziness', 'confusion'],
        'emergency_advice': 'No urine or confusion: urgent care needed.',
        'non_emergency_advice': 'Drink plenty of fluids. If severe, see doctor.'
    },
    {
        'name': 'Insomnia',
        'symptoms': ['difficulty sleeping', 'waking up frequently', 'fatigue', 'irritability'],
        'home_treatment': 'Good sleep hygiene, avoid screens, relaxation techniques.',
        'emergency_signs': ['severe sleep deprivation', 'hallucinations'],
        'emergency_advice': 'Severe sleep deprivation: see doctor.',
        'non_emergency_advice': 'Try sleep hygiene. If persists, see doctor.'
    },
    {
        'name': 'Depression',
        'symptoms': ['sadness', 'loss of interest', 'fatigue', 'sleep problems'],
        'home_treatment': 'Talk to someone, exercise, see mental health professional.',
        'emergency_signs': ['thoughts of self-harm', 'suicidal thoughts'],
        'emergency_advice': '🆘 Thoughts of self-harm: seek immediate help!',
        'non_emergency_advice': 'Talk to a mental health professional.'
    },
    {
        'name': 'Anxiety',
        'symptoms': ['excessive worry', 'restlessness', 'rapid heartbeat', 'sweating'],
        'home_treatment': 'Deep breathing, relaxation techniques, see therapist.',
        'emergency_signs': ['panic attacks', 'chest pain', 'difficulty breathing'],
        'emergency_advice': 'Panic attacks or chest pain: see doctor.',
        'non_emergency_advice': 'Try relaxation techniques. See therapist if needed.'
    },
    {
        'name': 'Vertigo',
        'symptoms': ['dizziness', 'spinning sensation', 'nausea', 'balance problems'],
        'home_treatment': 'Rest, avoid sudden movements, see doctor.',
        'emergency_signs': ['severe dizziness', 'hearing loss', 'vision problems'],
        'emergency_advice': 'Severe dizziness with hearing/vision problems: see doctor.',
        'non_emergency_advice': 'Rest and avoid sudden movements. See doctor if persists.'
    },
    {
        'name': 'Sciatica',
        'symptoms': ['lower back pain', 'leg pain', 'numbness', 'tingling'],
        'home_treatment': 'Rest, gentle stretching, pain relievers.',
        'emergency_signs': ['severe pain', 'loss of bladder control', 'numbness'],
        'emergency_advice': 'Loss of bladder control or severe numbness: emergency care.',
        'non_emergency_advice': 'Rest and gentle stretching. If severe, see doctor.'
    },
    {
        'name': 'Carpal Tunnel Syndrome',
        'symptoms': ['hand numbness', 'tingling', 'weakness', 'pain'],
        'home_treatment': 'Wrist splint, rest, ergonomic adjustments.',
        'emergency_signs': ['severe pain', 'muscle wasting', 'complete numbness'],
        'emergency_advice': 'Severe pain or muscle wasting: see doctor.',
        'non_emergency_advice': 'Use wrist splint. If severe, see doctor.'
    },
    {
        'name': 'Tennis Elbow',
        'symptoms': ['elbow pain', 'forearm pain', 'weakness', 'stiffness'],
        'home_treatment': 'Rest, ice, pain relievers, gentle stretching.',
        'emergency_signs': ['severe pain', 'inability to move arm'],
        'emergency_advice': 'Severe pain or inability to move: see doctor.',
        'non_emergency_advice': 'Rest and ice. If persists, see doctor.'
    },
    {
        'name': 'Plantar Fasciitis',
        'symptoms': ['heel pain', 'foot pain', 'stiffness', 'worse in morning'],
        'home_treatment': 'Stretching, proper footwear, rest, ice.',
        'emergency_signs': ['severe pain', 'inability to walk'],
        'emergency_advice': 'Severe pain or inability to walk: see doctor.',
        'non_emergency_advice': 'Stretch and use proper footwear. If severe, see doctor.'
    },
    {
        'name': 'Hemorrhoids',
        'symptoms': ['rectal pain', 'bleeding', 'itching', 'swelling'],
        'home_treatment': 'Warm baths, fiber, stool softeners.',
        'emergency_signs': ['severe bleeding', 'severe pain', 'fever'],
        'emergency_advice': 'Severe bleeding or fever: see doctor.',
        'non_emergency_advice': 'Try home remedies. If persists, see doctor.'
    },
    {
        'name': 'Gallstones',
        'symptoms': ['upper abdominal pain', 'nausea', 'vomiting', 'back pain'],
        'home_treatment': 'Low-fat diet, pain relievers, see doctor.',
        'emergency_signs': ['severe pain', 'fever', 'yellow skin'],
        'emergency_advice': 'Severe pain or yellow skin: emergency care needed.',
        'non_emergency_advice': 'Low-fat diet. If severe, see doctor.'
    },
    {
        'name': 'Diverticulitis',
        'symptoms': ['abdominal pain', 'fever', 'nausea', 'constipation'],
        'home_treatment': 'Clear liquids, rest, see doctor.',
        'emergency_signs': ['severe pain', 'fever', 'bleeding'],
        'emergency_advice': 'Severe pain or bleeding: emergency care needed.',
        'non_emergency_advice': 'Clear liquids and rest. See doctor for treatment.'
    },
    {
        'name': 'Gout',
        'symptoms': ['joint pain', 'swelling', 'redness', 'stiffness'],
        'home_treatment': 'Rest, ice, pain relievers, avoid purine-rich foods.',
        'emergency_signs': ['severe pain', 'fever', 'multiple joints'],
        'emergency_advice': 'Severe pain or fever: see doctor.',
        'non_emergency_advice': 'Rest and ice. If severe, see doctor.'
    },
    {
        'name': 'Osteoarthritis',
        'symptoms': ['joint pain', 'stiffness', 'swelling', 'reduced range of motion'],
        'home_treatment': 'Exercise, weight management, pain relievers.',
        'emergency_signs': ['severe pain', 'joint deformity', 'inability to move'],
        'emergency_advice': 'Severe pain or joint deformity: see doctor.',
        'non_emergency_advice': 'Exercise and weight management. If severe, see doctor.'
    },
    {
        'name': 'Rheumatoid Arthritis',
        'symptoms': ['joint pain', 'stiffness', 'swelling', 'fatigue'],
        'home_treatment': 'See doctor for proper treatment.',
        'emergency_signs': ['severe pain', 'joint deformity', 'fever'],
        'emergency_advice': 'Severe pain or fever: see doctor.',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    },
    {
        'name': 'Lupus',
        'symptoms': ['fatigue', 'joint pain', 'skin rash', 'fever'],
        'home_treatment': 'See doctor for proper treatment.',
        'emergency_signs': ['chest pain', 'severe headache', 'seizures'],
        'emergency_advice': 'Chest pain or seizures: emergency care needed.',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    },
    {
        'name': 'Multiple Sclerosis',
        'symptoms': ['numbness', 'weakness', 'vision problems', 'balance issues'],
        'home_treatment': 'See doctor for proper treatment.',
        'emergency_signs': ['severe weakness', 'vision loss', 'difficulty speaking'],
        'emergency_advice': 'Severe weakness or vision loss: emergency care needed.',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    },
    {
        'name': 'Epilepsy',
        'symptoms': ['seizures', 'confusion', 'unconsciousness', 'muscle spasms'],
        'home_treatment': 'See doctor for proper treatment.',
        'emergency_signs': ['prolonged seizure', 'multiple seizures', 'injury'],
        'emergency_advice': '🆘 Prolonged seizure: emergency care needed!',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    },
    {
        'name': 'Parkinson\'s Disease',
        'symptoms': ['tremors', 'stiffness', 'slow movement', 'balance problems'],
        'home_treatment': 'See doctor for proper treatment.',
        'emergency_signs': ['severe tremors', 'falling', 'difficulty breathing'],
        'emergency_advice': 'Severe symptoms or falling: see doctor.',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    },
    {
        'name': 'Alzheimer\'s Disease',
        'symptoms': ['memory loss', 'confusion', 'personality changes', 'difficulty with tasks'],
        'home_treatment': 'See doctor for proper treatment.',
        'emergency_signs': ['severe confusion', 'wandering', 'aggression'],
        'emergency_advice': 'Severe confusion or wandering: see doctor.',
        'non_emergency_advice': 'See doctor for proper diagnosis and treatment.'
    }
]

EMERGENCY_KEYWORDS = [
    'chest pain', 'trouble breathing', 'loss of consciousness', 'face drooping', 'slurred speech',
    'no urine', 'severe pain', 'yellow eyes', 'dark urine', 'vision loss', 'unconscious', 'confusion',
    'vomiting blood', 'blood in stool', 'severe dehydration', 'cannot walk', 'emergency', 'hospital'
]

def diagnose(symptoms_list):
    """
    Given a list of symptoms, return best-matching disease(s), emergency status, and advice.
    """
    matched = []
    emergency = False
    emergency_reason = ''
    for disease in DISEASE_DATABASE:
        match_count = sum(1 for s in symptoms_list if any(s.lower() in sym.lower() for sym in disease['symptoms']))
        if match_count > 0:
            matched.append((disease, match_count))
            # Emergency check
            for ek in disease['emergency_signs']:
                if any(ek.lower() in s.lower() for s in symptoms_list):
                    emergency = True
                    emergency_reason = ek
    if not matched:
        return {
            'condition': 'Unknown',
            'home_treatment': 'Consult a healthcare professional for proper diagnosis.',
            'advice': 'Immediate consultation recommended.',
            'emergency': False
        }
    # Sort by match count
    matched.sort(key=lambda x: x[1], reverse=True)
    best = matched[0][0]
    if emergency:
        return {
            'condition': best['name'],
            'home_treatment': best['home_treatment'],
            'advice': best['emergency_advice'],
            'emergency': True,
            'emergency_reason': emergency_reason
        }
    else:
        return {
            'condition': best['name'],
            'home_treatment': best['home_treatment'],
            'advice': best['non_emergency_advice'],
            'emergency': False
        }

def is_emergency(symptoms_list):
    """
    Quick check for emergency keywords in symptoms.
    """
    for s in symptoms_list:
        for ek in EMERGENCY_KEYWORDS:
            if ek in s.lower():
                return True, ek
    return False, '' 