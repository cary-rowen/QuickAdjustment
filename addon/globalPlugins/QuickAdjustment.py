#-*- coding:utf-8 -*-

import winreg
import ui
import scriptHandler
import addonHandler
import globalPluginHandler
import languageHandler
from keyboardHandler import KeyboardInputGesture

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("QuickAdjustment")

	@scriptHandler.script(
		description=_("Switch touchpad"), 
		gestures=["kb:nvda+'"])
	def script_SwitchTouchpad(self, gesture):
		if getTouchpadStatus() == None:
			ui.message("not support")
			return
		else:
			KeyboardInputGesture.fromName("windows+control+f24").send()
		if getTouchpadStatus():
			ui.message("Touchpad enabled")
		else:
			ui.message("Touchpad disabled")

	@scriptHandler.script(
		description=_("Switch Chinese input mode(Shuangpin or Quanpin)"), 
		gestures=["kb:NVDA+alt+b"])
	def script_SwitchPinyinMode(self, gesture):
		if isDoublePinyin() == None or not(isLanSupport('zh_CN')):
			ui.message("not support")
			return
		else:
			setPinyinMode(int(not isDoublePinyin()))
		if isDoublePinyin():
			ui.message("Shuangpin input")
		else:
			ui.message("QuanPin input")


	@scriptHandler.script(
		description=_("Simulate pressing the Application key"), 
		gestures=["kb:nvda+;"])
	def script_PressApplication(self, gesture):
		KeyboardInputGesture.fromName("applications").send()
       

def isDoublePinyin():
	try:
		key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\InputMethod\Settings\CHS")
		return bool(winreg.QueryValueEx(key, "Enable Double Pinyin")[0])
	except:
		return None


def setPinyinMode(mode):
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\InputMethod\Settings\CHS")
		winreg.SetValueEx(key, "Enable Double Pinyin", 0, winreg.REG_DWORD, mode)
	except:
		pass


def getTouchpadStatus():
	try:
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\PrecisionTouchPad\Status")
		return bool(winreg.QueryValueEx(key, "Enabled")[0])
	except:
		return None


def isLanSupport(*lan):
	return True if languageHandler.getLanguage() in lan else False
