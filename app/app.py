import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Smart Waste AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS NUANSA IJO TUA ELEGAN ---
st.markdown("""
    <style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Background ijo tua solid */
    .stApp {
        background: #0a2f1f;
        background-image: radial-gradient(circle at 10% 20%, rgba(30, 80, 50, 0.3) 0%, rgba(10, 47, 31, 1) 90%);
    }
    
    /* Container utama */
    .main-container {
        background: #0d3623;
        border-radius: 30px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    }
    
    /* Header */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #d4ff8c;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 0px #0a2f1f;
        letter-spacing: 1px;
    }
    
    .subtitle {
        text-align: center;
        color: #b8e4a0;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 400;
        background: rgba(0,0,0,0.2);
        display: inline-block;
        width: auto;
        margin-left: auto;
        margin-right: auto;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
    }
    
    /* Card Premium Ijo Tua */
    .premium-card {
        background: #0f3d28;
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        border: 1px solid #2a6b46;
        margin-bottom: 1.5rem;
    }
    
    .premium-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border-color: #4c9a6e;
    }
    
    /* Judul card */
    .premium-card h3, .premium-card h2 {
        color: #d4ff8c !important;
        font-weight: 700;
    }
    
    /* Upload Area */
    .stFileUploader > div {
        border: 2px solid #2a6b46;
        border-radius: 20px;
        background: #0a2f1f;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #6fbf4c;
        background: #0d3623;
        transform: scale(1.02);
    }
    
    /* Label uploader */
    .stFileUploader label {
        color: #d4ff8c !important;
        font-weight: 600;
    }
    
    /* Text & font umum */
    p, li, span, div {
        color: #c8e6b5;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #2a6b46 0%, #1b4d32 100%);
        color: #d4ff8c;
        border: 1px solid #4c9a6e;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #3a7b56 0%, #2a5b3e 100%);
        border-color: #6fbf4c;
        color: #e8ffc4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6fbf4c, #d4ff8c);
        border-radius: 10px;
    }
    
    .stProgress > div {
        background-color: #1b4d32;
    }
    
    /* Info, success, error messages */
    .stAlert {
        background-color: #1b4d32;
        border-left: 4px solid #6fbf4c;
        color: #d4ff8c;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #0f3d28;
        color: #d4ff8c;
        font-weight: 600;
        border-radius: 12px;
        border: 1px solid #2a6b46;
    }
    
    .streamlit-expanderContent {
        background-color: #0d3623;
        border-radius: 12px;
        color: #c8e6b5;
    }
    
    /* Divider premium */
    .premium-divider {
        background: linear-gradient(90deg, transparent, #4c9a6e, #d4ff8c, #4c9a6e, transparent);
        height: 2px;
        border-radius: 2px;
        margin: 2rem 0;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a2f1f;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a6b46;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4c9a6e;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    /* Stats boxes */
    .stat-box {
        text-align: center;
        background: #0a2f1f;
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #2a6b46;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #8bc34a;
        font-size: 0.8rem;
        padding: 1rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .premium-card {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI BYPASS LAYER (TIDAK DIUBAH - KRUSIAL) ---
def fix_layer(cls):
    return lambda **kwargs: cls(**{k: v for k, v in kwargs.items() if k not in ['batch_shape', 'optional', 'dtype']})

from tensorflow.keras.layers import InputLayer, Conv2D, Dense, Flatten, MaxPooling2D, BatchNormalization, ReLU

custom_objects = {
    'InputLayer': lambda **kwargs: InputLayer(input_shape=(224, 224, 3), **{k: v for k, v in kwargs.items() if k not in ['batch_shape', 'optional', 'dtype', 'input_shape']}),
    'Conv2D': fix_layer(Conv2D),
    'Dense': fix_layer(Dense),
    'Flatten': fix_layer(Flatten),
    'MaxPooling2D': fix_layer(MaxPooling2D),
    'BatchNormalization': fix_layer(BatchNormalization),
    'ReLU': fix_layer(ReLU)
}

@st.cache_resource
def load_model():
    return tf.keras.models.load_model('model_waste_final.h5', custom_objects=custom_objects, compile=False)

# --- KONTEN UTAMA ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-title'>♻️ SMART WASTE AI</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'><p class='subtitle'>AI PINTAR PEMILAH SAMPAH ORGANIK & ANORGANIK</p></div>", unsafe_allow_html=True)

# Stats Preview
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="stat-box">
            <p style="font-size: 2rem; margin: 0;">🎯</p>
            <p style="font-weight: 700; color: #d4ff8c; margin: 0;">Akurasi Tinggi</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="stat-box">
            <p style="font-size: 2rem; margin: 0;">⚡</p>
            <p style="font-weight: 700; color: #d4ff8c; margin: 0;">Deteksi Cepat</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="stat-box">
            <p style="font-size: 2rem; margin: 0;">🌱</p>
            <p style="font-weight: 700; color: #d4ff8c; margin: 0;">Ramah Lingkungan</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

# Layout Kolom
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom: 1rem;'>📸 UPLOAD FOTO</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem;'>💡 Pastikan foto jelas dan pencahayaan cukup</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Klik atau seret file foto", 
        type=["jpg", "jpeg", "png"],
        help="Format: JPG, JPEG, PNG"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption="📷 PREVIEW FOTO", use_container_width=True)
        
        if st.button("🔄 GANTI FOTO", use_container_width=True):
            st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <p style="font-size: 3rem; margin: 0;">📤</p>
                <p style="color: #b8e4a0;">Belum ada foto</p>
                <p style="font-size: 0.75rem; color: #8bc34a;">Upload foto sampah untuk analisis</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Edukasi
    with st.expander("🌿 PANDUAN PEMILAHAN", expanded=False):
        st.markdown("""
        **🗑️ SAMPAH ORGANIK** (Warna Hijau)
        - Sisa makanan, sayur, buah
        - Daun kering, ranting
        - Dapat diurai menjadi kompos
        
        **♻️ SAMPAH ANORGANIK** (Warna Biru/Kuning)
        - Plastik, botol, kemasan
        - Kaleng, kaca, logam
        - Perlu didaur ulang
        """)

with right_col:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom: 1rem;'>🤖 HASIL ANALISIS</h3>", unsafe_allow_html=True)
    
    if uploaded_file:
        try:
            model = load_model()
            
            with st.spinner('🧠 AI sedang menganalisis...'):
                time.sleep(0.3)
                
                img_resized = image.resize((224, 224))
                img_array = np.array(img_resized) / 255.0
                img_array = np.expand_dims(img_array, axis=0).astype('float32')
                
                prediction = model.predict(img_array)
                score = float(prediction[0][0])
                
                if score > 0.5:
                    label, color, icon, bg_color, saran = "ANORGANIK", "#ff9966", "🥤", "#2a2a2a", "Masukkan ke tempat sampah **Anorganik** (Plastik, Kaleng, Kaca)"
                    confidence = score * 100
                else:
                    label, color, icon, bg_color, saran = "ORGANIK", "#a8e6a0", "🍎", "#2a2a2a", "Masukkan ke tempat sampah **Organik** (Sisa makanan, daun)"
                    confidence = (1 - score) * 100
                
                # Progress bar animasi
                bar = st.progress(0)
                for i in range(100):
                    bar.progress(i + 1)
                    time.sleep(0.008)
                
                # Hasil
                st.markdown(f"""
                    <div style="background: {bg_color}; border-radius: 20px; padding: 1.5rem; text-align: center; border: 2px solid {color}; margin-top: 1rem;">
                        <div style="font-size: 3.5rem;">{icon}</div>
                        <div style="background: {color}; display: inline-block; padding: 0.4rem 1.2rem; border-radius: 40px; margin: 0.5rem 0;">
                            <span style="color: #0a2f1f; font-weight: 800; font-size: 1.2rem;">{label}</span>
                        </div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: {color}; margin: 0.5rem 0;">
                            {confidence:.1f}%
                        </div>
                        <p style="color: #d4ff8c; font-weight: 600;">Tingkat Keyakinan AI</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.success(f"💡 SARAN: {saran}")
                st.caption("✨ AI ini membantu menjaga kebersihan lingkungan")
                
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            st.info("Pastikan file 'model_waste_final.h5' tersedia")
    else:
        st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem;">🖼️</div>
                <h4 style="color: #d4ff8c;">Belum Ada Foto</h4>
                <p style="color: #b8e4a0;">Upload foto sampah untuk melihat hasil</p>
                <div style="margin-top: 1rem;">
                    <span class="badge" style="background: #2a6b46; color: #d4ff8c;">🍎 Organik</span>
                    <span class="badge" style="background: #2a6b46; color: #d4ff8c;">🥤 Anorganik</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-text">
        🌿 <strong>SMART WASTE MANAGEMENT SYSTEM</strong> 🌿<br>
        Powered Fauzi - Ghevira - Fadhillah | © 2026
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
