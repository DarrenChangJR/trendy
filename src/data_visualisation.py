import plotly.express as px 
 
 
# Creating the Figure instance
fig = px.line(x=[1,2, 3], y=[1, 2, 3]) 
 
# printing the figure instance
print(fig)
fig.show()