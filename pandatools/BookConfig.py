import os
import re
import commands
import ConfigParser

sectionName = 'book'
confFile = os.path.expanduser('%s/pbook.cfg' % os.environ['PANDA_CONFIG_ROOT'])


# create config file when missing
if not os.path.exists(confFile):
    parser=ConfigParser.ConfigParser()
    parser.add_section(sectionName)
    # set dummy time
    parser.set(sectionName,'last_synctime','')
    confFH = open(confFile,'w')
    parser.write(confFH)
    confFH.close()

# get config
def getConfig():
    # instantiate parser
    parser=ConfigParser.ConfigParser()
    parser.read(confFile)
    # config class
    class _bookConfig:
        pass
    bookConf = _bookConfig()
    # expand sequencer section
    for key,val in parser.items(sectionName):
        # convert int/bool
        if re.search('^\d+$',val) != None:
            val = int(val)
        elif re.search('true',val,re.I) != None:
            val = True
        elif re.search('false',val,re.I) != None:
            val = False
        # set attributes    
        setattr(bookConf,key,val)
    # return
    return bookConf


# update
def updateConfig(bookConf):
    # instantiate parser
    parser=ConfigParser.ConfigParser()
    parser.read(confFile)
    # set new values
    for attr in dir(bookConf):
        if not attr.startswith('_'):
            val = getattr(bookConf,attr)
            if val != None:
                parser.set(sectionName,attr,val)
    # keep old config
    status,out = commands.getstatusoutput('mv %s %s.back' % (confFile,confFile))
    if status != 0:
        print "WARNING : cannot make backup for %s" % confFile
        return
    # update conf
    conFH = open(confFile,'w')
    parser.write(conFH)
    # close
    conFH.close()
