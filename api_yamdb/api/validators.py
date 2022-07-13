from rest_framework import serializers


class NotFoundValidationError(serializers.ValidationError):
    status_code = 404


def username_restriction(username):
    if username == 'me':
        raise serializers.ValidationError(
            'Not allowed to use "me" as username'
        )
    return username
