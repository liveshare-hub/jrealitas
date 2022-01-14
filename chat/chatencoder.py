from json import JSONEncoder

class ChatEncoder(JSONEncoder):
    def default(self, o):
        return o._asdict()