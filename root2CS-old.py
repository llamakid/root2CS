#importing libraries that will be needed
import os
import json
import glob
import string
import pprint

template = {'animations':{'fadeinAnimation':{'type':'Animation','properties':[{'property':'alpha','animationFunction':'EaseInOut','duration':'2.0','delay':'0.6','repeatCount':'0','autoreverses':'false','fromValue':0.001,'toValue':1}]},'fadeOutAnimation':{'type':'Animation','properties':[{'property':'alpha','animationFunction':'EaseInOut','duration':'2.0','delay':'0','repeatCount':'0','autoreverses':'false','fromValue':1,'toValue':0.001}]}}, 'actions':{}, 'frames':[], 'metaData':{'applicationStartPage':'App_Pages','flurryAPIKey':'','shortTitle':'', 'startPage': 'App_Pages', 'title': '', 'serverPaths':{}},  'overlays':{}, 'pageSets':{'App_Pages':{'pages':[], 'transitionDuration':'0.5','transitionTypeNext': 'slide', 'transitionTypePrevious': 'slideBack'}},'pages':{}, 'screenSupport':{'screens':[{'fonts':[{'fontName':'georgia','fontSize':14,'name':'normal'}],'height':1024,'orientation':'Portrait','suffix':'','width':768},{'fonts':[{'fontName':'georgia','fontSize':12,'name':'normal'}],'height':480,'orientation':'Portrait','suffix':'-iphone','width':320},{'fonts':[{'fontName':'georgia','fontSize':12,'name':'normal'}],'height':960,'orientation':'Portrait','suffix':'-retina','width':640}],'useScreenRatio':'true'}}

ContentSpec = template

o = 'ContentSpec.json' #setting up the location of the output
f = open(o,"w")	#setting up var to open/create the template file and write to it

#open root.json and store the data into memory
rootFile = open('root.json').read() #open root.json 
rootData = json.loads(rootFile) #store data into memory
rootDict = rootData[1]
rootKeys = rootDict.keys()
pageKeys = rootDict['toc']

pageNames = []
pages = {}
overlays = {}
containerOverlays = {}

#adding the pages into the ContentSpec
for item in pageKeys:
	item = item.replace("section_","")
	pageNames.append(item + '_page')
	pages.update({item + '_page':{'frames':[],'image':'','overlays':[{'overlayId':item + '_container'}],'thumbnail':'','transitionTypeNext':'slide','backgroundColor':'#ffffff','title':item}})
	overlays.update({item:{'x':'0%','y':'0%','width':'100%','height':'100%','verticalAlign':'top','horizontalAlign':'left','relative':'parent','type':'webview','url':'pages/'+ item +'.html','bounce':'true'},'coverVideo':{'type':'video','video':'cover.mov','fullscreen':'false','x':'50%','y':'50%','relative':'screen','width':'100%','height':'100%','controlType':'none'},'mahb_container':{'x':'0%','y':'2%','width':'25%','height':'72%','horizontalAlign':'left','verticalAlign':'top','relative':'screen','type':'container','paging':'false','persistence':'page','overlays':[{'overlayId':'mahb_logo'}]},'mahb_logo':{'x':'12.39%','y':'6.54%','images':['mahb_logo.png'],'relative':'screen','type':'image','verticalAlign':'center','horizontalAlign':'center'}})
	containerOverlays.update({item + '_container':{'type':'container','relative':'screen','horizontalAlign':'center','verticalAlign':'center','userScrolling':'vertical','width':'100%','height':'100%','x':'50%','y':'50%','overlays':[{'overlayId':item}],'paging':'true'}})
	

ContentSpec['pageSets']['App_Pages']['pages'] = pageNames
ContentSpec['pages'] = pages
ContentSpec['overlays'] = dict(overlays.items() + containerOverlays.items())

#write the file in json format
p = json.dumps(ContentSpec, sort_keys=True, indent=2)
print >> f, p