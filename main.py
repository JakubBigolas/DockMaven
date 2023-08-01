import sys
from modules.dock_maven.app import App
from modules.dock_maven.error import DmvnError

try:

    dockMaven = App()

    args = sys.argv[1:]

    dockMaven.execute(args)

except DmvnError as e:
    if e.error is not None:
        print(e)
    exit(e.error_code)

exit(0)
