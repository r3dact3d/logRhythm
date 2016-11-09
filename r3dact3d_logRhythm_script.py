#!/usr/bin/env python
# written by brady r3dact3d
# currently only supports RHEL 5/6 and Solaris
# contact brady to add support for other distros - will work for redbulls
#
# This Script will do the following logic:
# 1. Get OS version, hostname, ip address, architect and use the agent
#       install pkg.
# 2. If pkg is not installed it will install it and start it
# 3. If syslog or rsyslog is not configured it will config it
# 4. If scsm.ini is incomplete or missing it will fix it < best to double check
#       correct ip is used if multiple interfaces exists...ie data and mgmt
# 5. Validate all is good and clean up after done.
#
# Some reasons for not working even after this script... check route to Mediator
#       sometimes port 443 is blocked.
#You HAVE TO RUN THIS SCRIPT AS MR. ROOT

import platform
import time
import os
import socket

def getVersions(osVers):
    print '----------------------------------------------------'
    print '''Checking host platform and version for compatibility...
Success: ''' + osVers
    print '----------------------------------------------------'
    time.sleep(2)
    if 'el5' in osVers:
        print '----------------------------------------------------'
        print 'Passed! This is RHEL 5 x86_64, configuring myself...'
        time.sleep(2)
        rpmVers = 'el5'
        return rpmVers
    elif 'el6' in osVers:
        print '----------------------------------------------------'
        print 'Passed! This is RHEL 6, configuring myself...'
        time.sleep(2)
        rpmVers = 'el6'
        return rpmVers
    elif 'SunOS' in osVers:
        print '----------------------------------------------------'
        print 'Passed! This is SunOS, configuring myself...'
        time.sleep(2)
        rpmVers = 'solaris'
        return rpmVers
    else:
        print '----------------------------------------------------'
        print '''FAILED! Version of OS is not compatible with this script.
This platform is %s''' % (osVers)
        exit(0)

def getBit(osVers):
    if 'x86_64' in osVers:
        print '------------------------------'
        print 'This Linux is 64 bit... configuring pkg'
        bitVers = 'x86_64'
        return bitVers
    elif 'i686' in osVers:
        print '------------------------------'
        print 'This Linux is i686... configuring pkg'
        bitVers = 'i686'
        return bitVers
    elif 'sparc' in osVers:
        print '------------------------------'
        print 'This Solaris is sparc... configuring pkg'
        bitVers = 'sparc'
        return bitVers
    else:
        print '------------------------------'
        print 'This Solaris is x86... configuring pkg'
        bitVers = 'x86'
        return bitVers

def getLogconf(rpmVers):
    if rpmVers == 'el5':
        logConf = '/etc/syslog.conf'
        return logConf
    elif rpmVers == 'el6':
        logConf = '/etc/rsyslog.conf'
        return logConf
    elif rpmVers == 'solaris':
        logConf = '/etc/syslog.conf'
        return logConf
    else:
        print '''FAILED! No versions match the type we are looking for!
  Please ensure this is RHEL 5, RHEL 6, or Solaris machine.'''

def getLog(rpmName):
    if 'rhel' in rpmName:
        logFile = '/var/log/messages'
        return logFile
    elif 'solaris' in rpmName:
        logFile = '/var/adm/messages'
        return logFile
    else:
        print 'Something went wrong and my brain is to hot to know what.'
        exit(0)

def rpmName(rpmVers, bitVers):
    if rpmVers == 'solaris' and bitVers == 'sparc':
        rpmName = '%s9_10_11_%s.zip' % (rpmVers, bitVers)
        return rpmName
    elif rpmVers == 'solaris' and bitVers == 'x86':
        rpmName = '%s10_11_%s.zip' % (rpmVers, bitVers)
        return rpmName
    else:
        rpmName = 'rhel-scsm-7.1.6.8004-1.%s.%s.rpm' % (rpmVers, bitVers)
        return rpmName
    print rpmName

def startPkg(rpmName):
    if 'rhel' in rpmName:
        startCmd = '/sbin/service scsm restart'
        startProc = os.popen(startCmd)
        #startResult = str(startProc.read())
        #print startResult
    elif 'solaris' in rpmName:
        startCmd = '/opt/logrhythm/scsm/bin/scsm stop && /opt/logrhythm/scsm/bin/scsm start'
        startProc = os.popen(startCmd)
        #startResult = str(startProc.read())
        #print startResult
    else:
        print 'Something went wrong and my brain is to hot to know what.'
        exit(0)

def installPkg(rpmName):
    try:
        if 'rhel' in rpmName:
            print 'I have been instructed to install %s' % rpmName
            installCmd = '/bin/rpm -ivh /tmp/logRhythm_g6/' + rpmName
            installProc = os.popen(installCmd)
            installResult = str(installProc.read())
            print installResult
    except:
        pass
    try:
        if 'solaris' in rpmName:
            print 'I have been instructed to install %s' % rpmName
            installCmd = 'cd /tmp/logRhythm_g6/;/usr/bin/unzip %s;/bin/tar xvf solaris*scsm*.tar;pkgadd -d . scsm' % rpmName
            installProc = os.popen(installCmd)
            installResult = str(installProc.read())
            print installResult
    except:
        pass

def checkLinuxPkg(rpmName):
    checkRPM = '/bin/rpm -qa | grep -i scsm | grep -v grep'
    checkProc = '/bin/ps -ef | grep -i scsm | grep -v grep'
    runcheckRPM = os.popen(checkRPM)
    rpmResult = str(runcheckRPM.read())
    runcheckProc = os.popen(checkProc)
    procResult = str(runcheckProc.read())
    if 'scsm' in rpmResult and procResult:
        print 'LogRhythm is installed and running.'
        time.sleep(2)
    elif 'scsm' in rpmResult and not procResult:
        print 'LogRhythm is installed, but NOT running'
        print 'I am starting now, cause I\'m awesome sauce...'
        time.sleep(2)
        startPkg(rpmName)
    else:
        print 'LogRhythm is NOT installed, Your\'s Truly will install it...'
        time.sleep(2)
        installPkg(rpmName)

def checkSolarisPkg(rpmName):
    checkPkg = '/usr/bin/pkginfo scsm'
    runcheckPkg = os.popen(checkPkg)
    pkgResult = str(runcheckPkg.read())
    checkProc = '/bin/ps -ef | grep -i scsm | grep -v grep'
    runcheckProc = os.popen(checkProc)
    procResult = str(runcheckProc.read())
    if 'scsm' in pkgResult and procResult:
        print 'LogRhythm is installed and running.'
        time.sleep(2)
    elif 'scsm' in pkgResult and not procResult:
        print 'LogRhythm is installed, but NOT running'
        print 'I am starting now, cause I\'m awesome sauce...'
        time.sleep(2)
        startPkg(rpmName)
    else:
        print 'LogRhythm is NOT installed, Your\'s Truly will install it...'
        time.sleep(2)
        installPkg(rpmName)

def checkPkg(rpmVers, rpmName):
    if rpmVers == 'solaris':
        print 'Checking if LogRhythm is installed and Configured - solaris'
        time.sleep(2)
        print '------------------------------------------------------------'
        checkSolarisPkg(rpmName)
    elif rpmVers == 'el6' or 'el5':
        print 'Checking if LogRhythm is installed and Configured - linux'
        time.sleep(2)
        print '-----------------------------------------------------------'
        checkLinuxPkg(rpmName)
    else:
        print 'Something has gone wrong!'
        exit(0)

def checkConfig(logConf, rpmName):
    logger = 'logr1'
    confFile = open(logConf, 'a+')
    data = '''
*.debug                                         @your.mediator.net
auth.info                                       @your.mediator.net
audit.notice                                    @your.mediator.net
'''
    if logger in confFile.read():
        print '----------------------------'
        print '%s is already configured.' % logConf
        time.sleep(2)
        confFile.close()
    elif 'env1' in confFile.read():
        print '----------------------------'
        print '%s is configured wrong. I will fix it!' % logConf
        confFile.write(data)
        print 'I will need to restart SCSM process, I am smart enough!'
        time.sleep(2)
        startPkg(rpmName)
        confFile.close()
    else:
        print '----------------------------'
        print '%s is not configured. I will configure it for you!' % logConf
        time.sleep(2)
        confFile.write(data)
        print 'I will need to restart SCSM process, I am smart enough!'
        time.sleep(2)
        startPkg(rpmName)
        confFile.close()

def configIni(mediator, iface, iniFile_orig, rpmName):
    #Don't tell python we gonna use perl below
    perlCmd = "perl -p -i -e  's/ClientAddress=0/ClientAddress=" + iface + "/' " + iniFile_orig + "; perl -p -i -e  's/Host=CHANGE_THIS/Host=" + mediator + "/' " + iniFile_orig
    print '-----------------------------------------------'
    print 'Found IP Address to configure ini file as ' + iface
    time.sleep(2)
    if iface == '127.0.0.1':
        print 'This IP will NOT work for this scsm.ini file'
    else:
        print '---------------------------------------------'
        print 'Customizing scsm.ini for you, please validate correct IP is used!'
        os.system(perlCmd)
        startPkg(rpmName)

def checkIni(hostName, rpmName):
    iniFile_orig = '/opt/logrhythm/scsm/config/scsm.ini'
    iniFile_new = '/tmp/logRhythm/scsm.ini'
    existsCheck = os.path.exists(iniFile_orig)
    # Get IP address if needed for .ini file
    iface = socket.gethostbyname(socket.gethostname())
    mediator = 'YOUR MEDIATOR IP'
    if existsCheck == True:
        print '----------------------------------------------------------'
        print 'SCSM.INI is present, I will check config for you...'
        time.sleep(2)
        openiniFile_orig = open(iniFile_orig, 'r')
        if iface and mediator in openiniFile_orig.read():
            print '----------------------------------------------------'
            print 'SCSM.INI is configured for this host!'
            openiniFile_orig.close()
            print '##############################################'
            print 'Looks like this host is GOOD, but I will check log anyways...'
        else:
            print '------------------------------------------------------'
            print 'Configuring SCSM.INI for you...'
            configIni(mediator, iface, iniFile_orig, rpmName)
            openiniFile_orig.close()
    else:
        print '----------------------------------------------------------'
        print 'SCSM.INI is not present, I will create it for you...'
        os.system('cp ' + iniFile_new + ' ' + iniFile_orig)
        print '---------------------------------------------------'
        print 'Rechecking if SCSM.INI is present now.'
        if existsCheck == True:
            openiniFile_orig = open(iniFile_orig, 'r')
            configIni(mediator, iface, iniFile_orig, rpmName)
            openiniFile_orig.close()

def checkLog(logFile, hostName):
    time.sleep(2)
    logFile_open = open(logFile, 'r')
    standard = 'LogRhythm Agent'
    bad = 'Failed connection attempt to Mediator'
    good = 'Acceptance pending message received for System Monitor Agent'
    if 'HOSTNAME=' + hostName and standard and good in logFile_open.read():
        print '------------------------------'
        print 'CONGRATS, all is peachy in the world'
        print 'Check scsm.ini or ports'
        logFile_open.close()
    elif 'HOSTNAME=' + hostName and standard and bad in logFile_open.read():
        print '-------------------------------------'
        print 'ERROR - Failed connection attempt to Mediator'
    else:
        print '-------------------------------'
        print 'OOPS, please check %s, something isn\'t right!' % logFile
        logFile_open.close()

def cleanup():
    tarFile = '/tmp/logRhythm_r3dact3d.tar'
    workingDir = '/tmp/logRhythm_r3dact3d/'
    print '-----------------------------'
    print 'Attempting to remove evidence!'
    if os.path.exists(workingDir):
        files = os.listdir(workingDir)
        for scriptFile in files:
            path = workingDir + scriptFile
            os.unlink(path)
        os.rmdir(workingDir)
        os.unlink(tarFile)
        print 'PASS: All evidence removed!'

osVers = platform.platform()
hostName = platform.node()
rpmVers = getVersions(osVers)
bitVers = getBit(osVers)
logConf = getLogconf(rpmVers)
rpmName = rpmName(rpmVers, bitVers)
logFile = getLog(rpmName)
checkPkg = checkPkg(rpmVers, rpmName)
checkConfig = checkConfig(logConf, rpmName)
checkIni = checkIni(hostName, rpmName)
checkLog = checkLog(logFile, hostName)
cleanup()
