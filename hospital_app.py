import streamlit as st
import pandas as pd
import pickle

#LOAD MODEL
 
@st.cache_resource
def load_mode():
  with open('hospital_model_linshengkai.pkl','rb') as f:
    return pickle.load(f)

bundle = load_model()

#unpack our bundle into seperate columns/data
model = bundle['model']
scaler = bundle['scaler']
features = bundle['features']
cols_to_scale = bundle['cols_to_scale']
dept_map_inv = bundle['dept_Map_inv']
gender_map = bundle['gender_map']
temp_map = bundle['temp_map']
hr_map = bundle['hr_map']
dur_map = bundle ['dur_map']
cc_map = bundle['cc_map']

#Department info
DEPT_INFO = {
    'Respiratory Medicine': {
        'icon': '🫁', 'color': '#0284c7',
        'desc': 'Specialises in conditions affecting the lungs and airways.',
        'steps': ['Visit Level 2, Wing B', 'Estimated wait: 15–25 min', 'Please wear a mask'],
    },
    'Cardiology': {
        'icon': '❤️', 'color': '#dc2626',
        'desc': 'Specialises in heart and cardiovascular conditions.',
        'steps': ['Visit Level 3, Wing A', 'Estimated wait: 20–30 min', 'Bring any previous ECG reports'],
    },
    'Gastroenterology': {
        'icon': '🫃', 'color': '#d97706',
        'desc': 'Specialises in digestive system and abdominal conditions.',
        'steps': ['Visit Level 1, Wing C', 'Estimated wait: 10–20 min', 'Avoid eating before consultation'],
    },
    'Neurology': {
        'icon': '🧠', 'color': '#7c3aed',
        'desc': 'Specialises in brain, spine, and nervous system conditions.',
        'steps': ['Visit Level 4, Wing A', 'Estimated wait: 25–35 min', 'Bring list of current medications'],
    },
    'General Medicine': {
        'icon': '🩺', 'color': '#059669',
        'desc': 'Handles general health concerns and non-specialist conditions.',
        'steps': ['Visit Level 1, Wing A', 'Estimated wait: 10–15 min', 'Registration desk is open 24/7'],
    },
    'Dermatology': {
        'icon': '🔬', 'color': '#b45309',
        'desc': 'Specialises in skin, hair, and nail conditions.',
        'steps': ['Visit Level 2, Wing D', 'Estimated wait: 15–20 min', 'Bring photos of affected area if possible'],
    },
}


def predict_department(inputs: dict) -> tuple[str,float,list]:
 patient_df = pd.DataFrame([inputs])
 patient_df[cols_to_scale] = scaler.transform(patient_df[cols_to_scale])
 #run the model
 predicted_class = model.predict(patient_df[features])[0]
 all_proba = model.predict_proba(patient_df[features])[0]

# Convert Number to human readable label
 dept_name = dept_map_inv[predicted_class]
 confidence = all_proba[predicted_class]*100

 return dept_name, confidence, all_proba

def show_header():
 st.markdown("""
  <div style="background: linear-gradient(135deg, #1e3a8a,#1a56db,#0ea5e9);
              padding:3rem 2rem; text-align: center; margin-bottom: 2rem:">
      <p style = "color: #ededed ; font-size: 13px;
          FUTURE CLASSROOM: Machine Learning
      </p>
      <h1 style = "color:white;">
        Smart Hospital Patient Navigator
      </h1>
      <p style = color : white;font-size: 18px;>
          Find the right department for your symptoms
      </p>
  </div>
 """, unsafe_allow_html=True)

def show_symptom_section():
    """Returns a dict of symptom checkboxes {symptom_name: True/False}"""
    st.subheader("1. What are your main symptoms?")

    col1, col2, col3, col4 = st.columns(4)
    symptoms = {}

    with col1:
        symptoms['fever'] = st.checkbox("🌡️ Fever")
        symptoms['cough'] = st.checkbox("🤧 Cough")
    with col2:
        symptoms['headache']   = st.checkbox("🤕 Headache")
        symptoms['chest_pain'] = st.checkbox("💔 Chest Pain")
    with col3:
        symptoms['stomach_pain']     = st.checkbox("🤢 Stomach Pain")
        symptoms['shortness_breath'] = st.checkbox("😮‍💨 Shortness of Breath")
    with col4:
        symptoms['nausea_vomiting'] = st.checkbox("🤮 Nausea / Vomiting")
        symptoms['dizziness']       = st.checkbox("😵 Dizziness")

    col5, _, _, _ = st.columns(4)
    with col5:
        symptoms['skin_rash'] = st.checkbox("🔴 Skin Rash")

    return symptoms
def show_duration_section():
    """Returns chief_complaint and duration strings"""
    st.subheader("2. How long have you had these symptoms?")

    col1, col2 = st.columns(2)
    with col1:
        chief_complaint = st.selectbox("Chief complaint", options=list(cc_map.keys()))
    with col2:
        duration = st.selectbox("Duration", options=list(dur_map.keys()), index=1)

    return chief_complaint, duration
  
def show_severity_section():
    """Returns temperature and heart rate strings"""
    st.subheader("3. How would you rate the severity?")

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.selectbox("Temperature", options=list(temp_map.keys()), index=1)
    with col2:
        heart_rate = st.selectbox("Heart rate", options=list(hr_map.keys()), index=1)

    return temperature, heart_rate

def main():
    st.set_page_config(page_title="Smart Hospital Patient Navigator", page_icon="🏥", layout="wide")

    show_header()


def main():
    st.set_page_config(page_title="Smart Hospital Patient Navigator", page_icon='🏥', layout="wide")

    show_header()


if __name__ == "__main__":
   main()




      






