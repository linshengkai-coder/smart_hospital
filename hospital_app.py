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
