from dash import Dash, html
import dash_cytoscape as cyto

app = Dash()

app.layout = html.Div([
    html.H1('Gerenciador de Sistema Distribuido'),
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': 'one', 'label': 'udpServer'}, 'position': {'x': 75, 'y': 75},
                'style': {
                'background-color': 'red'
        }},
            {'data': {'id': 'two', 'label': 'udpReceiver'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'},
              "style": [
    {
      'selector': 'node',
      'style': {
        'label': 'data(id)',
        'background-color': 'red'

      }
    }
  ]
        }]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
