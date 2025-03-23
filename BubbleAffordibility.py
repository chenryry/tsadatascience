import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('data.csv')

df['City'] = df['ZIP Code'].apply(lambda x: 'Charlotte' if str(x).startswith('282') else 'Detroit')

percentile_10 = df['More than 30 percent'].quantile(0.10)

df_trimmed_10 = df[df['More than 30 percent'] > percentile_10].reset_index(drop=True)

df_trimmed_10['Bubble Size'] = np.interp(
    df_trimmed_10['More than 30 percent'],
    (df_trimmed_10['More than 30 percent'].min(), df_trimmed_10['More than 30 percent'].max()),
    (1, 50)
)

y_range = df_trimmed_10['Median Home Value'].max() - df_trimmed_10['Median Home Value'].min()
y_min_adjusted = df_trimmed_10['Median Home Value'].min() - y_range * 0.1
y_max_adjusted = df_trimmed_10['Median Home Value'].max() + y_range * 0.1

fig = px.scatter(
    df_trimmed_10,
    x='Gini Index',
    y='Median Home Value',
    size='Bubble Size',
    color='City',
    hover_data={'ZIP Code': True, 'More than 30 percent': True},
    color_discrete_map={'Charlotte': 'blue', 'Detroit': 'red'},
    title='Income Inequality vs. Median Home Price (sizing relatively indexed)',
    labels={
        'Gini Index': 'Income Inequality (Gini Index)',
        'Median Home Value': 'Median Home Value',
        'More than 30 percent': '% Spending 30%+ on Housing'
    },
    size_max=50
)

fig.update_traces(marker=dict(sizemode='area', opacity=0.4))

fig.update_layout(
    template='simple_white',
    title_font_size=24,
    font=dict(size=14),
    legend=dict(title='City', orientation='h', x=0.5, xanchor='center', y=-0.2),
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=40, r=40, t=60, b=60),
    yaxis=dict(range=[y_min_adjusted, y_max_adjusted])
)

fig.show()
