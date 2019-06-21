import wx
import os
import hashlib
from pathlib import Path
import re
import os 
from datetime import datetime

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
        self.SetSize(900, 750)
        self.onInitialCurrencyLoad()
        self.mainPanel()

    def onInitialCurrencyLoad(self):
        self.filePath = os.path.dirname(os.path.realpath(__file__))
        self.filePath+='\\currency.txt'

        try:

            self.contents = []
            self.dict = {}

            with open(self.filePath, 'r', encoding='utf-8-sig') as f:
                self.contents = [re.sub(r"[\n\t]*", "", x) for x in f.readlines()]

                for i in self.contents:
                    currName, currFactor, currSymbol = i.split(',')
                    self.dict['British Pound (GBP) to ' + currName] = (float(currFactor.replace(" ", "")), currSymbol.replace(" ", ""))

            del self.contents
            del currName
            del currFactor
            del currSymbol

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
        self.currencyDrop = wx.ComboBox(self.mainPanel, choices=list(self.dict.keys()), style=wx.CB_READONLY)
        self.measurementDrop.SetSelection(0)
        self.currencyDrop.SetSelection(0)
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
        self.fileDirectoryButton = wx.Button(self.mainPanel,1003, "Click to select a file/directory to inspect", size=(300, 30))
        self.choices = ['Inspect single file (default)', 'Inspect directory', 'Inspect directory meta-data']
        self.fileSelectionChoices = wx.RadioBox(self.mainPanel, wx.ID_ANY, choices=self.choices, style=wx.RA_SPECIFY_ROWS)
        self.writeToFile = wx.CheckBox(self.mainPanel, wx.ID_ANY, label='Output generated output to disk', style=wx.RA_SPECIFY_ROWS)
        self.fileDirectorySizer = wx.StaticBoxSizer(self.fileDirectorySelection, wx.VERTICAL)
        self.fileDirectorySizer.Add(self.fileDirectoryButton, flag=wx.ALIGN_CENTER)
        self.fileDirectorySizer.Add(self.fileSelectionChoices, flag=wx.ALIGN_CENTER)
        self.fileDirectorySizer.AddSpacer(10)
        self.fileDirectorySizer.Add(self.writeToFile, flag=wx.ALIGN_CENTER)
        self.fileDirectorySizer.AddSpacer(10)
        self.i = 0

        # Adding stuff to the fileDirectorySizer boxSizer, which allows it to scale.
        self.sizer.Add(self.fileDirectorySizer, flag=wx.ALIGN_LEFT)

        # Creating various UI elements for the unit hash-algorithm picker module
        self.algorithmSelection = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Algorithms", pos=(340, 163), size=(242, 115))
        self.algorithms = ['Message Digest 5, 128-bit', 'Secure Haashing Algorithm, 256-bit', 'Secure Hashing Algorithm 3, 512-bit']
        self.algorithmChoices = wx.RadioBox(self.mainPanel, wx.ID_ANY, choices=self.algorithms, pos=(350, 180), style=wx.RA_SPECIFY_ROWS)

        # Creating various UI elements for the logging module
        self.textAreaBorder = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Logging Output", pos=(18, 350), size=(847, 300))
        self.textArea = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "", pos=(25, 370), size=(833,272), style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.textArea.HideNativeCaret()
        self.textArea.SetForegroundColour(wx.WHITE)
        self.textArea.SetBackgroundColour(wx.BLACK)

        # Bind events to things
        self.Bind(wx.EVT_BUTTON, self.onCurrConvert, self.currConvertButton)
        self.Bind(wx.EVT_BUTTON, self.onUnitConvert, self.unitConvertButton)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearThings)
        self.Bind(wx.EVT_BUTTON, self.loadFileorDirectory, self.fileDirectoryButton, id=1003)

        # Basically making sure it's responsive
        self.outHSizer.Add(self.sizer, flag=wx.ALL, proportion=15)
        self.outHSizer.AddStretchSpacer(1)
        self.outVSizer.Add(self.outHSizer, flag=wx.ALL, proportion=15)
        self.mainPanel.SetSizer(self.outVSizer)

    def makeMenuBar(self):
        """Renders the menuBar"""

        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        loadCurrency = fileMenu.Append(1001, '&Load Currency File...')
        loadFileOrDirectory = fileMenu.Append(1002, '&Load File or Directory...')
        hideLogWindow = fileMenu.Append(1003, '&Enable/Disable log window...')
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onExit,source=exitItem)
        self.Bind(wx.EVT_MENU, self.onAbout,source=aboutItem)
        self.Bind(wx.EVT_MENU, self.onLoadCurrency,source=loadCurrency, id=1001)
        self.Bind(wx.EVT_MENU, self.loadFileorDirectory,source=loadFileOrDirectory,id=1002)
        self.Bind(wx.EVT_MENU, self.onHide,source=hideLogWindow,id=1003)

    def onExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def onHide(self, event):
        self.Refresh()
        if self.textArea.IsShown() == True:
            self.textArea.Show(False)
            self.textAreaBorder.Show(False)
            self.SetSize(900, 410)
        else:
            self.textAreaBorder.Show(True)
            self.textArea.Show(True)
            self.SetSize(900, 750)

    def onLoadCurrency(self, event):
        self.defaultPath = os.path.dirname(os.path.realpath(__file__))
        self.openFileDialog = wx.FileDialog(self, "Open and import a currency...", self.defaultPath , "","Text files (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.openFileDialog.ShowModal()
        self.Refresh()

        try:
            self.contents = []
            self.dict = {}
            self.currName = ""
            self.currFactor = 00.00
            self.currSymbol = "'"

            with open(self.openFileDialog.GetPath(), 'r', encoding='utf-8-sig') as f:
                self.contents = [re.sub(r"[\n\t]*", "", x) for x in f.readlines()]

                for i in self.contents:

                    try:

                        self.currName, self.currFactor, self.currSymbol = i.split(',')

                        try:
                            self.currFactor = float(self.currFactor)
                        except:
                            self.currname = ""
                            self.currFactor = 00.00
                            self.currSymbol = ""
                            continue
                    except:
                        continue
                    finally:
                        if self.currName and self.currFactor and self.currSymbol:
                            self.currencyDrop.Clear()
                            self.dict['British Pound (GBP) to ' + self.currName] = (float(self.currFactor), self.currSymbol.replace(" ", ""))
                            self.currencyDrop.Append(list(self.dict.keys()))
                            self.measurementDrop.SetSelection(0)
                            self.currencyDrop.SetSelection(0)

        except Exception as exception:
            print(exception)
    
    def loadFileorDirectory(self, event):
        self.defaultPath = os.path.dirname(os.path.realpath(__file__))
        self.openFileDialog = wx.FileDialog(self, "Open and load a directory...", self.defaultPath, "","", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.openFileDialog.ShowModal()
        font1 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.Refresh()

        try:

            if self.returnUserChoice() == 0:
                self.textArea.SetFont(font1)
                self.textArea.Clear()
                self.i = 0
                self.textArea.AppendText("Directory '{}'\nFile No, Filename, Hash".format(self.openFileDialog.GetDirectory()))
                self.singleFile(self.openFileDialog.GetFilename(),  self.openFileDialog.GetDirectory())
            elif self.returnUserChoice() == 1:
                self.textArea.SetFont(font1)
                self.i = 0
                self.textArea.Clear()
                self.textArea.AppendText("Directory '{}'\nFile No, Filename, Hash".format(self.openFileDialog.GetDirectory()))
                self.multipleFiles(self.openFileDialog.GetFilename(), self.openFileDialog.GetDirectory())
            elif self.returnUserChoice() == 2:
                self.textArea.SetFont(font1)
                self.textArea.Clear()
                self.i = 0
                self.textArea.AppendText("Directory '{}' meta-data\nFile No, Filename, Hash, Last Modified".format(self.openFileDialog.GetDirectory()))
                self.multipleFilesMetaData(self.openFileDialog.GetFilename(), self.openFileDialog.GetDirectory())

        except Exception as excepti:
            print(excepti)

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
        self.Refresh()

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
        return self.dict[self.currencyDrop.GetStringSelection()][0]

    def getUnitFactor(self):
        return self.unitFactors[self.measurementDrop.GetSelection()]

    def getSymbol(self):
         return self.dict[self.currencyDrop.GetStringSelection()][1]

    def getDefault(self):
        return "£"

    def unitCalculation(self):

        if self.measurementDrop.GetSelection() in (0, 1, 2, 4, 6):
            if self.globalCalcReverse.GetValue():
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertDivi(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertMulti(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
        elif self.measurementDrop.GetSelection() == 3:
            if self.globalCalcReverse.GetValue():
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertMulti(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertDivi(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
        elif self.measurementDrop.GetSelection() == 5:
            if self.globalCalcReverse.GetValue():
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertNeg(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setUnitResult(self.convertPlus(self.getUnitFactor(), int(self.unitUserInputBox.GetValue())))

    def currencyCalculation(self):

        self.r = range(0, len(self.dict))

        if self.currencyDrop.GetSelection() in self.r:
            if self.globalCalcReverse.GetValue():
                self.globalCount += 1
                self.globalCountText.SetLabelText(self.CountText + str(self.globalCount) + "  ")
                self.setCurrResult(self.convertDivi(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))
            else:
                self.globalCount += 1
                self.globalCountText.SetLabelText(
                self.CountText + str(self.globalCount) + "  ")
                self.setCurrResult(self.convertMulti(self.getCurrencyFactor(), float(self.currencyInput.GetValue())))

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

    def returnAlgorithm(self):
        return self.algorithmChoices.GetSelection()

    def returnUserChoice(self):
        return self.fileSelectionChoices.GetSelection()

    def singleFile(self, filename, directory):
        
        self.algo = algorithmGeneration()

        try:
            with open(directory+'\\'+filename, 'r') as f:
                self.contents = [re.sub(r"[\n\t]*", "", x) for x in f.readlines()]

        except Exception as ex:
            print(ex)
        finally:

            if self.returnAlgorithm() == 0:
                self.algo.md5.produceFileHash(self, self.contents)
                self.i += 1                 
                self.textArea.AppendText("\n{}.  {}  {}".format(self.i,filename,str(self.algo.md5.getHash(self)[0:128])))
                
                if self.writeToFile.GetValue() == True:
                    stringToWrite = directory+' : '+filename+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.md5.getHash(self)[0:128])
                    self.writeLineToFile(stringToWrite, str(self.algo.md5.getHash(self)[0:128]))
                else:
                    stringToWrite = directory+' : '+filename+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.md5.getHash(self)[0:128])

            elif self.returnAlgorithm() == 1:
                self.algo.sha256.produceFileHash(self, self.contents)
                self.i += 1                  
                self.textArea.AppendText("\n{}.  {}  {}".format(self.i,filename,str(self.algo.sha256.getHash(self)[0:256])))
            
                if self.writeToFile.GetValue() == True:
                    stringToWrite = directory+' : '+filename+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha256.getHash(self)[0:256])
                    self.writeLineToFile(stringToWrite, str(self.algo.sha256.getHash(self)[0:256]))
                else:
                    stringToWrite = directory+' : '+filename+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha256.getHash(self)[0:256])

            elif self.returnAlgorithm()== 2:
                self.algo.sha3_512.produceFileHash(self, self.contents)

                self.i += 1
                self.textArea.AppendText("\n{}.  {}  {}".format(self.i,filename,str(self.algo.sha3_512.getHash(self)[0:512])))
                
                if self.writeToFile.GetValue() == True:
                    stringToWrite = directory+' : '+filename+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha3_512.getHash(self)[0:512])
                    self.writeLineToFile(stringToWrite, str(self.algo.sha3_512.getHash(self)[0:512]))
                else:
                    stringToWrite = directory+' : '+filename+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha3_512.getHash(self)[0:512])

    def multipleFiles(self, filename, directory):
        del filename

        self.algo = algorithmGeneration()

        # List all files in directory using pathlib
        basepath = Path(directory)
        files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
        for item in files_in_basepath:
            try:
                with open(directory+"\\"+item.name, 'r') as f:
                    self.contents = [re.sub(r"[\n\t]*", "", x) for x in f.readlines()]
            except Exception as exceptio:
                continue
            finally:

                if self.returnAlgorithm() == 0:
                    self.algo.md5.produceDirHash(self, self.contents)

                    self.i += 1
                    self.textArea.AppendText("\n{}.  {}  {}".format(self.i,item.name,str(self.algo.md5.getHash(self)[0:128])))
                    
                    if self.writeToFile.GetValue() == True:
                        stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.md5.getHash(self)[0:128])
                        self.writeLineToFile(stringToWrite, str(self.algo.md5.getHash(self)[0:128]))
                    else:
                        stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.md5.getHash(self)[0:128])

                elif self.returnAlgorithm() == 1:
                    self.algo.sha256.produceDirHash(self, self.contents)

                    self.i += 1
                    self.textArea.AppendText("\n{}.  {}  {}".format(self.i,item.name,str(self.algo.sha256.getHash(self)[0:256])))

                    if self.writeToFile.GetValue() == True:
                        stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha256.getHash(self)[0:256])
                        self.writeLineToFile(stringToWrite, str(self.algo.sha256.getHash(self)[0:256]))
                    else:
                        stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha256.getHash(self)[0:256])
                        

                elif self.returnAlgorithm() == 2:
                    self.algo.sha3_512.produceDirHash(self, self.contents)

                    self.i += 1                     
                    self.textArea.AppendText("\n{}.  {}  {}".format(self.i,item.name,str(self.algo.sha3_512.getHash(self)[0:512])))
                    
                    if self.writeToFile.GetValue() == True:
                        stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha3_512.getHash(self)[0:512])
                        self.writeLineToFile(stringToWrite, str(self.algo.sha3_512.getHash(self)[0:512]))
                    else:
                        stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha3_512.getHash(self)[0:512])

    def multipleFilesMetaData(self, filename, directory):
        del filename

        self.algo = algorithmGeneration()
        basepath = Path(directory)
        files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
        for item in files_in_basepath:

            self.importedFile = os.stat(directory+"\\"+item.name)

            if self.returnAlgorithm() == 0:
                self.algo.md5.produceDirMetaHash(self, self.importedFile.st_size)

                self.i += 1
                self.textArea.AppendText("\n{}.  {}  {}  {}".format(self.i,item.name,str(self.algo.md5.getHash(self)[0:128]), datetime.fromtimestamp(self.importedFile.st_mtime)))

                if self.writeToFile.GetValue() == True:
                    stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.md5.getHash(self)[0:128])
                    self.writeLineToFile(stringToWrite, str(self.algo.md5.getHash(self)[0:128]))
                else:
                    stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.md5.getHash(self)[0:128])

            elif self.returnAlgorithm() == 1:
                self.algo.sha256.produceDirMetaHash(self, self.importedFile.st_size)

                self.i += 1                     
                self.textArea.AppendText("\n{}.  {}  {}  {}".format(self.i,item.name,str(self.algo.sha256.getHash(self)[0:256]), datetime.fromtimestamp(self.importedFile.st_mtime)))

                if self.writeToFile.GetValue() == True:
                    stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha256.getHash(self)[0:256])
                    self.writeLineToFile(stringToWrite, str(self.algo.sha256.getHash(self)[0:256]))
                else:
                    stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha256.getHash(self)[0:256])

            elif self.returnAlgorithm() == 2:
                self.algo.sha3_512.produceDirMetaHash(self, self.importedFile.st_size)
                
                self.i += 1                     
                self.textArea.AppendText("\n{}.  {}  {}  {}".format(self.i,item.name,str(self.algo.sha3_512.getHash(self)[0:512]), datetime.fromtimestamp(self.importedFile.st_mtime)))

                if self.writeToFile.GetValue() == True:
                    stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha3_512.getHash(self)[0:512])
                    self.writeLineToFile(stringToWrite, str(self.algo.sha3_512.getHash(self)[0:512]))
                else:
                    stringToWrite = directory+' : '+item.name+' : '+str(self.returnUserChoice())+' : '+str(self.returnAlgorithm())+' : '+str(self.algo.sha3_512.getHash(self)[0:512])

    def writeLineToFile(self, lineToWrite, file_hash):
        self.defaultPath = os.path.dirname(os.path.realpath(__file__))
        self.defaultPath+='\\'
        self.hash = file_hash

        if os.path.isfile(self.defaultPath+"final.txt")  == False:
            with open(self.defaultPath+"final.txt","w+") as f:
                f.write(lineToWrite+'\n')
                f.close()
        else:
            self.contents = set([re.sub(r"[\n\t]*", "", line) for line in open(self.defaultPath+"final.txt")])
            
            imported_path, imported_file, imported_choice, imported_algo, imported_hashy_boi = lineToWrite.split(" : ")
            imported_hashy_boi = self.hash

            if self.contents:

                for line in self.contents:
                    path_name, file_name, user_choice, algorithm_choice, hashy_boi = line.split(" : ")
                    this_string = path_name + ' : ' + file_name  + ' : ' + user_choice  + ' : ' + algorithm_choice
                    string_to_add = imported_path  + ' : ' + imported_file  + ' : ' + imported_choice  + ' : ' + imported_algo 

                    if string_to_add == this_string and imported_hashy_boi != hashy_boi:
                        this_string = path_name + ' : ' + file_name  + ' : ' + user_choice  + ' : ' + algorithm_choice + ' : ' + hashy_boi
                        string_to_add = imported_path  + ' : ' + imported_file  + ' : ' + imported_choice  + ' : ' + imported_algo + ' : ' + imported_hashy_boi
                        self.contents.remove(this_string)
                        self.contents.add(string_to_add)
                        self.onAltered(file_name, hashy_boi, imported_hashy_boi)
                        print('-------------\nfallen into main if statement\nline removed = {}\nline added = {}'.format(this_string, string_to_add))
                        self.cleaned = True

                        if self.cleaned:
                            with open(self.defaultPath+"final.txt","w+") as f:
                                for self.this_line in self.contents:
                                    f.write(self.this_line+'\n')
                    
                    else: ##this must mean that the curent imported file does not exist within final.txt, thus print it to the file
                        string_to_add = imported_path  + ' : ' + imported_file  + ' : ' + imported_choice  + ' : ' + imported_algo + ' : ' + imported_hashy_boi
                        self.contents = set([line.strip("\n") for line in open(self.defaultPath+"final.txt")])
                        self.contents.add(string_to_add)
                        print('-------------\nfallen into else')
                        with open(self.defaultPath+"final.txt","w+") as f:
                            for extra in self.contents:
                                print('{} is unique and in self.contents'.format(extra))
                                f.write(extra+'\n')
            else:
                print('self.contents is null, {} has been written'.format(lineToWrite))
                with open(self.defaultPath+"final.txt","w+") as f:
                    f.write(lineToWrite+'\n')
                    f.close()

    def onAltered(self, fileAltered, oldFileHash, newFileHash):
        """Display dialog saying it's empty"""
        wx.MessageBox("Old hash is '{}'\nNew hash '{}'".format(oldFileHash,newFileHash),
                      "'{}' altered".format(fileAltered),
                      wx.OK | wx.ICON_ERROR)

    def onFinished(self):
        """Display dialog saying it's empty"""
        wx.MessageBox("All operations have been finished",
                      "FINISHED OPERATION",
                      wx.OK | wx.ICON_ERROR)

class algorithmGeneration:

    class md5:
        
        def produceFileHash(self, byte):
            self.hashString = hashlib.md5(str([b for b in byte]).encode('utf-8')).hexdigest()

        def produceDirHash(self, byte):
            self.hashString = hashlib.md5(str([b for b in byte]).encode('utf-8')).hexdigest()
            
        def produceDirMetaHash(self, fileSize):
            self.hashString = hashlib.md5(str(fileSize).encode('utf-8')).hexdigest()

        def getHash(self):
            return self.hashString

    class sha256:

        def produceFileHash(self, byte):
            self.hashString = hashlib.sha256(str([b for b in byte]).encode('utf-8')).hexdigest()

        def produceDirHash(self, byte):
            self.hashString = hashlib.sha256(str([b for b in byte]).encode('utf-8')).hexdigest()

        def produceDirMetaHash(self, fileSize):
            self.hashString = hashlib.sha256(str(fileSize).encode('utf-8')).hexdigest()

        def getHash(self):
            return self.hashString

    class sha3_512:

        def produceFileHash(self, byte):
            self.hashString = hashlib.sha3_512(str([b for b in byte]).encode('utf-8')).hexdigest()

        def produceDirHash(self, byte):
            self.hashString = hashlib.sha3_512(str([b for b in byte]).encode('utf-8')).hexdigest()

        def produceDirMetaHash(self, fileSize):
            self.hashString = hashlib.sha3_512(str(fileSize).encode('utf-8')).hexdigest()

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