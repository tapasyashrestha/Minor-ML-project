import os
import sys
import pickle
import streamlit as st
import pandas as pd

# Add the project root and src directory to sys.path for robust imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if current_dir not in sys.path:
    sys.path.append(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from preprocess import clean_text

# Set page configuration
st.set_page_config(
    page_title="Intelligent SMS Spam Detector",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design & Aesthetics (Dynamic Dark/Light Mode)
theme_mode = st.sidebar.selectbox("🌓 Select Theme Mode", ["Light Mode", "Dark Mode"])

if theme_mode == "Dark Mode":
    st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit Footer & Menu */
    footer {
        visibility: hidden !important;
    }
    .sidebar-footer {
        position: fixed;
        bottom: 15px;
        left: 20px;
        font-size: 0.75rem;
        color: rgba(250, 249, 246, 0.45) !important;
        font-family: 'Space Grotesk', sans-serif;
        z-index: 9999;
        font-weight: 400;
    }
    
    /* Global Styles */
    html, body, p, h1, h2, h3, h4, h5, h6, label, li, a, input, textarea, select {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Streamlit App Canvas Redesign */
    [data-testid="stAppViewContainer"] {
        background-color: #181013 !important;
        background-image: radial-gradient(rgba(209, 61, 133, 0.08) 1px, transparent 0);
        background-size: 16px 16px;
        color: #FAF9F6 !important;
    }
    
    /* Streamlit Header Override */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Streamlit Sidebar Redesign (Split Screen Deepest Murrey) */
    [data-testid="stSidebar"] {
        background-color: #12020A !important;
        border-right: 1px solid rgba(209, 61, 133, 0.2);
    }
    /* Restrict styling to prevent breaking icon fonts */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li {
        color: #FAF9F6 !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    [data-testid="stSidebar"] div[data-testid="stNotification"] {
        background-color: rgba(209, 61, 133, 0.08) !important;
        border: 1px solid rgba(209, 61, 133, 0.2) !important;
        color: #FAF9F6 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stNotification"] svg {
        fill: #D13D85 !important;
    }
    
    /* Title and Header styling */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #D13D85;
        letter-spacing: -0.03em;
        margin-bottom: 0.1rem;
        text-transform: uppercase;
    }
    .sub-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        color: #A69498;
        margin-bottom: 2rem;
        letter-spacing: -0.01em;
    }
    
    /* Metric Card styling */
    .metric-card {
        background-color: rgba(209, 61, 133, 0.05) !important;
        border-radius: 4px;
        padding: 12px 15px;
        border-left: 4px solid #D13D85 !important;
        border-top: 1px solid rgba(209, 61, 133, 0.15) !important;
        border-right: 1px solid rgba(209, 61, 133, 0.15) !important;
        border-bottom: 1px solid rgba(209, 61, 133, 0.15) !important;
        margin-bottom: 12px;
        box-shadow: none !important;
    }
    .metric-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        color: #A69498 !important;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.7rem;
        font-weight: 700;
        color: #FAF9F6 !important;
    }
    
    /* Result Box styling */
    .result-box-spam {
        background-color: #3D1222 !important;
        border: 1px solid rgba(209, 61, 133, 0.4) !important;
        border-radius: 4px !important;
        padding: 20px;
        color: #FAF9F6 !important;
        border-left: 6px solid #D13D85 !important;
        margin-top: 15px;
        box-shadow: none !important;
    }
    .result-box-ham {
        background-color: #142B1A !important;
        border: 1px solid rgba(78, 135, 92, 0.4) !important;
        border-radius: 4px !important;
        padding: 20px;
        color: #FAF9F6 !important;
        border-left: 6px solid #4E875C !important;
        margin-top: 15px;
        box-shadow: none !important;
    }
    
    /* Card style for elements */
    .ui-card {
        background-color: #22161A;
        border-radius: 6px;
        padding: 25px;
        border: 1px solid rgba(209, 61, 133, 0.2);
        box-shadow: none !important;
        position: relative;
    }
    .ui-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background-color: #D13D85;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    
    /* Streamlit Button Styling (Secondary outline by default, primary filled) */
    div.stButton > button {
        background-color: transparent !important;
        color: #D13D85 !important;
        border-radius: 4px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1.2rem !important;
        border: 1px solid rgba(209, 61, 133, 0.45) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: none !important;
    }
    div.stButton > button:hover {
        background-color: rgba(209, 61, 133, 0.08) !important;
        border-color: #D13D85 !important;
        color: #D13D85 !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Primary buttons (Analyze Message, Train Model) */
    div.stButton > button[kind="primary"] {
        background-color: #D13D85 !important;
        color: #FAF9F6 !important;
        border: 1px solid #D13D85 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 2.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #FAF9F6 !important;
        color: #D13D85 !important;
        border-color: #FAF9F6 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Form Input elements override */
    div[data-baseweb="textarea"] textarea, div[data-baseweb="input"] input {
        background-color: #22161A !important;
        color: #FAF9F6 !important;
        border: 1px solid rgba(209, 61, 133, 0.3) !important;
        border-radius: 4px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    div[data-baseweb="textarea"] textarea:focus, div[data-baseweb="input"] input:focus {
        border-color: #D13D85 !important;
        box-shadow: 0 0 0 1px #D13D85 !important;
    }
    
    /* Custom progress bar indicator */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #D13D85 !important;
    }
    
    /* Monospace Code & Tokens styling */
    code {
        font-family: 'Share Tech Mono', monospace !important;
        background-color: #12020A !important;
        color: #FAF9F6 !important;
        border-radius: 4px;
        padding: 3px 6px;
    }
</style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit Footer & Menu */
    footer {
        visibility: hidden !important;
    }
    .sidebar-footer {
        position: fixed;
        bottom: 15px;
        left: 20px;
        font-size: 0.75rem;
        color: rgba(250, 249, 246, 0.45) !important;
        font-family: 'Space Grotesk', sans-serif;
        z-index: 9999;
        font-weight: 400;
    }
    
    /* Global Styles */
    html, body, p, h1, h2, h3, h4, h5, h6, label, li, a, input, textarea, select {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Streamlit App Canvas Redesign */
    [data-testid="stAppViewContainer"] {
        background-color: #F5F3EC !important;
        background-image: radial-gradient(rgba(139, 0, 75, 0.05) 1px, transparent 0);
        background-size: 16px 16px;
        color: #241C1E !important;
    }
    
    /* Streamlit Header Override */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Streamlit Sidebar Redesign (Split Screen Deep Murrey) */
    [data-testid="stSidebar"] {
        background-color: #2D0018 !important;
        border-right: 1px solid rgba(139, 0, 75, 0.15);
    }
    /* Restrict styling to prevent breaking icon fonts */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li {
        color: #FAF9F6 !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    [data-testid="stSidebar"] div[data-testid="stNotification"] {
        background-color: rgba(245, 243, 236, 0.05) !important;
        border: 1px solid rgba(245, 243, 236, 0.15) !important;
        color: #FAF9F6 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stNotification"] svg {
        fill: #8B004B !important;
    }
    
    /* Title and Header styling */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #8B004B;
        letter-spacing: -0.03em;
        margin-bottom: 0.1rem;
        text-transform: uppercase;
    }
    .sub-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        color: #756569;
        margin-bottom: 2rem;
        letter-spacing: -0.01em;
    }
    
    /* Metric Card styling */
    .metric-card {
        background-color: rgba(245, 243, 236, 0.04) !important;
        border-radius: 4px;
        padding: 12px 15px;
        border-left: 4px solid #8B004B !important;
        border-top: 1px solid rgba(245, 243, 236, 0.1) !important;
        border-right: 1px solid rgba(245, 243, 236, 0.1) !important;
        border-bottom: 1px solid rgba(245, 243, 236, 0.1) !important;
        margin-bottom: 12px;
        box-shadow: none !important;
    }
    .metric-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        color: #756569 !important;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.7rem;
        font-weight: 700;
        color: #F5F3EC !important;
    }
    
    /* Result Box styling */
    .result-box-spam {
        background-color: #FDF2F4 !important;
        border: 1px solid rgba(139, 0, 75, 0.25) !important;
        border-radius: 4px !important;
        padding: 20px;
        color: #8B004B !important;
        border-left: 6px solid #8B004B !important;
        margin-top: 15px;
        box-shadow: none !important;
    }
    .result-box-ham {
        background-color: #F2F7F2 !important;
        border: 1px solid rgba(63, 110, 76, 0.25) !important;
        border-radius: 4px !important;
        padding: 20px;
        color: #3F6E4C !important;
        border-left: 6px solid #3F6E4C !important;
        margin-top: 15px;
        box-shadow: none !important;
    }
    
    /* Card style for elements */
    .ui-card {
        background-color: #FAF9F6;
        border-radius: 6px;
        padding: 25px;
        border: 1px solid rgba(139, 0, 75, 0.15);
        box-shadow: none !important;
        position: relative;
    }
    .ui-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background-color: #8B004B;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    
    /* Streamlit Button Styling (Secondary outline by default, primary filled) */
    div.stButton > button {
        background-color: transparent !important;
        color: #8B004B !important;
        border-radius: 4px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1.2rem !important;
        border: 1px solid rgba(139, 0, 75, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: none !important;
    }
    div.stButton > button:hover {
        background-color: rgba(139, 0, 75, 0.06) !important;
        border-color: #8B004B !important;
        color: #8B004B !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Primary buttons (Analyze Message, Train Model) */
    div.stButton > button[kind="primary"] {
        background-color: #8B004B !important;
        color: #FAF9F6 !important;
        border: 1px solid #8B004B !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 2.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #2D0018 !important;
        color: #FAF9F6 !important;
        border-color: #2D0018 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Form Input elements override */
    div[data-baseweb="textarea"] textarea, div[data-baseweb="input"] input {
        background-color: #FAF9F6 !important;
        color: #241C1E !important;
        border: 1px solid rgba(139, 0, 75, 0.2) !important;
        border-radius: 4px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    div[data-baseweb="textarea"] textarea:focus, div[data-baseweb="input"] input:focus {
        border-color: #8B004B !important;
        box-shadow: 0 0 0 1px #8B004B !important;
    }
    
    /* Custom progress bar indicator */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #8B004B !important;
    }
    
    /* Monospace Code & Tokens styling */
    code {
        font-family: 'Share Tech Mono', monospace !important;
        background-color: #2D0018 !important;
        color: #FAF9F6 !important;
        border-radius: 4px;
        padding: 3px 6px;
    }
</style>
    """, unsafe_allow_html=True)

# Helper function to load model payload
@st.cache_resource
def load_model_payload():
    model_path = os.path.join(current_dir, "models", "model.pkl")
    if not os.path.exists(model_path):
        return None
    try:
        with open(model_path, 'rb') as f:
            payload = pickle.load(f)
        return payload
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load the model
payload = load_model_payload()

# Sidebar UI
st.sidebar.markdown("### 🛠️ Model Information")
if payload is not None:
    st.sidebar.success(f"Loaded: **{payload['model_name']}**")
    
    # Display model metrics
    st.sidebar.markdown("#### Test Set Performance")
    metrics = payload['metrics']
    
    primary_color = "#D13D85" if theme_mode == "Dark Mode" else "#8B004B"
    acc2 = "#E5569D" if theme_mode == "Dark Mode" else "#A22368"
    acc3 = "#F07CAF" if theme_mode == "Dark Mode" else "#B83E82"
    acc4 = "#FAA3C3" if theme_mode == "Dark Mode" else "#CE589C"

    st.sidebar.markdown(f"""
    <div class="metric-card" style="border-left-color: {primary_color};">
        <div class="metric-title">F1-Score (Primary)</div>
        <div class="metric-value">{metrics['F1-Score']:.4f}</div>
    </div>
    <div class="metric-card" style="border-left-color: {acc2};">
        <div class="metric-title">Accuracy</div>
        <div class="metric-value">{metrics['Accuracy']:.4f}</div>
    </div>
    <div class="metric-card" style="border-left-color: {acc3};">
        <div class="metric-title">Precision</div>
        <div class="metric-value">{metrics['Precision']:.4f}</div>
    </div>
    <div class="metric-card" style="border-left-color: {acc4};">
        <div class="metric-title">Recall</div>
        <div class="metric-value">{metrics['Recall']:.4f}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.warning("⚠️ No model loaded. Please train the model.")
    
    if st.sidebar.button("Train Model Now", type="primary"):
        with st.spinner("Training models in background..."):
            try:
                from train import load_and_preprocess_data, train_and_evaluate, save_pipeline
                csv_path = os.path.join(current_dir, "data", "spam.csv")
                df = load_and_preprocess_data(csv_path)
                vectorizer, best_model, best_model_name, best_metrics, _, _, _, _, _ = train_and_evaluate(df)
                save_path = os.path.join(current_dir, "models", "model.pkl")
                save_pipeline(vectorizer, best_model, best_model_name, best_metrics, save_path)
                st.sidebar.success("Training complete!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Training failed: {e}")

# Sidebar Explanations
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Text Preprocessing Details")
st.sidebar.info(
    "Every input message is preprocessed using NLTK before classification:\n"
    "1. **Lowercase conversion**\n"
    "2. **Punctuation & digit removal**\n"
    "3. **Stopword removal** (using English stopwords)\n"
    "4. **Stemming** (using Porter Stemmer)"
)

# Sidebar Footer
st.sidebar.markdown('<div class="sidebar-footer">created with love</div>', unsafe_allow_html=True)

# Main Dashboard Layout
st.markdown('<div class="main-title">📧 SMS Spam Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">An end-to-end Machine Learning classifier using natural language preprocessing.</div>', unsafe_allow_html=True)

# Grid Layout for Input and Output
col1, col2 = st.columns([3, 2], gap="large")

# Preset messages helper
presets = {
    "Ham Example 1": "Hey! Are we still meeting for lunch today? Let me know.",
    "Ham Example 2": "I'm on my way home now. Will call you when I reach.",
    "Spam Example 1": "WINNER! You have won a £1,000 cash prize or a free cruise! Text CLAIM to 89555 now to collect. TS&Cs apply.",
    "Spam Example 2": "URGENT! Your mobile number has been selected for a free £500 gift card. Call 09066362231 to claim."
}

with col1:
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.subheader("✉️ Enter SMS Message")
    
    # Preset Quick Select Buttons
    st.write("💡 Quick Test Presets:")
    preset_cols = st.columns(4)
    selected_preset = ""
    for idx, (label, val) in enumerate(presets.items()):
        if preset_cols[idx].button(label):
            selected_preset = val
            
    # Text input area
    input_text = st.text_area(
        "Type or paste your message here:",
        value=selected_preset if selected_preset else "",
        height=150,
        placeholder="e.g., Congratulations! You've been selected for a free gift..."
    )
    
    analyze_btn = st.button("Analyze Message", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ui-card" style="height: 100%;">', unsafe_allow_html=True)
    st.subheader("🔍 Prediction Results")
    
    if analyze_btn and input_text.strip():
        if payload is None:
            st.error("No model is loaded. Please train the model from the sidebar first.")
        else:
            # 1. Preprocess the input message
            cleaned_msg = clean_text(input_text)
            
            # 2. Vectorize the preprocessed text
            vectorizer = payload['vectorizer']
            model = payload['model']
            
            msg_vec = vectorizer.transform([cleaned_msg])
            
            # 3. Predict and compute probability
            pred = model.predict(msg_vec)[0]
            prob = model.predict_proba(msg_vec)[0] # shape: [prob_ham, prob_spam]
            
            # Probability score formatting
            spam_probability = prob[1] * 100
            ham_probability = prob[0] * 100
            
            # Display results
            if pred == 1:
                st.markdown(f"""
                <div class="result-box-spam">
                    <h3 style="margin-top:0;">🚨 SPAM DETECTED</h3>
                    <p>This message has been flagged as potential spam with high confidence.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                st.metric(label="Spam Probability", value=f"{spam_probability:.2f}%")
                st.progress(prob[1])
            else:
                st.markdown(f"""
                <div class="result-box-ham">
                    <h3 style="margin-top:0;">✅ LEGITIMATE (HAM)</h3>
                    <p>This message appears to be safe and clean.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                st.metric(label="Ham Probability", value=f"{ham_probability:.2f}%")
                st.progress(prob[0])
            
            # Show preprocessed tokens
            st.markdown("---")
            st.write("🧠 **How the Machine Learning model sees it:**")
            if cleaned_msg:
                st.code(f"Tokens: {cleaned_msg.split()}", language="python")
            else:
                st.write("*All words were removed as stopwords or the text was empty!*")
            
            st.write(f"⚙️ **Active Model:** `{payload['model_name']}`")
            
    elif analyze_btn:
        st.warning("⚠️ Please enter a non-empty message to analyze.")
    else:
        st.write("Enter an SMS message on the left and click **Analyze Message** to see predictions.")
    st.markdown('</div>', unsafe_allow_html=True)
