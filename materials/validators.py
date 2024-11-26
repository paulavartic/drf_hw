from rest_framework.serializers import ValidationError


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = 'http://youtube.com'
        if value.get('video'):
            if url not in value.get('video'):
                raise ValidationError('Only YT links')
        return None
