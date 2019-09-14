import pandas as pd
import numpy as np
import os


class importerObj:
    def __init__(self, drug, source=None, masterDf=None):
        self.drug = drug
        self.rx_quantity = 120  # Eventually get info from a drug/ndc info file
        self.source = source
        self.masterDf = None
        self.rawFields = [
            "Week",
            "TRx_Quantity",
            "NRx_Quantity"
        ]
        self.updatedFields = [
            "Week",
            "Year",
            "Month",
            "TRx_Quantity",
            "NRx_Quantity",
            "Normalized_TRx",
            "Normalized_NRx",
            "Normalized_RRx",
            "TRx_Wow_Growth",
            "NRx_Wow_Growth",
            "RRx_Wow_Growth",
            "Week_Of_Year",
            "Four_Week_MA_TRx",
            "Four_Week_MA_NRx",
            "Four_Week_MA_RRx",
            "Eight_Week_MA_TRx",
            "Eight_Week_MA_NRx",
            "Eight_Week_MA_RRx",
            "Thirteen_Week_MA_TRx",
            "Thirteen_Week_MA_NRx",
            "Thirteen_Week_MA_RRx",
            "Four_Week_MA_TRx_WoW_Growth",
            "Four_Week_MA_NRx_WoW_Growth",
            "Four_Week_MA_RRx_WoW_Growth",
            "Eight_Week_MA_TRx_WoW_Growth",
            "Eight_Week_MA_NRx_WoW_Growth",
            "Eight_Week_MA_RRx_WoW_Growth",
            "Thirteen_Week_MA_TRx_WoW_Growth",
            "Thirteen_Week_MA_NRx_WoW_Growth",
            "Thirteen_Week_MA_RRx_WoW_Growth"
        ]
        if source is None:
            try:
                self.import_from_updated_weekly_data()
                self.source = "Updated (originally None)"
            except FileNotFoundError:
                self.import_from_raw_weekly_data()
                self.source = "Raw (originally None)"
        elif (source == "Updated"):
            self.import_from_updated_weekly_data()
        elif (source == "Raw"):
            self.import_from_raw_weekly_data()
        else:
            print("Provided source not valid.")
            self.source = "Non-valid source"

    def __repr__(self):
        return f"Drug Name: {self.drug}, Rx Quantity: {self.rx_quantity}, Source: {self.source}, and Fields: \n Updated Fields: {self.updatedFields} \n Raw Fields: {self.rawFields}"

    def save_to_csv(self, df, fileName, folderPath=None):
        """
        Saves the given Dataframe to the csv file called "Vascepa_Updated_Weekly_Data.csv" 

        PARAMETERS:
        df: the Dataframe to save to a csv file.
        fileName: desired name of newly created/ overwritten csv file 
        folderPath: the desired path to the location of where to save the csv file(default: None, the path of the python script file)
        """
        if folderPath is None:
            folderPath = os.getcwd()
        fullFileName = f"{self.drug}_{fileName}.csv"
        newPath = os.path.join(folderPath, fullFileName)
        df.to_csv(newPath, sep=',', index=None)

    def import_from_raw_weekly_data(self):
        """
        Imports raw bloomberg csv file of Rx Quantity and calcualtes the Normalixed Rx columns (TRx and NRx)
        """
        fields = self.rawFields
        df = pd.read_csv(f"drugData/{self.drug}_Weekly_Raw_Data.csv", parse_dates=[
                         'Week'], skipinitialspace=True, usecols=fields)
        df["Week"] = df["Week"].dt.date
        df["Year"] = df.apply(lambda row: row.Week.year, axis=1)
        df["Month"] = df.apply(lambda row: row.Week.month, axis=1)
        df = self.create_Normalized_Rx(df)
        df = self.create_Wow_Growth(df)
        df = self.enumerate_week(df)
        df = self.create_Rx_Moving_Averages(df)
        df = self.create_WoW_Moving_averages(df)
        self.save_to_csv(df, "Weekly_Updated_Data")
        # drop inf/-inf/nan values
        self.masterDf = df.replace([np.inf, -np.inf], np.nan).dropna()

    def import_from_updated_weekly_data(self):
        """
        Imports existing updated csv file of weekly data (contains "Normalized_TRx", "Normalized_NRx", "Normalized_RRX")
        """
        fields = self.updatedFields
        df = pd.read_csv(f"drugData/{self.drug}_Weekly_Updated_Data.csv", parse_dates=[
                         'Week'], skipinitialspace=True, usecols=fields)
        df["Week"] = df["Week"].dt.date
        # drop inf/-inf/nan values
        self.masterDf = df.replace([np.inf, -np.inf], np.nan).dropna()

    # Helper functions for import_from_raw_weekly_data().
    # Create most data/calculations from raw data
    def create_Normalized_Rx(self, df):
        """
        RETURNS: the modified dataframe

        PARAMETERS: 
        df: the Dataframe in which to add "Normalized_TRx", "Normalized_NRx", "Normalized_RRx"
        """
        # Cast to int to get rid of decimal places by truncating
        # Create Normalized_TRx from TRx_Quantitity
        df['Normalized_TRx'] = df.apply(lambda row: int(
            row.TRx_Quantity/self.rx_quantity), axis=1)
        df['Normalized_NRx'] = df.apply(lambda row: int(
            row.NRx_Quantity/self.rx_quantity), axis=1)
        df['Normalized_RRx'] = df.apply(lambda row: int(
            row.Normalized_TRx - row.Normalized_NRx), axis=1)
        return df

    def create_Wow_Growth(self, df):
        """
        RETURNS: the modified dataframe

        PARAMETERS: 
        df: the Dataframe in which to add "TRx_Wow_Growth", "NRx_Wow_Growth", "RRx_Wow_Growth"
        """
        df["TRx_Wow_Growth"] = round(
            (df["Normalized_TRx"] - df["Normalized_TRx"].shift(-1))/df["Normalized_TRx"].shift(-1), 4)
        df["NRx_Wow_Growth"] = round(
            (df["Normalized_NRx"] - df["Normalized_NRx"].shift(-1))/df["Normalized_NRx"].shift(-1), 4)
        df["RRx_Wow_Growth"] = round(
            (df["Normalized_RRx"] - df["Normalized_RRx"].shift(-1))/df["Normalized_RRx"].shift(-1), 4)
        return df

    def create_Rx_Moving_Averages(self, df):
        df["Four_Week_MA_TRx"] = round((df["Normalized_TRx"] + df["Normalized_TRx"].shift(-1) +
                                        df["Normalized_TRx"].shift(-2) + df["Normalized_TRx"].shift(-3))/4)
        df["Four_Week_MA_NRx"] = round((df["Normalized_NRx"] + df["Normalized_NRx"].shift(-1) +
                                        df["Normalized_NRx"].shift(-2) + df["Normalized_NRx"].shift(-3))/4)
        df["Four_Week_MA_RRx"] = round((df["Normalized_RRx"] + df["Normalized_RRx"].shift(-1) +
                                        df["Normalized_RRx"].shift(-2) + df["Normalized_RRx"].shift(-3))/4)

        df["Eight_Week_MA_TRx"] = round((df["Normalized_TRx"] + df["Normalized_TRx"].shift(-1) + df["Normalized_TRx"].shift(-2) + df["Normalized_TRx"].shift(-3) +
                                         df["Normalized_TRx"].shift(-4) + df["Normalized_TRx"].shift(-5) + df["Normalized_TRx"].shift(-6) + df["Normalized_TRx"].shift(-7))/8)
        df["Eight_Week_MA_NRx"] = round((df["Normalized_NRx"] + df["Normalized_NRx"].shift(-1) + df["Normalized_NRx"].shift(-2) + df["Normalized_NRx"].shift(-3) +
                                         df["Normalized_NRx"].shift(-4) + df["Normalized_NRx"].shift(-5) + df["Normalized_NRx"].shift(-6) + df["Normalized_NRx"].shift(-7))/8)
        df["Eight_Week_MA_RRx"] = round((df["Normalized_RRx"] + df["Normalized_RRx"].shift(-1) + df["Normalized_RRx"].shift(-2) + df["Normalized_RRx"].shift(-3) +
                                         df["Normalized_RRx"].shift(-4) + df["Normalized_RRx"].shift(-5) + df["Normalized_RRx"].shift(-6) + df["Normalized_RRx"].shift(-7))/8)

        df["Thirteen_Week_MA_TRx"] = round((df["Normalized_TRx"] + df["Normalized_TRx"].shift(-1) + df["Normalized_TRx"].shift(-2) + df["Normalized_TRx"].shift(-3) + df["Normalized_TRx"].shift(-4) + df["Normalized_TRx"].shift(-5) +
                                            df["Normalized_TRx"].shift(-6) + df["Normalized_TRx"].shift(-7) + df["Normalized_TRx"].shift(-8) + df["Normalized_TRx"].shift(-9) + df["Normalized_TRx"].shift(-10) + df["Normalized_TRx"].shift(-11) + df["Normalized_TRx"].shift(-12))/13)
        df["Thirteen_Week_MA_NRx"] = round((df["Normalized_NRx"] + df["Normalized_NRx"].shift(-1) + df["Normalized_NRx"].shift(-2) + df["Normalized_NRx"].shift(-3) + df["Normalized_NRx"].shift(-4) + df["Normalized_NRx"].shift(-5) +
                                            df["Normalized_NRx"].shift(-6) + df["Normalized_NRx"].shift(-7) + df["Normalized_NRx"].shift(-8) + df["Normalized_NRx"].shift(-9) + df["Normalized_NRx"].shift(-10) + df["Normalized_NRx"].shift(-11) + df["Normalized_NRx"].shift(-12))/13)
        df["Thirteen_Week_MA_RRx"] = round((df["Normalized_RRx"] + df["Normalized_RRx"].shift(-1) + df["Normalized_RRx"].shift(-2) + df["Normalized_RRx"].shift(-3) + df["Normalized_RRx"].shift(-4) + df["Normalized_RRx"].shift(-5) +
                                            df["Normalized_RRx"].shift(-6) + df["Normalized_RRx"].shift(-7) + df["Normalized_RRx"].shift(-8) + df["Normalized_RRx"].shift(-9) + df["Normalized_RRx"].shift(-10) + df["Normalized_RRx"].shift(-11) + df["Normalized_RRx"].shift(-12))/13)

        return df

    def create_WoW_Moving_averages(self, df):
        df["Four_Week_MA_TRx_WoW_Growth"] = round(
            (df["TRx_Wow_Growth"] + df["TRx_Wow_Growth"].shift(-1) + df["TRx_Wow_Growth"].shift(-2) + df["TRx_Wow_Growth"].shift(-3))/4, 4)
        df["Four_Week_MA_NRx_WoW_Growth"] = round(
            (df["NRx_Wow_Growth"] + df["NRx_Wow_Growth"].shift(-1) + df["NRx_Wow_Growth"].shift(-2) + df["NRx_Wow_Growth"].shift(-3))/4, 4)
        df["Four_Week_MA_RRx_WoW_Growth"] = round(
            (df["RRx_Wow_Growth"] + df["RRx_Wow_Growth"].shift(-1) + df["RRx_Wow_Growth"].shift(-2) + df["RRx_Wow_Growth"].shift(-3))/4, 4)

        df["Eight_Week_MA_TRx_WoW_Growth"] = round((df["TRx_Wow_Growth"] + df["TRx_Wow_Growth"].shift(-1) + df["TRx_Wow_Growth"].shift(-2) + df["TRx_Wow_Growth"].shift(
            -3) + df["TRx_Wow_Growth"].shift(-4) + df["TRx_Wow_Growth"].shift(-5) + df["TRx_Wow_Growth"].shift(-6) + df["TRx_Wow_Growth"].shift(-7))/8, 4)
        df["Eight_Week_MA_NRx_WoW_Growth"] = round((df["NRx_Wow_Growth"] + df["NRx_Wow_Growth"].shift(-1) + df["NRx_Wow_Growth"].shift(-2) + df["NRx_Wow_Growth"].shift(
            -3) + df["NRx_Wow_Growth"].shift(-4) + df["NRx_Wow_Growth"].shift(-5) + df["NRx_Wow_Growth"].shift(-6) + df["NRx_Wow_Growth"].shift(-7))/8, 4)
        df["Eight_Week_MA_RRx_WoW_Growth"] = round((df["RRx_Wow_Growth"] + df["RRx_Wow_Growth"].shift(-1) + df["RRx_Wow_Growth"].shift(-2) + df["RRx_Wow_Growth"].shift(
            -3) + df["RRx_Wow_Growth"].shift(-4) + df["RRx_Wow_Growth"].shift(-5) + df["RRx_Wow_Growth"].shift(-6) + df["RRx_Wow_Growth"].shift(-7))/8, 4)

        df["Thirteen_Week_MA_TRx_WoW_Growth"] = round((df["TRx_Wow_Growth"] + df["TRx_Wow_Growth"].shift(-1) + df["TRx_Wow_Growth"].shift(-2) + df["TRx_Wow_Growth"].shift(-3) + df["TRx_Wow_Growth"].shift(-4) + df["TRx_Wow_Growth"].shift(
            -5) + df["TRx_Wow_Growth"].shift(-6) + df["TRx_Wow_Growth"].shift(-7) + df["TRx_Wow_Growth"].shift(-8) + df["TRx_Wow_Growth"].shift(-9) + df["TRx_Wow_Growth"].shift(-10) + df["TRx_Wow_Growth"].shift(-11) + df["TRx_Wow_Growth"].shift(-12))/13, 4)
        df["Thirteen_Week_MA_NRx_WoW_Growth"] = round((df["NRx_Wow_Growth"] + df["NRx_Wow_Growth"].shift(-1) + df["NRx_Wow_Growth"].shift(-2) + df["NRx_Wow_Growth"].shift(-3) + df["NRx_Wow_Growth"].shift(-4) + df["NRx_Wow_Growth"].shift(
            -5) + df["NRx_Wow_Growth"].shift(-6) + df["NRx_Wow_Growth"].shift(-7) + df["NRx_Wow_Growth"].shift(-8) + df["NRx_Wow_Growth"].shift(-9) + df["NRx_Wow_Growth"].shift(-10) + df["NRx_Wow_Growth"].shift(-11) + df["NRx_Wow_Growth"].shift(-12))/13, 4)
        df["Thirteen_Week_MA_RRx_WoW_Growth"] = round((df["RRx_Wow_Growth"] + df["RRx_Wow_Growth"].shift(-1) + df["RRx_Wow_Growth"].shift(-2) + df["RRx_Wow_Growth"].shift(-3) + df["RRx_Wow_Growth"].shift(-4) + df["RRx_Wow_Growth"].shift(
            -5) + df["RRx_Wow_Growth"].shift(-6) + df["RRx_Wow_Growth"].shift(-7) + df["RRx_Wow_Growth"].shift(-8) + df["RRx_Wow_Growth"].shift(-9) + df["RRx_Wow_Growth"].shift(-10) + df["RRx_Wow_Growth"].shift(-11) + df["RRx_Wow_Growth"].shift(-12))/13, 4)

        return df

    def enumerate_week(self, df):
        '''
        RETURNS: the modified dataframe

        HELPER function for import_from_raw_weekly_data
        Creates 'Week_Of_Year' and enumerates each week of the year. Each year has 52 (or 53 weeks sometimes).
        Starts counting the first week when the week date (the week's end date)
        is January 4th or later (and before January 11th)

        PARAMETERS:
        df: the Dataframe in which to add the "Week_Of_Year" column
        '''
        list_of_weeks = []
        counter = 0
        df = df.iloc[::-1]  # reverse the order of the datarame
        for date in df['Week']:
            if (date.month == 1 and date.day >= 4 and date.day < 11):
                counter = 1
            else:
                counter = counter+1
            list_of_weeks = list_of_weeks + [counter]
        df['Week_Of_Year'] = list_of_weeks
        # reverse the order of the datarame back to original
        df = df.iloc[::-1]
        return df
