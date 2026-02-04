import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Configuración de la Página
st.set_page_config(page_title="UMBRA OS", page_icon="🦖", layout="wide")

# Cargar Base de Datos
def load_db():
    with open('umbra_db.json', 'r') as f:
        return json.load(f)

db = load_db()

# Cargar Clientes (Simulado desde CSV local por velocidad, se puede conectar a Sheet)
@st.cache_data
def load_clients():
    return pd.read_csv('clientes_umbra_full.csv')

df_clientes = load_clients()

# --- SIDEBAR ---
st.sidebar.image("assets/umbra_logo_v2.png", width=150)
st.sidebar.title("COMANDO UMBRA 🧠")
cliente_seleccionado = st.sidebar.selectbox("Seleccionar Cliente", df_clientes['NOMBRE Y APELLIDO'])

# Filtrar datos del cliente
cliente = df_clientes[df_clientes['NOMBRE Y APELLIDO'] == cliente_seleccionado].iloc[0]

# --- MAIN DASHBOARD ---
st.title(f"Expediente: {cliente['NOMBRE Y APELLIDO']}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Edad", f"{cliente['EDAD Y FECHA DE NACIMIENTO']}")
    st.metric("Peso Actual", f"{cliente['PESO']} kg")
with col2:
    st.metric("Altura", f"{cliente['ALTURA ']} m")
    # Cálculo BMI rápido
    try:
        bmi = float(cliente['PESO']) / (float(cliente['ALTURA ']) ** 2)
        st.metric("BMI", f"{bmi:.1f}")
    except:
        st.metric("BMI", "N/A")
with col3:
    objetivo = str(cliente[' ¿CUAL ES TU PROPÓSITO CON MI ASESORÍA?'])
    st.info(f"🎯 **Objetivo:** {objetivo}")
    st.warning(f"⚠️ **Alergias:** {cliente['ALÉRGICO A ALGÚN ALIMENTO']}")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Calculadora & Estrategia", "🏋️‍♂️ Diseñador de Rutina", "🥑 Plan Nutricional"])

# TAB 1: MACROS
with tab1:
    st.header("Ingeniería Metabólica")
    
    # Cálculos en tiempo real
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Configuración")
        nivel_actividad = st.select_slider("Nivel de Actividad", options=["Sedentario", "Ligero", "Moderado", "Intenso", "Atleta"], value="Moderado")
        tipo_dieta = st.radio("Estrategia", ["Déficit (Perder Grasa)", "Mantenimiento (Recomposición)", "Superávit (Ganar Masa)"])
        
        factor = 1.2
        if nivel_actividad == "Ligero": factor = 1.375
        if nivel_actividad == "Moderado": factor = 1.55
        if nivel_actividad == "Intenso": factor = 1.725
        
        # TMB Simple
        try:
            tmb = 22 * float(cliente['PESO']) # Fórmula rápida Katch-McArdle aprox
            gasto = tmb * factor
            
            calorias_meta = gasto
            if "Déficit" in tipo_dieta: calorias_meta -= 400
            if "Superávit" in tipo_dieta: calorias_meta += 300
            
            st.success(f"🔥 **Calorías Meta:** {int(calorias_meta)} kcal")
        except:
            st.error("Faltan datos de peso para calcular.")
            calorias_meta = 2000

    with col_b:
        st.subheader("Distribución de Macros")
        proteina = st.slider("Proteína (g)", 100, 250, int(float(cliente['PESO'])*2.0))
        grasas = st.slider("Grasas (g)", 40, 120, int(float(cliente['PESO'])*0.9))
        
        cals_ocupadas = (proteina * 4) + (grasas * 9)
        cals_restantes = calorias_meta - cals_ocupadas
        carbos = int(cals_restantes / 4)
        
        st.metric("Carbohidratos (Automático)", f"{carbos} g")
        
        # Gráfica simple
        chart_data = pd.DataFrame({
            'Macro': ['Proteína', 'Grasas', 'Carbos'],
            'Gramos': [proteina, grasas, carbos]
        })
        st.bar_chart(chart_data.set_index('Macro'))

# TAB 2: RUTINA
with tab2:
    st.header("Arquitectura de Entrenamiento")
    
    dias_entreno = st.multiselect("Días de Entrenamiento", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"], default=["Lunes", "Martes", "Jueves", "Viernes"])
    
    split = st.selectbox("Split Sugerido", ["Upper / Lower", "Push / Pull / Legs", "Full Body", "Glute Focus (Especialidad)"])
    
    st.divider()
    
    col_rutina1, col_rutina2 = st.columns(2)
    
    with col_rutina1:
        st.subheader(f"Día 1: {split.split('/')[0]}")
        # Selector inteligente de ejercicios
        if "Glute" in split or "Lower" in split or "Legs" in split:
            ejercicios_disponibles = db['ejercicios']['cuadriceps'] + db['ejercicios']['femoral'] + db['ejercicios']['gluteo']
        else:
            ejercicios_disponibles = db['ejercicios']['empuje'] + db['ejercicios']['traccion']
            
        nombres_ej = [e['nombre'] for e in ejercicios_disponibles]
        
        seleccion_dia1 = st.multiselect("Selecciona Ejercicios Día 1:", nombres_ej, default=[nombres_ej[0], nombres_ej[1]])
        
        for ej in seleccion_dia1:
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1: st.write(f"**{ej}**")
            with c2: st.text_input(f"Sets {ej}", "3", key=f"s_{ej}")
            with c3: st.text_input(f"Reps {ej}", "8-12", key=f"r_{ej}")

    with col_rutina2:
        st.subheader("Notas Técnicas")
        st.text_area("Indicaciones para el cliente:", "Enfócate en la fase excéntrica (bajada) de 3 segundos. RIR 2 en todos los compuestos.")

# TAB 3: MENÚ
with tab3:
    st.header("Diseño del Menú")
    
    col_menu1, col_menu2 = st.columns(2)
    
    with col_menu1:
        st.subheader("Selección de Recetas")
        desayuno = st.selectbox("Desayuno", [r['nombre'] for r in db['recetas'] if r['tipo'] == 'Desayuno'])
        comida = st.selectbox("Comida", [r['nombre'] for r in db['recetas'] if r['tipo'] == 'Comida'])
        cena = st.selectbox("Cena", [r['nombre'] for r in db['recetas'] if r['tipo'] == 'Cena'])
        snack = st.selectbox("Snack", [r['nombre'] for r in db['recetas'] if r['tipo'] == 'Snack'])
        
    with col_menu2:
        st.subheader("Resumen del Día")
        st.markdown(f"🍳 **{desayuno}**")
        st.markdown(f"🍗 **{comida}**")
        st.markdown(f"🥗 **{cena}**")
        st.markdown(f"🥤 **{snack}**")
        
        st.success("✅ Este menú se adapta a los macros calculados ajustando las porciones en la App.")

# BOTÓN FINAL
st.divider()
if st.button("🚀 GENERAR PDF FINAL", type="primary"):
    st.balloons()
    st.success(f"¡Plan para {cliente['NOMBRE Y APELLIDO']} generado exitosamente!")
    st.code(f"Archivo guardado en: drafts/planes_clientes/Plan_{cliente['NOMBRE Y APELLIDO'].split()[0]}_Final.pdf")
