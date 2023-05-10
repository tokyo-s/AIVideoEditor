import logging as log
from ast import literal_eval
import os

APP_SERVICE_ADDRESS = 'APP_SERVICE_ADDRESS'
APP_SERVICE_PORT = 'APP_SERVICE_PORT'


ENV_VARS_DICT = {APP_SERVICE_ADDRESS: 'localhost',
             APP_SERVICE_PORT: 8000}

class EnvironmentVariables:
    def __init__(self):
        global ENV_VARS_DICT
        self.vars = {}
        for key, default in ENV_VARS_DICT.items():
            self.vars[key] = self._read_env_variable(key, default)

    def _read_env_variable(self, key, default):
        value = os.environ.get(key)
        if value is None:
            log.info(f'The "{key}" env variable is missing. Fallback to {default}')
            value = default
        else:
            log.info(f'Env variable "{key}" is present with value {value}')
        try:
            value = literal_eval(value)
        except:
            pass
        return value
    
    def __getitem__(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            raise AttributeError(f'No such attribute: {name}')
