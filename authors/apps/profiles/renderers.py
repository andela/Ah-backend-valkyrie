from rest_framework.renderers import JSONRenderer
import json


class ProfileJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        errors = data.get('errors', None)
        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)

        return json.dumps({
            'profile': data
        })


class FollowJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'followers': data
        })


class FollowingsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'followings': data
        })
