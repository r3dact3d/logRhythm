# logRhythm
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

This will be missing the actual linux rpms and solaris tars, but listed below are what this script will support:                rhel-scsm-7.1.6.8004-1.el6.x86_64.rpm
rhel-scsm-7.1.6.8004-1.el5.i686.rpm    
rhel-scsm-7.1.6.8004-1.el5.x86_64.rpm  
rhel-scsm-7.1.6.8004-1.el6.i686.rpm    
solaris9_10_11_sparc.zip
solaris9_10_11_scsm7.1.6.8004_sparc.tar
solaris10_11_x86.zip

IMPORTANT NOTE:
If you change the name of the actual script or tar file, the cleanup module will BREAK!  < I am not responsible if you delete something unintended if you don't use this script as written.
ie ->  see tarFile and workingDir variables below:
def cleanup():
    tarFile = '/tmp/logRhythm_g6.tar'
    workingDir = '/tmp/logRhythm_g6/'
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
