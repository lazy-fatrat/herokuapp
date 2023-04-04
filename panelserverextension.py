from subprocess import Popen

def load_jupyter_server_extension(nbapp):
    """serve the App.py directory with bokeh server"""
    Popen(["panel", "serve", "App.ipynb", "--allow-websocket-origin=*"])
