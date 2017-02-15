#!/usr/bin/python
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

- EcocompteurManager

@author: Fritz <fritz.smh@gmail.com>
@copyright: (C) 2007-2014 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from domogik.common.plugin import Plugin
from domogikmq.message import MQMessage
from domogikmq.reqrep.client import MQSyncReq

from domogik_packages.plugin_ecocompteur.lib.ecocompteur import Ecocompteur, EcocompteurException
import threading
import traceback
import re
import json
import time


class EcocompteurManager(Plugin):
    """ Get ecocompteurrmation informations
    """

    def __init__(self):
        """ Init plugin
        """
        Plugin.__init__(self, name='ecocompteur')

        # check if the plugin is configured. If not, this will stop the plugin and log an error
        #if not self.check_configured():
        #    return

        # get the devices list
        self.devices = self.get_device_list(quit_if_no_device = True)
		#self.log.info(u"==> device:   %s" % format(self.devices))

        # get the sensors id per device : 
        # {device_id1 : {"sensor_name1" : sensor_id1,
        #                "sensor_name2" : sensor_id2},
        #  device_id2 : {"sensor_name1" : sensor_id1,
        #                "sensor_name2" : sensor_id2}}
        self.sensors = self.get_sensors(self.devices)

        # create a Ecocompteur for each device
        threads = {}
        ecocompteur_list = {}
        for a_device in self.devices:
            try:
                # global device parameters
                device = self.get_parameter(a_device, "device")
                device_id = a_device["id"]
                interval = self.get_parameter(a_device, "interval")
                
                ecocompteur_list[device] = Ecocompteur(self.log, self.send_data, self.get_stop(), device, device_id, interval)

                # start the ecocompteur thread
                self.log.info(u"Start monitoring ecocompteur device '{0}'".format(device))
                thr_name = "{0}".format(device)
                threads[thr_name] = threading.Thread(None,
                                              ecocompteur_list[device].check,
                                              thr_name,
                                              (),
                                              {})
                threads[thr_name].start()
                self.register_thread(threads[thr_name])
            except:
                self.log.error(u"{0}".format(traceback.format_exc()))
                # we don't quit plugin if an error occured
                # a ecocompteur device can be KO and the others be ok
                #self.force_leave()
                #return
        self.ready()
        self.log.info(u"Plugin ready :)")

		
    def send_data(self, device_id, heureE, minuteE, data1, data2, data3, data4, data5, data6, data6m3, data7, data7m3, dateTimeE):
		self.log.debug(u"==> EcoCompteur '%s': data1='%s', data2='%s'" % (device_id, data1, data2))
		data = {}
	#	data[self.sensors[device_id]["heure"]] = heure  				#  "heure" = sensor name in info.json file
	#	data[self.sensors[device_id]["minute"]] = minute     			#  "minute" = sensor name in info.json file
		data[self.sensors[device_id]["data1"]] = data1                 	#  "data1" = sensor name in info.json file
		data[self.sensors[device_id]["data2"]] = data2       			#  "data2" = sensor name in info.json file
		data[self.sensors[device_id]["data3"]] = data3  				#  "data3" = sensor name in info.json file
        
		self.log.debug(u"==> EcoCompteur '%s': data1='%s', data2='%s'" % (device_id, data1, data2))
		try:
			self._pub.send_event('client.sensor', data)
		except:
			#We ignore the message if some values are not correct because it can happen with ecocompteur ...
			self.log.debug(u"Bad MQ message to send. This may happen due to some invalid ecocompteur data. MQ data is : {0}".format(data))
			pass
        
if __name__ == "__main__":
	ecocompteur = EcocompteurManager()
