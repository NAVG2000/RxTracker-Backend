import boto3
import json
from decimal import Decimal
import pandas as pd
import datetime


def addDrug(name, df):
    """[summary]

    Args:
        name (string): drug name as it appears in the dynamodb table 'RxTracker-DrugsTable'
        df (dataframe): dataframe that contains all the drug data.
    """
    table = boto3.resource('dynamodb').Table('RxTracker-DrugsTable')
    df = df.copy(deep=True)
    df["Week"] = df.apply(lambda row: row.Week.strftime('%-Y/%-m/%-d'), axis=1)
    df_as_dict = df.to_dict('records')
    final_dict = json.loads(json.dumps(
        {'name': name, 'data': df_as_dict}), parse_float=Decimal)
    print("before put in db", final_dict)
    try:
        print("start dynamo put")
        table.put_item(Item=final_dict,
                       ConditionExpression='attribute_not_exists(#n)',
                       ExpressionAttributeNames={'#n': 'name'})
    except Exception as e:
        print("dynamo put failed")
        print(e)


def getDrug(name):
    """[summary]

    Args:
        name (string): get the drug from dynamoDB
    """
    table = boto3.resource('dynamodb').Table('RxTracker-DrugsTable')
    try:
        response = table.get_item(Key={'name': name})
        print(response)
    except Exception as e:
        print("dynamo get failed")
        print(e)
