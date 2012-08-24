
# This class manages the toolbar in the main frame

import wx
import config
from constants import *
from images import *
from eventhandler import *

log = config.getLogger(__name__)

class ToolbarManager(wx.ToolBar):
    def __init__(self, parent, ID):
        wx.ToolBar.__init__(self, parent, ID)
        self.addButtons()
        self.setBindings()
    
    def addButtons(self):
        self.createNewFileToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_NEW, getNewImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Create a new pvs file", EMPTY_STRING)
        self.openFileToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_OPEN, getOpenImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Open a pvs file", EMPTY_STRING)
        self.saveFileToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_SAVE, getSaveImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Save the file", EMPTY_STRING)
        self.saveallFileToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_SAVEALL, getSaveAllImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Save All Files", EMPTY_STRING)
        self.AddSeparator()
        self.cutToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_CUT, getCutImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Cut text", EMPTY_STRING)
        self.copyToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_COPY, getCopyImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Copy text", EMPTY_STRING)
        self.pasteToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_PASTE, getPasteImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Paste text here", EMPTY_STRING)
        self.AddSeparator()
        self.startPVSToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_STARTPVS, getStartPVSImage(), getStopPVSImage(), wx.ITEM_NORMAL, "Start pvs", EMPTY_STRING)
        self.typecheckToolbarItem = self.AddLabelTool(wx.ID_ANY, LABEL_TYPECHECK, getTypecheckImage(), wx.NullBitmap, wx.ITEM_NORMAL, "Parse and typecheck file", EMPTY_STRING)

    def setBindings(self):
        config.frame.Bind(wx.EVT_TOOL, onCreateNewFile, self.createNewFileToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onOpenFile, self.openFileToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onSaveFile, self.saveFileToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onSaveAllFiles, self.saveallFileToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onCutText, self.cutToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onCoptText, self.copyToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onPasteText, self.pasteToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onStartPVS, self.startPVSToolbarItem)
        config.frame.Bind(wx.EVT_TOOL, onTypecheck, self.typecheckToolbarItem)
        
        
    def enableStartPVS(self, value = True):
        self.startPVSToolbarItem.Enable(value)