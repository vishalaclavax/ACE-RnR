# from azure.cosmos.cosmos_client import CosmosClient
# from azure.cosmos.errors import CosmosError


# class CosmosConnect(object):
#     """CosmosDB connection class for flask"""
#     def __init__(self, app=None):
#         if app:
#             self.init_app(app)

#     def init_app(self, app):
#         self.host_uri = app.config.get('COSMOS_HOST_URI')
#         self.auth_master_key = app.config.get('COSMOS_AUTH_MASTER_KEY')
#         self.database_id = app.config.get('COSMOS_DATABASE_ID')
#         self.collection_id = app.config.get('COSMOS_COLLECTION_ID')
#         self.database_link = 'dbs/%s' % self.database_id
#         self.collection_link = '%s/colls/%s' % (self.database_link, self.collection_id)

#         self.client = CosmosClient(self.host_uri, {'masterKey': self.auth_master_key})
#         self.entity_field = 'discriminator'
#         self.error = None

#     def create_document_link(self, document_id):
#         return '%s/docs/%s' % (self.collection_link, document_id)

#     def query_items(self, query, options={'enableCrossPartitionQuery':True}, partition_key=None):
#         try:
#             self.error = None
#             return self.client.QueryItems(self.collection_link, query, options, partition_key)
#         except CosmosError as e:
#             self.error = e
#             return None

#     def create_item(self, document, options=None):
#         try:
#             self.error = None
#             return self.client.CreateItem(self.collection_link, document, options)
#         except CosmosError as e:
#             self.error = e
#             return None

#     def read_item(self, document_id, options=None):
#         try:
#             self.error = None
#             return self.client.ReadItem(self.create_document_link(document_id), options)
#         except CosmosError as e:
#             self.error = e
#             return None

#     def update_item(self, document, options=None):
#         try:
#             self.error = None
#             return self.client.ReplaceItem(document['_self'], document, options)
#         except CosmosError as e:
#             self.error = e
#             return None

#     def upsert_item(self, document, options=None):
#         try:
#             self.error = None
#             return self.client.UpsertItem(self.collection_link, document, options)
#         except CosmosError as e:
#             self.error = e
#             return None

#     def delete_item(self, document_id, options=None):
#         try:
#             self.error = None
#             return self.client.DeleteItem(self.create_document_link(document_id), options)
#         except CosmosError as e:
#             self.error = e
#             return None
