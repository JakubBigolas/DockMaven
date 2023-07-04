import sys
import config
from modules.dock_maven.app import App
from modules.dock_maven.error import DmvnError

try:

    dockMaven = App()

    args = sys.argv[1:]

    dockMaven.execute(args)

except DmvnError as e:
    print(e)

exit(0)
