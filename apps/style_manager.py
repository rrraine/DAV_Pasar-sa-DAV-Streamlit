import streamlit as st


def inject_global_css():
    css = """
    <style>
    /*
        Theme Colors:
        - Primary Accent (Blue): #003366 (Deep Navy)
        - Secondary Accent (Green): #0A6E44 (Dark Forest Green)
        - Tertiary Accent (Brown/Cream): #B08968 (Muted Brown) / #F5EDE0 (Light Background Base)
    */

    /* --------------------------------------------------
                    CUSTOM FONT
    -------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* --------------------------------------------------
                GLOBAL PAGE BACKGROUND (Light Gradient with Animation)
    -------------------------------------------------- */

    .stApp {
        background: linear-gradient(135deg, #F5EDE0, #e7f4f5, #edf5fb);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --------------------------------------------------
                    HEADERS (Blue Accent)
    -------------------------------------------------- */

    h3, h2, h1 {
        
            /* 1. Apply Gradient Background (Blue to Green) */
        background: -webkit-linear-gradient(45deg, #003366, #0A6E44);
        background-clip: text;
        -webkit-background-clip: text;
        
        /* 2. Make Text Transparent so Gradient Shows Through */
        -webkit-text-fill-color: transparent;
        color: transparent; /* Fallback for non-webkit browsers */
        
        /* 3. Centering */
        text-align: center; 
        
        /* Reset left padding/border required for left alignment */
        padding-left: 0; 
        border-left: none; 
    
        
        font-weight: 700;
    }

    /* --------------------------------------------------
                    GLASSMORPHIC BASE STYLES
    -------------------------------------------------- */

    /* General Container Style */
    [data-testid="stContainer"], 
    [data-testid="stExpander"],
    .stDataFrame {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 5px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }

    /* Custom Class for the Overview Text Box (Manual Markdown Div) */
    .glass-card {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #B0896850; 
        box-shadow: 
            0 0 15px rgba(0, 51, 102, 0.3),
            0 4px 20px rgba(0,0,0,0.1);
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 0 15px rgba(0, 51, 102, 0.3),
            0 12px 30px rgba(0,0,0,0.18);
    }

    /* --- THE NEW CLASS FOR BLUE ACCENT SHADOW --- */
    /* Target the container element specifically for this accent */
    .accent-glass-container {
        /* Inherits background/blur from the general styles */
        box-shadow: 0 0 20px rgba(0, 51, 102, 0.5), /* Blue Glow */
                    0 8px 15px rgba(0,0,0,0.2); /* Standard Shadow */
        border: 2px solid #00336680; /* Subtle Blue Border */
        transform: scale(1.01); /* Slightly larger pop */
    }
    .accent-glass-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(0, 51, 102, 0.7), 
                    0 10px 20px rgba(0,0,0,0.3);
    }
    /* ------------------------------------------- */

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* --------------------------------------------------
                    INPUTS: SELECTBOX, SLIDERS (Green Accent)
    -------------------------------------------------- */

    /* Selectbox Label */
    .stSelectbox label {
        font-weight: 600;
        color: #003366; /* Blue text for label */
    }

    /* Selectbox Border */
    .stSelectbox select {
        border-radius: 10px !important;
        border: 2px solid #0A6E44 !important; /* Green border */
    }

    /* Slider Track */
    .stSlider > div[data-baseweb="slider"] > div > div {
        background: #0A6E44 !important; /* Green track */
    }

    /* Slider Thumb */
    .stSlider .thumb {
        background: #003366 !important; /* Blue thumb */
        border: 2px solid #F5EDE0 !important; /* Light border */
    }

    /* --------------------------------------------------
                    BUTTONS (Blue to Green Gradient)
    -------------------------------------------------- */

    .stButton>button {
        /* Gradient uses Primary Blue and Secondary Green */
        background: linear-gradient(135deg, #003366, #0A6E44); 
        color: white;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 600;
        transition: 0.25s ease-in-out;
        border: none;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        /* Gradient reverses on hover */
        background: linear-gradient(135deg, #0A6E44, #003366); 
        box-shadow: 0 4px 15px rgba(0, 51, 102, 0.4);
    }

    /* --------------------------------------------------
                    LINKS (Green Accent)
    -------------------------------------------------- */
    a {
        color: #0A6E44 !important; /* Green link color */
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease;
    }

    a:hover {
        text-decoration: underline;
        color: #003366 !important; /* Blue hover for contrast */
    }

    /* --------------------------------------------------
                    FOOTER (Match Header)
    -------------------------------------------------- */
    .footer-container {
        background-color: #003366; /* Blue background */
        color: #F5EDE0; /* Cream text */
        border-top: 3px solid #0A6E44 !important; /* Green border */
        padding: 10px 20px;
        text-align: center;
        font-size: 14px;
        margin-top: 50px;
    }
    .footer-container a {
        color: #F5EDE0 !important; /* Cream links */
    }
    
    
    .filter-reset-container {
        position: relative !important;
        z-index: 10;
        float: none !important;
        background: rgba(255, 255, 255, 0.6); 
        border-radius: 10px;
    }
    
    
    /*Experimentation Please Dont Mind*/
    /* ------------------------------
       DASHBOARD GRID
    ------------------------------ */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
        gap: 25px;
        margin-top: 20px;
    }
    
    
    /* ------------------------------
       CARD COMPONENTS
    ------------------------------ */
    .card {
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(14px);
        background: rgba(255,255,255,0.45);
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
        transition: 0.25s ease-in-out;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    .card-title {
        font-size: 20px;
        color: #003366;
        font-weight: 700;
        border-left: 5px solid #1A7340;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)