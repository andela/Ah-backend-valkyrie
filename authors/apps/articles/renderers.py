import json

from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        try:
            errors = data.get('errors', None)
            if errors is not None:
                return super(ArticleJSONRenderer, self).render(data)

            return json.dumps({
                'article': data
            })
        except Exception as identifier:
            pass
