import streamlit as st
import pandas as pd
import sqlite3

#----------------login---------------------------
USUARIO = "Claribel"
CONTRASEÑA = "Clari1234"

if "login" not in st.session_state:
    st.session_state.login = False

def login():
    st.title("🔐 Iniciar sesión")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == USUARIO and password == CONTRASEÑA:
            st.session_state.login = True  
            st.success("Acceso concedido")
            st.rerun()
        else:
            st.error("Usuario y/o contraseña incorrectos")    
    
if not st.session_state.login:
    login()
    st.stop()



#------------ config y base de datos de la web---------------------
st.set_page_config(page_title="Mi registro de productos", page_icon="🛒")

conn = sqlite3.connect("Reg de ventas clari.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
              CREATE TABLE IF NOT EXISTS registros (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT NOT NULL,
              precio FLOAT NOT NULL,
              cantidad INTEGER NOT NULL, 
              total REAL NOT NULL 
               )
               """)
conn.commit()
 

st.title("🛒 Registro de productos")

#-------------------------- OCULTAR BOTONES DE LA MISMA WEB-----------------------------------
st.markdown("""
<style>

/* Ocultar footer normal */
footer {visibility: hidden;}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* Ocultar elementos flotantes móviles comunes */
[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

/* Botones flotantes abajo */
button[kind="header"] {
    display:none;
}

/* Solo móvil */
@media (max-width: 768px) {
    footer, header {
        display:none !important;
    }
}

</style>
""", unsafe_allow_html=True)
#-----------AQUI ACABA EL QUITAR BOTONES DE LA WEB--------------




# Meoria temporal por el momento--------------------------------------------


# Formulario
with st.form("formulario"):
    nombre = st.text_input("Nombre del producto")
    precio = st.number_input("precio unitario", min_value=0.0, format="%.2f")
    cantidad = st.number_input("cantidad", min_value=1, step=1)

    guardar = st.form_submit_button("Registrar producto")

    if guardar:
        total = precio * cantidad

        cursor.execute("""
        INSERT INTO registros (nombre, precio, cantidad, total)
        VALUES (?, ?, ?, ?)
        """, (nombre, precio, cantidad, total)) 

        conn.commit()

        st.success("Producto guardado correctamente")


#-------------Editar productos--------
st.subheader("✏️ Editar producto")

#esto leera los productos
df = pd.read_sql_query("SELECT * FROM registros", conn)

if not df.empty:
    seleccion = st.selectbox(
        "Seleccionar productos POR SU ID",
        df["id"].astype(str) + " - " + df["nombre"]
    )

    producto_id = int(seleccion.split(" - ")[0])

    fila_filtrada = df[df["id"] == producto_id]
    if not fila_filtrada.empty:
        fila = fila_filtrada.iloc[0]

    else:
        st.warning("Producto no encontrado")
        st.rerun()    

    nuevo_nombre = st.text_input("Nombre", value=fila["nombre"])
    
    nuevo_precio = st.number_input("Precio", min_value=0.0, value=float(fila["precio"]), format="%.2f")

    nueva_cantidad = st.number_input("Cantidad", min_value=1, value=int(fila["cantidad"]), step=1)

    if st.button("💾 Guardar cambios"):

        nuevo_total = nuevo_precio * nueva_cantidad

        cursor.execute("""
        UPDATE registros
        SET nombre = ?,
            precio = ?,           
            cantidad = ?,
            total = ?
        WHERE id = ?
        """,(
            nuevo_nombre,
            nuevo_precio,
            nueva_cantidad,
            nuevo_total,
            producto_id
        ))

        conn.commit()

        st.success("Producto actualizado")

        st.rerun()  
    if st.button("🗑️ Eliminar producto"):    
        cursor.execute("""
        DELETE FROM registros
        WHERE id = ?
        """, (producto_id,))
        conn.commit()

        st.success("Producto eliminado")

        st.rerun()                                
                       
#Mostrar la tabla--------
df = pd.read_sql_query("SELECT * FROM registros", conn)

if not df.empty:
    st.subheader("📦 Productos registrados")
    st.dataframe(df, use_container_width=True)

suma_total = df["total"].sum()

st.metric("💰 Total General", f"${suma_total:.2f}")

if st.button("🗑️ Limpiar todo"):
   cursor.execute("DELETE FROM registros")
   conn.commit()
   st.rerun()            
