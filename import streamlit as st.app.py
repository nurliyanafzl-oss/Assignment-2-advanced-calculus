import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp

st.set_page_config(page_title="MAT201 Calculus App")
st.title("Aplikasi Visualisasi Gradien (MAT201)")

# Input Fungsi
st.sidebar.header("Tetapan Input")
equation = st.sidebar.text_input("Masukkan fungsi f(x, y):", "x**2 + y**2")
x_point = st.sidebar.slider("Titik x:", -5.0, 5.0, 1.0)
y_point = st.sidebar.slider("Titik y:", -5.0, 5.0, 1.0)

# Pengiraan Matematik
x, y = sp.symbols('x y')
f = sp.sympify(equation)
fx = sp.diff(f, x)
fy = sp.diff(f, y)

grad_x = float(fx.subs({x: x_point, y: y_point}))
grad_y = float(fy.subs({x: x_point, y: y_point}))

st.write(f"### Fungsi: $f(x, y) = {sp.latex(f)}$")
st.write(f"Vektor Gradien pada titik ({x_point}, {y_point}) adalah:")
st.latex(rf"\nabla f = \langle {grad_x:.2f}, {grad_y:.2f} \rangle")

# Visualisasi Plotly
x_range = np.linspace(-5, 5, 50)
y_range = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x_range, y_range)
f_func = sp.lambdify((x, y), f, 'numpy')
Z = f_func(X, Y)

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8)])
z_point = float(f.subs({x: x_point, y: y_point}))

# Tambah anak panah gradien
fig.add_trace(go.Scatter3d(
    x=[x_point, x_point + grad_x*0.2],
    y=[y_point, y_point + grad_y*0.2],
    z=[z_point, z_point],
    mode='lines+markers',
    line=dict(color='red', width=10),
    name="Arah Gradien"
))

st.plotly_chart(fig)