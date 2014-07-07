from rest_framework.serializers import Field


# This is necessary because the PickleField is
# interpreted as a text field, so the output
# is an encoded string and not a usable primitive
class JSONField(Field):
    def to_native(self, obj):
        return obj
