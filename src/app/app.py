import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, Input, Output, dcc, callback
import dash_daq as daq
import dash_bootstrap_components as dbc

from config import MART_DIR

DATA = MART_DIR / 'customer_segments.parquet'

df = pd.read_parquet(DATA)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

genders = [{'label': gen, 'value': gen} for gen in df['gender'].unique()]
categories = [{'label': cat, 'value': cat} for cat in df['favorite_category'].unique()]
devices = [{'label': dev, 'value': dev} for dev in df['device_type'].unique()]

slicerStyle = {
    'minWidth': '200px',
    'maxWidth': '300px',
    'flex': '1', 
    'minHeight': '110px',
    "boxShadow": "0 4px 16px rgba(0,0,0,0.1)",
    "borderRadius": "1rem",
    "padding": "0.2rem",
    "backgroundColor": "white"
}

cardStyle={
        "boxShadow": "0 4px 16px rgba(0,0,0,0.1)",
        "borderRadius": "1rem",
        "padding": "1rem",
        "backgroundColor": "white",
        # 'outline': 'none'
    }

segOrder = {
    'segment': [
        'Top Customers',
        'Others - Premium',
        'Others - Not premium',
        'At Risk',
        'Dormant',
        'New Customers'
    ]
}

segColors = {
    'Top Customers': "#2D8D55",
    'Others - Premium': "#216897",
    'Others - Not premium': '#95A5A6',
    'At Risk': "#BA6114",
    'Dormant': "#AB2617",
    'New Customers': "#723A89"
}

slicers = [
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Label(
                    'Genders'
                ),
                dcc.Dropdown(
                    id='genderDD',
                    options=genders,
                    placeholder='All genders'
                )
            ]
        ),
        style=slicerStyle
    ),
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Label(
                    'Prefered categories'
                ),
                dcc.Dropdown(
                    id='categoryDD',
                    options=categories,
                    multi=True,
                    placeholder='All categories'
                )
            ]
        ),
        style=slicerStyle
    ),
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Label(
                    'Device used'
                ),
                dcc.Dropdown(
                    id='deviceDD',
                    options=devices,
                    placeholder='All devices'
                )
            ]
        ),
        style=slicerStyle
    ),
    dbc.Card(
        dbc.CardBody(
            [
                daq.ToggleSwitch(
                    id='subscriptionTGL',
                    label='Premium subscription'
                )
            ]
        ),
        style=slicerStyle
    ),
    dbc.Card(
        dbc.CardBody(
            [
                daq.ToggleSwitch(
                    id='marketingTGL',
                    label='Marketing comms opt-in'
                )
            ]
        ),
        style=slicerStyle
    )
]

app.layout = dbc.Container([
    # Header
    html.Div([
        html.H1(
            'Customer segmentation dashboard'
        ),
        html.H3(
            'Using RFM methodology'
        ),
        html.Br()
    ]),
    # Filters
    dbc.Stack(
        slicers,
        style={
            'flexWrap': 'wrap',
            'alignItems': 'flex-start'},
        direction='horizontal',
        gap=3
    ),
    html.Br(),
    # Score cards
    dbc.Stack([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    id='totalRevenueCard',
                    style=cardStyle
                )
            ]),
            dbc.Col([
                dbc.Card(
                    id='customersCard',
                    style=cardStyle
                )
            ]),
            dbc.Col([
                dbc.Card(
                    id='avgRevenueCard',
                    style=cardStyle
                )
            ])
        ], className="mb-4"),
        # html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody([
                            html.H4('Distribution by segment')
                        ]),
                        dcc.Graph(id='distributionPie')
                    ],
                    style=cardStyle,
                    )
            ]),
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody([
                            html.H4('Support tickets by segment')
                        ]),
                        dcc.Graph(id='ticketsColumn')
                    ],
                    style=cardStyle
                )
            ])
        ], className="mb-4"),
        # html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody([
                            html.H4('Loyalty points by segment')
                        ]),
                        dcc.Graph(id='loyaltyColumn')
                    ],
                    style=cardStyle
                )
            ]),
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody([
                            html.H4('Geographical distribution of customers')
                        ]),
                        dcc.Graph(id='distributionMap')
                    ],
                style=cardStyle
                )
            ])
        ], className="mb-4"),
        # html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody([
                            html.H4('Product consumption by segment')
                        ]),
                        dcc.Graph(id='categorySegmentMatrix')
                    ],
                style=cardStyle
                )
            ])
        ], className="mb-4")
    ])
], 
style={
    'backgroundColor': "#cdcdcdff",
    'padding': '2rem',
    'minHeight': '100vh'
})

@callback(
        Output('totalRevenueCard', 'children'),
        Output('customersCard', 'children'),
        Output('avgRevenueCard', 'children'),
        Output('distributionPie', 'figure'),
        Output('ticketsColumn', 'figure'),
        Output('loyaltyColumn', 'figure'),
        Output('distributionMap', 'figure'),
        Output('categorySegmentMatrix', 'figure'),
        Input('genderDD', 'value'),
        Input('categoryDD', 'value'),
        Input('deviceDD', 'value'),
        Input('subscriptionTGL', 'value'),
        Input('marketingTGL', 'value')
)

def update_visuals (selGender, selCategory, selDevice, selSubscription, selOptIn):
    df2 = df.copy()
    if selGender:
        df2 = df2[df2['gender'] == selGender]
    if selCategory:
        df2 = df2[df2['favorite_category'].isin(selCategory)]
    if selDevice:
        df2 = df2[df2['device_type'] == selDevice]
    if selSubscription:
        df2 = df2[df2['subscription'] == selSubscription]
    if selOptIn:
        df2 = df2[df2['marketing_opt_in'] == selOptIn]
    
    # 1st Row
    revenue = f"$ {df2['monetary'].sum():,.0f}"
    customers = f" {df2['customer_id'].nunique():,.0f}"
    avgsales = f"$ {df2['monetary'].mean():,.0f}"

    fig_r = dbc.CardBody([
        html.H4('Total revenue'),
        html.P(revenue, className='card-text', style={'marginBottom': '0'})
    ])
    fig_c = dbc.CardBody([
        html.H4('Total customers'),
        html.P(customers, className='card-text')
    ])
    fig_a = dbc.CardBody([
        html.H4('Average revenue'),
        html.P(avgsales, className='card-text')
    ])

    #2nd Row
    dist = df2['segment'].value_counts()
    ticks = df2.groupby(['segment', 'support_tickets'])['customer_id'].count().reset_index()

    fig_d = px.pie(
        dist,
        values=dist.values,
        names=dist.index,
        hole=0.3,
        category_orders=segOrder,
        color_discrete_map=segColors,
        color=dist.index
    )
    fig_d.update_traces(
        textinfo='label+percent',
        textposition='outside',
        showlegend=False
    )

    fig_t = px.bar(
        ticks,
        x='support_tickets',
        y='customer_id',
        color='segment',
        category_orders=segOrder,
        color_discrete_map=segColors
    )
    fig_t.update_layout(
        plot_bgcolor='white',
        xaxis_title=None,
        yaxis_title=None,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            x=0.5,
            xanchor='center'
        )
    )

    # 3rd Row
    loy = df2.groupby('segment')['loyalty_points'].mean().round(2).reset_index()
    maps = df2.groupby('ISO3').agg({'country':'first', 'customer_id': 'count'}).reset_index()

    fig_l = px.bar(
        loy,
        x='segment',
        y='loyalty_points',
        color='segment',
        color_discrete_map=segColors
    )
    fig_l.update_layout(
        plot_bgcolor='white',
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )

    fig_m = px.choropleth(
        maps,
        locations='ISO3',
        color='customer_id',
        hover_name='country',
        color_continuous_scale='Blues',
        range_color=(350, 450)
    )

    # 4th row
    segs = df2.pivot_table(index='segment', columns='favorite_category', values='customer_id', aggfunc='count', observed=True)
    fig_s = go.Figure(
        go.Heatmap(
            x=segs.columns,
            y=segs.index,
            z=segs.values,
            colorscale='Blues'
        )
    )
    fig_s.update_layout(
        xaxis_side='top'
    )

    return fig_r, fig_c, fig_a, fig_d, fig_t, fig_l, fig_m, fig_s


if __name__ == '__main__':
    app.run(debug=True, port=8050)