from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, ERROR, FileHandler, NullHandler
import traceback
import os
import sys

class MLOGGER:
	@staticmethod
	def get_logger(name):
		if not name:
			raise ValueError('Name parameter can not be empty.')
		return MLOGGER(name)

	@staticmethod
	def __create_stream_handler(level):
		handler = StreamHandler()
		handler.setLevel(level)
		handler.setFormatter(
			Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
		return handler

	@staticmethod
	def __create_file_handler(level, filename):
		filename_path = str(os.path.dirname(os.path.realpath(__file__))) + '/' + str(filename)
		fileHandler = FileHandler(filename_path, mode='w')
		fileHandler.setLevel(level)
		fileHandler.setFormatter(
			Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
		return fileHandler

	def __init__(self, name, level=INFO, logtype='CONSOLE', filename=None):
		# logtype  : {'CONSOLE', 'FILE', 'BOTH', 'NONE'}
		# level : {INFO, DEBUG, ERROR}
		self.user_variables = {}
		self.user_variables['instance_id'] = self.__class__.__name__
		self.logger = getLogger(name)
		self.logger.setLevel(level)
		if logtype == 'CONSOLE':
			self.logger.addHandler(MLOGGER.__create_stream_handler(level))
		elif logtype == 'FILE':
			if filename is not None:
				self.logger.addHandler(MLOGGER.__create_file_handler(level, filename))
			else:
				raise ValueError('filename cannot be empty')
				sys.exit()
		elif logtype == 'BOTH':
			self.logger.addHandler(MLOGGER.__create_stream_handler(level))
			if filename is not None:
				self.logger.addHandler(MLOGGER.__create_file_handler(level, filename))
			else:
				raise ValueError('filename cannot be empty')
				sys.exit()
		elif logtype == 'NONE':
			self.logger.addHandler(NullHandler())

	def __set_message(self, message):
		tb = traceback.extract_stack()
		return(tb[1][2] + ' - ' + message)

	def debug(self, message):
		self.logger.debug(self.__set_message(message), extra=self.user_variables)

	def info(self, message):
		self.logger.info(self.__set_message(message), extra=self.user_variables)

	def warn(self, message):
		self.logger.warn(self.__set_message(message), extra=self.user_variables)

	def error(self, message):
		self.logger.error(self.__set_message(message), extra=self.user_variables)