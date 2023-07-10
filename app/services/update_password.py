# from time import time
# from webbrowser import get
# from flask import current_app
# import uuid
# from app import cosmos
# from app.entities.forgot_password import ForgotPasswordEntity,ForgotPassword
# from app.services.api_client_service import APIClient


# ForgotPassword = ForgotPasswordEntity()
# ForgotPasswordModal = ForgotPassword()


# def read_link_by_id(id):
#     print(id)
#     doc = cosmos.query_items({
#     'query': "SELECT * FROM s WHERE s.{}=@discriminator and s.id=@id".format(cosmos.entity_field),
#     'parameters': [
#         {'name': '@discriminator', 'value': ForgotPassword.name},
#         {'name': '@id', 'value': id},
#     ]
#     })
#     doc = list(doc)
#     if len(doc) > 0:
#         doc =  doc[0]
#     else:
#         doc =  None
#     # print(doc)    
#     return doc


# def create_link(link_dict):
#     link_data = ForgotPassword(
#         id=str(uuid.uuid4()),
#         created_at=time(),
#         email=link_dict.get('email')
#     )
#     doc = cosmos.create_item(link_data)
#     return doc


# def update_link(doc_id, link_dict):
#     doc = read_link_by_id(doc_id)
#     if doc and ForgotPassword.check_entity_field(doc):
#         link_dict['updated_at'] = time()
#         doc.update(link_dict)
#         updated_doc = cosmos.update_item(doc)
#         return None if cosmos.error else updated_doc
#     else:
#         return None


