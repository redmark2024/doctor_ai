import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
#import cv2
from PIL import Image
import io
import hashlib
import datetime
import csv
import os
import random
import time
import numpy as np
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import qrcode
import folium
from streamlit_folium import folium_static
import json
import re

# Page configuration
st.set_page_config(
    page_title="RedMark - The AI Doctor",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {
        'total_users': 0,
        'active_users': 0,
        'diseases_count': {},
        'languages_used': {},
        'user_locations': {},
        'last_activity': {},
        'total_diagnoses': 0,
        'emergency_cases': 0,
        'donation_amount': 0
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_user' not in st.session_state:
    st.session_state.current_user = {
        'name': '',
        'age': '',
        'language': 'en',
        'location': 'Unknown'
    }

# Language mappings
LANGUAGES = {
    'en': 'English',
    'hi': 'हिंदी',
    'bn': 'বাংলা',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'mr': 'मराठी'
}

# --- Symptom patterns and disease database ---
SYMPTOM_PATTERNS = {
    "fever": [
        "fever", "temperature", "high temperature", "body is hot", "my body is hot",
        "i feel hot", "i have a fever", "my temperature is", "104 degree", "high fever",
        "i am burning up", "i feel chills", "i am shivering", "my body is burning"
    ],
    "common cold": [
        "cold", "runny nose", "sneezing", "sore throat", "blocked nose", "stuffy nose"
    ],
    "headache": [
        "headache", "head hurts", "pain in my head", "my head is aching", "i have a headache"
    ],
    "constipation": [
        "constipation", "no bowel movement", "hard stool", "difficulty passing stool"
    ],
    "acidity": [
        "acidity", "indigestion", "heartburn", "acid reflux", "burning in stomach"
    ],
    "diarrhea": [
        "diarrhea", "loose motion", "watery stool", "frequent stool", "stomach upset"
    ],
    "cough": [
        "cough", "coughing", "dry cough", "wet cough", "i am coughing", "i have a cough"
    ],
    "skin allergy": [
        "skin allergy", "rash", "itchy skin", "red spots", "skin irritation"
    ],
    "body pain": [
        "body pain", "muscle pain", "body ache", "pain all over", "sore muscles"
    ],
    # Emergency
    "heart attack": [
        "chest pain", "left arm pain", "sweating with pain", "pressure in chest"
    ],
    "stroke": [
        "face drooping", "slurred speech", "weakness on one side", "can't move arm", "sudden confusion"
    ],
    "high fever": [
        "high fever", "temperature above 102", "very high temperature", "burning up badly"
    ],
    "breathing difficulty": [
        "breathing difficulty", "can't breathe", "wheezing", "gasping", "shortness of breath"
    ],
    "severe dehydration": [
        "severe dehydration", "no urine", "dizziness", "dry mouth", "sunken eyes"
    ],
    "severe abdominal pain": [
        "severe abdominal pain", "can't walk due to pain", "vomiting with pain", "sharp stomach pain"
    ],
    "unconsciousness": [
        "unconscious", "not responding", "fainted", "passed out"
    ],
    "jaundice": [
        "yellow eyes", "dark urine", "yellow skin", "jaundice"
    ],
    "vision loss": [
        "vision loss", "sudden blindness", "blurry vision", "can't see"
    ]
}

DISEASE_DATABASE = {
    "common cold": {
        "condition": "Common Cold",
        "home_treatment": "Steam inhalation, rest, and plenty of fluids.",
        "advice": "Monitor for high fever (>101°F).",
        "watch_out_for": "High fever > 101°F",
        "emergency": False
    },
    "fever": {
        "condition": "Mild Fever (<100.5°F)",
        "home_treatment": "Drink fluids, rest, and take paracetamol if needed.",
        "advice": "If fever lasts more than 3 days, consult a doctor.",
        "watch_out_for": "Lasts >3 days",
        "emergency": False
    },
    "headache": {
        "condition": "Headache",
        "home_treatment": "Sleep, hydration, and gentle massage.",
        "advice": "If sudden, severe, or one-sided, seek medical attention.",
        "watch_out_for": "Sudden, severe, or one-sided",
        "emergency": False
    },
    "constipation": {
        "condition": "Constipation",
        "home_treatment": "Increase fiber, drink warm water.",
        "advice": "If no bowel movement for 5+ days, consult a doctor.",
        "watch_out_for": "No bowel for 5+ days",
        "emergency": False
    },
    "acidity": {
        "condition": "Acidity / Indigestion",
        "home_treatment": "Cold milk, antacids.",
        "advice": "If persistent after meals, see a doctor.",
        "watch_out_for": "Persistent after meals",
        "emergency": False
    },
    "diarrhea": {
        "condition": "Mild Diarrhea",
        "home_treatment": "ORS, banana, curd.",
        "advice": "If blood in stool or dehydration, seek medical help.",
        "watch_out_for": "Blood in stool, dehydration",
        "emergency": False
    },
    "cough": {
        "condition": "Cough (Dry or Wet)",
        "home_treatment": "Ginger tea, honey.",
        "advice": "If lasts more than 1 week, consult a doctor.",
        "watch_out_for": "Lasts >1 week",
        "emergency": False
    },
    "skin allergy": {
        "condition": "Minor Skin Allergy",
        "home_treatment": "Aloe vera, antihistamine.",
        "advice": "If rash is spreading, see a doctor.",
        "watch_out_for": "Spreading rash",
        "emergency": False
    },
    "body pain": {
        "condition": "Mild Body Pain",
        "home_treatment": "Rest, hot compress.",
        "advice": "If pain doesn't reduce, consult a doctor.",
        "watch_out_for": "Pain that doesn't reduce",
        "emergency": False
    },
    # Emergency conditions
    "heart attack": {
        "condition": "Possible Heart Attack",
        "home_treatment": "",
        "advice": "🆘 Chest pain, sweating, left arm pain: Call emergency now!",
        "watch_out_for": "Chest pain, sweating, left arm pain",
        "emergency": True
    },
    "stroke": {
        "condition": "Possible Stroke",
        "home_treatment": "",
        "advice": "🆘 Face drooping, slurred speech, weakness: Immediate hospital visit!",
        "watch_out_for": "Face drooping, slurred speech, weakness",
        "emergency": True
    },
    "high fever": {
        "condition": "High Fever (>102°F)",
        "home_treatment": "",
        "advice": "Shivering, confusion, vomiting: Doctor visit required.",
        "watch_out_for": "Shivering, confusion, vomiting",
        "emergency": True
    },
    "breathing difficulty": {
        "condition": "Breathing Difficulty",
        "home_treatment": "",
        "advice": "Wheezing, gasping, can't talk: Go to emergency room.",
        "watch_out_for": "Wheezing, gasping, can't talk",
        "emergency": True
    },
    "severe dehydration": {
        "condition": "Severe Dehydration",
        "home_treatment": "",
        "advice": "No urine, dizziness, dry mouth: Urgent IV fluids needed.",
        "watch_out_for": "No urine, dizziness, dry mouth",
        "emergency": True
    },
    "severe abdominal pain": {
        "condition": "Severe Abdominal Pain",
        "home_treatment": "",
        "advice": "Can't walk, vomiting: Doctor urgently.",
        "watch_out_for": "Can't walk, vomiting",
        "emergency": True
    },
    "unconsciousness": {
        "condition": "Unconsciousness",
        "home_treatment": "",
        "advice": "No response: Immediate help required.",
        "watch_out_for": "No response",
        "emergency": True
    },
    "jaundice": {
        "condition": "Yellow Eyes + Dark Urine (Possible Jaundice)",
        "home_treatment": "",
        "advice": "Doctor checkup required.",
        "watch_out_for": "Possible liver/jaundice",
        "emergency": True
    },
    "vision loss": {
        "condition": "Sudden Vision Loss / Blurriness",
        "home_treatment": "",
        "advice": "Neurological issue: Emergency eye care needed.",
        "watch_out_for": "Neurological issue",
        "emergency": True
    }
}

def translate_text(text, target_lang):
    """Translate text to target language"""
    try:
        if target_lang == 'en':
            return text
        translator = GoogleTranslator(source='en', target=target_lang)
        return translator.translate(text)
    except:
        return text

def get_user_location():
    """Get user location based on IP"""
    try:
        ip = requests.get('https://api.ipify.org').text
        geo = requests.get(f'https://ipapi.co/{ip}/json/').json()
        city = geo.get('city', 'Unknown')
        country = geo.get('country_name', 'Unknown')
        return f"{city}, {country}"
    except:
        return "Unknown"

def update_user_stats(language, disease=None, emergency=False):
    """Update user statistics"""
    current_time = datetime.datetime.now()
    user_location = get_user_location()
    
    # Update total users
    st.session_state.user_stats['total_users'] += 1
    
    # Update active users (within last 5 minutes)
    st.session_state.user_stats['last_activity'][user_location] = current_time
    active_count = sum(1 for time in st.session_state.user_stats['last_activity'].values() 
                      if (current_time - time).seconds < 300)
    st.session_state.user_stats['active_users'] = active_count
    
    # Update language usage
    if language in st.session_state.user_stats['languages_used']:
        st.session_state.user_stats['languages_used'][language] += 1
    else:
        st.session_state.user_stats['languages_used'][language] = 1
    
    # Update disease count
    if disease:
        if disease in st.session_state.user_stats['diseases_count']:
            st.session_state.user_stats['diseases_count'][disease] += 1
        else:
            st.session_state.user_stats['diseases_count'][disease] = 1
    
    # Update location count
    if user_location in st.session_state.user_stats['user_locations']:
        st.session_state.user_stats['user_locations'][user_location] += 1
    else:
        st.session_state.user_stats['user_locations'][user_location] = 1
    
    # Update diagnosis counts
    st.session_state.user_stats['total_diagnoses'] += 1
    if emergency:
        st.session_state.user_stats['emergency_cases'] += 1

def voice_to_text():
    """Convert voice input to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.error("No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            st.error("Could not understand audio. Please try again.")
            return None
        except Exception as e:
            st.error(f"Error: {e}")
            return None

def text_to_speech(text, language):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        
        # Set language-specific voice
        voices = engine.getProperty('voices')
        if language == "hi" and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        elif language == "bn" and len(voices) > 2:
            engine.setProperty('voice', voices[2].id)
        
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        st.error(f"Speech synthesis error: {e}")
        return False

def analyze_image(image):
    """Analyze uploaded image for symptoms"""
    try:
        # Convert to OpenCV format
        img_array = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Simple color analysis for symptom detection
        hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV)
        
        # Detect red areas (potential rash)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # Detect yellow areas (potential jaundice)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Detect white areas (potential fungal infection)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        red_pixels = cv2.countNonZero(red_mask)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        white_pixels = cv2.countNonZero(white_mask)
        total_pixels = img_array.shape[0] * img_array.shape[1]
        
        red_percentage = (red_pixels / total_pixels) * 100
        yellow_percentage = (yellow_pixels / total_pixels) * 100
        white_percentage = (white_pixels / total_pixels) * 100
        
        if red_percentage > 5:
            return "rash"
        elif yellow_percentage > 5:
            return "jaundice"
        elif white_percentage > 10:
            return "fungal"
        else:
            return "normal"
    except Exception as e:
        st.error(f"Image analysis error: {e}")
        return "unknown"

def create_pdf_report(user_name, symptoms, diagnosis, language):
    """Generate PDF report of diagnosis"""
    try:
        filename = f"health_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        c = canvas.Canvas(filename, pagesize=letter)
        c.setTitle("Health Diagnosis Report")
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "AI Health Assistant - Diagnosis Report")
        c.line(50, 740, 550, 740)
        
        # Patient Info
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 700, "Patient Information:")
        c.setFont("Helvetica", 10)
        c.drawString(50, 680, f"Name: {user_name if user_name else 'Not provided'}")
        c.drawString(50, 660, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        c.drawString(50, 640, f"Language: {LANGUAGES.get(language, language)}")
        
        # Symptoms
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 600, "Reported Symptoms:")
        c.setFont("Helvetica", 10)
        y_pos = 580
        for symptom in symptoms:
            c.drawString(50, y_pos, f"• {symptom}")
            y_pos -= 15
        
        # Diagnosis
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos - 20, "Diagnosis:")
        c.setFont("Helvetica", 10)
        c.drawString(50, y_pos - 40, f"Condition: {diagnosis['condition']}")
        c.drawString(50, y_pos - 60, f"Home Treatment: {diagnosis['home_treatment']}")
        c.drawString(50, y_pos - 80, f"Advice: {diagnosis['advice']}")
        c.drawString(50, y_pos - 100, f"**Watch Out For:** {diagnosis.get('watch_out_for', '')}")
        
        # Emergency warning if applicable
        if diagnosis.get('emergency', False):
            c.setFont("Helvetica-Bold", 12)
            c.setFillColorRGB(1, 0, 0)  # Red color
            c.drawString(50, y_pos - 120, "⚠️ EMERGENCY CASE - SEEK IMMEDIATE MEDICAL ATTENTION")
            c.setFillColorRGB(0, 0, 0)  # Reset to black
        
        # Footer
        c.setFont("Helvetica", 8)
        c.drawString(50, 50, "Disclaimer: This report is for informational purposes only and should not replace professional medical advice.")
        
        c.save()
        return filename
    except Exception as e:
        st.error(f"PDF generation error: {e}")
        return None

def create_analytics_charts():
    """Create analytics charts"""
    charts = {}
    
    # Language usage pie chart
    if st.session_state.user_stats['languages_used']:
        lang_df = pd.DataFrame(list(st.session_state.user_stats['languages_used'].items()), 
                              columns=['Language', 'Count'])
        charts['language_pie'] = px.pie(lang_df, values='Count', names='Language', 
                                       title='Language Usage Distribution')
    
    # Disease frequency bar chart
    if st.session_state.user_stats['diseases_count']:
        disease_df = pd.DataFrame(list(st.session_state.user_stats['diseases_count'].items()), 
                                 columns=['Disease', 'Count'])
        charts['disease_bar'] = px.bar(disease_df, x='Disease', y='Count', 
                                      title='Most Common Diagnoses')
    
    # Emergency vs Non-emergency pie chart
    emergency_data = {
        'Emergency Cases': st.session_state.user_stats['emergency_cases'],
        'Non-Emergency Cases': st.session_state.user_stats['total_diagnoses'] - st.session_state.user_stats['emergency_cases']
    }
    emergency_df = pd.DataFrame(list(emergency_data.items()), columns=['Type', 'Count'])
    charts['emergency_pie'] = px.pie(emergency_df, values='Count', names='Type', 
                                    title='Emergency vs Non-Emergency Cases')
    
    return charts

def create_user_map():
    """Create a map showing user locations"""
    if not st.session_state.user_stats['user_locations']:
        return None
    
    # Create a map centered on India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    for location, count in st.session_state.user_stats['user_locations'].items():
        if location != "Unknown":
            # Simple geocoding (in real app, use proper geocoding service)
            folium.Marker(
                location=[random.uniform(8, 37), random.uniform(68, 97)],  # India bounds
                popup=f"{location}: {count} users",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
    return m

def chatbot_followup(symptoms, diagnosis):
    """Generate follow-up questions for better diagnosis"""
    followup_questions = []
    
    if 'fever' in ' '.join(symptoms).lower():
        followup_questions.append("Is the fever continuous or on/off?")
        followup_questions.append("What is your temperature?")
    
    if 'pain' in ' '.join(symptoms).lower():
        followup_questions.append("On a scale of 1-10, how severe is the pain?")
        followup_questions.append("Is the pain constant or intermittent?")
    
    if 'cough' in ' '.join(symptoms).lower():
        followup_questions.append("Is it a dry cough or productive cough?")
        followup_questions.append("When does the cough worsen?")
    
    if 'rash' in ' '.join(symptoms).lower():
        followup_questions.append("Is the rash itchy?")
        followup_questions.append("When did the rash first appear?")
    
    return followup_questions

def extract_symptoms(user_input):
    user_input = user_input.lower()
    found = []
    for symptom, patterns in SYMPTOM_PATTERNS.items():
        for pat in patterns:
            if re.search(rf"\b{re.escape(pat)}\b", user_input):
                found.append(symptom)
                break
    return found

def diagnose(symptoms):
    for symptom in symptoms:
        if symptom in DISEASE_DATABASE:
            return DISEASE_DATABASE[symptom]
    # Default fallback
    return {
        "condition": "Unknown",
        "home_treatment": "",
        "advice": "Sorry, I couldn't identify your condition. Please consult a doctor if you feel unwell.",
        "watch_out_for": "",
        "emergency": False
    }

def main():
    st.title("🩸 RedMark - Your Medical Guide")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        # Language selector
        language = st.selectbox(
            "Select Language / भाषा चुनें / ভাষা নির্বাচন করুন",
            list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x]
        )
        st.session_state.current_user['language'] = language
        # Remove username input from sidebar
        # Input mode selector
        input_mode = st.radio(
            "Input Mode / इनपुट मोड / ইনপুট মোড",
            ["Chat", "Text", "Voice", "Image"]
        )
        # Donation section
        st.header("💝 Support the Project")
        st.info("UPI ID: 6294921690@okbizaxis")
        # Quick stats
        st.header("📊 Quick Stats")
        st.metric("Total Users", st.session_state.user_stats['total_users'])
        st.markdown(f"**Active Users:** 🟢 {st.session_state.user_stats['active_users']}")
        st.metric("Total Diagnoses", st.session_state.user_stats['total_diagnoses'])
        st.metric("Emergency Cases", st.session_state.user_stats['emergency_cases'])
        # Talk to real doctor button
        st.header("🩺 Need Real Help?")
        if st.button("Talk to a Real Doctor"):
            st.info("📞 Call: +91-1800-XXX-XXXX\n📧 Email: doctor@aihealth.com\n💬 WhatsApp: +91-98765-43210")
    # Main area
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("User Information")
        if not st.session_state.current_user['name']:
            st.markdown('<div style="font-size:2rem;font-weight:600;color:#d7263d;font-family:sans-serif;margin-bottom:10px;">Enter your name</div>', unsafe_allow_html=True)
            user_name = st.text_input("", value="", key="name_input")
            if user_name:
                st.session_state.current_user['name'] = user_name
                st.success(f"Welcome, {user_name}! Start chatting below.")
            else:
                st.stop()
        else:
            st.info(f"You are chatting as: {st.session_state.current_user['name']}")
        st.header("💬 Chat with RedMark AI Doctor")
        st.markdown('<style>.user-msg{background:#e6f7ff;padding:10px;border-radius:10px;margin-bottom:5px;}.ai-msg{background:#fff3f3;padding:10px;border-radius:10px;margin-bottom:5px;}</style>', unsafe_allow_html=True)
        # Chat input
        user_message = st.text_input("Type your message:", key="chat_input")
        if st.button("Send"):
            if user_message:
                symptoms = extract_symptoms(user_message)
                if not symptoms:
                    st.session_state.chat_history.append({
                        "role": "assistant", "name": "RedMark",
                        "content": "Sorry, I couldn't detect any symptoms. Please describe how you feel in more detail."
                    })
                else:
                    diagnosis = diagnose(symptoms)
                    st.session_state.chat_history.append({
                        "role": "assistant", "name": "RedMark",
                        "content": (
                            f"**Condition:** {diagnosis['condition']}\n"
                            f"**Home Treatment:** {diagnosis['home_treatment']}\n"
                            f"**Advice:** {diagnosis['advice']}\n"
                            f"**Watch Out For:** {diagnosis.get('watch_out_for', '')}\n"
                            + ("🚨 Your symptoms may indicate a serious condition. Please consult a doctor immediately or visit the nearest hospital."
                               if diagnosis['emergency'] else
                               "This appears to be a non-emergency. Please try the suggested home treatments. If symptoms persist or worsen after 3–5 days, please consult a doctor.")
                        )
                    })
        # Display chat history in a user-friendly way
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-msg"><b>{message["name"]}:</b> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-msg"><b>RedMark:</b> {message["content"]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.header("📈 Analytics Dashboard")
        
        # Create charts
        charts = create_analytics_charts()
        
        # Display charts
        if 'language_pie' in charts:
            st.plotly_chart(charts['language_pie'], use_container_width=True)
        
        if 'disease_bar' in charts:
            st.plotly_chart(charts['disease_bar'], use_container_width=True)
        
        if 'emergency_pie' in charts:
            st.plotly_chart(charts['emergency_pie'], use_container_width=True)
        
        # User map
        st.subheader("🗺️ User Locations")
        user_map = create_user_map()
        if user_map:
            folium_static(user_map)
        else:
            st.info("No location data available yet.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>⚠️ Disclaimer: This is not a substitute for professional medical advice. Always consult a healthcare provider for proper diagnosis and treatment.</p>
            <p>🚨 Emergency: If you're experiencing severe symptoms, call emergency services immediately.</p>
            <p>📞 Emergency Numbers: 108 (India), 911 (US), 112 (EU)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 
