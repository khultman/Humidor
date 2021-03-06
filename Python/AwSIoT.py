from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import logging
import sys
import time

class IoT(object):
	def __init__(self, endpoint, rootCAPath, certificatePath, privatekeyPath, useWebsocket, clientId, topic):
		# Setup Logging
		self._log = logging.getLogger(__name__)
		self._logging_variables = {}
		self._logging_variables['instance_id'] = self.__class__.__name__
		self._streamHandler = logging.StreamHandler()
		self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self._streamHandler.setFormatter(self._formatter)
		self._log.addHandler(self._streamHandler)
		# Read in passed vars
		self._endpoint = endpoint
		self._rootCAPath = rootCAPath
		self._certificatePath = certificatePath
		self._privatekeyPath = privatekeyPath
		self._useWebsocket = useWebsocket
		self._clientID = clientId
		self._topic = topic
		# Init AWSIoTMQTTClient
		if self._useWebsocket:
			self._AWSIoTMQTTClient = AWSIoTMQTTClient(self._clientID, useWebsocket=True)
			self._AWSIoTMQTTClient.configureEndpoint(self._endpoint, 443)
			self._AWSIoTMQTTClient.configureCredentials(self._rootCAPath)
		else:
			self._AWSIoTMQTTClient = AWSIoTMQTTClient(self._clientID)
			self._AWSIoTMQTTClient.configureEndpoint(self._endpoint, 8883)
			self._AWSIoTMQTTClient.configureCredentials(self._rootCAPath, self._privatekeyPath, self._certificatePath)
		self._AWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
		self._AWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
		self._AWSIoTMQTTClient.configureDrainingFrequency(2)
		self._AWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
		self._AWSIoTMQTTClient.configureMQTTOperationTimeout(5)
		self._AWSIoTMQTTClient.connect()
		#self._AWSIoTMQTTClient.subscribe(topic, 1, self.subscribe_callback)

	def subscribe_callback(self, client, userdata, message):
		print("Received a new message: ")
		print(message.payload)
		print("from topic: ")
		print(message.topic)
		print("--------------\n\n")

	def publish(self, message):
		self._AWSIoTMQTTClient.publish(self._topic, message, 1)

	def publish_dict(self, data):
		data['humidor_id'] = self._clientID
		data['time_stamp'] = time.time()
		data = json.dumps(data)
		self.publish(data)
