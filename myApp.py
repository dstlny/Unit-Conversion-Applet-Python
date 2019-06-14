import wx
import io
import itertools 

class AppFrame(wx.Frame):

    def __init__(self, *args, **kw):
        """Constructor for this class"""

        # ensure the parent's __init__ is called
        super(AppFrame, self).__init__(*args, **kw)
        # create a menu bar
        self.makeMenuBar()
        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to my Python port of my Java application!")
        self.onInitialCurrencyLoad()
        self.SetSize(900, 900)
        self.mainPanel()

    def onInitialCurrencyLoad(self):
        self.filePath = "C:\\Users\\Luke\\Documents\\GitHub\\Java-Projects-Combined\\src\\currency.txt"

        try:
            self.currencyCombo = []
            self.currencyFactors = []
            self.currencySymbols = []
            self.contents = []

            with io.open(self.filePath, 'r', encoding='utf-8') as f:
                self.contents = f.readlines()

            self.contents = [x.strip('\t') for x in self.contents]
            self.contents = [x.strip('\n') for x in self.contents] 
            self.contents = [x.replace('\t','') for x in self.contents]
            self.contents = [x.replace(', ',',') for x in self.contents]
            ##print(self.contents)  

            for i in self.contents:
                currName, currFactor, currSymbol = i.split(',')
                self.currencyCombo.append(currName)
                self.currencyFactors.append(float(currFactor))
                self.currencySymbols.append(currSymbol)

        except Exception as exception:
            print(exception)

    def mainPanel(self):
        #Setting up the panel and stuff.
        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(wx.WHITE)
        self.outVSizer = wx.BoxSizer(wx.VERTICAL)
        self.outHSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.outVSizer.AddStretchSpacer(1)
        self.outHSizer.AddStretchSpacer(1)
        self.sizer = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=20)

        #setting up various variables
        self.unitFactors = [2.54, 1.609344, 0.4535, 0.21997, 0.3048, 273.15, 0.404685642] 
        self.globalCount = 0
        self.measureResult = 00.00
        self.currencyConvertLab = 00.00
        self.unitCombo = ["Inches/Centimeters", "Miles/Kilometres", "Pounds/Kilograms", "Gallons/Litres", "Feet/Metres", "Celcius/Kelvin", "Acres/Hectare"]
        self.CountText = "   Conversion Count: "
        
        # Creating various UI elements for the unit conversion module
        self.unitConversion = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Unit Conversion", size=(850,100))
        self.userInputLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "   Value: ")
        self.unitResultLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "  "+str(self.measureResult)+"                ")
        self.globalCountText = wx.StaticText(self.mainPanel, wx.ID_ANY, self.CountText + str(self.globalCount) + "   ")
        self.unitUserInputBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
        self.unitConvertButton = wx.Button(self.mainPanel, wx.ID_ANY, "Convert")
        self.clearThings = wx.Button(self.mainPanel, wx.ID_ANY, "Clear")
        self.globalCalcReverse = wx.CheckBox(self.mainPanel,  wx.ID_ANY, "Reverse calculation")
        self.measurementDrop = wx.ComboBox(self.mainPanel, choices=self.unitCombo, style=wx.CB_READONLY)

        #Adding stuff to the unitConversion boxSizer, which allows it to scale.
        self.unitConversionSizer = wx.StaticBoxSizer(self.unitConversion, wx.HORIZONTAL)
        self.unitConversionSizer.Add(self.measurementDrop)
        self.unitConversionSizer.Add(self.userInputLabel)
        self.unitConversionSizer.Add(self.unitUserInputBox)
        self.unitConversionSizer.Add(self.unitResultLabel)
        self.unitConversionSizer.Add(self.unitConvertButton)
        self.unitConversionSizer.Add(self.clearThings)
        self.unitConversionSizer.Add(self.globalCountText)
        self.unitConversionSizer.Add(self.globalCalcReverse)
        self.sizer.Add(self.unitConversionSizer, flag=wx.EXPAND)

        # Creating various UI elements for the currency conversion module
        self.currencyConversion = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Currency Conversion", size=(850,100))
        self.currencyDrop = wx.ComboBox(self.mainPanel, choices=self.currencyCombo, style=wx.CB_READONLY)
        self.userCurrencyLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "   Value: ")
        self.currencyInput = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
        self.currencyResult = wx.StaticText(self.mainPanel, wx.ID_ANY, "  "+str(self.currencyConvertLab)+"                ")
        self.currConvertButton = wx.Button(self.mainPanel, wx.ID_ANY, "Convert")

        #Adding stuff to the currencyConversion boxSizers, which allows it to scale.
        self.currencyConversionSizer = wx.StaticBoxSizer(self.currencyConversion, wx.HORIZONTAL)
        self.currencyConversionSizer.Add(self.currencyDrop)
        self.currencyConversionSizer.Add(self.userCurrencyLabel)
        self.currencyConversionSizer.Add(self.currencyInput)
        self.currencyConversionSizer.Add(self.currencyResult)
        self.currencyConversionSizer.Add(self.currConvertButton)
        self.sizer.Add(self.currencyConversionSizer, flag=wx.EXPAND)

        # Bind events to things
        self.Bind(wx.EVT_BUTTON, self.onCurrConvert, self.currConvertButton)
        self.Bind(wx.EVT_BUTTON, self.onUnitConvert, self.unitConvertButton)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearThings)

        # Basically making sure it's responsive
        self.outHSizer.Add(self.sizer, flag=wx.EXPAND, proportion=15)
        self.outHSizer.AddStretchSpacer(1)
        self.outVSizer.Add(self.outHSizer, flag=wx.EXPAND, proportion=15)
        self.mainPanel.SetSizer(self.outVSizer)

                      
    def makeMenuBar(self):
        """Renders the menuBar"""

        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        loadCurrency = fileMenu.Append(wx.ID_OPEN, '&Load Currency File..')
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.onLoadCurrency, loadCurrency)
        
    def onExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def onLoadCurrency(self, event):
        self.openFileDialog = wx.FileDialog(self, "Open a currency file...", "", "", 
        "Text files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.openFileDialog.ShowModal()
        self.filePath = self.openFileDialog.GetPath()

        try:
            self.currencyCombo = []
            self.currencyFactors = []
            self.currencySymbols = []
            self.contents = []
            self.currName = ""
            self.currFactor = ""
            self.currSymbol = ""

            with io.open(self.filePath, 'r', encoding='utf-8') as f:
                self.contents = f.readlines()

            self.contents = [x.strip('\t') for x in self.contents]
            self.contents = [x.strip('\n') for x in self.contents] 
            self.contents = [x.replace('\t','') for x in self.contents]
            self.contents = [x.replace(', ',',') for x in self.contents]
             
            for i in self.contents:
                
                try:

                    self.currName, self.currFactor, self.currSymbol = i.split(',')
                    
                    try:
                        self.currFactor = float(self.currFactor)
                    except Exception as exception:
                        print(exception)

                        self.currName = ""
                        self.currFactor = 00.00
                        self.currSymbol = ""
                        continue

                except ValueError as exception:
                    print(exception)
                    continue

                else:
                    self.currencyCombo.append(self.currName)
                    self.currencyFactors.append(self.currFactor)
                    self.currencySymbols.append(self.currSymbol)
                    self.currencyDrop.Clear()
                    self.currencyDrop.AppendItems(self.currencyCombo)
                    

        except Exception as exception:
            print(exception)

    def onClear(self, event):
        """Do something"""
        self.unitUserInputBox.Clear()
        self.currencyInput.Clear()
        self.globalCount = 0
        self.curencyConvertLab = 00.00
        self.measureResult = 00.00
        self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "               ")
        self.unitResultLabel.SetLabelText("  "+str(round(self.measureResult, 2)) + "  ")
        self.currencyResult.SetLabelText("  "+str(self.currencyConvertLab)+"                ")
        self.measurementDrop.SetSelection(0)
        self.currencyDrop.SetSelection(0)
    
    def setUnitResult(self, result):
        self.unitResultLabel.SetLabelText("  "+str(round(result, 2)) + "     ")
    def setCurrResult(self, result):
        if self.globalCalcReverse.GetValue() == False:
            self.currencyResult.SetLabelText("  "+str(self.getSymbol())+""+str(round(result, 2))+ "     ")
        else:
            self.currencyResult.SetLabelText("  "+str(self.getDefault())+""+str(round(result, 2))+ "     ")
    def convertMulti(self, a, b):
        return (b * a)
    def convertDivi(self, a, b):
        return (b / a)
    def convertPlus(self, a, b):
        return (b + a)
    def convertNeg(self, a, b):
        return (b - a)
    def getCurrencyFactor(self):
        return self.currencyFactors[self.currencyDrop.GetSelection()]
    def getUnitFactor(self):
        return self.unitFactors[self.measurementDrop.GetSelection()]
    def getSymbol(self):
        return self.currencySymbols[self.currencyDrop.GetSelection()]
    def getDefault(self):
        return "£"

    def unitCalculation(self):

        self.n = self.measurementDrop.GetSelection()
        
        if self.n in (0,1,2,4,6):
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertMulti(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertDivi(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
        elif self.n == 3:
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertDivi(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertMulti(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
        elif self.n == 5:
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertPlus(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertNeg(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))

    def currencyCalculation(self):

        self.bn = self.currencyDrop.GetSelection()
        self.r = range(0,8)
        
        if self.bn in self.r:
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setCurrResult(self.convertMulti(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))
                print(self.convertMulti(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))
            else:
                self.globalCount+=1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setCurrResult(self.convertDivi(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))
                print(self.convertDivi(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))

    def onUnitConvert(self, event):
        """Do something"""
        if self.unitUserInputBox.GetValue().isnumeric() == False:
            self.onNonNumeric()
        else:
            self.unitCalculation()

    def onCurrConvert(self, event):
        """Do something"""
        if self.currencyInput.GetValue().isnumeric() == False:
            self.onNonNumeric()
        else:
            self.currencyCalculation()

    def onAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Simple Python program which allows the user to convert between different measurements",
                      "About this program",
                      wx.OK|wx.ICON_INFORMATION)

    def onNonNumeric(self):
        """Display dialog saying it's empty"""
        wx.MessageBox("Cannot enter non-numeric items",
                      "ERROR",
                      wx.OK|wx.ICON_ERROR)
        self.unitUserInputBox.Clear()
        self.currencyInput.Clear()
        

#Main program loop
def main():
    """"Sets up the programs main window"""
    app = wx.App()
    frm = AppFrame(None, title='Python port of Java Application')
    frm.Show()
    app.MainLoop()  


#Main main, but it's ugly, thus the redirect
if __name__ == '__main__':
    main()
