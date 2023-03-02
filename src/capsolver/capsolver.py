import time

import capsolver.error
from capsolver.capsolver_object import CapsolverObject
from capsolver.check import _check_params

_DEFAULT_RETRIES = 60
_DEFAULT_INTERVAL = 1


class Capsolver(CapsolverObject):

    def __init__(self, api_key=None, api_base=None, **params):
        super().__init__(api_key, api_base, **params)


    @staticmethod
    def check_params(params:dict):
        return _check_params(params)
    
    @classmethod
    def postTask(cls, params:dict):
        r = cls().check_params(params=params)
        if isinstance(r, capsolver.error.CapsolverError):
            raise r 
        return cls().request("post", "/createTask", {"task":params})

    @classmethod
    def getTask(cls, **params):
        for _ in range(_DEFAULT_RETRIES):
            time.sleep(_DEFAULT_INTERVAL)
            r = cls().request("post", "/getTaskResult", params)
            if isinstance(r,capsolver.error.CapsolverError):
                raise r
            if r["status"]=="processing":
                continue
            return r
        raise capsolver.error.Timeout('Failed to get results')

    @classmethod
    def solve(cls,params:dict):
        r = cls.postTask(params)
        if isinstance(r, capsolver.error.CapsolverError):
            raise r
        if r['status']=="ready":
            return r['solution']
        r = cls.getTask(taskId=r['taskId'])
        if isinstance(r, capsolver.error.CapsolverError):
            raise r
        return r['solution']


    @classmethod
    def balance(cls):
        r = cls().request("post", "/getBalance",{})
        return r



