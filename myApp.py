import wx,  os, hashlib, pathlib, glob  

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
        self.SetSize(900, 750)
        self.mainPanel()

    def onInitialCurrencyLoad(self):
        self.filePath = "C:\\Users\\Luke\\Documents\\GitHub\\Java-Projects-Combined\\src\\currency.txt"

        try:
            self.currencyCombo = []
            self.currencyFactors = []
            self.currencySymbols = []
            self.contents = []

            with open(self.filePath, 'r', encoding='utf-8-sig') as f:
                self.contents = f.readlines()

            self.contents = [x.strip('\t \n') for x in self.contents]
            self.contents = [x.replace('\t', '') for x in self.contents]
            self.contents = [x.replace(', ', ',') for x in self.contents]

            for i in self.contents:
                currName, currFactor, currSymbol = i.split(',')
                self.currencyCombo.append('British Pounds (GBP) to ' + currName)
                self.currencyFactors.append(float(currFactor))
                self.currencySymbols.append(currSymbol)

        except Exception as exception:
            print(exception)

    def mainPanel(self):
        # Setting up the panel and stuff.
        self.mainPanel = wx.Panel(self)
        self.hashString = ''
        self.mainPanel.SetBackgroundColour(wx.WHITE)
        self.outVSizer = wx.BoxSizer(wx.VERTICAL)
        self.outHSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.outVSizer.AddStretchSpacer(1)
        self.outHSizer.AddStretchSpacer(1)
        self.sizer = wx.FlexGridSizer(rows=4, cols=1, vgap=10, hgap=20)

        # setting up various variables
        self.unitFactors = [2.54, 1.609344, 0.4535,0.21997, 0.3048, 273.15, 0.404685642]
        self.globalCount = 0
        self.measureResult = 00.00
        self.currencyConvertLab = 00.00
        self.unitCombo = ["Inches/Centimeters", "Miles/Kilometres", "Pounds/Kilograms","Gallons/Litres", "Feet/Metres", "Celcius/Kelvin", "Acres/Hectare"]
        self.CountText = "   Conversion Count: "

        # Creating various UI elements for the unit conversion module
        self.unitConversion = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Unit Conversion", size=(850, 100))
        self.userInputLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "   Value: ")
        self.unitResultLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "  "+str(self.measureResult)+"                ")
        self.globalCountText = wx.StaticText(self.mainPanel, wx.ID_ANY, self.CountText + str(self.globalCount) + "   ")
        self.unitUserInputBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
        self.unitConvertButton = wx.Button(self.mainPanel, wx.ID_ANY, "Convert")
        self.clearThings = wx.Button(self.mainPanel, wx.ID_ANY, "Clear")
        self.globalCalcReverse = wx.CheckBox(self.mainPanel,  wx.ID_ANY, "Reverse calculation")
        self.measurementDrop = wx.ComboBox(self.mainPanel, choices=self.unitCombo, style=wx.CB_READONLY)

        # Adding stuff to the unitConversion boxSizer, which allows it to scale.
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
        self.currencyConversion = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Currency Conversion", size=(850, 100))
        self.currencyDrop = wx.ComboBox(self.mainPanel, choices=self.currencyCombo, style=wx.CB_READONLY)
        self.userCurrencyLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "   Value: ")
        self.currencyInput = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
        self.currencyResult = wx.StaticText(self.mainPanel, wx.ID_ANY, "  "+str(self.currencyConvertLab)+"                ")
        self.currConvertButton = wx.Button(self.mainPanel, wx.ID_ANY, "Convert")

        # Adding stuff to the currencyConversion boxSizers, which allows it to scale.
        self.currencyConversionSizer = wx.StaticBoxSizer(self.currencyConversion, wx.HORIZONTAL)
        self.currencyConversionSizer.Add(self.currencyDrop)
        self.currencyConversionSizer.Add(self.userCurrencyLabel)
        self.currencyConversionSizer.Add(self.currencyInput)
        self.currencyConversionSizer.Add(self.currencyResult)
        self.currencyConversionSizer.Add(self.currConvertButton)
        self.sizer.Add(self.currencyConversionSizer, flag=wx.EXPAND)

        # Creating various UI elements for the unit file-selection module
        self.fileDirectorySelection = wx.StaticBox(self.mainPanel, wx.ID_ANY, "File/Directory Selection")
        self.fileDirectoryButton = wx.Button(self.mainPanel, wx.ID_ANY, "Click to select a file/directory to inspect", size=(300, 30))
        self.choices = ['Inspect single file (default)', 'Inspect directory', 'Inspect directory meta-data']
        self.fileSelectionChoices = wx.RadioBox(self.mainPanel, wx.ID_ANY, choices=self.choices, style=wx.RA_SPECIFY_ROWS)
        self.writeToFile = wx.CheckBox(self.mainPanel, wx.ID_ANY, label='Output generated output to disk', style=wx.RA_SPECIFY_ROWS)
        self.fileDirectorySizer = wx.StaticBoxSizer(self.fileDirectorySelection, wx.VERTICAL)
        self.fileDirectorySizer.Add(self.fileDirectoryButton, flag=wx.ALIGN_CENTER)
        self.fileDirectorySizer.Add(self.fileSelectionChoices, flag=wx.ALIGN_CENTER)
        self.fileDirectorySizer.AddSpacer(10)
        self.fileDirectorySizer.Add(self.writeToFile, flag=wx.ALIGN_CENTER)
        self.fileDirectorySizer.AddSpacer(10)

        # Adding stuff to the fileDirectorySizer boxSizer, which allows it to scale.
        self.sizer.Add(self.fileDirectorySizer, flag=wx.ALIGN_LEFT)

        # Creating various UI elements for the unit hash-algorithm picker module
        self.algorithmSelection = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Algorithms", pos=(340, 163), size=(242, 115))
        self.algorithms = ['Message Digest 5, 128-bit', 'Secure Haashing Algorithm, 256-bit', 'Secure Hashing Algorithm 3, 512-bit']
        self.algorithmChoices = wx.RadioBox(self.mainPanel, wx.ID_ANY, choices=self.algorithms, pos=(350, 180), style=wx.RA_SPECIFY_ROWS)
        self.algorithmSelectionSizer = wx.StaticBoxSizer(self.algorithmSelection, wx.VERTICAL)

        # Bind events to things
        self.Bind(wx.EVT_BUTTON, self.onCurrConvert, self.currConvertButton)
        self.Bind(wx.EVT_BUTTON, self.onUnitConvert, self.unitConvertButton)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearThings)
        self.Bind(wx.EVT_BUTTON, self.loadFileorDirectory, self.fileDirectoryButton)

        # Basically making sure it's responsive
        self.outHSizer.Add(self.sizer, flag=wx.ALL, proportion=15)
        self.outHSizer.AddStretchSpacer(1)
        self.outVSizer.Add(self.outHSizer, flag=wx.ALL, proportion=15)
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

    def loadFileorDirectory(self, event):
        self.defaultPath = os.path.dirname(os.path.realpath(__file__))
        self.openFileDialog = wx.FileDialog(self, "Open a currency file...", self.defaultPath, "","", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.openFileDialog.ShowModal()
        self.filePath = self.openFileDialog.GetPath()
        self.fileParent = self.openFileDialog.GetDirectory()
        self.fileName = self.openFileDialog.GetFilename()

        try:
            
            self.pathChoice = self.returnUserChoice()

            if self.pathChoice == 0:
                self.accessFile(self.fileName, self.filePath)
            else:
                self.accessFile(self.fileName, self.fileParent)

        except Exception as excepti:
            print(excepti)

    def onLoadCurrency(self, event):
        self.openFileDialog = wx.FileDialog(self, "Open a currency file...", "", "","Text files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.openFileDialog.ShowModal()
        self.filePath = self.openFileDialog.GetPath()

        try:
            self.currencyCombo.clear()
            self.currencyFactors.clear()
            self.currencySymbols.clear()
            self.contents.clear()
            self.currName = ""
            self.currFactor = ""
            self.currSymbol = ""

            with open(self.filePath, 'r', encoding='utf-8-sig') as f:
                self.contents = f.readlines()

            self.contents = [x.strip('\t \n') for x in self.contents]
            self.contents = [x.replace('\t', '') for x in self.contents]
            self.contents = [x.replace(', ', ',') for x in self.contents]

            for i in self.contents:

                try:

                    self.currName, self.currFactor, self.currSymbol = i.split(',')

                    try:
                        self.currFactor = float(self.currFactor)
                    except Exception as exception:

                        self.currName = ""
                        self.currFactor = 00.00
                        self.currSymbol = ""
                        continue

                except ValueError as exception:
                    continue

                else:
                    self.currencyCombo.append('British Pounds (GBP) to ' + self.currName)
                    self.currencyFactors.append(self.currFactor)
                    self.currencySymbols.append(self.currSymbol)
                    self.currencyDrop.Clear()
                    self.currencyDrop.AppendItems(self.currencyCombo)
                    self.measurementDrop.SetSelection(0)
                    self.currencyDrop.SetSelection(0)

        except Exception as exception:
            print(exception)

    def onClear(self, event):
        """Do something"""
        self.unitUserInputBox.Clear()
        self.currencyInput.Clear()
        self.globalCount = 0
        self.curencyConvertLab = 00.00
        self.measureResult = 00.00
        self.globalCountText.SetLabelText(
        self.CountText + str(self.globalCount) + "               ")
        self.unitResultLabel.SetLabelText("  "+str(round(self.measureResult, 2)) + "  ")
        self.currencyResult.SetLabelText("  "+str(self.currencyConvertLab)+"                ")
        self.measurementDrop.SetSelection(0)
        self.currencyDrop.SetSelection(0)

    def setUnitResult(self, result):
        self.unitResultLabel.SetLabelText("  "+str(round(result, 2)) + "     ")

    def setCurrResult(self, result):
        if self.globalCalcReverse.GetValue() == False:
            self.currencyResult.SetLabelText("  "+str(self.getSymbol())+""+str(round(result, 2)) + "     ")
        else:
            self.currencyResult.SetLabelText("  "+str(self.getDefault())+""+str(round(result, 2)) + "     ")

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

        if self.n in (0, 1, 2, 4, 6):
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertMulti(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertDivi(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
        elif self.n == 3:
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertDivi(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertMulti(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
        elif self.n == 5:
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertPlus(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertNeg(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))

    def currencyCalculation(self):

        self.bn = self.currencyDrop.GetSelection()
        self.r = range(0, len(self.currencyFactors))

        if self.bn in self.r:
            if self.globalCalcReverse.GetValue() == False:
                self.globalCount += 1
                self.globalCountText.SetLabelText(
                self.CountText + str(self.globalCount) + "  ")
                self.setCurrResult(self.convertMulti(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setCurrResult(self.convertDivi(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))

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
                      wx.OK | wx.ICON_INFORMATION)

    def onNonNumeric(self):
        """Display dialog saying it's empty"""
        wx.MessageBox("Cannot enter non-numeric items",
                      "ERROR",
                      wx.OK | wx.ICON_ERROR)
        self.unitUserInputBox.Clear()
        self.currencyInput.Clear()

    def accessFile(self, name, directory):
        self.choice = self.returnUserChoice()

        if self.choice == 0:
            self.singleFile(name, directory)
        elif self.choice == 1:
            self.multipleFiles(name, directory)
        elif self.choice == 2:
            self.multipleFilesMetaData(name, directory)
        
    def returnAlgorithm(self):
        return self.algorithmChoices.GetSelection()

    def returnUserChoice(self):
        return self.fileSelectionChoices.GetSelection()

    def singleFile(self, filename, directory):
        self.importedFile = os.stat(directory)
        self.fileSize =  self.importedFile.st_atime
        self.importedFilePath = directory
        self.fileName = filename
        self.algo = algorithmGeneration()

        print('-------------------------------------')

        try:
            with open(self.importedFilePath, 'r') as f:
                self.contents = f.readlines()
                self.contents = [x.strip('\t \n') for x in self.contents]
        except Exception as ex:
            print(ex)
        else:
            self.algoChoice = self.returnAlgorithm()

            if self.algoChoice == 0:
                self.algo.md5.produceFileHash(self, self.contents)
                print(self.fileName)
                print(self.algo.md5.getHash(self)[0:128])
            elif self.algoChoice == 1:
                self.algo.sha256.produceFileHash(self, self.contents)
                print(self.fileName)
                print(self.algo.sha256.getHash(self)[0:256])
            elif self.algoChoice == 2:
                self.algo.sha3_512.produceFileHash(self, self.contents)
                print(self.fileName)
                print(self.algo.sha3_512.getHash(self)[0:512])
    
    def multipleFiles(self, filename, directory):

        self.algo = algorithmGeneration()

        x = [i[2] for i in os.walk(directory)]

        print('-------------------------------------')

        for t in x:
            for names in t:
                self.fileName = names
                try:
                    with open(directory+r"\\"+names, 'r') as f:
                        self.contents = f.readlines()
                        self.contents = [x.strip('\t \n') for x in self.contents]
                except Exception as exceptio:
                    print(exceptio)
                    continue
                finally:
                    self.algoChoice = self.returnAlgorithm()

                    if self.algoChoice == 0:
                        self.algo.md5.produceDirHash(self, self.contents)
                        print(self.fileName)
                        print(self.algo.md5.getHash(self)[0:128])
                    elif self.algoChoice == 1:
                        self.algo.sha256.produceDirHash(self, self.contents)
                        print(self.fileName)
                        print(self.algo.sha256.getHash(self)[0:256])
                    elif self.algoChoice == 2:
                        self.algo.sha3_512.produceDirHash(self, self.contents)
                        print(self.fileName)
                        print(self.algo.sha3_512.getHash(self)[0:512])

    def multipleFilesMetaData(self, filename, directory):

        self.algo = algorithmGeneration()

        x = [i[2] for i in os.walk(directory)]

        print('-------------------------------------')

        for t in x:
            for names in t:
                self.fileName = names
                self.importedFile = os.stat(directory+r"\\"+names)
                self.fileSize = self.importedFile.st_size
                self.algoChoice = self.returnAlgorithm()

                if self.algoChoice == 0:
                    self.algo.md5.produceDirMetaHash(self, self.fileSize)
                    print(self.fileName)
                    print(self.algo.md5.getHash(self)[0:128])
                elif self.algoChoice == 1:
                    self.algo.sha256.produceDirMetaHash(self, self.fileSize)
                    print(self.fileName)
                    print(self.algo.sha256.getHash(self)[0:256])
                elif self.algoChoice == 2:
                    self.algo.sha3_512.produceDirMetaHash(self, self.fileSize)
                    print(self.fileName)
                    print(self.algo.sha3_512.getHash(self)[0:512])

class algorithmGeneration:

    class md5:
        

        def produceFileHash(self, byte):
            
            self.m = hashlib.md5()
            
            for b in byte:
                self.m.update(str(b).encode('utf-8'))
                self.hashString = self.m.hexdigest()

        def produceDirHash(self, byte):
            
            self.m = hashlib.md5()

            for b in byte:
                self.m.update(str(b).encode('utf-8'))
                self.hashString = self.m.hexdigest()
            

        def produceDirMetaHash(self, fileSize):

            self.m = hashlib.md5()

            self.m.update(str(fileSize).encode('utf-8'))
            self.hashString = self.m.hexdigest()

        def getHash(self):
            return self.hashString

    class sha256:

        def produceFileHash(self, byte):
            self.m = hashlib.sha256()
            
            for b in byte:
                self.m.update(str(b).encode('utf-8'))
                self.hashString = self.m.hexdigest()

        def produceDirHash(self, byte):
            self.m = hashlib.sha256()
            
            for b in byte:
                self.m.update(str(b).encode('utf-8'))
                self.hashString = self.m.hexdigest()

        def produceDirMetaHash(self, fileSize):
            self.m = hashlib.sha256()

            self.m.update(str(fileSize).encode('utf-8'))
            self.hashString = self.m.hexdigest()

        def getHash(self):
            return self.hashString

    class sha3_512:

        def produceFileHash(self, byte):
            self.m = hashlib.sha3_512()
            
            for b in byte:
                self.m.update(str(b).encode('utf-8'))
                self.hashString = self.m.hexdigest()

        def produceDirHash(self, byte):
            self.m = hashlib.sha3_512()
            
            for b in byte:
                self.m.update(str(b).encode('utf-8'))
                self.hashString = self.m.hexdigest()

        def produceDirMetaHash(self, fileSize):
            self.m = hashlib.sha3_512()

            self.m.update(str(fileSize).encode('utf-8'))
            self.hashString = self.m.hexdigest()

        def getHash(self):
            return self.hashString


# Main program loop
def main():
    """"Sets up the programs main window"""
    app = wx.App()
    frm = AppFrame(None, title='Python port of Java Application')
    frm.Show()
    app.MainLoop()

# Main main, but it's ugly, thus the redirect
if __name__ == '__main__':
    main()