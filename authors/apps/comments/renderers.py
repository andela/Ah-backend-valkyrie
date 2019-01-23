import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class CommentsRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, render_context=None):
        # switch between list and dict to render the appropriate data type
        if not isinstance(data, ReturnList):
            errors = data.get("error", None)
            if errors is not None:
                return super(CommentsRenderer, self).render(data)
            return json.dumps({"comment": data})
        return json.dumps({"comments": data, "commentsCount": len(data)})