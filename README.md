Addon watchstates handler
=========================
Module addon for Kodi enables storing watchstates (watched/partially watched) for video addons separately from Kodi DB.
Generally, Kodi stores above watchstates, identifing it by paths (links) or virtual paths. Links, in reality, may be changed over time on sites that may also change the virtual paths in addons. This module maintains the above watchstates, identifying them by one of the three combinations:

 - a title,
 - a combination of title / season number / series number,
 - a combination of title / season number / series title or date.

The first option is suitable for movies or any video clips. Second - for the TV series. The third - for the TV series, when the series number is not specified, but we know only the title or release date of the series.

This module can be used by installing it in parallel with the addon, or by including it as an internal library. (Note: The second option I have not tested yet). Other advantages, in addition to the immutability of the watchstates marks with the time, is the sharing of watchstates DB between addons using the module, and saving those marks when cleaning the Kodi library.

At this moment, there is a necessary condition for the use of the module: the importing addons must use setResolvedUrl function for video playback. This is due to only this function correctly maintains the watchstates marks of viewing videos using the virtual paths in Kodi DB. Since the module is not the service-addon, it must use this information to then associate it with the above-described combinations. Also, I must to add that the module only tested when using virtual paths kind of plugin://... For real paths, most likely it will not work, however this option I have not tested yet.

Usage:
------
The following instruction explains how to embed and use the module in an addons.  
At first import and initialize the module:

    import AWSHandler
    AWSHandler.InitDB()

To get information about the status of a ListItem, create a dictionary with one of the three combinations:
 - a title,
 - a combination of a title / season number / series number,
 - a combination of a title / season number / series title or date,  
and request for watchstate information:

    info = {'title': title, 'season': season, 'episode': episode, 'episode_info': episode_info}
    res = AWSHandler.CheckWS(info)

here, title - is unicode-string with the movie or TV show title,  
episode_info - unicode-string with the title of a series or a series release date,  
season and episode - integer or string with the season number and the series number. Season number can be not specified (i.e, if the season is not known, it is better not to specify it, because season 1 will have a different identifier).

Set the watchstate mark (I plan to move it inside the module in future):

    if res:
        if res ['wflag']: listitem.setInfo(type = 'video', infoLabels = {'playcount': 1, 'overlay': 5})
        else:
            listitem.setProperty('ResumeTime', res['resumetime'])
            listitem.setProperty('TotalTime', res['totaltime'])

When playback is started, add the above-described combination 'info' for ListItem into the update queue. This can be done both before and after running. After is better, as this will not waste time at playback startup:

    xbmcplugin.setResolvedUrl(h, True, listitem)
    AWSHandler.QueueWS(info)

**Development plans:**

- Add an interface for importing another DB.
- Add an interface to manage watchstates, including the ability to specify alternative names (aliases) of movies / TV series.
- Add the possibility to process ListItem in CheckWS(), setting the mark automatically.
- Add CheckWSMany() function to process array of ListItems.
- Move the excessive log messages into the debug mode.

The module was tested by me, but it is on alpha-stage because not all functions from the development plans are implemented yet.


