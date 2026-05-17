import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        /* Main background and text */
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        
        /* Metric Cards (KPIs) */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border: 1px solid #334155;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease-in-out;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            border-color: #3B82F6;
        }
        
        /* Metric Text Styling */
        div[data-testid="metric-container"] label {
            color: #94A3B8 !important;
            font-weight: 600;
            font-size: 1.1rem;
        }
        div[data-testid="metric-container"] div {
            color: #F8FAFC !important;
            font-weight: 700;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1E293B;
            border-right: 1px solid #334155;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)