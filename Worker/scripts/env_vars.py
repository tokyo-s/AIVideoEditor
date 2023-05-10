import logging as log
from ast import literal_eval
import os

DISCOVERY_SERVICE_ADDRESS = 'DISCOVERY_SERVICE_ADDRESS'
DISCOVERY_SERVICE_PORT = 'DISCOVERY_SERVICE_PORT'
WORKER_NAME = 'WORKER_NAME'
WORKER_ADDRESS = 'WORKER_ADDRESS'
WORKER_PORT = 'WORKER_PORT'

ENV_VARS_DICT = {DISCOVERY_SERVICE_ADDRESS: 'localhost',
             DISCOVERY_SERVICE_PORT: 8002,
             WORKER_NAME: 'worker',
             WORKER_ADDRESS: 'localhost',
             WORKER_PORT: 8003}

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
