from datetime import datetime, timedelta
from app.utils import format_date
import hashlib

def calc_target_time(start_datetime_str, validity_seconds):
    # compare with utc time (use comment lines)
    # datetime_str_parts = start_datetime_str.split('.')
    # datetime_object = datetime.strptime(datetime_str_parts[0], '%Y-%m-%dT%H:%M:%S')
    da = format_date(start_datetime_str)
    datetime_object = datetime.strptime(da, '%d-%m-%Y %H:%M %p')
    target_datetime_object = datetime_object + timedelta(seconds=validity_seconds)
    return target_datetime_object.timestamp() * 1000


def check_target_time(target_timestamp):
    return target_timestamp > datetime.utcnow().timestamp() * 1000


def get_utc_date(start_datetime_str):
    datetime_str_parts = start_datetime_str.split('.')
    return datetime.strptime(datetime_str_parts[0], '%Y-%m-%dT%H:%M:%S')


def get_res_error_msg(res, default_msg='Something went wrong! Please try again later.'):
    error_msg = None
    errors = res.get('errors')
    message = res.get('message')
    if errors and isinstance(errors, list) and len(errors):
        error = errors[0]
        if error and isinstance(error, dict) and 'detail' in error:
            if isinstance(error['detail'], list) and len(error['detail']):
                error_detail = error['detail'][0]
                if error_detail and isinstance(error_detail, dict) and 'message' in error_detail and isinstance(error_detail['message'], str):
                    error_msg = error_detail['message']
            elif isinstance(error['detail'], str):
                error_msg = error['detail']
    return error_msg or message or default_msg

def get_hash_string(str):
    hash_string = hashlib.sha256(str.encode())
    hash_str = hash_string.hexdigest()
    return hash_str
