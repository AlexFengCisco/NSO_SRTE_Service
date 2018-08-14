# -*- mode: python; python-indent: 4 -*-

'''
Created on July 10, 2018

@author: Alex Feng 

alfeng@cisco.com
'''


import sys
import ncs
from ncs.application import Service
import requests
from requests.auth import HTTPBasicAuth
import json

# ------------------------
# SERVICE CALLBACK EXAMPLE  
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        self.config_sr_policy(tctx, root, service)

    
    def config_sr_policy(self, tctx, root, service):

        #RPC rest call get SID list from WAE
	JSON_HEADERS = {"Content-Type": "application/vnd.yang.operation+json",
                    "Accept": "application/vnd.yang.data+json"}

	sr_te_metric= "te"

	api = "http://10.75.58.27:8080/api/running/networks/network/DARE/opm/te-path/_operations/run"
	payload = {
            "input": {
                "source-node": service.src_pe_name,
                "destination-node": "R4",
                "te-type": "segment_routing",
                "metric": sr_te_metric
            }

        }

	response = requests.post(api, data=json.dumps(payload), headers=JSON_HEADERS,auth=HTTPBasicAuth('admin', 'admin'))

	if response.status_code != 200:
    		print "HTTP pos request failed!"
		self.log.info('HTTP POST request failed')
	else:
    		print str(response.json())
		self.log.info('Response content %s'%response.json())
	
	
	segment_list = response.json()
	'''
	segment_list = {
 			 "cisco-wae-opm-te-path:output": {
        		"status": "true",
        		"message": "success",
        		"segment_list": [
            			"16002",
            			"16005",
            			"16006"
        			]
    			}
		}
	'''
        index_start = 0
        index_interval = 10

	hops = segment_list["cisco-wae-opm-te-path:output"]["segment_list"]
        sl_name = service.policy_name
	rt_str = {"segment_routing_list_name": sl_name, "hops": []}
	
        path_index = index_start
	for hop in hops:
		path = {}
		path_index += index_interval
		path["index"] = path_index
		path["label"] = int(hop)
		rt_str["hops"].append(path)

        self.log.info('Construct segment routing list %s'%str(rt_str))

	#apply variable to template seg_list_dev.xml
			
	for path in rt_str["hops"]:
		variables = ncs.template.Variables()
		template = ncs.template.Template(service)
		variables.add("PE",service.src_pe_name)
		variables.add("segment_list_name",service.policy_name)
		variables.add("index",path["index"])
		variables.add("sid",path["label"])
		#template.apply("sr_policy_dev",variables)
        	#Create segment routing te policy
		#self.log.info('Create router segment routing traffic engineering policy')
		#variables = ncs.template.Variables()
        	#template = ncs.template.Template(service)
        

        	variables.add("PE", service.src_pe_name)
        	variables.add("policy_name", service.policy_name)
        	variables.add("segment_list_name", service.policy_name)
        	variables.add("pe_des_ip_address", service.pe_des_ip_address)
        	variables.add("color", service.color)
        	variables.add("preference_id", service.preference)
        	variables.add("binding_mpls_sid", service.binding_mpls_sid)
        	template.apply('sr_policy_dev', variables)
        
        self.log.info('apply sr policy device template finished')



    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('sr_te', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
