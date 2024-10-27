import plotly.express as px
import plotly.graph_objects as go

def plot_raw_tensor(raw_tensor, event_dates):
    fig = go.Figure()
    for i, event_date in enumerate(event_dates):
        fig.add_trace(go.Scatter(
            x=list(range(len(raw_tensor[i]))),
            y=raw_tensor[i],
            mode='lines',
            name=f'Event {event_date}'
        ))
    fig.update_layout(
        title='Raw Tensor Plot',
        xaxis_title='Time',
        yaxis_title='Value'
    )
    fig.show()

def plot_delta_tensor(delta_tensor, event_dates):
    fig = go.Figure()
    for i, event_date in enumerate(event_dates):
        fig.add_trace(go.Scatter(
            x=list(range(len(delta_tensor[i]))),
            y=delta_tensor[i],
            mode='lines',
            name=f'Event {event_date}'
        ))
    fig.update_layout(
        title='Delta Tensor Plot',
        xaxis_title='Time',
        yaxis_title='Value'
    )
    fig.show()

def plot_alpha_tensor(alpha_tensor, event_dates):
    fig = go.Figure()
    for i, event_date in enumerate(event_dates):
        fig.add_trace(go.Scatter(
            x=list(range(len(alpha_tensor[i]))),
            y=alpha_tensor[i],
            mode='lines',
            name=f'Event {event_date}'
        ))
    fig.update_layout(
        title='Alpha Tensor Plot',
        xaxis_title='Time',
        yaxis_title='Value'
    )
    fig.show()
