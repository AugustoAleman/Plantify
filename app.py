import dash
import dash_html_components as html
from components import footer, navbar
import dash_bootstrap_components as dbc



app = dash.Dash(__name__, title='Plantify', use_pages = True, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Set the title
app.title = 'Plantify'  # Alternate way to set the title

# Define the app layout
app.layout = html.Div([
    html.Link(href="assets\styles.css", rel="stylesheet"),
    # Navbar with logo and options
    navbar.navbar(),
    
    # Page Body
    dash.page_container,

    footer.footer()
])

# Define callback function(s) here if needed

if __name__ == '__main__':
    app.run_server(debug=True)
