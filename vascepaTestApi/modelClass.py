from fbprophet import Prophet


class modelObj:
    def __init__(self, masterDf, weeksToTrainOn, target, periodsToPredict):
        # check masterDf in drugObj, since drugObj creates modelObj when necessary
        self.masterDf = masterDf
        # check target in drugObj, since drugObj creates modelObj when necessary
        self.target = target
        self.weeksToTrainOn = weeksToTrainOn  # check weeks to train on in drugObj
        self.periodsToPredict = periodsToPredict
        self.createTrainingData()
        self.createAndTrainModel()
        self.createForecast()
        self.createTargetPredictions()

    def createTrainingData(self):
        self.prophetDf = self.masterDf[['Week', self.target]].copy()
        self.prophetDf = self.prophetDf[0:self.weeksToTrainOn]
        self.prophetDf.columns = ["ds", "y"]

    def createAndTrainModel(self):
        self.model = Prophet(seasonality_mode='multiplicative')
        self.model.fit(self.prophetDf)

    def createForecast(self):
        # "custom" freq, not mentioned by prophet documentation. Uses fact that pd.date_range (which Prophet's make_future_dataframe uses) accepts multiples of a frquency alias.
        self.futureDatesDf = self.model.make_future_dataframe(
            periods=self.periodsToPredict, freq='7D', include_history=False)
        self.fullForecastDf = self.model.predict(self.futureDatesDf)

    def createTargetPredictions(self):
        # can include uncertanties to graph those as well
        self.predictionDf = self.fullForecastDf[["ds", "yhat"]].copy()
        self.predictionDf.columns = ["Week", self.target]
        # reverse the order of the datarame but keep index order
        self.predictionDf = self.predictionDf.iloc[::-1].reset_index(drop=True)
