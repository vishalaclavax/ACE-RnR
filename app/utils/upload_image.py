from flask import current_app
import os, random, string, uuid, urllib, common_functions
import re
from werkzeug.utils import secure_filename
from app.utils.file_type import is_valid_file, get_file_extension, bytes_to_unit, get_mimes, get_mime_list, IMG_EXTENSIONS
from azure.storage.blob import ContentSettings,BlockBlobService
import PIL
from PIL import Image
from datetime import datetime
from app.services import auth_service
import pandas as pd

class UploadImage(object):
    """Upload images class for flask"""      

    def upload_images(self, img_file):
        page_err = None
        # mimetype=get_mimes(get_file_extension(img_file.filename))
        name_len = len(img_file.filename.split('.'))
        
        if not is_valid_file(img_file.filename,['png', 'jpg', 'jpeg', 'gif'],img_file.mimetype):
            print('if----')
            page_err = 'Please select valid file to upload.'
        elif name_len >= 3:
            print("elif")
            page_err = 'Please select valid file to upload.'
        elif len(img_file.read()) > current_app.config['MAX_UPLOAD_SIZE']:
            page_err = 'Please select file of maximum ' + bytes_to_unit(current_app.config['MAX_UPLOAD_SIZE']) + ' size.'
        else:
            img_file.seek(0)
            # blob_username = current_app.config['BLOB_USERNAME']
            # blob_key = current_app.config['BLOB_KEY']
            # container = current_app.config['CONTAINER']
            # block_blob_service =BlockBlobService(account_name=blob_username, account_key=blob_key)
            org_filename = secure_filename(img_file.filename)
            filename = str(uuid.uuid4()) + '_' + org_filename
            target_url = os.getcwd() + '/app/static/uploads/temp/'
            img_file.save(os.path.join(target_url, filename))
            source_url = target_url + filename
            # blob_props = block_blob_service.create_blob_from_path(
            #     container,
            #     filename,
            #     source_url,
            #     content_settings=ContentSettings(content_type='image/png')
            # )
            # return None, block_blob_service.make_blob_url(container, filename)
            return None,filename,source_url
        return page_err, None
  
    def upload_excel(self, img_file):
        page_err = None
        filename = ''
        mimetype=get_mimes(get_file_extension(img_file.filename))
        name_len = len(img_file.filename.split('.'))
        customer_schema = current_app.config.get('CUSTOMER_SCHEMA')
        df = pd.read_csv(img_file)
        column_names = list(df.columns)
        if not is_valid_file(img_file.filename, ['xls','xlsx', 'csv'], img_file.mimetype):
            print('if----')
            page_err = 'Please select valid file to upload.'
        elif column_names != customer_schema:
            print("1st elif")
            page_err = 'Column Mismatch'
        elif name_len >= 3:
            print("elif")
            page_err = 'Please select valid file to upload.'
        elif len(img_file.read()) > current_app.config['MAX_UPLOAD_SIZE']:
            page_err = 'Please select file of maximum ' + \
                bytes_to_unit(current_app.config['MAX_UPLOAD_SIZE']) + ' size.'
        else:
            img_file.seek(0)
            org_filename = secure_filename(img_file.filename)
            # filename = str(uuid.uuid4()) + '_' + org_filename
            # "CustReg" + DateTime.Now.ToString("ddMMyyyymmhhssfffff") + "_" + (FilesData?.Count - 1).ToString() + "_" + DateTime.UtcNow + "." + file?.FileName.Split('.')[1]
            filename = "CustReg" + \
                str(datetime.now().strftime("%m%d%Y%H%M%S")) + "_" + str(34) + \
                "_" + str(datetime.utcnow().strftime("%m%d%Y%H%M%S")) + org_filename
            target_url = os.getcwd() + '/app/static/uploads/temp/'
            img_file.save(os.path.join(target_url, filename))
            source_url = target_url + filename
            return None, filename, source_url
        return page_err, None

    def upload_activi_images(self, img_file):
        try:
            page_err = None
            # mimetype=get_mimes(get_file_extension(img_file.filename))
            name_len = len(img_file.filename.split('.'))

            if not is_valid_file(img_file.filename, ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'], img_file.mimetype):
                print('if----')
                page_err = 'Please select valid file to upload.'
            elif name_len >= 3:
                print("elif")
                page_err = 'Please select valid file to upload.'
            elif len(img_file.read()) > current_app.config['MAX_UPLOAD_SIZE']:
                page_err = 'Please select file of maximum ' + bytes_to_unit(
                    current_app.config['MAX_UPLOAD_SIZE']) + ' size.'
            else:
                img_file.seek(0)
                # blob_username = current_app.config['BLOB_USERNAME']
                # blob_key = current_app.config['BLOB_KEY']
                # container = current_app.config['CONTAINER']
                # block_blob_service =BlockBlobService(account_name=blob_username, account_key=blob_key)
                org_filename = secure_filename(img_file.filename)
                filename = str(uuid.uuid4()) + '_' + org_filename
                target_url = os.getcwd() + '/app/static/uploads/temp/'
                img_file.save(os.path.join(target_url, filename))
                source_url = target_url + filename

                mywidth = 762
                img_file = Image.open(source_url)
                wpercent = (mywidth / float(img_file.size[0]))
                hsize = int((float(img_file.size[1]) * float(wpercent)))
                img_file = img_file.resize((mywidth, hsize), PIL.Image.ANTIALIAS)
                # filename = str(uuid.uuid4()) + '_' + org_filename
                # target_url = os.getcwd() + '/app/static/uploads/temp/'
                img_file.save(os.path.join(target_url, filename))
                # blob_props = block_blob_service.create_blob_from_path(
                #     container,
                #     filename,
                #     source_url,
                #     content_settings=ContentSettings(content_type='image/png')
                # )
                # return None, block_blob_service.make_blob_url(container, filename)
                return None, filename, source_url
            return page_err, None, None
        except Exception as exp:
            print(exp,"exception from file upload to local")
            return None, None, None


    def upload_string(self, source_url, filename):
        page_err = None
        blob_username = current_app.config['BLOB_USERNAME']
        blob_key = current_app.config['BLOB_KEY']
        container = current_app.config['CONTAINER']
        block_blob_service = BlockBlobService(account_name=blob_username, account_key=blob_key)
        blob_props = block_blob_service.create_blob_from_path(
            container,
            filename,
            source_url,
            content_settings=ContentSettings(content_type='text/csv')
        )
        return None, block_blob_service.make_blob_url(container, filename)    

    def delete_image(self,blob_url):
        blob_username = current_app.config['BLOB_USERNAME']
        blob_key = current_app.config['BLOB_KEY']
        container = current_app.config['CONTAINER']
        block_blob_service = BlockBlobService(account_name=blob_username, account_key=blob_key)
        return block_blob_service.delete_blob(container,blob_url)        

    def delete_igp_image(self,blob_name):
        blob_name = blob_name.split('images/')[1]
        blob_username = current_app.config['BLOB_USERNAME']
        blob_key = current_app.config['BLOB_KEY']
        container = current_app.config['CONTAINER']
        block_blob_service =BlockBlobService(account_name=blob_username, account_key=blob_key)
        return block_blob_service.delete_blob(container,blob_name)

    def upload_igp_image(self, file_name, igp_image_url):
        try:
            blob_username = current_app.config['BLOB_USERNAME']
            blob_key = current_app.config['BLOB_KEY']
            container = current_app.config['CONTAINER']
            filename = file_name
            target_url = os.getcwd() + '/app/static/uploads/temp/'
            source_url, http_info = common_functions.download_file(igp_image_url, os.path.join(target_url, filename))
            print('source_url====', source_url, 'http_info+++')
            block_blob_service = BlockBlobService(account_name=blob_username, account_key=blob_key)
            blob_props = block_blob_service.create_blob_from_path(
                container,
                filename,
                source_url,
                content_settings=ContentSettings(content_type='image/png')
            )
            return None, block_blob_service.make_blob_url(container, filename)

        except Exception as e:
            print(e)
            return e, None