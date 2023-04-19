import numpy as np
import plotly.express as px
x = [i for i in range(60)]
y = np.random.normal(2000, 100, 60)
fig = px.line(x=x, y=y)
fig.show()