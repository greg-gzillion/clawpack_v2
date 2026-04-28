def run(args):
    """Animate a mathematical function and open interactive plot in browser.
    Usage: /animate sin(x + t) from t=0 to 4*pi
           /animate 3d x**2 + y**2 + sin(t) from t=0 to 2*pi
    """
    if not args:
        return "Usage: /animate sin(x + t) from t=0 to 4*pi\n       /animate 3d x**2 + y**2 from t=0 to 2*pi"

    try:
        import numpy as np
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots
        import sympy as sp
        import webbrowser
        from pathlib import Path
        import re

        # Parse: "sin(x + t) from t=0 to 4*pi" or "3d surface from t=0 to 2*pi"
        is_3d = args.lower().startswith('3d')
        if is_3d:
            args = args[2:].strip()

        # Split expression from range
        if ' from ' in args.lower():
            expr_part, range_part = args.lower().split(' from ', 1)
        else:
            return "Usage: /animate sin(x + t) from t=0 to 4*pi"

        # Parse range: "t=0 to 4*pi"
        range_match = re.match(r'(\w+)\s*=\s*(.+?)\s+to\s+(.+)', range_part)
        if not range_match:
            return "Range format: t=0 to 4*pi"
        
        var = range_match.group(1)
        t0 = float(sp.sympify(range_match.group(2)))
        t1 = float(sp.sympify(range_match.group(3)))

        if is_3d:
            # 3D surface animation
            x = sp.Symbol('x')
            y = sp.Symbol('y')
            t = sp.Symbol(var)
            expr = sp.sympify(expr_part)
            f = sp.lambdify((x, y, t), expr, modules=['numpy'])

            X, Y = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
            frames = []
            times = np.linspace(t0, t1, 30)
            
            for ti in times:
                Z = f(X, Y, ti)
                frames.append(go.Surface(
                    x=X, y=Y, z=Z,
                    colorscale='viridis',
                    showscale=False
                ))

            fig = go.Figure(
                data=[frames[0]],
                layout=go.Layout(
                    title=f'f(x,y,{var}) = {expr_part}',
                    scene=dict(
                        xaxis_title='x',
                        yaxis_title='y',
                        zaxis_title='f(x,y)'
                    ),
                    updatemenus=[dict(
                        type='buttons',
                        buttons=[
                            dict(label='Play', method='animate', args=[None]),
                            dict(label='Pause', method='animate', args=[[None], dict(frame=dict(duration=0))])
                        ]
                    )]
                ),
                frames=[go.Frame(data=[f], name=str(i)) for i, f in enumerate(frames)]
            )

        else:
            # 2D animation
            x = sp.Symbol('x')
            t = sp.Symbol(var)
            expr = sp.sympify(expr_part)
            f = sp.lambdify((x, t), expr, modules=['numpy'])

            X = np.linspace(-10, 10, 500)
            frames = []
            times = np.linspace(t0, t1, 60)

            fig = go.Figure()
            
            for i, ti in enumerate(times):
                Y = f(X, ti)
                fig.add_trace(go.Scatter(
                    x=X, y=Y,
                    mode='lines',
                    line=dict(width=2),
                    name=f'{var}={ti:.2f}',
                    visible=(i == 0)
                ))

            # Create slider steps
            steps = []
            for i in range(len(times)):
                step = dict(
                    method='update',
                    args=[{'visible': [j == i for j in range(len(times))]},
                          {'title': f'f(x,{var}) = {expr_part}  |  {var} = {times[i]:.3f}'}]
                )
                steps.append(step)

            sliders = [dict(
                active=0,
                currentvalue={'prefix': f'{var} = '},
                steps=steps
            )]

            fig.update_layout(
                title=f'f(x,{var}) = {expr_part}',
                xaxis_title='x',
                yaxis_title='f(x)',
                sliders=sliders,
                hovermode='x unified'
            )

        # Save and open
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        filename = export_dir / f"animate_{expr_part.replace('*','x').replace(' ','_')[:40]}.html"
        fig.write_html(str(filename))
        webbrowser.open(str(filename.absolute()))

        return f"Animation saved and opened: {filename}"

    except Exception as e:
        return f"Animation error: {e}"