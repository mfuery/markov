import json


class mydict(dict):
    """
    This is for debugging.
    """
    def __str__(self):
        return json.dumps(self)
