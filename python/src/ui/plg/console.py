
# This class manages the GUI's console for PVS

import wx
import codecs
import logging
from constants import *
from wx.lib.pubsub import setupkwargs, pub 
from ui.plugin import PluginPanel
import pvscomm

class ConsolePlugin(PluginPanel):
    """This class represents and manages the console.
    This console shows the PVS output, and the user can enter a line of input"""
    
    def __init__(self, parent, definition):
        PluginPanel.__init__(self, parent, definition)
        self.prompt = EMPTY_STRING
        self.history = []
        self.pvsout = wx.TextCtrl(self, wx.ID_ANY, EMPTY_STRING, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.pvsin = wx.TextCtrl(self, wx.ID_ANY, EMPTY_STRING, style=wx.TE_PROCESS_ENTER)

        consoleSizer = wx.BoxSizer(wx.VERTICAL)
        consoleSizer.Add(self.pvsout, 1, wx.EXPAND | wx.LEFT, 5)
        consoleSizer.Add(self.pvsin, 0, wx.EXPAND | wx.LEFT, 5)
        self.SetSizer(consoleSizer)

        self.Bind(wx.EVT_TEXT_ENTER, self.onPVSInTextEntered, self.pvsin)
        self.Bind(wx.EVT_TEXT, self.onPVSInText, self.pvsin)
        pub.subscribe(self.clearIn, PUB_CONSOLECLEARIN)
        pub.subscribe(self.initializeConsole, PUB_CONSOLEINITIALIZE)
        pub.subscribe(self.writeLine, PUB_CONSOLEWRITELINE)
        pub.subscribe(self.writePrompt, PUB_CONSOLEWRITEPROMPT)
        pub.subscribe(self.pvsModeUpdated, PUB_UPDATEPVSMODE)


    def pvsModeUpdated(self, pvsMode=PVS_MODE_OFF):
        pass

    def clearOut(self):
        """Clears the PVS output text in the console"""
        self.pvsout.Clear()
        logging.debug("Clearing pvsout")
        
    def clearIn(self):
        """Clears the PVS prompt box in the console"""
        self.pvsin.Clear()
        logging.debug("Clearing pvsin")
                
    def initializeConsole(self):
        """Initializes PVS In and Out"""
        self.pvsout.Clear()
        self.pvsin.Clear()
        self.prompt = EMPTY_STRING
        self.history = []
        #self.pvsModeUpdated(PVS_MODE_OFF)
        
    def appendLineToOut(self, line):
        logging.debug("Appending '%s' to pvsout", line)
        self.pvsout.AppendText(line + NEWLINE)
        
    def appendTextToOut(self, text):
        logging.debug("Appending '%s' to pvsout", text)
        self.pvsout.AppendText(text)      
        
    def appendTextToIn(self, text):
        logging.debug("Appending '%s' to pvsin", text)
        self.pvsin.AppendText(text)
        
    def writeTextToIn(self, text):
        logging.debug("Writing '%s' to pvsin", text)
        self.pvsin.write(text)
        
    def writeLine(self, line):
        self.appendLineToOut(line)
        
    def writePrompt(self, prompt):
        self.clearIn()
        self.writeTextToIn(prompt)
        self.prompt = prompt
                
    def onPVSInTextEntered(self, event):
        """This method is called whenever the user types something in the prompt and Enters."""
        logging.info("Event handler `onPVSInTextEntered' not implemented")
        whole = event.GetString()
        pl = len(self.prompt)
        command = whole[pl:]
        logging.info("Command is %s", command)
        self.appendLineToOut(whole)
        self.clearIn()
        self.history.append(command)
        result = pvscomm.PVSCommandManager().lisp(command)
        self.appendLineToOut(result)
        #event.Skip()
    
    def onPVSInText(self, event):
        """This method is called whenever PVS sends some text to the Editor"""
        st = event.GetString()
        logging.info("Received: %s", st)
        if not st.startswith(self.prompt):
            self.clearIn()
            self.writeTextToIn(self.prompt)
        #event.Skip()
        

        
        