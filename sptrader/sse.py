import json
# SSE "protocol" is described here: http://mzl.la/UPFyxY
###############################################################################
#
# Copyright (C) 2016 Bitquant Research Laboratories (Asia) Limited
#
# Licensed under the Simplified BSD License
#
###############################################################################

class ServerSentEvent(object):
    def __init__(self, data, event=None, id=None):
        try:
            self.data = json.dumps(data)
        except:
            print("Json error %s %s" % (id, event), data)
            self.data = None
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
