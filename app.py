import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp

# Page Config
st.set_page_config(page_title="Calculus MAT201 - Gradient Visualizer")

# Application Title
st.title("Gradient and Direction of Steepest Ascent Visualizer")

# Sidebar Input 
st.sidebar.header("Input Settings")
equation_input = st.sidebar.text_input("Enter function f(x, y):", "x**2 + y**2")
x_coord = st.sidebar.slider("Point x:", -5.0, 5.0, 1.0)
y_coord = st.sidebar.slider("Point y:", -5.0, 5.0, 1.0)

# Mathematical Calculations
x, y = sp.symbols('x y')
f_sym = sp.sympify(equation_input)
fx = sp.diff(f_sym, x)
fy = sp.diff(f_sym, y)

grad_x_val = float(fx.subs({x: x_coord, y: y_coord}))
grad_y_val = float(fy.subs({x: x_coord, y: y_coord}))

# Results Display
st.write(f"### Function: $f(x, y) = {sp.latex(f_sym)}$")
st.write(f"The Gradient Vector at point ({x_coord}, {y_coord}) is:")
st.latex(rf"\nabla f = \langle {grad_x_val:.2f}, {grad_y_val:.2f} \rangle")

# Plotly 3D Visualization
x_range = np.linspace(-5, 5, 50)
y_range = np.linspace(-5, 5, 50)
X_grid, Y_grid = np.meshgrid(x_range, y_range)
f_numpy = sp.lambdify((x, y), f_sym, 'numpy')
Z_grid = f_numpy(X_grid, Y_grid)

fig = go.Figure(data=[go.Surface(z=Z_grid, x=X_grid, y=Y_grid, colorscale='Viridis', opacity=0.8)])
z_coord = float(f_sym.subs({x: x_coord, y: y_coord}))

# Adding the Gradient Arrow (yellow line)
fig.add_trace(go.Scatter3d(
    x=[x_coord, x_coord + grad_x_val * 0.8], 
    y=[y_coord, y_coord + grad_y_val * 0.8],
    z=[z_coord, z_coord],
    mode='lines',
    line=dict(color='yellow', width=12), 
    name="Gradient Direction"
))

# Adding the Gradient Arrow Head (The Cone)
fig.add_trace(go.Cone(
    x=[x_coord + grad_x_val * 0.5],
    y=[y_coord + grad_y_val * 0.5],
    z=[z_coord],
    u=[grad_x_val],
    v=[grad_y_val],
    w=[0],
    sizemode="absolute",
    sizeref=1,
    colorscale=[[0, 'yellow'], [1, 'yellow']],
    showscale=False,
    name="Arrow Head"
))

# Update Layout for better viewing
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='f(x,y)',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
    ),
        
    margin=dict(l=0, r=0, b=0, t=0),
    height=600
)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error in function: {e}. Please ensure you use Python math syntax (e.g., x**2 for x²).")

st.markdown("---")
st.caption("Developed for Advanced Calculus (MAT201) Assignment 2.")



st.plotly_chart(fig)


