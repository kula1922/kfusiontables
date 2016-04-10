import logging
from httplib2 import Http

from apiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
from oauth2client.service_account import ServiceAccountCredentials

from kfusiontables.kftapi.exceptions import IncorrectAccessFilePathException


logger = logging.getLogger(__name__)


class KFTApiBase:
    """
    Base KFT Api Class. KFTApi is a oauth2client extension for fusiontables.
    Build service for google fusiontables.
    """
    SCOPES = ['https://www.googleapis.com/auth/fusiontables']
    SERVICE = None
    PATH_TO_KEY = None

    def __init__(self, path_to_key):
        """
        Set path to google apps access key and build service.

        :param string path_to_key: Path to google apps credentials file.
        """
        self.PATH_TO_KEY = path_to_key
        self.build_service()

    def build_service(self):
        """
        Build service for connect to google fusiontables.
        """

        logger.info('Build service for connect to google fusiontables server.')

        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.PATH_TO_KEY,
                scopes=['https://www.googleapis.com/auth/fusiontables']
            )
            http_auth = credentials.authorize(Http())
        except IOError:
            raise IncorrectAccessFilePathException(
                "Access key path '{0}' is incorrect.".format(
                    self.PATH_TO_KEY
                )
            )

        self.SERVICE = build('fusiontables', 'v2', http=http_auth)

    def execute_query(self, query):
        """
        Simple execute google fusiontables sql query.
        """

        logger.debug('Executing query: %s', query)

        return self.SERVICE.query().sql(sql=query).execute()

    def table_exist(self, table_id=None):
        """
        Remote check if google fusiontables table exist.
        """
        logger.debug('Check if table exist for id: %s', table_id)

        try:
            self.SERVICE.table().get(tableId=table_id).execute()
            return True
        except GoogleHttpError as exc:
            if exc.resp.get('status') == '404':
                return False
            raise exc
