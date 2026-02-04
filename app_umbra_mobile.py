import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
import os

# Configuración API (Usamos la tuya gratis)
API_KEY = "AIzaSyDmh1QVojtNOw3pv6XGEr5xtLLR9iNRTmo"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Config Página
st.set_page_config(page_title="UMBRA MOBILE", page_icon="🦖", layout="centered") # Centered es mejor para móvil

# Cargar DB Clientes
@st.cache_data
def load_data():
    return pd.read_csv('clientes_umbra_full.csv')

df = load_data()

# --- HEADER MÓVIL ---
st.image("assets/umbra_logo_v2.png", width=100)
st.title("UMBRA OS 📱")
st.write("**Sistema de Control de Clientes**")

# --- SELECTOR ---
cliente_nom = st.selectbox("Seleccionar Atleta:", df['NOMBRE Y APELLIDO'].unique())
cliente = df[df['NOMBRE Y APELLIDO'] == cliente_nom].iloc[0]

# --- TARJETA CLIENTE ---
with st.expander("👤 Ver Perfil del Cliente", expanded=True):
    c1, c2 = st.columns(2)
    c1.metric("Peso", f"{cliente['PESO']} kg")
    c2.metric("Altura", f"{cliente['ALTURA ']} m")
    st.info(f"🎯 **Objetivo:** {cliente[' ¿CUAL ES TU PROPÓSITO CON MI ASESORÍA?']}")
    
    if str(cliente['ALÉRGICO A ALGÚN ALIMENTO']).lower() != 'no':
        st.error(f"⚠️ Alergia: {cliente['ALÉRGICO A ALGÚN ALIMENTO']}")

# --- BRAIN IA ---
st.divider()
st.subheader("🧠 MASTER COACH IA")

if st.button("✨ GENERAR PLAN INTELIGENTE", type="primary", use_container_width=True):
    with st.spinner("Analizando biomecánica y metabolismo..."):
        # Prompt para el Sub-Agente
        prompt = f"""
        Act as UMBRA MASTER COACH.
        Client: {cliente_nom}
        Stats: {cliente['PESO']}kg, {cliente['ALTURA ']}m, {cliente['EDAD Y FECHA DE NACIMIENTO']}
        Goal: {cliente[' ¿CUAL ES TU PROPÓSITO CON MI ASESORÍA?']}
        Injuries/Health: {cliente['SI TIENES ALGUNA PATOLOGIA (FAVOR DE AGREGARLA)']}
        Food preferences: {cliente['ALIMENTOS DE TU AGRADO:']}
        
        Generate a summary plan:
        1.  **Calories & Macros** (Specific numbers).
        2.  **Training Split** (Push/Pull/Legs or Upper/Lower) with reasoning.
        3.  **Key Focus** (e.g., "Glute prioritization").
        4.  **1 Diet Hack** based on their likes.
        
        Keep it short, direct, and motivating. Spanish.
        """
        
        response = model.generate_content(prompt)
        
        st.success("¡Plan Generado!")
        st.markdown(response.text)
        
        # Botón Simulado de Envío
        st.info("👇 Copia esto y envíalo por WhatsApp")
        st.code(response.text, language='markdown')

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Yoshi 🦖")
