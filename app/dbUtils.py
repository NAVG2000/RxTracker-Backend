import boto3
import pandas as pd


def addDrug(name, df):
    """[summary]

    Args:
        name (string): drug name as it appears in the dynamodb table 'RxTracker-DrugsTable'
        df (dataframe): dataframe that contains all the drug data.
    """
    client = boto3.client('dynamodb')
    df_as_dict = df.to_dict('records')
    final_dict = {'name': name, 'data': df_as_dict}
    try:
        client.put_item(
            TableName='RxTracker-DrugsTable', Item=final_dict, ConditionExpression='attribute_not_exists(name)')
    except:
        pass
