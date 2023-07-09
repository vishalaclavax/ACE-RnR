import pytz, random, string
from datetime import datetime
from copy import deepcopy
from collections import OrderedDict
import hashlib, html
from werkzeug.datastructures import Headers
from flask import request, current_app, render_template, jsonify
import json


class ResponseDict(dict):
    schema = OrderedDict({
        'success': True,
        'message': None,
        'errors': None,
        'data': None,
    })

    data = {}

    def __init__(self, *args, **kwargs):
        self.data = deepcopy(self.schema)
        if len(args) and isinstance(args[0], dict):
            self.data.update(args[0])
        else:
            self.data.update(kwargs)
        super().__init__(self.data)


class AttrDict(dict):
    """Dict behaving like an object, with attribute-style access."""

    __strict_attr__ = True
    __attr_default__ = None

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            if self.__strict_attr__:
                raise AttributeError(name)
            else:
                return self.__attr_default__

    def __setattr__(self, name, value):
        if name not in ('__strict_attr__', '__attr_default__'):
            self[name] = value


def parse_date(date_str):
    """Parse Date string"""
    formats = (
        '%Y-%m-%dT%H:%M:%S.%3f', '%Y-%m-%d %H:%M:%S.%3f',
        '%Y-%m-%dT%H:%M:%S.%3fZ', '%Y-%m-%d %H:%M:%S.%3fZ',
        '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S+%f:00', '%Y-%m-%d %H:%M:%S+%f:00',
        '%d-%m-%Y %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%m-%d-%Y',
        '%m/%d/%Y',
        '%d-%m-%Y',
        '%d/%m/%Y'
    )
    if date_str:
        for date_format in formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                pass
    return None


def utc_to_tz(utc_dt, tzinfo):
    tz_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tzinfo)
    return tzinfo.normalize(tz_dt)


def format_date(date, date_format='%d-%m-%Y %I:%M %p', is_datetime_str=True, is_timestamp=False, is_utc=True):
    """Format Date"""
    if is_datetime_str:
        date_object = parse_date(date.split('.')[0])
    elif is_timestamp:
        date_object = datetime.fromtimestamp(date)
    else:
        date_object = date
    try:
        if is_utc:
            return utc_to_tz(date_object, current_app.config['APP_TZINFO']).strftime(date_format) if date_object else 'Invalid Date'
        else:
            return date_object.strftime(date_format) if date_object else 'Invalid Date'
    except ValueError:
        return 'Invalid Date'


def handle_web_http_error(error, template_name='errors/http-error.html'):
    headers = error.get_headers(request.environ)
    return render_template(template_name, error=error), error.code, headers


def handle_api_http_error(error):
    error_headers = Headers(error.get_headers(request.environ))
    error_headers.remove('content-type')
    response_dict = ResponseDict(
        success=False,
        message=error.description,
        errors=['{} - {}'.format(error.code, error.name)],
    )
    return jsonify(response_dict), error.code, error_headers


def genreate_code(prefix, length=9):
    code = str(prefix) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(length)))
    return code


def random_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choices(chars, k=size))

def create_hash(value):
    """Create sha512 hash"""
    return hashlib.sha512(str(value).encode('utf-8')).hexdigest()


def remove_html(str):
    """Convert the number to int if after decimal only 0"""
    try:
        if str is not None:
            data = html.unescape(str).strip()
            print("-----remove_html-------->",data)
            return data
        else:
            return ""
    except Exception as exp:
        print("exp from remove_html")
        print(exp)
        return ""

def escape_single_quotes(string):
    # The two backslashes are interpreted as a single one
    # because the backslash is the escaping character.
    return string.replace("'", "\\'")

def change_to_dmy_format(date_str):
    try:
        arr_date = date_str.split("-")
        formatted_date = "{}/{}/{}".format(arr_date[2], arr_date[1], arr_date[0])
    except:
        formatted_date = ''
    return formatted_date

def date_month_name(date_str):
    try:
        arr_date = date_str.split("-")
        month = arr_date[1]
        month_param = {

            "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
            "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"

        }
        month_name = month_param[month]
        formatted_date = "{} {}".format(arr_date[0], month_name)
    except:
        formatted_date = ''
    return formatted_date

def convert_to_json(item_list):
    try:
        str_data = json.dumps(item_list)
    except:
        str_data = ''
    return str_data
