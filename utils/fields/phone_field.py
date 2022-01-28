from django.db.models import CharField


class PhoneField(CharField):
    # TODO: add validations on phone numbers
    # TODO: change how field is saved

    def __init__(self, max_length=16, *args, **kwargs):
        super().__init__(*args, max_length=max_length, **kwargs)
