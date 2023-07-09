"""File type utilities"""
import math
import os


FILE_TYPES = {
    'csv': ['text/x-comma-separated-values', 'text/comma-separated-values', 'application/vnd.ms-excel', 'application/x-csv', 'text/x-csv', 'text/csv', 'application/csv', 'application/excel', 'application/vnd.msexcel'],
    'xls': ['application/vnd.ms-excel', 'application/msexcel', 'application/x-msexcel', 'application/x-ms-excel', 'application/x-excel', 'application/x-dos_ms_excel', 'application/xls', 'application/x-xls', 'application/excel'],
    'xlsx': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
    'pdf': ['application/pdf'],
    'json': ['application/json', 'text/json'],
    'xml': ['application/xml', 'text/xml'],
    'zip': ['application/x-zip', 'application/zip', 'application/x-zip-compressed', 'application/s-compressed', 'multipart/x-zip'],
    'jpg': ['image/jpeg', 'image/pjpeg'],
    'jpeg': ['image/jpeg', 'image/pjpeg'],
    'png': ['image/png', 'image/x-png'],
    'ico': ['image/x-icon', 'image/x-ico', 'image/vnd.microsoft.icon'],
    'gif': ['image/gif'],
}


IMG_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

def bytes_to_unit(byte_size):
    """Parse byte size to respective unit size"""
    base = 1024
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    exponent = int(min(math.floor(math.log(byte_size) / math.log(base)), len(units) - 1))
    size = str(round(byte_size / math.pow(base, exponent), 2))
    unit = units[exponent]
    return size + unit


def get_mimes(ext, default=None):
    return FILE_TYPES.get(ext, default or [])


def get_mime_list(ext_list):
    mime_list = []
    for ext in ext_list:
        mimes = get_mimes(ext)
        if mimes:
            mime_list.extend(mimes)
    return mime_list


def get_file_extension(filename):
	# return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    ext = os.path.splitext(filename)[1]
    if ext.startswith('.'):
        ext = ext[1:]
    return ext.lower()


def has_file_extensions(filename, extension_list):
    return get_file_extension(filename) in extension_list


def is_valid_file(filename, allowed_extensions, mimetype=None):
    if filename:
        print(filename, "filename--------------")
        ext = get_file_extension(filename)
        if not ext:
            return False
        allowed_mimetypes = get_mimes(ext)
        valid_mimetype = mimetype in allowed_mimetypes if mimetype and allowed_mimetypes else True
        return (ext in allowed_extensions) and valid_mimetype


def is_sheet_file(filename, mimetype=None):
    return is_valid_file(filename, IMG_EXTENSIONS, mimetype)
