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

# Custom CSS for Premium Design & Aesthetics (Harmonious colors, fonts, hover effects)
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Title and Header styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3182bd, #31a354);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    
    /* Metric Card styling */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3182bd;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    /* Result Box styling */
    .result-box-spam {
        background-color: #fde8e8;
        border: 1px solid #f8b4b4;
        border-radius: 10px;
        padding: 20px;
        color: #9b1c1c;
        border-left: 8px solid #e34a33;
        margin-top: 15px;
    }
    .result-box-ham {
        background-color: #def7ec;
        border: 1px solid #bcf0da;
        border-radius: 10px;
        padding: 20px;
        color: #03543f;
        border-left: 8px solid #31a354;
        margin-top: 15px;
    }
    
    /* Custom button hover effects */
    div.stButton > button {
        background-color: #3182bd !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(49, 130, 189, 0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #1f6b9c !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(49, 130, 189, 0.3) !important;
    }
    
    /* Card style for elements */
    .ui-card {
        background-color: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid #eaeaea;
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
    
    st.sidebar.markdown(f"""
    <div class="metric-card" style="border-left-color: #3182bd;">
        <div class="metric-title">F1-Score (Primary)</div>
        <div class="metric-value">{metrics['F1-Score']:.4f}</div>
    </div>
    <div class="metric-card" style="border-left-color: #31a354;">
        <div class="metric-title">Accuracy</div>
        <div class="metric-value">{metrics['Accuracy']:.4f}</div>
    </div>
    <div class="metric-card" style="border-left-color: #f39c12;">
        <div class="metric-title">Precision</div>
        <div class="metric-value">{metrics['Precision']:.4f}</div>
    </div>
    <div class="metric-card" style="border-left-color: #9b59b6;">
        <div class="metric-title">Recall</div>
        <div class="metric-value">{metrics['Recall']:.4f}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.warning("⚠️ No model loaded. Please train the model.")
    
    if st.sidebar.button("Train Model Now"):
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
    
    analyze_btn = st.button("Analyze Message")
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
