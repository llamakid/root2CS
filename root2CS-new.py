#importing libraries that will be needed
import os
import json
import sys

bundle_path = sys.argv[1]

# look for root.json in the bundle
root_dot_json = os.path.join(bundle_path, 'root.json')
if not os.path.isfile(root_dot_json):
    sys.exit('Error: Cannot find root.json')

# open the content spec template
file = open('ContentSpecTemplate.json', 'r')
ContentSpec = json.loads(file.read())
file.close()

#open root.json and store the data into memory
rootFile = open(root_dot_json, 'r') #open root.json 
rootData = json.loads(rootFile.read()) #store data into memory
rootFile.close()
rootDict = rootData[1]
rootKeys = rootDict.keys()
pageKeys = rootDict['toc']

pageNames = []
pages = {}
overlays = {}
containerOverlays = {}
items_count = 0
toc_btn_list = []

#adding the pages into the ContentSpec
for item in pageKeys:
    item = item.replace("section_","")
    pageNames.append(item + '_page')
    toc_btn_num = str(items_count).zfill(2)

    if item in rootDict['pages']:
        page_thumbnail = rootDict['pages'][item][1]['pageImage']
    else:
        page_thumbnail = ''

    pages.update(
    {
        item + '_page':{
            'frames':[],
            'image':'',
            'overlays':[
                {'overlayId': item + '_container'},
                {"overlayId": "musicRunAction"},
                {"overlayId": "mahbRunAction"},
                {"overlayId": "runActionReplaceToc_btn_pg_" + toc_btn_num}
            ],
            'thumbnail': page_thumbnail,
            'transitionTypeNext':'slide',
            'backgroundColor':'#ffffff',
            'title': item
        }
    })

    if items_count == 1:
        pages[item + '_page']['overlays'].append({'overlayId': 'overlay1'})
        pages[item + '_page']['overlays'].append({'overlayId': 'topnavContainer'})

    overlays.update(
    {
        item: {
            'x':'0%',
            'y':'0%',
            'width':'100%',
            'height':'100%',
            'verticalAlign':'top',
            'horizontalAlign':'left',
            'relative':'parent',
            'type':'webview',
            'url':'pages/'+ os.path.basename(rootDict['pages'][item][1]['pageFilename']),
            'bounce':'true'
        },
        item + '_container': {
            'type':'container',
            'relative':'screen',
            'horizontalAlign':'center',
            'verticalAlign':'center',
            'userScrolling':'vertical',
            'width':'100%',
            'height':'100%',
            'x':'50%',
            'y':'50%',
            'overlays':[
                {'overlayId':item}
            ],
            'paging':'true'
        },
        "toc_btn_" +toc_btn_num: {
            "x": "70%",
            "y": "35px",
            "horizontalAlign": "center",
            "verticalAlign": "center",
            "images": ["topbar_btn_contents copy.png"],
            "imagesDown": ["topbar_btn_contents_tap.png"],
            "relative": "parent",
            "type": "Button",
            "toggle": True,
            "actions": [
                {
                    "action": "#spawnOnce",
                    "trigger": "TouchDown",
                    "data": {
                        "overlayId": "overlay4"
                    }
                },
                {
                    "action": "animate",
                    "trigger": "toggleOn",
                    "target": "overlay4",
                    "data": {
                        "animationId": "animation5"
                    }
                },
                {
                    "action": "animate",
                    "trigger": "toggleOff",
                    "target": "overlay4",
                    "data": {
                        "animationId": "animation6"
                    }
                },
                {
                    "action": "bringToFront",
                    "trigger": "touchUpInside",
                    "target": "overlay4"
                },
                {
                    "action": "gotoPageIndexAction",
                    "target": "overlay2",
                    "delay": 0.5,
                    "data": {
                        "pageIndex": items_count
                    }
                }
            ]
        },
        "runActionReplaceToc_btn_pg_"+toc_btn_num: {
            "type": "runActionLogic",
            "actions": [
                {
                    "action": "replaceOverlays",
                    "trigger": "now",
                    "target": "topnavContainer",
                    "data": {
                        "overlays": [
                            {"overlayId": "library_btn"},
                            {"overlayId": "store_btn"},
                            {"overlayId": "cover_btn"},
                            {"overlayId": "multimedia_btn"},
                            {"overlayId": "toc_btn_" + toc_btn_num}
                        ]
                    }
                }
            ]
        }
    })

    toc_btn_list.append("toc_btn_" +toc_btn_num)

    items_count = items_count + 1

# add this action with targets to trans_close_btn
ContentSpec['overlays']['trans_close_btn']['actions'].append({
    "action": "toggleButtonOff", 
    "targets": toc_btn_list, 
    "trigger": "touchUpInside"
})

# add videos overlays
for video in rootDict['videos']:
    overlays.update(
    {
        'Video_'+video: {
            'controlType': 'fullscreen',
            'fullScreen': True,
            'height': '100%',
            'relative': 'screen',
            'type': 'video',
            'video': 'video/'+os.path.basename(rootDict['videos'][video][1]['videoURL']),
            'width': '100%',
            'x': '50%',
            'y': '50%'
        },
        'Video_'+video+'_button': {
            'type': 'button',
            'images': ['buttonClear.png'],
            'x': '0%',
            'y': '0%',
            'relative': 'parent',
            'horizontalAlign': 'left',
            'verticalAlign': 'top',
            'target': 'Video_'+video
        }
    })

# add imagegallery overlays
gallery_count = 0
for gallery in rootDict['galleries']:
    gallery_count = gallery_count + 1
    gallery_count_str = str(gallery_count).zfill(2)
    overlays.update(
    {
        'ImageGallery_'+gallery_count_str: {
            'type': 'imagegallery',
            'images': [],
            'overlays': [],
            'backButton': 'close_buttonWhite.png',
            'pagingIndicatorOff': '',
            'pagingIndicatorOn': '',
            'swipeAudio': '',
            'captionAudio': ''
        },
        'ImageGallery_'+gallery_count_str+'_button': {
            'type': 'button',
            'images': ['buttonClear.png'],
            'x': '0%',
            'y': '0%',
            'relative': 'parent',
            'horizontalAlign': 'left',
            'verticalAlign': 'top',
            'target': 'ImageGallery_'+gallery_count_str
        },
        'ImageGallery_'+gallery_count_str+'_caption': {
            'type': 'caption',
            'x': '50%',
            'y': '50%',
            'relative': 'parent',
            'horizontalAlign': 'left',
            'verticalAlign': 'top',
            'text': ''
        }
    })

    for g in rootDict['galleries'][gallery]:
        overlays['ImageGallery_'+gallery_count_str]['images'].append(g['image'])
        overlays['ImageGallery_'+gallery_count_str]['overlays'].append('ImageGallery_'+gallery_count_str+'_caption')

# create tab overlays
# and containers to hold these overlays
# but first generate tab list in order
tab_items = {}
tab_container_list = []
for persNav in rootDict['persNavs']:
    section_name = rootDict['persNavs'][persNav]['navSection'].replace("section_","")
    tab_items.update(
    {
        rootDict['persNavs'][persNav]['navIndex']: {
            "title": rootDict['persNavs'][persNav]['navTitle'],
            "section": section_name
        }
    })

    overlays.update(
    {
        'tab_container_'+section_name: {
            'height': '72%', 
            'horizontalAlign': 'center', 
            'overlays': [
                {'overlayId': 'mahb_logo'}
            ], 
            'paging': 'false', 
            'persistence': 'page', 
            'relative': 'screen', 
            'type': 'container', 
            'verticalAlign': 'center', 
            'width': '25%', 
            'x': '13.41%', 
            'y': '40.23%'
        }
    })

    # add containers to a list
    # we're gonna need them later
    tab_container_list.append('tab_container_'+section_name)

tab_pos_y = 17
tab_count = 0
for tab in tab_items:
    tab_name = tab_items[tab]['section']
    tab_title = tab_items[tab]['title']
    tab_count = tab_count + 1
    if tab_count > 1:
        tab_pos_y = tab_pos_y + 5
    overlays.update(
    {
        'tab_'+tab_name: {
            'horizontalAlign': 'center', 
            'images': [
                'pages/MaHBImages/mahb_tab_'+tab_title+'.png'
            ], 
            'relative': 'screen', 
            'target': tab_name+'_page', 
            'type': 'button', 
            'verticalAlign': 'center', 
            'x': '12%', 
            'y': str(tab_pos_y)+'%'
        },
        'tab_'+tab_name+'_on': {
            'horizontalAlign': 'center', 
            'images': [
                'pages/MaHBImages/mahb_tab_'+tab_title+'_on.png'
            ], 
            'relative': 'screen', 
            'target': tab_name+'_page', 
            'type': 'button', 
            'verticalAlign': 'center', 
            'x': '12%', 
            'y': str(tab_pos_y)+'%'
        }
    })

    # update mahbRunAction targets
    ContentSpec['overlays']['mahbRunAction']['actions'][0]['targets'].append('tab_container_'+tab_name)

    pages[tab_name+'_page']['overlays'].append(
        {
            'overlayId': 'tab_container_'+tab_name,
            'persistence': 'application'
        })

    for tbl in tab_container_list:
        if 'tab_container_'+tab_name == tbl:
            overlays[tbl]['overlays'].append({'overlayId': 'tab_'+tab_name+'_on'})
        else:
            overlays[tbl]['overlays'].append({'overlayId': 'tab_'+tab_name})

# add new json items to ContentSpec
ContentSpec['pageSets']['App_Pages']['pages'] = pageNames
ContentSpec['pages'] = pages
ContentSpec['overlays'].update(dict(overlays.items()))

#write the file in json format
file = open(os.path.join(bundle_path, 'ContentSpec.json'), "w")
file.write(json.dumps(ContentSpec, indent=4, sort_keys=True))
file.close()
