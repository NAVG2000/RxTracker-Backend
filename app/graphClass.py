import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import mpld3

plt.switch_backend("Agg")
sns.set()


class graphObj:
    def __repr__(self):
        return f"Drug Name: {self.drug}\nChart Title: {self.title}\nChart Type: {self.chartType}\nNumber Of Weeks: {self.weeks}\nY Label: {self.yLabel}\nY Data:\n{self.yData}\nX Label: {self.xLabel}\nX Data:\n{self.xData}\nMaster Df:\n{self.masterDf}\nAvailable Chart Types:{self.availableChartTypes.keys()}"

    def setX(self, xLabel):
        assert isinstance(xLabel, str), "xLabel must be a string"
        df = self.masterDf
        self.xLabel = xLabel
        self.xData = df[xLabel]

    def setY(self, yLabels, yLabel):
        assert isinstance(yLabels, list), "yLabels must be a list of strings"
        df = self.masterDf
        self.yLabels = yLabels
        self.yData = []
        for eachYLabel in yLabels:
            self.yData.append(df[eachYLabel])
        if yLabel is None:
            if len(yLabels) == 1:
                # since only 1 yLabel in array, extracts string value from array. Makes yLabel in chart look better
                self.yLabel = self.yLabels[0]
            else:
                self.yLabel = self.yLabels
        else:
            # "custom" yLabel (label to be shown in chart) provided
            self.yLabel = yLabel

    def setTitle(self, title):
        if title is None:
            assert (
                self.xLabel == "Week"
            ), "Provided xLabel is not 'Week' thus title cannot be autogenerated. Please provide a custom title."
            startDate = str(self.masterDf[self.xLabel][self.weeks])
            endDate = str(self.masterDf[self.xLabel][0])
            self.title = f"{self.drug} {self.yLabel} \n({startDate} to {endDate})"
        else:
            self.title = title

    def setWeeks(self, weeks):
        self.weeks = weeks

    def setMasterDf(self, masterDf):
        self.masterDf = masterDf.replace(
            [np.inf, -np.inf], np.nan
        ).dropna()  # drop inf/-inf/nan values
        if self.weeks > self.masterDf["Week"].count() - 1:
            print(
                "Given number of weeks is more than the weeks/rows in the data set. Will use all rows in dataset for graph."
            )
            self.setWeeks(self.masterDf["Week"].count() - 1)
        self.masterDf = self.masterDf.iloc[0: self.weeks + 1]

    def setAvailableChartTypes(self):
        self.availableChartTypes = {
            "scatter": self.ax.scatter,
            "plot": self.ax.plot,
            "logy_scatter": self.ax.scatter,
            "logy_plot": self.ax.semilogy,
        }

    def setChartType(self, chartType):
        for index, eachChartType in enumerate(chartType):
            chartType[index] = eachChartType.lower()
            assert (
                chartType[index] in self.availableChartTypes
            ), f"Given chartType ({chartType[index]}) not valid."
        self.chartType = chartType

    def __init__(
        self,
        drug,
        masterDf,
        weeks,
        xLabel,
        yLabels,
        chartType,
        yLabel=None,
        title=None,
        ax=None,
        fig=None,
        figW=10,
        figH=5.625
    ):
        if ax is None and fig is None:
            self.fig, self.ax = plt.subplots(figsize=(figW, figH))
        else:
            assert (
                ax is not None and fig is not None
            ), "Pass in eiher BOTH fig and ax or NEITHER fig and ax"
            self.fig = fig
            self.ax = ax
        self.drug = drug
        self.setWeeks(weeks)
        self.setMasterDf(masterDf)
        self.setX(xLabel)
        self.setY(yLabels, yLabel)
        self.setTitle(title)
        self.setAvailableChartTypes()
        self.setChartType(chartType)
        self.generateChart(self.chartType)

    def generateChart(self, chartType, xData=None, yData=None):
        # specify colormap (to avoid color conflict when using different plotting styles in same figure, such as in drugObj.graph_normalizedTRxAndAllMAs())
        yData = self.yData if yData is None else yData
        xData = self.xData if xData is None else xData
        assert len(chartType) == len(
            yData
        ), "The number of chartType inputs must be the same as the number of y inputs (yData list length must be same as chartType list length)."
        if yData is None:
            yData = self.yData
        for index, y in enumerate(yData):
            try:
                # availableChartTypes[chartType] selects the plotting function
                self.availableChartTypes[chartType[index]](
                    xData, y, label=self.yLabels[index]
                )
            except TypeError:
                self.availableChartTypes[chartType[index]](
                    xData.tolist(), y.tolist(), label=self.yLabels[index]
                )
        self.ax.set_title(self.title)
        if chartType == "logy_scatter":
            self.ax.set_yscale("log")
        self.ax.set_xlabel(self.xLabel)
        self.ax.set_ylabel(self.yLabel)
        if self.xLabel == "Week":
            self.ax.tick_params(axis="x", rotation=45)
        self.ax.legend()

    # save to png here

    def show_dataframe(self, df, entries=None):
        """
        Prints either the entire given dataframe or
        the first number of rows as specified by the given number in the "entries" parameter

        PARAMETERS:
        df: the dataframe to print. (dataframe)
        entries: the number of rows to display. (int) (optional, default=None)
        """
        if entries is None:
            print(df.to_string())
        else:
            if not (entries - 1 < df["Week"].count()):
                print(
                    "Given number of weeks is more than the weeks/rows in the data set. Thus, displaying all rows."
                )
                entries = df["Week"].count()
            print(df.iloc[0:entries].to_string())
