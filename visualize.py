import plotly.express as px


def plotBar(data, x, y, title):
    return px.bar(data, x = x, y = y, title = title)

    