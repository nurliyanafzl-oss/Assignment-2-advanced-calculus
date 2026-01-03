import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp

# 1. Page Config
st.set_page_config(page_title="Calculus MAT201 - Gradient Visualizer", layout="wide")

# 2. Application Title
st.title("Gradient and Direction of Steepest Ascent Visualizer")
st.write("This app visualizes how the gradient vector points in the direction of the steepest ascent on a 3D surface.")

# 3. Sidebar Input 
st.sidebar.header("Input Settings")
equation_input = st.sidebar.text_input("Enter function f(x, y):", "x**2 + y**2")
x_coord = st.sidebar.slider("Point x:", -5.0, 5.0, 1.0)
y_coord = st.sidebar.slider("Point y:", -5.0, 5.0, 1.0)

try:
    # 4. Mathematical Calculations
    x, y = sp.symbols('x y')
    f_sym = sp.sympify(equation_input)
    fx = sp.diff(f_sym, x)
    fy = sp.diff(f_sym, y)

    grad_x_val = float(fx.subs({x: x_coord, y: y_coord}))
    grad_y_val = float(fy.subs({x: x_coord, y: y_coord}))
    z_coord = float(f_sym.subs({x: x_coord, y: y_coord}))

    # 5. Results Display
    st.write(f"### Function: $f(x, y) = {sp.latex(f_sym)}$")
    st.latex(rf"\nabla f({x_coord}, {y_coord}) = \langle {grad_x_val:.2f}, {grad_y_val:.2f} \rangle")

    # 6. Plotly 3D Visualization
    x_range = np.linspace(-5, 5, 50)
    y_range = np.linspace(-5, 5, 50)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    f_numpy = sp.lambdify((x, y), f_sym, 'numpy')
    Z_grid = f_numpy(X_grid, Y_grid)

    fig = go.Figure()

    # Surface Plot
    fig.add_trace(go.Surface(z=Z_grid, x=X_grid, y=Y_grid, colorscale='Viridis', opacity=0.7))

    # Scale factor for the arrow length
    scale = 0.5 

    # Adding the Gradient Arrow direction (The Line)
    fig.add_trace(go.Scatter3d(
        x=[x_coord, x_coord + grad_x_val * scale], 
        y=[y_coord, y_coord + grad_y_val * scale],
        z=[z_coord, z_coord],
        mode='lines',
        line=dict(color='yellow', width=10), 
        name="Gradient Direction"
    ))

    # Adding the Gradient Arrow Head (The Cone)
    fig.add_trace(go.Cone(
        x=[x_coord + grad_x_val * scale],
        y=[y_coord + grad_y_val * scale],
        z=[z_coord],
        u=[grad_x_val],
        v=[grad_y_val],
        w=[0],
        sizemode="absolute",
        sizeref=1,
        colorscale=[[0, 'yellow'], [1, 'yellow']],
        showscale=False,
        name="Gradient Head"
    ))

    fig.update_layout(scene=dict(aspectmode='cube'), height=700)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}. Please check your function syntax.")

st.divider()
st.caption("Calculus MAT201 | Created with Streamlit and Plotly")
