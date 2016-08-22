import json
# SSE "protocol" is described here: http://mzl.la/UPFyxY


class ServerSentEvent(object):
    def __init__(self, data, event=None, id=None):
        self.data = json.dumps(data)
        self.event = event
        self.id = id
        self.desc_map = {
            self.data: "data",
            self.event: "event",
            self.id: "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.items() if k]
        return "%s\n\n" % "\n".join(lines)
