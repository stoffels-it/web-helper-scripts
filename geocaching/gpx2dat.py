#!/usr/bin/python
# coding: utf-8
#
# Read files which contain your found geocaches from different platforms as
# gpx data with sorting by date, finding duplicates
#
# 2016 - Sarah Stoffels
#

import sys
from xml.dom.minidom import parse
import yaml

with open("gc_config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    for section in cfg:
        gc_username = cfg["gc_username"]
	oc_de_username = cfg["oc_de_username"]

curr_id = 2

def get_xmltext(parent, subnode_name):
    node = parent.getElementsByTagName(subnode_name)[0]
    return "".join([ch.toxml() for ch in node.childNodes])


def format_time(time):
    year = time[:4]
    month = time[5:7]
    day = time[8:10]
    hour = time[11:13]
    minute = time[14:16]
    sec = time[17:19]
    return year + month + day + hour + minute + sec


all_wps = {}
gc_ids = [] 

iterargv = iter(sys.argv)
next(iterargv)
for arg in iterargv:

    dom = parse(arg)
    these_wps = {}

    author = get_xmltext(dom, "author")
    if (author == "Groundspeak"):
	username = gc_username
    elif (author == "Opencaching.de"):
	username = oc_de_username

    for node in dom.getElementsByTagName("wpt"):

	gc_id = ""
	name = get_xmltext(node, "name")
	urlname = get_xmltext(node, "urlname")

	for child in node.childNodes:
	    if (child.nodeName == "groundspeak:cache"):
		gs_cache = child
	        prop_container = get_xmltext(gs_cache, "groundspeak:container")
	        prop_difficulty = get_xmltext(gs_cache, "groundspeak:difficulty")
	        prop_terrain = get_xmltext(gs_cache, "groundspeak:terrain")
                long_description = get_xmltext(gs_cache, "groundspeak:long_description")
    
                if (author == "Opencaching.de"):
		    try:
		        indx = long_description.index("GC")
		    except Exception as e:
		        indx = -1
		    if (indx != -1):
		        gc_id = long_description[indx:indx+7]
			try:
			    whitespace = gc_id.index(" ")
			except Exception as e:
			    whitespace = -1
		        if (whitespace != -1):
			    gc_id = ""

	for child in gs_cache.childNodes:
	    if (child.nodeName == "groundspeak:logs"):
		gs_logs = child
	
	for child in gs_logs.childNodes:
	    if (child.nodeName == "groundspeak:log"):
		finder = get_xmltext(child, "groundspeak:finder")
		if (finder == username):
	            log_time = format_time(get_xmltext(child, "groundspeak:date"))
	            while log_time in these_wps:
		        log_time = str(int(log_time) + 1)

                    these_wps[log_time] = {}
	            log_text = format_time(get_xmltext(child, "groundspeak:text"))
		    break

	these_wps[log_time]["log_text"] = log_text
	these_wps[log_time]["prop_container"] = prop_container
	these_wps[log_time]["prop_difficulty"] = prop_difficulty
	these_wps[log_time]["prop_terrain"] = prop_terrain
        these_wps[log_time]["name"] = name
	these_wps[log_time]["urlname"] = urlname
	if (gc_id != ""):
	    these_wps[log_time]["gc_id"] = gc_id
	    gc_ids.append(gc_id)

    all_wps = dict(all_wps.items() + these_wps.items()) 


for key in sorted(all_wps.iterkeys()):
    found = False
    for gc_id in gc_ids:
        if (gc_id == all_wps[key]["name"]):
	    found = True
    
    if not found:
	print "ID: " + str(curr_id)
	year = key[:4]
	month = key[4:6]
	day = key[6:8]
	print "Date: " + day + "." + month + "." + year
	waypoint = all_wps[key]["name"]
	if ("gc_id" in all_wps[key]):
	    waypoint = waypoint + ", " + all_wps[key]["gc_id"]
	print "Waypoint: " + waypoint 
	print "Title: " + all_wps[key]["urlname"]
	prop_container = all_wps[key]["prop_container"]
	if (prop_container == "Not chosen"):
	    prop_container = ""
	print "Tag: D" + all_wps[key]["prop_difficulty"] + " T" + all_wps[key]["prop_terrain"] + " " + prop_container
	print "----"
	curr_id = curr_id + 1
