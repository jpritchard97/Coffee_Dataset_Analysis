'''
Import Libraries
----------------
Import Dash, components, Pandas, Plotly Express, and dash-bootstrap-components
Load and clean dataset (CSV, age, coffee consumption columns)

App Layout
----------
Initialize Dash app with external stylesheets
Set app title: "Coffee Consumption Dashboard"

Data Preparation
----------------
Create dataframes for favorite coffee drinks and employment status

Navigation Bar
--------------
Create navigation bar with links to Overview, Coffee Preferences, Age Analysis, and Demographics pages

Page Layouts
------------
Overview: Title and welcome text
Coffee Preferences: Header and bar chart of favorite drinks
Age Analysis: Header, dropdown for cups per day, bar chart for consumption by age, pie chart for age distribution
Demographics: Header, bar chart for employment status, histogram for monthly spending, bar chart for political affiliation and coffee preferences

Main Layout
-----------
Define app layout with navigation bar and dynamic page content container

Callbacks
---------
Coffee consumption by age group based on dropdown selection
Update page content based on URL

Run App
-------
Run Dash server with debug mode enabled

'''

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load and clean the dataset
# Read the CSV file into a DataFrame
df = pd.read_csv("cleaned_combined_coffee_dataset_bq.csv")

# Convert the 'What_is_your_age' column to string type for consistent processing
df['What_is_your_age'] = df['What_is_your_age'].astype(str)

# Convert the cups of coffee column to numeric, coercing errors to NaN
df['How_many_cups_of_coffee_do_you_typically_drink_per_day'] = pd.to_numeric(df['How_many_cups_of_coffee_do_you_typically_drink_per_day'], errors='coerce')

# Drop NaN values and convert the remaining values to integers
df['How_many_cups_of_coffee_do_you_typically_drink_per_day'] = df['How_many_cups_of_coffee_do_you_typically_drink_per_day'].dropna().astype(int)

# Initialize the Dash app with Bootstrap styling and suppress callback exceptions
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Coffee Consumption Dashboard"  # Set the title of the app

# Create dataframes for visualizations
# Count occurrences of each favorite coffee drink
favorite_coffee_counts = df['What_is_your_favorite_coffee_drink'].value_counts().reset_index()
favorite_coffee_counts.columns = ['Coffee_Drink', 'Count']  # Rename columns for clarity

# Count occurrences of each employment status
employment_counts = df['Employment_Status'].value_counts().reset_index()
employment_counts.columns = ['Status', 'Count']  # Rename columns for clarity

# Creation of the navbar for navigation between pages
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="/page-1")),
        dbc.NavItem(dbc.NavLink("Coffee Preferences", href="/page-2")),
        dbc.NavItem(dbc.NavLink("Age Analysis", href="/page-3")),
        dbc.NavItem(dbc.NavLink("Demographics", href="/page-4"))
    ],
    brand="Coffee Consumption Dashboard",  # Brand name displayed on the navbar
    brand_href="/",  # Link for the brand name
    color="primary",  # Navbar color
    dark=True,  # Dark mode for the navbar
)


# Page 1: Overview
page_1_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Coffee Consumption Dashboard", className="my-4")) # Set header for page
        ]),
        dbc.Row([
            dbc.Col(html.P("The Coffee Consumption Dashboard serves as a valuable resource for anyone looking to gain insights into coffee consumption trends and preferences. Its interactive features and well-structured visualizations make it a powerful tool for analysis, enabling users to make data-driven decisions in the coffee industry or simply satisfy their curiosity about coffee habits. Whether you're a coffee enthusiast, a business owner, or a researcher, this dashboard provides a comprehensive look at the rich landscape of coffee consumption.", className="mb-4")) #My own personalised text
        ])
    ])
])

# Page 2: Coffee Preferences
page_2_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Coffee Preferences", className="my-4"))
        ]),
        dbc.Row([
            dbc.Col([
                html.P("The chart below gives evidence that  Pour-over and Latte coffee drinks are the most favored among respondents, with significantly higher counts compared to other drinks such as Cortado and Cold Brew. This preference suggests a strong market for these types of coffee, which may guide coffee shops and brands in their product offerings. Conversely, the lower popularity of drinks like Mocha and Cold Brew indicates potential areas for growth or re-evaluation in marketing strategies.", className="mb-3"), #My own personalised text
                dcc.Graph(
                    figure=px.bar(
                        favorite_coffee_counts,
                        x='Coffee_Drink',
                        y='Count',
                        title='Favorite Coffee Drink Distribution',
                        color='Coffee_Drink'
                    ).update_layout(margin=dict(l=50, r=50, t=80, b=50))
                )
            ], width=12)
        ]),
    ])
])

# Page 3: Age Analysis
page_3_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Age Analysis of Coffee Consumption", className="my-4"))
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Select the number of cups per day to see how consumption varies across age groups.", className="mb-3"),
                html.Label("Select Number of Cups per Day:"),
                dcc.Dropdown(
                    id='cups-dropdown',
                    options=[{'label': str(x), 'value': x} 
                            for x in sorted(df['How_many_cups_of_coffee_do_you_typically_drink_per_day'].unique()) if pd.notnull(x)],
                    value=df['How_many_cups_of_coffee_do_you_typically_drink_per_day'].min(),
                    style={'marginBottom': '20px'}
                ),
                dcc.Graph(id='age-consumption-pattern')
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                html.P("In comparing age with daily coffee consumption, younger consumers, especially those aged 25-34, drink 2 to 4 cups daily, reflecting a strong coffee preference. Conversely, older individuals, particularly those 55 and above, consume 1 cup or less per day, indicating a decline in consumption with age. This generational shift in habits may be biased if the survey disproportionately includes younger participants, potentially underrepresenting older consumers.", className="my-3"),#My own personalised text
                dcc.Graph(
                    figure=px.pie(
                        df,
                        names='What_is_your_age',
                        title='Age Distribution'
                    ).update_layout(margin=dict(l=50, r=50, t=80, b=50))
                )
            ], width=12)
        ])
    ])
])

# Page 4: Demographics layout
page_4_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Demographic Analysis of Coffee Consumption", className="my-4"))
        ]),
        dbc.Row([
            dbc.Col([
                html.P(" The analysis of employment status and monthly coffee spending indicates that full-time employees typically spend $40 to $100 monthly on coffee, viewing it as essential for productivity. In contrast, students and unemployed individuals often spend under $20. This trend suggests that financial stability directly influences coffee consumption habits, but the dataset may be biased due to an overrepresentation of employed respondents, potentially skewing the overall spending patterns.", className="mb-3"), #My own personalised text
                dcc.Graph(
                    figure=px.bar(
                        employment_counts,
                        x='Status',
                        y='Count',
                        title='Employment Status Distribution',
                        color='Status'
                    ).update_layout(margin=dict(l=50, r=50, t=80, b=50))
                )
            ], width=6),
            dbc.Col([
                html.P("", className="mb-3"),
                dcc.Graph(
                    figure=px.histogram(
                        df,
                        x='In_total_much_money_do_you_typically_spend_on_coffee_in_a_month',
                        title='Monthly Coffee Spending Distribution'
                    ).update_layout(margin=dict(l=50, r=50, t=80, b=50))
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.P("The analysis below presents interesting correlations between political beliefs and coffee choices. For instance, some coffee beverages are favored by certain kinds of political groups; this would mean that marketing campaigns could targeting certain audiences based on their political affiliations, leading to higher customer engagement in brands.", className="mb-3"), #My own personalised text
                dcc.Graph(
                    figure=px.bar(
                        df,
                        x='Political_Affiliation',
                        color='What_is_your_favorite_coffee_drink',
                        title='Political Affiliation and Coffee Preferences',
                        barmode='group',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    ).update_layout(
                        xaxis_title="Political Affiliation",
                        yaxis_title="Count",
                        showlegend=True,
                        legend_title="Favorite Coffee Drink",
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=1.05,
                            bgcolor='rgba(255, 255, 255, 0.8)'
                        ),
                        margin=dict(l=50, r=250, t=80, b=50),
                        height=600,
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    ).update_xaxes(
                        tickangle=45,
                        title_font=dict(size=14),
                        tickfont=dict(size=12),
                        gridcolor='lightgrey'
                    ).update_yaxes(
                        title_font=dict(size=14),
                        tickfont=dict(size=12),
                        gridcolor='lightgrey'
                    ).update_traces(
                        opacity=0.85
                    )
                )
            ], width=12)
        ])
    ])
])

# Define the main layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Location component for URL routing
    navbar,  # Include the navbar
    html.Div(id='page-content')  # Placeholder for page content
])

# Callback to update the age consumption pattern graph based on selected cups
@app.callback(
    Output('age-consumption-pattern', 'figure'),
    [Input('cups-dropdown', 'value')]  # Input from the dropdown for cups
)
def update_age_consumption(selected_cups):
    filtered_df = df[df['How_many_cups_of_coffee_do_you_typically_drink_per_day'] == selected_cups]  # Filter DataFrame based on selected cups
    
    # Count occurrences of each age group
    age_counts = filtered_df['What_is_your_age'].value_counts().reset_index()
    age_counts.columns = ['Age_Group', 'Count']  # Rename columns for clarity
    
    fig = px.bar(
        age_counts,
        x='Age_Group',  # X-axis for age groups
        y='Count',  # Y-axis for count of people
        title=f'Daily Coffee Consumption Pattern by Age Group ({selected_cups} cups)',  # Title of the graph
        color_discrete_sequence=['#2E86C1']  # Color for the bars
    )
    
    fig.update_layout(
        xaxis_title="Age Group",  # X-axis title
        yaxis_title="Number of People",  # Y-axis title
        showlegend=False,  # Hide legend
        margin=dict(l=50, r=50, t=80, b=50),  # Adjust margins
        plot_bgcolor='white',  # Background color for the plot
        paper_bgcolor='white',  # Background color for the paper
        bargap=0.2  # Gap between bars
    )
    
    # Update bar width and opacity
    fig.update_traces(
        marker_line_color='rgb(8,48,107)',  # Line color for bar edges
        marker_line_width=1.5,  # Line width for bar edges
        opacity=0.8  # Set opacity for bars
    )
    
    return fig  # Return the updated figure

# Callback to update the political affiliation chart based on selected affiliations
@app.callback(
    Output('political-affiliation', 'figure'),
    [Input('political-dropdown', 'value')]  # Input from the dropdown for political affiliations
)
def update_political_chart(selected_affiliations):
    if not selected_affiliations:  # If no affiliations are selected
        filtered_df = df  # Use the full DataFrame
    else:
        filtered_df = df[df['Political_Affiliation'].isin(selected_affiliations)]  # Filter DataFrame based on selected affiliations
    
    # Count occurrences of each political affiliation
    political_counts = filtered_df['Political_Affiliation'].value_counts().reset_index()
    political_counts.columns = ['Political_Affiliation', 'Count']  # Rename columns for clarity
    
    fig = px.bar(
        political_counts,
        x='Political_Affiliation',  # X-axis for political affiliations
        y='Count',  # Y-axis for count of people
        title='Political Affiliation Distribution',  # Title of the graph
        color_discrete_sequence=['#2E86C']
    )
    
    # Rotate x-axis labels if they're too long
    fig.update_xaxes(tickangle=45)  # Adjust x-axis label angle for better readability
    
    return fig  # Return the updated figure

# Callback to display the appropriate page based on the URL path
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]  # Input for the current URL path
)
def display_page(pathname):
    if pathname == '/' or pathname == '/page-1':  # Check for the overview page
        return page_1_layout  # Return the overview layout
    elif pathname == '/page-2':  # Check for the coffee preferences page
        return page_2_layout  # Return the coffee preferences layout
    elif pathname == '/page-3':  # Check for the age analysis page
        return page_3_layout  # Return the age analysis layout
    elif pathname == '/page-4':  # Check for the demographics page
        return page_4_layout  # Return the demographics layout
    else:
        return '404: Page Not Found'  # Return a 404 message for unknown paths

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)  # Start the server in debug mode