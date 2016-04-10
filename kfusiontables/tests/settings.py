from kfusiontables.settings import *  # noqa

SECRET_KEY = 'fake-key'

KFUSIONTABLES_ACCESS_FILE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'fake_access_key.json'
    )
)

KFUSIONTABLES_AUTO_SYNC = False

LOGGING = {}
