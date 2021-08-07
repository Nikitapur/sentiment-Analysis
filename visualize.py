import plotly.express as px


def plotBar(data, x, y, title):
    return px.bar(data, x = x, y = y, title = title)

def plotHistogram(data, x, title):
    return px.histogram(data, x = x, title = title)

    
def plotPie(data, names, values, title):
    return px.pie(data, names = names, values = values, title = title)