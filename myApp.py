import wx

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
        self.SetSize(900, 300)

        #Setting up the panel and stuff.
        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(wx.WHITE)
        self.outVSizer = wx.BoxSizer(wx.VERTICAL)
        self.outHSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.outVSizer.AddStretchSpacer(1)
        self.outHSizer.AddStretchSpacer(1)
        self.sizer = wx.FlexGridSizer(rows=1, cols=1, vgap=55, hgap=20)


        #setting up various bvariables
        self.inchTOcm = 2.54
        self.milesTOkilometres = 1.609344
        self.poundsTOkilograms = 0.4535
        self.gallonsTOlitres = 0.21997
        self.celsiusTOkelvin = 273.15
        self.feetTOmetres = 0.3048
        self.acresTOhectares = 0.404685642
        self.globalCount = 0
        self.result = 00.00

        # Creating various UI elements 
        self.measurementBox = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Unit Conversion", size=(850,200))
        self.uerInputLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "   Value: ")
        self.resultLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, "  "+str(self.result)+"                ")
        self.globalCountText = wx.StaticText(self.mainPanel, wx.ID_ANY, "   Conversion Count: " + str(self.globalCount) + "   ")
        self.userInputBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
        self.convertButton = wx.Button(self.mainPanel, wx.ID_ANY, "Convert")
        self.clearThings = wx.Button(self.mainPanel, wx.ID_ANY, "Clear")
        self.checkbox = wx.CheckBox(self.mainPanel,  wx.ID_ANY, "Reverse calculation")
        self.combo = ["Inches/Centimeters", "Miles/Kilometres", "Pounds/Kilograms", "Gallons/Litres", "Feet/Metres", "Celcius/Kelvin", "Acres/Hectare"]
        self.measurementDrop = wx.ComboBox(self.mainPanel, choices=self.combo, style=wx.CB_READONLY)
        
        #Adding stuff to the boxSizers, which allows it to scale.
        self.boxSizer = wx.StaticBoxSizer(self.measurementBox, wx.HORIZONTAL)
        self.boxSizer.Add(self.measurementDrop)
        self.boxSizer.Add(self.uerInputLabel)
        self.boxSizer.Add(self.userInputBox)
        self.boxSizer.Add(self.resultLabel)
        self.boxSizer.Add(self.convertButton)
        self.boxSizer.Add(self.clearThings)
        self.boxSizer.Add(self.globalCountText)
        self.boxSizer.Add(self.checkbox)
        self.sizer.Add(self.boxSizer, flag=wx.EXPAND)

        # Bind events to things
        self.Bind(wx.EVT_BUTTON, self.OnConvert, self.convertButton)
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.clearThings)

        # Basically making sure it's responsive
        self.outHSizer.Add(self.sizer, flag=wx.EXPAND, proportion=15)
        self.outHSizer.AddStretchSpacer(1)
        self.outVSizer.Add(self.outHSizer, flag=wx.EXPAND, proportion=15)
        self.mainPanel.SetSizer(self.outVSizer)
        

    def makeMenuBar(self):
        """Renders the menuBar"""

        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnClear(self, event):
        """Do something"""
        self.userInputBox.Clear()
        self.globalCount = 0
        self.result = 00.00
        self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "               ")
        self.resultLabel.SetLabelText("  "+str(round(self.result, 2)) + "  ")
        self.measurementDrop.SetSelection(0)
    
    def setResult(self, result):
        self.resultLabel.SetLabelText("  "+str(round(result, 2)) + "     ")
    def convertMulti(self, a, b):
        result = a*b
        return self.setResult(result)
    def convertDivi(self, a, b):
        result = a/b
        return self.setResult(result)
    def convertPlus(self, a, b):
        result = a+b
        return self.setResult(result)
    def convertNeg(self, a, b):
        result = a-b
        return self.setResult(result)

    def ChooseCalculation(self):

        n = self.measurementDrop.GetSelection()

        if self.userInputBox.IsEmpty() == False:
            if n == 0:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertMulti(self.inchTOcm, int(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertDivi(self.inchTOcm, int(self.userInputBox.GetValue()))
            elif n == 1:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertMulti(self.milesTOkilometres, int(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.convertDivi(self.milesTOkilometres, int(self.userInputBox.GetValue()))
            elif n == 2:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertMulti(self.poundsTOkilograms, int(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertDivi(self.poundsTOkilograms, int(self.userInputBox.GetValue()))
            elif n == 3:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertDivi(self.gallonsTOlitres, float(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertMulti(self.gallonsTOlitres, float(self.userInputBox.GetValue()))
            elif n == 4:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertMulti(self.feetTOmetres, float(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertDivi(self.feetTOmetres, float(self.userInputBox.GetValue()))
            elif n == 5:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertPlus(self.celsiusTOkelvin, float(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertNeg(self.celsiusTOkelvin, float(self.userInputBox.GetValue()))
            elif n == 6:
                if self.checkbox.GetValue() == False:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertMulti(self.acresTOhectares, float(self.userInputBox.GetValue()))
                else:
                    self.globalCount+=1
                    self.globalCountText.SetLabelText("   Conversion Count: " + str(self.globalCount) + "  ")
                    self.convertDivi(self.acresTOhectares, float(self.userInputBox.GetValue()))
        else:
            self.onEmpty()
    
    def OnConvert(self, event):
        """Do something"""
        if self.userInputBox.IsEmpty() == True or self.userInputBox.GetValue().isnumeric() == False:
            self.onNonNumeric()
        else:
            self.ChooseCalculation()

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Simple Python program which allows the user to convert between differet measurements",
                      "About this program",
                      wx.OK|wx.ICON_INFORMATION)

    def onEmpty(self, event):
        """Display dialog saying it's empty"""
        wx.MessageBox("You cannot enter null values",
                      "ERROR",
                      wx.OK|wx.ICON_ERROR)

    def onNonNumeric(self):
        """Display dialog saying it's empty"""
        wx.MessageBox("Cannot enter non-numeric items",
                      "ERROR",
                      wx.OK|wx.ICON_ERROR)

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