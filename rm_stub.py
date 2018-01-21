#!/usr/bin/python
import datetime
import os
import sys

def has_query(query, string):
    for item in query:
        if string in item:
            return item[1]
    return False

def sku_error(sku):
    if sku == 'APA':
        return True
    return False

print "Content-type: application/xml\n"

doNetworkPermission = True
doScreenPermission = True
doQuality = False
doPreview = False
doInterval = False

guideJsonURLBase = '/core/v5/rights/mobitv/reference/5.0/'
default_skus = ['LIVE_1', 'LIVE_2', 'VODPROGRAM_1', 'VODSERVICE_EPISODES', 'VODPROGRAM_100_HOUR']
invalid = 'InvalidSKU'

#print "<font size=+1>Environment</font><\br>";
#for param in os.environ.keys():
#  print "<b>%20s</b>: %s<\br>" % (param,os.environ[param])
query = [ x.split('=') for x in os.environ['QUERY_STRING'].split('&') ]

skus = []
sku_arg = os.environ['PATH_INFO'].split('/')[-1].strip('.xml')
if sku_arg == 'available':
    f = has_query(query, 'filter_by')
    if f:
        skus = f.split(',')
    else:  
        skus = default_skus
elif sku_arg:
    skus = [sku_arg]
else:
    # Handle this...
    pass

response = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + '\n'
response += '<o-ex:rights xmlns:o-dd="http://odrl.net/1.1/ODRL-DD" xmlns:o-ex-mobi="http://www.mobitv.com/schemas/odrl_ex_cmp" xmlns:o-ex="http://odrl.net/1.1/ODRL-EX" xmlns:ns4="http://www.w3.org/2000/09/xmldsig#">' + '\n'

time_now = datetime.datetime.utcnow()
time_start = time_now - datetime.timedelta(minutes=5)
time_end = time_now + datetime.timedelta(minutes=10080) # one weak

for sku in skus:
    if not sku_error(sku):
        response += '<o-ex:agreement>' + '\n'
        response += '   <o-ex:context>' + '\n'
        response += '       <o-dd:uid>123456.67890.PKX</o-dd:uid>' + '\n'
        response += '       <o-dd:version>1.2.30-1232456</o-dd:version>' + '\n'
        response += '    </o-ex:context>' + '\n'
        response += '    <o-ex:asset o-ex:id="' + sku + '">' + '\n'
        response += '        <o-ex:context>' + '\n'
        response += '            <o-dd:uid>' + guideJsonURLBase + sku + '.json</o-dd:uid>' + '\n'
        response += '        </o-ex:context>' + '\n'
        response += '    </o-ex:asset>' + '\n'
        response += '    <o-ex:constraint>' + '\n'
        response += '        <o-dd:datetime>' + '\n'
        response += '            <o-dd:start>' + time_start.isoformat() + 'Z' + '</o-dd:start>' + '\n'
        response += '            <o-dd:end>' + time_end.isoformat() + 'Z' + '</o-dd:end>' + '\n'
        response += '        </o-dd:datetime>' + '\n'
        response += '    </o-ex:constraint>' + '\n'
        response += '    <o-ex:permission>' + '\n'
        response += '        <o-dd:play>' + '\n'
        response += '            <o-ex:constraint>' + '\n'
        response += '                <o-dd:datetime>' + '\n'
        response += '                    <o-dd:start>' + time_start.isoformat() + 'Z' + '</o-dd:start>' + '\n'
        response += '                    <o-dd:end>' + time_end.isoformat() + 'Z' + '</o-dd:end>' + '\n'
        response += '                </o-dd:datetime>' + '\n'
        response += '            </o-ex:constraint>' + '\n'

        if (doNetworkPermission):
            response += '            <o-ex:constraint>' + '\n'
            response += '                <o-ex:container type="in-or">' + '\n'
            response += '                    <o-dd:network o-ex:id="unknown"></o-dd:network>' + '\n'            
            response += '                    <o-dd:network o-ex:id="cdma"></o-dd:network>' + '\n'
            response += '                    <o-dd:network o-ex:id="gsm"></o-dd:network>' + '\n'
            response += '                    <o-dd:network o-ex:id="wifi"></o-dd:network>' + '\n'
            response += '                    <o-dd:network o-ex:id="wimax"></o-dd:network>' + '\n'
            response += '                    <o-dd:network o-ex:id="eth"></o-dd:network>' + '\n'
            response += '                </o-ex:container>' + '\n'
            response += '            </o-ex:constraint>' + '\n'

        if (doScreenPermission):
            response += '            <o-ex:constraint>' + '\n'
            response += '                <o-ex:container type="ex-or">' + '\n'
            response += '                    <o-dd:screen o-ex:id="Phone"></o-dd:screen>' + '\n'
            response += '                    <o-dd:screen o-ex:id="Tablet"></o-dd:screen>' + '\n'
            response += '                    <o-dd:screen o-ex:id="ExternalDisplay"></o-dd:screen>' + '\n'
            response += '                    <o-dd:screen o-ex:id="STB"></o-dd:screen>' + '\n'
            response += '                    <o-dd:screen o-ex:id="SmartTV"></o-dd:screen>' + '\n'
            response += '                    <o-dd:screen o-ex:id="HDCP"></o-dd:screen>' + '\n'
            response += '                </o-ex:container>' + '\n'
            response += '            </o-ex:constraint>' + '\n'

	if (doQuality):
            response += '            <o-ex:constraint>' + '\n'
            response += '                <o-ex-mobi:quality>' + '\n'
            response += '                    <o-ex-mobi:maxbitrate>2500</o-ex-mobi:maxbitrate>' + '\n'
            response += '                    <o-ex-mobi:maxheight>1480</o-ex-mobi:maxheight>' + '\n'
            response += '                    <o-ex-mobi:maxwidth>1320</o-ex-mobi:maxwidth>' + '\n'
            response += '                </o-ex-mobi:quality>' + '\n'
            response += '            </o-ex:constraint>' + '\n'

        if (doPreview):
            response += '            <o-ex:constraint>' + '\n'
            response += '                <o-ex-mobi:preview>' + '\n'
            response += '                    <o-ex:constraint>' + '\n'
            response += '                        <o-dd:range>' + '\n'
            response += '                            <o-dd:min>7</o-dd:min>' + '\n'
            response += '                            <o-dd:max>27</o-dd:max>' + '\n'
            response += '                        </o-dd:range>' + '\n'
            response += '                    </o-ex:constraint>' + '\n'
            response += '                </o-ex-mobi:preview>' + '\n'
            response += '            </o-ex:constraint>' + '\n'

        if (doInterval):
            response += '            <o-ex:constraint>' + '\n'
            response += '                <o-dd:interval>P1D</o-dd:interval>' + '\n'
            response += '            </o-ex:constraint>' + '\n'


        response += '            <o-ex:asset o-ex:idref="' + sku + '"/>' + '\n'
        response += '        </o-dd:play>' + '\n'
        response += '    </o-ex:permission>' + '\n'
        response += '</o-ex:agreement>'
    else:
        response += '<o-ex-mobi:error>';
        response += '    <o-ex:asset o-ex:id="' + sku + '">';
        response += '        <o-ex:context>';
        response += '            <o-dd:uid>' + guideJsonURLBase + sku + '.json</o-dd:uid>';
        response += '        </o-ex:context>';
        response += '    </o-ex:asset>';
        response += '    <o-ex-mobi:code>123456</o-ex-mobi:code>';
        response += '    <o-ex-mobi:message>Invaid SKU</o-ex-mobi:message>';
        response += '</o-ex-mobi:error>'; 

response += '</o-ex:rights>'
sys.stdout.write(response)
