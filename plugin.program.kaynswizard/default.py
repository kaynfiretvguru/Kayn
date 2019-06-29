import xbmc,xbmcaddon,xbmcgui,xbmcplugin,os,sys,base64
import shutil
import urllib2,urllib
import re
import time
import ntpath

from resources.lib.modules import downloader
from resources.lib.modules import extract
from resources.lib.modules import plugintools
from resources.lib.modules import zfile as zipfile


addon_id           = 'plugin.program.kaynswizard'
FANART             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON               = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

KAYN_URL           = base64.b64decode(b'aHR0cHM6Ly9rYXluZmlyZXR2Z3VydS53aXhzaXRlLmNvbS9rYXluLw==')
BGH_URL            = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2theW5maXJldHZndXJ1L0theW4vcmF3L21hc3Rlci8=')
BBB_URL            = base64.b64decode(b'aHR0cHM6Ly9iaXRidWNrZXQub3JnL2theW5maXJldHZndXJ1Lw==')

FRESHSTART_ICON    = BGH_URL + base64.b64decode(b'RnJlc2hTdGFydEljb24uanBn')
UPGRADE_ICON       = BGH_URL + base64.b64decode(b'VXBncmFkZUljb24uanBn')
SOURCES_ICON       = BGH_URL + base64.b64decode(b'U291cmNlc0ljb24uanBn')
KAYN_ICON          = BGH_URL + base64.b64decode(b'S2F5bkljb24uanBn')
VOID_ICON          = BGH_URL + base64.b64decode(b'Vk9JREljb24uanBn')
VOID_FANART        = BGH_URL + base64.b64decode(b'Vk9JREZhbmFydC5qcGc=')
KAYN_FANART        = BGH_URL + base64.b64decode(b'S2F5bkZhbmFydC5qcGc=')

MOBILE_URL         = BBB_URL + base64.b64decode(b'bW9iaWxlL2Rvd25sb2Fkcy8=')
TOOLS_URL          = BBB_URL + base64.b64decode(b'dG9vbHMvZG93bmxvYWRzLw==')
VOID_URL           = BBB_URL + base64.b64decode(b'dm9pZC9kb3dubG9hZHMv')

VOID_BUILD         = BBB_URL + base64.b64decode(b'dm9pZC9kb3dubG9hZHMvVk9JRC56aXA/ZGw9MQ==')
VOID_UPDATE        = BBB_URL + base64.b64decode(b'dG9vbHMvZG93bmxvYWRzL1VwZGF0ZV9WT0lELnppcD9kbD0x')
VOID_UPGRADE       = BBB_URL + base64.b64decode(b'dG9vbHMvZG93bmxvYWRzL1ZPSURfVXBncmFkZS56aXA/ZGw9MQ==')
VOIDM_BUILD        = BBB_URL + base64.b64decode(b'bW9iaWxlL2Rvd25sb2Fkcy9WT0lETW9iaWxlLnppcD9kbD0x')
VOIDM_UPDATE       = BBB_URL + base64.b64decode(b'dG9vbHMvZG93bmxvYWRzL1VwZGF0ZV9WT0lEX01vYmlsZS56aXA/ZGw9MQ==')
SOURCES            = BBB_URL + base64.b64decode(b'dG9vbHMvZG93bmxvYWRzL1NvdXJjZXMuemlwP2RsPTE=')
FRESHSTART         = BBB_URL + base64.b64decode(b'dG9vbHMvZG93bmxvYWRzL0ZyZXNoU3RhcnQuemlwP2RsPTE=')


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base=''
ADDON=xbmcaddon.Addon(id='plugin.program.kaynswizard')
dialog = xbmcgui.Dialog()    
VERSION = "1.1.9"
PATH = "Kayn's Wizard"            

    
def CATEGORIES():
    link = OPEN_URL('https://github.com/kaynfiretvguru/Kayn/raw/master/wizard.html').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addItem(name,url,1,iconimage,fanart,description)
    setView('movies', 'MAIN')


def INDEX():
	addItem('Fresh Start',KAYN_URL,1,FRESHSTART_ICON,KAYN_FANART,'ONLY INSTALL IF YOU HAVE ALREADY BACKED UP YOUR BUILD AND INSTALLED A NEW VERSION OF KODI. This tool is was designed to help with the Kodi upgrade process. The only Add-Ons in this download are minor maintenance Add-Ons to allow you to restore your backup after downloading and installing a newer version of Kodi.')
	addItem('VOID Build',KAYN_URL,2,VOID_ICON,VOID_FANART,'The latest build from Kayn. This build contains the following sections; Library, Live News, Movies, TV Shows, Kids, Maintenance, Add-ons, and Settings.')
	addItem('VOID Build (Mobile)',KAYN_URL,3,VOID_ICON,VOID_FANART,'A mobile version of the VOID Build. This build has been configured for small touchscreen devices, such as phones and tablets.')
	addItem('Update for VOID',KAYN_URL,4,VOID_ICON,VOID_FANART,'UPDATED ON: April 28th 2018. Update for the VOID Build. Only click this if you have the VOID Build installed.')
	addItem('Update for VOID (Mobile)',KAYN_URL,5,VOID_ICON,VOID_FANART,'UPDATED ON: April 28th 2018. Update for the Mobile VOID Build. Only click this if you have the Mobile VOID Build installed.')
	addItem('VOID Upgrade',KAYN_URL,6,UPGRADE_ICON,VOID_FANART,'UPDATED ON: June 27th 2019. Upgrade for the VOID Build to allow compatability for Kodi 18.')
	addItem('Sources',KAYN_URL,7,SOURCES_ICON,KAYN_FANART,'Repository Sources, not actual Repositories. Download if your sources.xml file has been corrupted or is missing.')
	addItem('Force Close Kodi',KAYN_URL,9,KAYN_ICON,KAYN_FANART,'Intantly Force Closes Kodi')
#	addItem(name,url,mode,iconimage,fanart,description)


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR=lightblue]Kayn's Wizard[/COLOR]","[COLOR=lightblue]DOWNLOADING[/COLOR]",'', '[COLOR=lightblue]Please Wait[/COLOR]')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"[COLOR=lightblue]EXTRACTING FILES[/COLOR]")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    AskToKillKodi()
        
      
def InstantKillKodi():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass      		
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")            


def AskToKillKodi():
    choice = xbmcgui.Dialog().yesno('[COLOR=lightblue]DOWNLOAD COMPLETE[/COLOR]', 'Please force close kodi to continue.', 'Click "Close" to force Kodi to close.', nolabel='Return',yeslabel='Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass      		
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")            


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addItem(name,url,mode,iconimage,fanart,description):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
		liz.setProperty( "Fanart_Image", fanart )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )




##############################    END    #########################################

#########################################################################
#						Which mode to select							#
#########################################################################

if mode==None or url==None or len(url)<1:
        INDEX()
        
elif mode==1:
        wizard('FreshStart',FRESHSTART,'')

elif mode==2:
		wizard('FreshStart',VOID_BUILD,'')

elif mode==3:
		wizard('FreshStart',VOIDM_BUILD,'')

elif mode==4:
		wizard('FreshStart',VOID_UPDATE,'')

elif mode==5:
		wizard('FreshStart',VOIDM_UPDATE,'')

elif mode==6:
        wizard('FreshStart',VOID_UPGRADE,'')

elif mode==7:
		wizard('FreshStart',SOURCES,'')

elif mode==8:
		AskToKillKodi()

elif mode==9:
		InstantKillKodi()

if mode==None or url==None or len(url)<1:
    xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
else: xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
