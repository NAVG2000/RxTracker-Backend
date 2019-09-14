from importerClass import importerObj
from graphClass import graphObj
from modelClass import modelObj

import pandas as pd
import numpy as np
import datetime


class drugObj:
    #maybe use function dictionary to simplify code based on user input
    def __init__(self,drug,weeks,source = None, predict = False):
        '''
        PARAMETERS:
        drug: name of the drug to be used by this drugObj. Must be string with no spaces. (string)
        weeks: number of weeks to dispaly for all graphs in this drugObj. 
            The graph displays the 0th entry to the specified number of weeks. (int)
        masterDf: Df to be used for most calculations/charts. (dataframe) (optional)
        '''
        self.drug = drug.capitalize()
        self.setWeeks(weeks)
        source = source if source is None else source.capitalize()
        self.predict = predict
        self.importerObj = importerObj(self.drug,source)
        self.masterDf = self.importerObj.masterDf
        self.weeksToTrainOn = round(len(self.masterDf) * 0.75)
        self.rx_quantity = self.importerObj.rx_quantity
        self.rawFields = self.importerObj.rawFields
        self.updatedFields = self.importerObj.updatedFields
        self.availableGraphs =  self.generateAvailableGraphsDict()
        
        #generation of charts (eventaully make functions that generates predecided charts (such as a 'createReport' function))
        #self.generateAllCharts(self.predict)
        
    def __repr__(self):
        return f"Drug Name: {self.drug}, Rx Quantity: {self.rx_quantity}, Fields: \n Updated Fields: {self.updatedFields} \n Raw Fields: {self.rawFields} \n ImporterObj: {self.importerObj} \n MasterDf: \n {self.masterDf}"
    
    def generateAvailableGraphsDict(self):
        self.normalizedTRxAndAllMAsChart = None
        self.normalizedTRxChart = None
        self.fourWeekMATRxChart = None
        self.eightWeekMATRxChart = None
        self.thirteenWeekMATRxChart = None
        self.normalizedTRxLogChart = None
        self.normalizedNRxChart = None
        self.normalizedNRxChart = None
        self.fourWeekMANRxChart = None
        self.eightWeekMANRxChart = None
        self.thirteenWeekMANRxChart = None
        self.normalizedNRxLogChart = None
        self.normalizedRRxChart = None
        self.fourWeekMARRxChart = None
        self.eightWeekMARRxChart = None
        self.thirteenWeekMARRxChart = None
        self.normalizedRRxLogChart = None
        self.trxWowGrowthChart = None
        self.fourWeekMATRxWoWGrowthChart = None
        self.eightWeekMATRxWoWGrowthChart = None
        self.thirteenWeekMATRxWoWGrowthChart = None
        self.nrxWowGrowthChart = None
        self.fourWeekMANRxWoWGrowthChart = None
        self.eightWeekMANRxWoWGrowthChart = None
        self.thirteenWeekMANRxWoWGrowthChart = None
        self.rrxWowGrowthChart = None
        self.fourWeekMARRxWoWGrowthChart = None
        self.eightWeekMARRxWoWGrowthChart = None
        self.thirteenWeekMARRxWoWGrowthChart = None
        self.normalizedAllRxChart = None

        availableGraphs = {
            "graph_normalizedTRxAndAllMAs": {'function': self.graph_normalizedTRxAndAllMAs, 'figName': self.normalizedTRxAndAllMAsChart},
            "graph_normalizedTRx": {'function': self.graph_normalizedTRx, 'figName': self.normalizedTRxChart},
            "graph_fourWeekMATRx": {'function': self.graph_fourWeekMATRx, 'figName': self.fourWeekMATRxChart},
            "graph_eightWeekMATRx": {'function': self.graph_eightWeekMATRx, 'figName': self.eightWeekMATRxChart},
            "graph_thirteenWeekMATRx": {'function': self.graph_thirteenWeekMATRx, 'figName': self.thirteenWeekMATRxChart},
            "graph_normalizedTRxLog": {'function': self.graph_normalizedTRxLog, 'figName': self.normalizedTRxLogChart},
            "graph_normalizedNRx": {'function': self.graph_normalizedNRx, 'figName': self.normalizedNRxChart},
            "graph_fourWeekMANRx": {'function': self.graph_fourWeekMANRx, 'figName': self.fourWeekMANRxChart},
            "graph_eightWeekMANRx": {'function': self.graph_eightWeekMANRx, 'figName': self.eightWeekMANRxChart},
            "graph_thirteenWeekMANRx": {'function': self.graph_thirteenWeekMANRx, 'figName': self.thirteenWeekMANRxChart},
            "graph_normalizedNRxLog": {'function': self.graph_normalizedNRxLog, 'figName': self.normalizedNRxLogChart},
            "graph_normalizedRRx": {'function': self.graph_normalizedRRx, 'figName': self.normalizedRRxChart},
            "graph_fourWeekMARRx": {'function': self.graph_fourWeekMARRx, 'figName': self.fourWeekMARRxChart},
            "graph_eightWeekMARRx": {'function': self.graph_eightWeekMARRx, 'figName': self.eightWeekMARRxChart},
            "graph_thirteenWeekMARRx": {'function': self.graph_thirteenWeekMARRx, 'figName': self.thirteenWeekMARRxChart},
            "graph_normalizedRRxLog": {'function': self.graph_normalizedRRxLog, 'figName': self.normalizedRRxLogChart},
            "graph_trxWowGrowth": {'function': self.graph_trxWowGrowth, 'figName': self.trxWowGrowthChart},
            "graph_fourWeekMATRxWoWGrowth": {'function': self.graph_fourWeekMATRxWoWGrowth, 'figName': self.fourWeekMATRxWoWGrowthChart},
            "graph_eightWeekMATRxWoWGrowth": {'function': self.graph_eightWeekMATRxWoWGrowth, 'figName': self.eightWeekMATRxWoWGrowthChart},
            "graph_thirteenWeekMATRxWoWGrowth": {'function': self.graph_thirteenWeekMATRxWoWGrowth, 'figName': self.thirteenWeekMATRxWoWGrowthChart},
            "graph_nrxWowGrowth": {'function': self.graph_nrxWowGrowth, 'figName': self.nrxWowGrowthChart},
            "graph_fourWeekMANRxWoWGrowth": {'function': self.graph_fourWeekMANRxWoWGrowth, 'figName': self.fourWeekMANRxWoWGrowthChart},
            "graph_eightWeekMANRxWoWGrowth": {'function': self.graph_eightWeekMANRxWoWGrowth, 'figName': self.eightWeekMANRxWoWGrowthChart},
            "graph_thirteenWeekMANRxWoWGrowth": {'function': self.graph_thirteenWeekMANRxWoWGrowth, 'figName': self.thirteenWeekMANRxWoWGrowthChart},
            "graph_rrxWowGrowth": {'function': self.graph_rrxWowGrowth, 'figName': self.rrxWowGrowthChart},
            "graph_fourWeekMARRxWoWGrowth": {'function': self.graph_fourWeekMARRxWoWGrowth, 'figName': self.fourWeekMARRxWoWGrowthChart},
            "graph_eightWeekMARRxWoWGrowth": {'function': self.graph_eightWeekMARRxWoWGrowth, 'figName': self.eightWeekMARRxWoWGrowthChart},
            "graph_thirteenWeekMARRxWoWGrowth": {'function': self.graph_thirteenWeekMARRxWoWGrowth, 'figName': self.thirteenWeekMARRxWoWGrowthChart},
            "graphNormalizedAllRx": {'function': self.graphNormalizedAllRx, 'figName': self.normalizedAllRxChart}
        }
        return availableGraphs

    def generateAllCharts(self):
        self.graph_normalizedTRxAndAllMAs(self.weeks, self.predict)
        self.graph_normalizedTRx(self.weeks, self.predict)
        self.graph_fourWeekMATRx(self.weeks, self.predict)
        self.graph_eightWeekMATRx(self.weeks, self.predict)
        self.graph_thirteenWeekMATRx(self.weeks, self.predict)
        self.graph_normalizedTRxLog(self.weeks, self.predict)
        
        self.graph_normalizedNRx(self.weeks, self.predict)
        self.graph_fourWeekMANRx(self.weeks, self.predict)
        self.graph_eightWeekMANRx(self.weeks, self.predict)
        self.graph_thirteenWeekMANRx(self.weeks, self.predict)
        self.graph_normalizedNRxLog(self.weeks, self.predict)
        
        self.graph_normalizedRRx(self.weeks, self.predict)
        self.graph_fourWeekMARRx(self.weeks, self.predict)
        self.graph_eightWeekMARRx(self.weeks, self.predict)
        self.graph_thirteenWeekMARRx(self.weeks, self.predict)
        self.graph_normalizedRRxLog(self.weeks, self.predict)
        
        self.graph_trxWowGrowth(self.weeks, self.predict)
        self.graph_fourWeekMATRxWoWGrowth(self.weeks, self.predict)
        self.graph_eightWeekMATRxWoWGrowth(self.weeks, self.predict)
        self.graph_thirteenWeekMATRxWoWGrowth(self.weeks, self.predict)
        
        self.graph_nrxWowGrowth(self.weeks, self.predict)
        self.graph_fourWeekMANRxWoWGrowth(self.weeks, self.predict)
        self.graph_eightWeekMANRxWoWGrowth(self.weeks, self.predict)
        self.graph_thirteenWeekMANRxWoWGrowth(self.weeks, self.predict)
        
        self.graph_rrxWowGrowth(self.weeks, self.predict)
        self.graph_fourWeekMARRxWoWGrowth(self.weeks, self.predict)
        self.graph_eightWeekMARRxWoWGrowth(self.weeks, self.predict)
        self.graph_thirteenWeekMARRxWoWGrowth(self.weeks, self.predict)
        
        self.graphNormalizedAllRx(self.weeks, self.predict)
    
    def setMasterDf(self,masterDf):
        self.masterDf = masterDf.replace([np.inf, -np.inf], np.nan).dropna() # drop inf/-inf/nan values
        
    def setWeeks(self,weeks):
        self.weeks = weeks

    def add_new_data_weekly(self, month, day, year, trx_quantity, nrx_quantity):
        """
        Adds a new row to the given dataframe (must have Normalized TRx/NRx column) and creates a datetime object of the week.
        Saves the updated dataframe to the csv file called "Vascepa_Updated_Weekly_Data.csv" 
        New Data must be exactly one week after the last entry to the df.

        PARAMETERS: 
        month: new script data's month. Used to create the new datetime object. (int)
        day: new script data's day. Used to create the new datetime object. (int)
        year: new script data's year. Used to create the new datetime object. (int)
        trx_quantity: new script data's TRx Quantity. (int)
        nrx_quantity: new script data's NRx Quantity. (int)

        rx_quantity: prescription count per bottle/refill. Denominator to determine normalized rxs. (int, default=120) (optional)
        normalized_trx: new script data's Normalized TRx. (trx_quantity/rx_quantity). (int) (optional)
        normalized_nrx: new script data's Normalized NRx. (nrx_quantity/rx_quantity). (int) (optional)
        normalized_rrx: new script data's Normalized Refil Rx. (normalized_trx - normalized_nrx) (int) (optional)
        trx_wow_growth: new script data's week over week growth of TRx. (float) (optional)
        nrx_wow_growth: new script data's week over week growth of NRx. (float) (optional)
        rrx_wow_growth: new script data's week over week growth of RRx. (float) (optional)
        week_of_year: new script data's enumeration of the week. (int) (optional)

        """
        week = datetime.datetime(year, month, day)
        week = week.date()
        df = self.masterDf
        if df["Week"][0] == week:
            print("That week is already in the data set")
        else:
            year = week.year
            month = week.month
            normalized_trx = (int) (trx_quantity/self.rx_quantity)
            normalized_nrx = (int) (nrx_quantity/self.rx_quantity)
            normalized_rrx = normalized_trx - normalized_nrx
            trx_wow_growth = (normalized_trx - df["Normalized_TRx"][0])/df["Normalized_TRx"][0]
            nrx_wow_growth = (normalized_nrx - df["Normalized_NRx"][0])/df["Normalized_NRx"][0]
            rrx_wow_growth = (normalized_rrx - df["Normalized_RRx"][0])/df["Normalized_RRx"][0]
            week_of_year = 1 if (week.month == 1 and week.day>=4 and week.day<11) else df['Week_Of_Year'][0]+1 # date should be changed to week I think
            four_week_ma_trx = round((normalized_trx + df["Normalized_TRx"][0] + df["Normalized_TRx"][1] + df["Normalized_TRx"][2])/4)
            four_week_ma_nrx = round((normalized_nrx + df["Normalized_NRx"][0] + df["Normalized_NRx"][1] + df["Normalized_NRx"][2])/4)
            four_week_ma_rrx = round((normalized_rrx + df["Normalized_RRx"][0] + df["Normalized_RRx"][1] + df["Normalized_RRx"][2])/4)
            eight_week_ma_trx = round((normalized_trx + df["Normalized_TRx"][0] + df["Normalized_TRx"][1] + df["Normalized_TRx"][2] + df["Normalized_TRx"][3]+ df["Normalized_TRx"][4] + df["Normalized_TRx"][5] + df["Normalized_TRx"][6])/8)
            eight_week_ma_nrx = round((normalized_nrx + df["Normalized_NRx"][0] + df["Normalized_NRx"][1] + df["Normalized_NRx"][2] + df["Normalized_NRx"][3]+ df["Normalized_NRx"][4] + df["Normalized_NRx"][5] + df["Normalized_NRx"][6])/8)
            eight_week_ma_rrx = round((normalized_rrx + df["Normalized_RRx"][0] + df["Normalized_RRx"][1] + df["Normalized_RRx"][2] + df["Normalized_RRx"][3]+ df["Normalized_RRx"][4] + df["Normalized_RRx"][5] + df["Normalized_RRx"][6])/8)
            thirteen_week_ma_trx = round((normalized_trx + df["Normalized_TRx"][0] + df["Normalized_TRx"][1] + df["Normalized_TRx"][2] + df["Normalized_TRx"][3]+ df["Normalized_TRx"][4] + df["Normalized_TRx"][5] + df["Normalized_TRx"][6] + df["Normalized_TRx"][7] + df["Normalized_TRx"][8] + df["Normalized_TRx"][9] + df["Normalized_TRx"][10] + df["Normalized_TRx"][11])/13)
            thirteen_week_ma_nrx = round((normalized_nrx + df["Normalized_NRx"][0] + df["Normalized_NRx"][1] + df["Normalized_NRx"][2] + df["Normalized_NRx"][3]+ df["Normalized_NRx"][4] + df["Normalized_NRx"][5] + df["Normalized_NRx"][6] + df["Normalized_NRx"][7] + df["Normalized_NRx"][8] + df["Normalized_NRx"][9] + df["Normalized_NRx"][10] + df["Normalized_NRx"][11])/13)
            thirteen_week_ma_rrx = round((normalized_rrx + df["Normalized_RRx"][0] + df["Normalized_RRx"][1] + df["Normalized_RRx"][2] + df["Normalized_RRx"][3]+ df["Normalized_RRx"][4] + df["Normalized_RRx"][5] + df["Normalized_RRx"][6] + df["Normalized_RRx"][7] + df["Normalized_RRx"][8] + df["Normalized_RRx"][9] + df["Normalized_RRx"][10] + df["Normalized_RRx"][11])/13)
            four_week_ma_trx_wow_growth = round((trx_wow_growth + df["TRx_Wow_Growth"][0] + df["TRx_Wow_Growth"][1] + df["TRx_Wow_Growth"][2])/4,4)
            four_week_ma_nrx_wow_growth = round((nrx_wow_growth + df["NRx_Wow_Growth"][0] + df["NRx_Wow_Growth"][1] + df["NRx_Wow_Growth"][2])/4,4)
            four_week_ma_rrx_wow_growth = round((rrx_wow_growth + df["RRx_Wow_Growth"][0] + df["RRx_Wow_Growth"][1] + df["RRx_Wow_Growth"][2])/4,4)
            eight_week_ma_trx_wow_growth = round((trx_wow_growth + df["TRx_Wow_Growth"][0] + df["TRx_Wow_Growth"][1] + df["TRx_Wow_Growth"][2] + df["TRx_Wow_Growth"][3] + df["TRx_Wow_Growth"][4] + df["TRx_Wow_Growth"][5] + df["TRx_Wow_Growth"][6])/8,4)
            eight_week_ma_nrx_wow_growth = round((nrx_wow_growth + df["NRx_Wow_Growth"][0] + df["NRx_Wow_Growth"][1] + df["NRx_Wow_Growth"][2] + df["NRx_Wow_Growth"][3] + df["NRx_Wow_Growth"][4] + df["NRx_Wow_Growth"][5] + df["NRx_Wow_Growth"][6])/8,4)
            eight_week_ma_rrx_wow_growth = round((rrx_wow_growth + df["RRx_Wow_Growth"][0] + df["RRx_Wow_Growth"][1] + df["RRx_Wow_Growth"][2] + df["RRx_Wow_Growth"][3] + df["RRx_Wow_Growth"][4] + df["RRx_Wow_Growth"][5] + df["RRx_Wow_Growth"][6])/8,4)
            thirteen_week_ma_trx_wow_growth = round((trx_wow_growth + df["TRx_Wow_Growth"][0] + df["TRx_Wow_Growth"][1] + df["TRx_Wow_Growth"][2] + df["TRx_Wow_Growth"][3] + df["TRx_Wow_Growth"][4] + df["TRx_Wow_Growth"][5] + df["TRx_Wow_Growth"][6] + df["TRx_Wow_Growth"][7] + df["TRx_Wow_Growth"][8] + df["TRx_Wow_Growth"][9] + df["TRx_Wow_Growth"][10] + df["TRx_Wow_Growth"][11])/13,4)
            thirteen_week_ma_nrx_wow_growth = round((nrx_wow_growth + df["NRx_Wow_Growth"][0] + df["NRx_Wow_Growth"][1] + df["NRx_Wow_Growth"][2] + df["NRx_Wow_Growth"][3] + df["NRx_Wow_Growth"][4] + df["NRx_Wow_Growth"][5] + df["NRx_Wow_Growth"][6] + df["NRx_Wow_Growth"][7] + df["NRx_Wow_Growth"][8] + df["NRx_Wow_Growth"][9] + df["NRx_Wow_Growth"][10] + df["NRx_Wow_Growth"][11])/13,4)
            thirteen_week_ma_rrx_wow_growth = round((rrx_wow_growth + df["RRx_Wow_Growth"][0] + df["RRx_Wow_Growth"][1] + df["RRx_Wow_Growth"][2] + df["RRx_Wow_Growth"][3] + df["RRx_Wow_Growth"][4] + df["RRx_Wow_Growth"][5] + df["RRx_Wow_Growth"][6] + df["RRx_Wow_Growth"][7] + df["RRx_Wow_Growth"][8] + df["RRx_Wow_Growth"][9] + df["RRx_Wow_Growth"][10] + df["RRx_Wow_Growth"][11])/13,4)
                      
            df.loc[-1] = [week,trx_quantity,nrx_quantity,
                          year,month,
                          normalized_trx,normalized_nrx,normalized_rrx,
                          trx_wow_growth,nrx_wow_growth,rrx_wow_growth,
                          week_of_year,
                          four_week_ma_trx,four_week_ma_nrx,four_week_ma_rrx,
                          eight_week_ma_trx,eight_week_ma_nrx,eight_week_ma_rrx,
                          thirteen_week_ma_trx,thirteen_week_ma_nrx,thirteen_week_ma_rrx,
                          four_week_ma_trx_wow_growth,four_week_ma_nrx_wow_growth,four_week_ma_rrx_wow_growth,
                          eight_week_ma_trx_wow_growth,eight_week_ma_nrx_wow_growth,eight_week_ma_rrx_wow_growth,
                          thirteen_week_ma_trx_wow_growth,thirteen_week_ma_nrx_wow_growth,thirteen_week_ma_rrx_wow_growth]  # adding a row
            df.index = df.index + 1  # shifting index
            df.sort_index(inplace=True)
            self.setMasterDf(df)
            self.importerObj.save_to_csv(df,"Weekly_Updated_Data")
            raw_df = df[['Week','TRx_Quantity', 'NRx_Quantity']].copy()
            self.importerObj.save_to_csv(raw_df,"Wekly_Raw_Data")
    
    def graph_normalizedTRx(self, weeks, predict):
        """
        UPDATE so that ending and starting weeks can be chosen 
        UPDATE so that it returns the plot (use "ax" from matplotlib) so that it can be manipulated outside of the function

        Creats and shows a graph of "Normalized_TRx" and the specified number of weeks from the given dataframe

        PARAMETERS: 
        weeks: number of weeks to dispaly. The graph displays the 0th entry to the specified number of weeks. (int)
        """
        self.normalizedTRxChart = graphObj(self.drug, self.masterDf, weeks, "Week" ,["Normalized_TRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Normalized_TRx",52).predictionDf
            self.normalizedTRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Normalized_TRx"]])
 
    def graph_normalizedNRx(self, weeks, predict):
        """
        UPDATE so that ending and starting weeks can be chosen 
        UPDATE so that it returns the plot (use "ax" from matplotlib) so that it can be manipulated outside of the function

        Creats and shows a graph of "Normalized_NRx" and the specified number of weeks from the given dataframe

        PARAMETERS: 
        weeks: number of weeks to dispaly. The graph displays the 0th entry to the specified number of weeks. (int)
        """
        self.normalizedNRxChart = graphObj(self.drug,self.masterDf, weeks,"Week",["Normalized_NRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Normalized_NRx",52).predictionDf
            self.normalizedNRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Normalized_NRx"]])

    def graph_normalizedRRx(self, weeks, predict):
        """
        UPDATE so that ending and starting weeks can be chosen 
        UPDATE so that it returns the plot (use "ax" from matplotlib) so that it can be manipulated outside of the function

        Creats and shows a graph of "Normalized_RRx" and the specified number of weeks from the given dataframe

        PARAMETERS: 
        weeks: number of weeks to dispaly. The graph displays the 0th entry to the specified number of weeks. (int)
        """
        self.normalizedRRxChart = graphObj(self.drug,self.masterDf, weeks,"Week",["Normalized_RRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Normalized_RRx",52).predictionDf
            self.normalizedRRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Normalized_RRx"]])

    def graph_trxWowGrowth(self, weeks, predict):
        """
        UPDATE so that ending and starting weeks can be chosen 
        UPDATE so that it returns the plot (use "ax" from matplotlib) so that it can be manipulated outside of the function

        Creats and shows a graph of "TRx_Wow_Growth" and the specified number of weeks from the given dataframe.

        PARAMETERS: 
        weeks: number of weeks to dispaly. The graph displays the 0th entry to the specified number of weeks. (int)
        df: the dataframe from which to use the data to be displayed in graph. Must have "TRx_Wow_Growth" column. (dataframe)
        """
        self.trxWowGrowthChart = graphObj(self.drug,self.masterDf, weeks,"Week",["TRx_Wow_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"TRx_Wow_Growth",52).predictionDf
            self.trxWowGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["TRx_Wow_Growth"]])
        
    def graph_nrxWowGrowth(self, weeks, predict):
        """
        UPDATE so that ending and starting weeks can be chosen 
        UPDATE so that it returns the plot (use "ax" from matplotlib) so that it can be manipulated outside of the function

        Creats and shows a graph of "NRx_Wow_Growth" and the specified number of weeks from the given dataframe.

        PARAMETERS: 
        weeks: number of weeks to dispaly. The graph displays the 0th entry to the specified number of weeks. (int)
        df: the dataframe from which to use the data to be displayed in graph. Must have "NRx_Wow_Growth" column. (dataframe)
        """
        self.nrxWowGrowthChart = graphObj(self.drug,self.masterDf, weeks,"Week",["NRx_Wow_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"NRx_Wow_Growth",52).predictionDf
            self.nrxWowGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["NRx_Wow_Growth"]])
        
    def graph_rrxWowGrowth(self, weeks, predict):
        """
        UPDATE so that ending and starting weeks can be chosen 
        UPDATE so that it returns the plot (use "ax" from matplotlib) so that it can be manipulated outside of the function

        Creats and shows a graph of "RRx_Wow_Growth" and the specified number of weeks from the given dataframe.

        PARAMETERS: 
        weeks: number of weeks to dispaly. The graph displays the 0th entry to the specified number of weeks. (int)
        df: the dataframe from which to use the data to be displayed in graph. Must have "RRx_Wow_Growth" column. (dataframe)
        """
        self.rrxWowGrowthChart = graphObj(self.drug,self.masterDf, weeks,"Week",["RRx_Wow_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"RRx_Wow_Growth",52).predictionDf
            self.rrxWowGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["RRx_Wow_Growth"]])
        
    def graphNormalizedAllRx(self,weeks, predict):
        self.normalizedAllRxChart = graphObj(self.drug,self.masterDf, weeks,"Week",["Normalized_TRx","Normalized_NRx","Normalized_RRx"],["scatter","scatter","scatter"], yLabel="Vascepa All Prescriptions")
        #implement prediction
        
    def graph_normalizedTRxLog(self,weeks, predict):
        self.normalizedTRxLogChart = graphObj(self.drug, self.masterDf, weeks,"Week",["Normalized_TRx"],["logy_plot"], yLabel="Normalized_TRx Log Scale")
        #might have wierd predict behavior 
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Normalized_TRx",52).predictionDf
            self.normalizedTRxLogChart.generateChart(["logy_plot"],predictionDf["Week"],[predictionDf["Normalized_TRx"]])
        
    def graph_normalizedNRxLog(self,weeks, predict):
        self.normalizedNRxLogChart = graphObj(self.drug, self.masterDf, weeks,"Week",["Normalized_NRx"],["logy_plot"], yLabel="Normalized_TRx Log Scale")
        #might have wierd predict behavior 
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Normalized_NRx",52).predictionDf
            self.normalizedNRxLogChart.generateChart(["logy_plot"],predictionDf["Week"],[predictionDf["Normalized_NRx"]])
        
    def graph_normalizedRRxLog(self,weeks, predict):
        self.normalizedRRxLogChart = graphObj(self.drug, self.masterDf, weeks,"Week",["Normalized_RRx"],["logy_plot"], yLabel="Normalized_TRx Log Scale")
        #might have wierd predict behavior 
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Normalized_RRx",52).predictionDf
            self.normalizedRRxLogChart.generateChart(["logy_plot"],predictionDf["Week"],[predictionDf["Normalized_RRx"]])
    
    def graph_fourWeekMATRx(self,weeks, predict):
        self.fourWeekMATRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Four_Week_MA_TRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Four_Week_MA_TRx",52).predictionDf
            self.fourWeekMATRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Four_Week_MA_TRx"]])
        
    def graph_fourWeekMANRx(self,weeks, predict):
        self.fourWeekMANRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Four_Week_MA_NRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Four_Week_MA_NRx",52).predictionDf
            self.fourWeekMANRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Four_Week_MA_NRx"]])
        
    def graph_fourWeekMARRx(self,weeks, predict):
        self.fourWeekMARRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Four_Week_MA_RRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Four_Week_MA_RRx",52).predictionDf
            self.fourWeekMARRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Four_Week_MA_RRx"]])
        
    def graph_eightWeekMATRx(self,weeks, predict):
        self.eightWeekMATRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Eight_Week_MA_TRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Eight_Week_MA_TRx",52).predictionDf
            self.eightWeekMATRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Eight_Week_MA_TRx"]])
        
    def graph_eightWeekMANRx(self,weeks, predict):
        self.eightWeekMANRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Eight_Week_MA_NRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Eight_Week_MA_NRx",52).predictionDf
            self.eightWeekMANRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Eight_Week_MA_NRx"]])
        
    def graph_eightWeekMARRx(self,weeks, predict):
        self.eightWeekMARRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Eight_Week_MA_RRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Eight_Week_MA_RRx",52).predictionDf
            self.eightWeekMARRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Eight_Week_MA_RRx"]])
        
    def graph_thirteenWeekMATRx(self,weeks, predict):
        self.thirteenWeekMATRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Thirteen_Week_MA_TRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Thirteen_Week_MA_TRx",52).predictionDf
            self.thirteenWeekMATRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Thirteen_Week_MA_TRx"]])
        
    def graph_thirteenWeekMANRx(self,weeks, predict):
        self.thirteenWeekMANRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Thirteen_Week_MA_NRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Thirteen_Week_MA_NRx",52).predictionDf
            self.thirteenWeekMANRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Thirteen_Week_MA_NRx"]])
        
    def graph_thirteenWeekMARRx(self,weeks, predict):
        self.thirteenWeekMARRxChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Thirteen_Week_MA_RRx"],["scatter"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Thirteen_Week_MA_RRx",52).predictionDf
            self.thirteenWeekMARRxChart.generateChart(["scatter"],predictionDf["Week"],[predictionDf["Thirteen_Week_MA_RRx"]])
        
    def graph_normalizedTRxAndAllMAs(self,weeks, predict):
        self.normalizedTRxAndAllMAsChart = graphObj(self.drug,self.masterDf, weeks,"Week",["Normalized_TRx","Four_Week_MA_TRx","Eight_Week_MA_TRx","Thirteen_Week_MA_TRx"],["scatter","plot","plot","plot"], yLabel="Vascepa TRx and All Moving Averages")
        #implement prediction
    
    #new:
    def graph_fourWeekMATRxWoWGrowth(self,weeks, predict):
        self.fourWeekMATRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Four_Week_MA_TRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Four_Week_MA_TRx_WoW_Growth",52).predictionDf
            self.fourWeekMATRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Four_Week_MA_TRx_WoW_Growth"]])
    
    def graph_fourWeekMANRxWoWGrowth(self,weeks, predict):
        self.fourWeekMANRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Four_Week_MA_NRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Four_Week_MA_NRx_WoW_Growth",52).predictionDf
            self.fourWeekMANRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Four_Week_MA_NRx_WoW_Growth"]])
    
    def graph_fourWeekMARRxWoWGrowth(self,weeks, predict):
        self.fourWeekMARRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Four_Week_MA_RRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Four_Week_MA_RRx_WoW_Growth",52).predictionDf
            self.fourWeekMARRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Four_Week_MA_RRx_WoW_Growth"]])
    
    def graph_eightWeekMATRxWoWGrowth(self,weeks, predict):
        self.eightWeekMATRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Eight_Week_MA_TRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Eight_Week_MA_TRx_WoW_Growth",52).predictionDf
            self.eightWeekMATRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Eight_Week_MA_TRx_WoW_Growth"]])
        
    def graph_eightWeekMANRxWoWGrowth(self,weeks, predict):
        self.eightWeekMANRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Eight_Week_MA_NRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Eight_Week_MA_NRx_WoW_Growth",52).predictionDf
            self.eightWeekMANRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Eight_Week_MA_NRx_WoW_Growth"]])
        
    def graph_eightWeekMARRxWoWGrowth(self,weeks, predict):
        self.eightWeekMARRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Eight_Week_MA_RRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Eight_Week_MA_RRx_WoW_Growth",52).predictionDf
            self.eightWeekMARRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Eight_Week_MA_RRx_WoW_Growth"]])
        
    def graph_thirteenWeekMATRxWoWGrowth(self,weeks, predict):
        self.thirteenWeekMATRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Thirteen_Week_MA_TRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Thirteen_Week_MA_TRx_WoW_Growth",52).predictionDf
            self.thirteenWeekMATRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Thirteen_Week_MA_TRx_WoW_Growth"]])
        
    def graph_thirteenWeekMANRxWoWGrowth(self,weeks, predict):
        self.thirteenWeekMANRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Thirteen_Week_MA_NRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Thirteen_Week_MA_NRx_WoW_Growth",52).predictionDf
            self.thirteenWeekMANRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Thirteen_Week_MA_NRx_WoW_Growth"]])
        
    def graph_thirteenWeekMARRxWoWGrowth(self,weeks, predict):
        self.thirteenWeekMARRxWoWGrowthChart = graphObj(self.drug,self.masterDf,weeks,"Week",["Thirteen_Week_MA_RRx_WoW_Growth"],["plot"])
        if predict == True: 
            predictionDf = modelObj(self.masterDf,self.weeksToTrainOn,"Thirteen_Week_MA_RRx_WoW_Growth",52).predictionDf
            self.thirteenWeekMARRxWoWGrowthChart.generateChart(["plot"],predictionDf["Week"],[predictionDf["Thirteen_Week_MA_RRx_WoW_Growth"]])
    