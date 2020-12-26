import boto3
import pandas as pd
import datetime


def addDrug(name, df):
    """[summary]

    Args:
        name (string): drug name as it appears in the dynamodb table 'RxTracker-DrugsTable'
        df (dataframe): dataframe that contains all the drug data.
    """
    table = boto3.resource('dynamodb').Table('RxTracker-DrugsTable')
    df["Week"] = df.apply(lambda row: row.strftime('%-y/%-m/%-d'), axis=1)
    df_as_dict = df.to_dict('records')
    final_dict = {'name': name, 'data': df_as_dict}
    print(final_dict)
    try:
        print("start dynamo put")
        table.put_item(Item=final_dict,
                       ConditionExpression='attribute_not_exists(name)')
    except Exception as e:
        print("dynamo put failed")
        print(e)
        pass
