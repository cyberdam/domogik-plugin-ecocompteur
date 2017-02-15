# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Ecocompteur 

Implements
==========

- Ecocompteur

@author: Fritz <fritz.smh@gmail.com>
@copyright: (C) 2007-2014 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import traceback
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import json
from datetime import datetime

ECOCOMPTEURURL = "/inst.json"


class EcocompteurException(Exception):
    """
    Ecocompteur exception
    """

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class Ecocompteur:
    """ Ecocompteur
        Frame format information in the read() function description
    """

    def __init__(self, log, callback, stop, device, device_id, interval):
        """ Init Ecocompteur object
            @param log : log instance
            @param callback : callback
            @param stop : stop flag
            @param device : teleinformation device
            @param device_id : domogik device id
            @param interval : interval in seconds between each read on the device
        """
        self.log = log
        self._callback = callback
        self._stop = stop
        self._device = device
        self._device_id = device_id
        self._interval = interval

		
    def check(self):
		while not self._stop.isSet():
			the_url = "http://" + self._device + ECOCOMPTEURURL
			self.log.debug(u"==> URL API called for ecocompteur '%s': '%s'" % (self._device, the_url))
			try:
				req = urllib2.urlopen(the_url)
				jsondata = json.loads(req.read().decode('ascii', errors='ignore'))            # Probleme with unicode !
                #self.log.info(u"==== '%s'" % format(jsondata))
			except HTTPError, err:
				self.log.error(u"### API GET '%s', HTTPError code: %d" % (the_url, err.code) )
			except URLError, err:
				self.log.error(u"### API GET '%s', URLError reason: %s" % (the_url, err.reason) )
			except ValueError as e:
				self.log.error(u"### API GET '%s', no json data : %s" % (the_url, e))
			else:
				self.log.debug(u"==> EcoCompteur '%s': analyse json %s" % (self._device, jsondata) )
				if jsondata["data1"] and jsondata["Date_Time"]:
					self.log.info(u"==> Data1 '%s'" % (jsondata["data1"]))       
					data1 = jsondata["data1"]
					self.log.info(u"==> Data2 '%s'" % (jsondata["data2"]))       
					heureE = jsondata["heure"]
					self.log.info(u"==> Data3 '%s'" % (jsondata["data3"])) 
					minuteE = jsondata["minute"]
					self.log.info(u"==> Data4 '%s'" % (jsondata["data4"])) 
					dateTimeE = jsondata["Date_Time"]
					self.log.info(u"==> Data5 '%s'" % (jsondata["data5"])) 
					self._callback(self._device_id, heureE, minuteE, data1, data2, data3, data4, data5, data6, data6m3, data7, data7m3, dateTimeE)
					self.log.info(u"==> Data6 '%s'" % (jsondata["data6"]))
				else:
					self.log.warning(u"### No data available for this device '%s': %s" % (self._device_id, format(jsondata)))
			self._stop.wait(300)
	