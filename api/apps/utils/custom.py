import datetime


class CustomUtil:
    def __init__(self):
        self.response = {
            'request_detail': {
                'description': '',
                'request_date_utc': datetime.datetime.utcnow(),
            },
            'data': {
                'message': ''
            },
            'status_code': 400,
        }
