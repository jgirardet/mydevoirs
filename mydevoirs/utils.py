import appdirs
from pathlib import Path
from mydevoirs.constants import APP_NAME

def get_dir(key):

    # test config dir
    dire = Path(getattr(appdirs, 'user_' + key + '_dir')(), APP_NAME)
    if not dire.is_dir():
        dire.mkdir(parents=True)
    return dire
