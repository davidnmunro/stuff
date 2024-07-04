import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.io as pio

# Generate sample data
np.random.seed(42)
num_lines = 100
num_groups = 10
points_per_line = 50

# Create a DataFrame with sample data
data = {
    'x': np.random.rand(num_lines * points_per_line),
    'y': np.random.rand(num_lines * points_per_line),
    'z': np.random.rand(num_lines * points_per_line),
    'group': np.repeat(np.arange(num_groups), num_lines // num_groups * points_per_line)
}

df = pd.DataFrame(data)

# Define colors for each group
colors = px.colors.qualitative.Plotly

# Create traces for each group
traces = []
groups = df['group'].unique()

for group in groups:
    group_df = df[df['group'] == group]
    color = colors[group % len(colors)]
    for i in range(num_lines // num_groups):
        segment_df = group_df.iloc[i * points_per_line:(i + 1) * points_per_line]
        trace = go.Scatter3d(
            x=segment_df['x'], 
            y=segment_df['y'], 
            z=segment_df['z'], 
            mode='lines', 
            line=dict(color=color),
            name=f'Group {group} Line {i+1}'
        )
        traces.append(trace)

# Create the figure with all traces
fig = go.Figure(data=traces)

# Create buttons for each group
buttons = []

for group in groups:
    visibility = [False] * len(traces)
    for i in range(num_lines // num_groups):
        visibility[group * (num_lines // num_groups) + i] = True
    button = dict(
        label=f'Group {group}',
        method='update',
        args=[{'visible': visibility},
              {'title': f'Showing Group {group}'}]
    )
    buttons.append(button)

# Add a button to show all groups
buttons.append(dict(
    label='All',
    method='update',
    args=[{'visible': [True] * len(traces)},
          {'title': 'Showing All Groups'}]
))

# Update layout with buttons
fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        direction="down",
        buttons=buttons,
        showactive=True,
    )],
    title="Showing All Groups"
)

# Save the figure as an HTML file
pio.write_html(fig, file='3d_line_plot.html', auto_open=True)

