from cleo import Application
from waterjet.commands.install import Install
from waterjet.commands.uninstall import Uninstall

def main():
    application = Application("waterjet", "0.1.0")
    application.add(Install())
    application.add(Uninstall())
    application.run()