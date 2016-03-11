#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib, urlparse, re, sys, os, sqlite3

debug_mode = Addon.getSetting("debug_mode") == 'true'


def ConstructRequest(params):
	return '%s?%s' % (p, urllib.urlencode(params))

def GetParams(sparams):
	sppc = sparams.partition('?')
	if sppc[2]: sparams = sppc[2]
	params = urlparse.parse_qs(sparams)
	params = {key: params[key][0] for key in params}
	#print params
	return params

def AddRow(name, params = {}, IF = True):
	li = xbmcgui.ListItem(name)
	uri = ConstructRequest(params)
	xbmcplugin.addDirectoryItem(h, uri, li, IF)


def Main(params):
	AddRow('Import DB', 'ImportDB')
	
	xbmcplugin.endOfDirectory(h)


def ImportDB():
	dbfile = xbmcgui.Doalog().browse(1, 'DB to import', 'files', '.db')
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute('SELECT Title, Season, Epidode, EpisodeDescr, PlayCount, TimeStamp, Duration, Watched FROM WatchStatus')
	t_ws = c.fetchall()








if debug_mode: print sys.argv
h = int(sys.argv[1])
p = sys.argv[0]
params = GetParams(sys.argv[2])
#print params
if 'func' in params: func = params['func']
else: func = 'Main'
pfunc = globals()[func]
pfunc(params)
