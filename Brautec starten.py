#!/usr/bin/python3

#imports
import os,json,urllib.request,urllib.parse,glob,zipfile,sys,shutil
from os.path import expanduser
#functions
def we_are_frozen():
    return hasattr(sys, "frozen")

def module_path():
    if we_are_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)
#Variablen
brautecversion='3'
mcversion='1.6.4'
forgeversion='9.11.1.953'
modpackdownload='http://users.minecraft.name/maha'
modpackversiondownload=modpackdownload+'/Brautec'+brautecversion+'.json'
modpackmodsdownload=modpackdownload+'/mods'
modpackconfigdownload=modpackdownload+'/config'
if os.name=='nt':
    minecraftlauncherdownload='https://s3.amazonaws.com/Minecraft.Download/launcher/Minecraft.exe'
    minecraftclient=os.path.abspath(module_path()+'/minecraft_launcher.exe')
    mcpath=os.path.abspath(os.getenv('APPDATA')+'/.minecraft')
elif os.name=='mac':
    minecraftlauncherdownload='https://s3.amazonaws.com/Minecraft.Download/launcher/Minecraft.jar'
    minecraftclient=os.path.abspath(module_path()+'/minecraft_launcher.jar')
    mcpath=os.path.abspath(expanduser('~')+'/Library/Application Support/minecraft')
else:
    minecraftlauncherdownload='https://s3.amazonaws.com/Minecraft.Download/launcher/Minecraft.jar'
    minecraftclient=os.path.abspath(module_path()+'/minecraft_launcher.jar')
    mcpath=os.path.abspath(expanduser('~')+'/.minecraft')
mcprofiles=os.path.abspath(mcpath+'/launcher_profiles.json')
modpackpath=os.path.abspath(mcpath+'/modpacks/brautec3')
modspath=os.path.abspath(modpackpath+'/mods')
configpath=os.path.abspath(modpackpath+'/config')
versionspath=os.path.abspath(mcpath+'/versions')
modpackversionfile=os.path.abspath(modpackpath+'/Brautec'+brautecversion)
print('Lade aktuelle Versionsinformationen herunter...')
getmodpackjson=urllib.request.urlopen(modpackversiondownload)
modpackjson=getmodpackjson.read().decode()
if modpackjson:
   j_modpackjson=json.loads(modpackjson)
   mcversion=j_modpackjson['MinecraftVersion']
   forgeversion=j_modpackjson['ForgeVersion']
else:
    print('Updateserver nicht erreichbar')
    if os.path.exists(modpackpath):
        print('Installation nicht moeglich: Abbruch!')
        exit(1)
forgedownload='http://files.minecraftforge.net/maven/net/minecraftforge/forge/'+mcversion+'-'+forgeversion+'/forge-'+mcversion+'-'+forgeversion+'-installer.jar'
minecraftjardownload='https://s3.amazonaws.com/Minecraft.Download/versions/'+mcversion+'/'+mcversion+'.jar'
minecraftjsondownload='https://s3.amazonaws.com/Minecraft.Download/versions/'+mcversion+'/'+mcversion+'.json'
forgeversionspath=os.path.abspath(versionspath+'/'+mcversion+'-Forge'+forgeversion)
mcversionspath=os.path.abspath(versionspath+'/'+mcversion)
#Code
print('Suche Minecraft Ordner')
print(mcpath)
if os.path.isfile(mcprofiles):
    fo = open(mcprofiles, 'r')
    j_mcprofiles = json.loads(fo.read())
    fo.close()
    auth = list(j_mcprofiles['authenticationDatabase'])
    if not auth:
        print("Kein Minecraft Profil gefunden. Bitte den Minecraft Launcher starten und einloggen!")
        exit(1)
    if os.name != 'nt' or os.path.exists(os.getenv('programfiles(x86)','C:\\this dir does not exist')):
        j_mcprofiles['profiles']['Brautec'+brautecversion]={'name':'Brautec'+brautecversion, 'gameDir':modpackpath, 'javaArgs':'-XX:InitialHeapSize=512M -XX:MaxHeapSize=2G -XX:MaxPermSize=256M -XX:+AggressiveOpts -XX:+UseFastAccessorMethods','lastVersionId':mcversion+'-Forge'+forgeversion,'playerUUID':auth[0]}
    else:
        j_mcprofiles['profiles']['Brautec'+brautecversion]={'name':'Brautec'+brautecversion, 'gameDir':modpackpath, 'javaArgs':'-XX:InitialHeapSize=512M -XX:MaxHeapSize=1024M -XX:MaxPermSize=256M','lastVersionId':mcversion+'-Forge'+forgeversion,'playerUUID':auth[0]}
    j_mcprofiles['selectedProfile'] = 'Brautec3'
    fo = open(mcprofiles, 'w+')
    fo.write(json.dumps(j_mcprofiles))
    fo.close()
else:
    print('Du musst Minecraft wenigstens einmal mit dem aktuellen Minecraft Client starten und dich einloggen.')
    print('Diesen bekommst du auf der Seite https://minecraft.net/download')
    exit(1)
#Hier wird die Minecraft Version heruntergeladen
if not os.path.exists(mcversionspath):
    print('Erstelle Versionsordner')
    os.makedirs(mcversionspath)
    print('Lade Minecraft Version '+mcversion+' herunter...')
    mcjarfile=os.path.abspath(mcversionspath+'/'+mcversion+'.jar')
    urllib.request.urlretrieve(minecraftjardownload,mcjarfile )
    print(mcjarfile+' herunter geladen')
    print('Lade Minecraft Profil '+mcversion+' herunter...')
    mcjsonfile=os.path.abspath(mcversionspath+'/'+mcversion+'.json')
    urllib.request.urlretrieve(minecraftjsondownload,mcjsonfile )
    print(mcjsonfile+' herunter geladen')
#Hier wird die Forge Version heruntergeladen
if not os.path.exists(forgeversionspath):
    print('Lade Forge Installationsassistent herunter...')
    print('Der Assistent wird im Anschluss gestartet.')
    print('Bitte fuehre anschliessend eine Clientinstallation durch')
    forgeinstallerfile=os.path.abspath(module_path()+'/minecraftforge-installer-'+mcversion+'-'+forgeversion+'.jar')
    urllib.request.urlretrieve(forgedownload,forgeinstallerfile )
    print(forgeinstallerfile+' herunter geladen')
    print('Forge Installationsassistent wird nun ausgefuehrt')
    if os.name == 'nt':
        os.system('"'+forgeinstallerfile+'"')
    else:
        os.system('java -jar "'+forgeinstallerfile+'"')
    os.remove(forgeinstallerfile)
    if not os.path.exists(forgeversionspath):
        print('Forgesetup wurde scheinbar abgebrochen oder es trat ein Fehler auf.')
        print('Brautec'+brautecversion+' Installation wird abgebrochen')
        exit(1)
else:
    print('Benoetigte Forge Version ist bereits installiert: '+mcversion+'-Forge'+forgeversion)
#Versionscheck
if os.path.isfile(modpackversionfile):
    fo = open(modpackversionfile, 'r')
    localmodpackversion=fo.readline()
    fo.close()
else:
    localmodpackversion='0'
print('Aktuell installierte Version: '+localmodpackversion)
if modpackjson:
   if (int(j_modpackjson['version']) > int(localmodpackversion)):
       if os.path.exists(modspath):
            installedmods=glob.glob(modspath+'/*')
            for installedmod in installedmods:
                if (installedmod.lower().find('jar') != -1) or (installedmod.lower().find('zip') != -1):
                    if not any(os.path.basename(installedmod).lower() == mod['file'].lower() for mod in j_modpackjson['mods']):
                        print(os.path.basename(installedmod).lower()+' wird geloescht')
                        os.remove(installedmod)
            if os.path.exists(modspath+'/'+mcversion):
                if os.name == 'nt':
                    os.system('CMD /C RMDIR /S /Q "'+modspath+'/'+mcversion+'"')
                else:
                    shutil.rmtree(modspath+'/'+mcversion)
       else:
            os.makedirs(modspath)
       for mod in j_modpackjson['mods']:
          if os.path.isfile(os.path.abspath(modspath+'/'+mod['file'])):
              print(mod['name']+' ist aktuell')
          else:
              print(mod['name']+' wird heruntergeladen')
              urllib.request.urlretrieve(urllib.parse.quote(modpackmodsdownload+'/'+mod['file'],safe="%/:=&?~#+!$,;'@()*[]"),os.path.abspath(modspath+'/'+mod['file']))
       print('Einstellungen werden heruntergeladen')
       for config in j_modpackjson['config']:
           configdownloadpath=os.path.abspath(module_path()+'/'+config['file'])
           print('Downloade '+config['name'])
           print(urllib.parse.quote(modpackconfigdownload+'/'+config['file'],safe="%/:=&?~#+!$,;'@()*[]"))
           urllib.request.urlretrieve(urllib.parse.quote(modpackconfigdownload+'/'+config['file'],safe="%/:=&?~#+!$,;'@()*[]"),configdownloadpath)
           print('Entpacke '+config['name'])
           if config['overwrite']==0:
               overwrite=0
               zippedfiles=zipfile.ZipFile(configdownloadpath,'r').namelist()
               for zippedfile in zippedfiles:
                   if not os.path.isfile(os.path.abspath(modpackpath+'/'+zippedfile)):
                       overwrite=1
           else:
               overwrite=1
           if overwrite==1:
               zipfile.ZipFile(configdownloadpath,'r').extractall(modpackpath)
           else:
               print(config['name']+' existiert bereits und wird nicht ueberschrieben')
           os.remove(configdownloadpath)
       fo = open(modpackversionfile, 'w+')
       fo.write(str(j_modpackjson['version']))
       fo.close()
   else:
       print('Version ist aktuell')
else:
    print('Modpackinformationen konnten nicht geladen werden.')
    print('Brautec wird trotzdem gestartet.')
if not os.path.isfile(minecraftclient):
    urllib.request.urlretrieve(minecraftlauncherdownload,minecraftclient)
if os.name == 'nt':
    os.system('"'+minecraftclient+'"')
else:
   os.system('java -jar "'+minecraftclient+'"')
