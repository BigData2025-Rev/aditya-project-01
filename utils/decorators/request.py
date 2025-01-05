import json


def json_required(f):
    def json_present(self, *args, **kwargs):
        try:
            self.data = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"message": "Expected JSON in request body. Got None"})
            return
        return f(self, *args, **kwargs)
    return json_present


def json_optional(f):
    def json_present(self, *args, **kwargs):
        self.data = None
        try:
            self.data = json.loads(self.request.body)
        except json.JSONDecodeError:
            pass
        return f(self, *args, **kwargs)
    return json_present