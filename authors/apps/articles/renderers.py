import json

from rest_framework.renderers import JSONRenderer


class LikeArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)
        custom_errors = {}

        if errors is not None:
            for key in errors:
                if key == 'article':
                    custom_errors.update({
                        key: '{} is a required field'.format(key)
                    })
                if key == 'like':
                    custom_errors.update({
                        key: '{} is a required field'.format(key)
                    })
            return super(LikeArticleJSONRenderer, self).render(custom_errors)

        return json.dumps(data)
