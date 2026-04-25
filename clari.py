import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mi registro de productos", page_icon="🛒")

st.title("🛒 Registro de productos")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Meoria temporal por el momento--------------------------------------------
if "productos" not in st.session_state:
    st.session_state.productos = []

# Formulario
with st.form("formulario"):
    nombre = st.text_input("Nombre del producto")
    precio = st.number_input("precio unitario", min_value=0.0, format="%.2f")
    cantidad = st.number_input("cantidad", min_value=1, step=1)

    guardar = st.form_submit_button("Registrar producto")

    if guardar:
        total = precio * cantidad

        st.session_state.productos.append({
            "Producto": nombre,
            "Precio": precio,
            "Cantidad": cantidad,
            "Total": total
        })  

        st.success("producto agregado")

#Mostrar la tabla--------
if st.session_state.productos:
    st.subheader("📦Productos registrados")

    df = pd.DataFrame(st.session_state.productos)
    st.dataframe(df, use_container_width=True)

    suma_total = df["Total"].sum()

    st.metric("💰 Total General", f"${suma_total:.2f}")

if st.button("🗑️ Limpiar todo"):
   st.session_state.productos = []
   st.rerun()            
