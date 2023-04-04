from subprocess import Popen

def load_jupyter_server_extension(nbapp):
    """serve the App.py directory with bokeh server"""
    Popen(["panel", "serve", "App_v2_RW_Cv2.py", "--allow-websocket-origin=*"])
