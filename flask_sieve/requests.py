from functools import wraps
from flask import request as flask_request
from flask_sieve.validator import Validator
from flask_sieve.exceptions import ValidationException


class FormRequest:
    def __init__(self, request=None):
        request = request or flask_request
        self._validator = Validator(
            rules=self.rules(),
            request=self._request_to_dict(request)
        )

    def validate(self):
        if self._validator.fails():
            raise ValidationException(self._validator.messages())
        return True

    def _request_to_dict(self, request):
        dict_request = {}
        dict_request.update(request.form.to_dict(flat=True))
        dict_request.update(request.files.to_dict(flat=True))
        return dict_request



class JsonRequest(FormRequest):
    def __init__(self, request=None):
        if not request.is_json():
            raise ValidationException({'request': 'Request must be valid JSON'})

        request = request or flask_request
        self._validator = Validator(
            rules=self.rules(),
            request=request.json
        )
