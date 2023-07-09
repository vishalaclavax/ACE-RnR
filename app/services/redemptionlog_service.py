from flask import current_app, g
import datetime
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from app.utils import random_str


def add_logs(request, api):
    partitionkey = str(random_str(8))+'_'+str(datetime.datetime.now().timestamp())
    data = {
        'partitionkey' : partitionkey,
        'rowkey' : g.current_user.get('id'),
        'mobile' : g.current_user.get('mobile'),
        'api' : api,
        'request' : str(request),
        'response' : "",
    }
    add_redemption_log(data)
    return partitionkey    
    
def payment_logs(response, request,browser):

    partitionkey = str(random_str(8))+'_'+str(datetime.datetime.now().timestamp())
    data = {
        'partitionkey' : partitionkey,
        'rowkey' : g.current_user.get('id'),
        'mobile' : g.current_user.get('mobile'),
        'request' : str(request),
        'response' : str(response),
        'browser':str(browser),
    }
    add_payment_log(data)
    return partitionkey

def update_logs(partitionkey, res, request, api):
    task = {
        'PartitionKey': partitionkey,
        'RowKey' : g.current_user.get('id'),
        'mobile' : g.current_user.get('mobile'),
        'api' : api,
        'request' : str(request),
        'response' : str(res),
    }
    update_redemption_log(task)

def updatepaymentlogs(partitionkey, res, request,browser):
    task = {
        'PartitionKey': partitionkey,
        'RowKey' : g.current_user.get('id'),
        'mobile' : g.current_user.get('mobile'),
        'request' : str(request),
        'response' : str(res),
        'browser':str(browser),
    }
    update_payment_log(task)    
    
    
def update_redemption_log(task):
    table_service = TableService(account_name=current_app.config['ACCOUNT_NAME'], account_key=current_app.config['ACCOUNT_KEY'])
    table_service.update_entity(current_app.config['ACCOUNT_TABLE_NAME'], task)

def update_payment_log(task):
    table_service = TableService(account_name=current_app.config['ACCOUNT_NAME'], account_key=current_app.config['ACCOUNT_KEY'])
    table_service.update_entity(current_app.config['ONLINE_PAYMENT_LOG_TABLE'], task)

def add_redemption_log(data):
    table_service = TableService(account_name=current_app.config['ACCOUNT_NAME'], account_key=current_app.config['ACCOUNT_KEY'])
    task = Entity()
    task.PartitionKey = data['partitionkey']
    task.RowKey = data['rowkey']
    task.mobile = data['mobile']
    task.api = data['api']
    task.request = data['request']
    task.response = data['response']
    table_service.insert_entity(current_app.config['ACCOUNT_TABLE_NAME'], task)

def add_payment_log(data):
    table_service = TableService(account_name=current_app.config['ACCOUNT_NAME'], account_key=current_app.config['ACCOUNT_KEY'])
    task = Entity()
    task.PartitionKey = data['partitionkey']
    task.RowKey = data['rowkey']
    task.mobile = data['mobile']
    task.request = data['request']
    task.response = data['response']
    task.browser = data['browser']
    table_service.insert_entity(current_app.config['ONLINE_PAYMENT_LOG_TABLE'], task)

