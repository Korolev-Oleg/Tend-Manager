import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    
    path = os.path.join(os.path.abspath("."), 'interface\icons', relative_path)
    return path
