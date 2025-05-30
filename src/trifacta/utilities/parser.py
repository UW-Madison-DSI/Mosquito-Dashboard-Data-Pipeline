################################################################################
#                                                                              #
#                                   parser.py                                  #
#                                                                              #
################################################################################
#                                                                              #
#        This is a utility for parsing a Wrangle recipe.                       #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#     Copyright (C) 2025, Data Science Institute, University of Wisconsin      #
################################################################################

from .tokenizer import Tokenizer

#
# parsing class
#

class Parser:

	#
	# constructor
	#

	def __init__(self):
		self.tokenizer = Tokenizer()
		self.tokens = []
		self.count = 0

	#
	# helper methods
	#

	def current(self):
		return self.tokens[self.count] if (self.count < len(self.tokens)) else None

	def next(self):
		return self.tokens[self.count + 1] if (self.count < len(self.tokens) - 1) else None

	def skip(self, number = 1):
		self.count += number

	#
	# unit parsing methods
	#

	def parse_array(self):
		array = []
		self.skip()
		while self.current() != ']':
			array.append(self.current())
			self.skip()
			if self.current() == ',':
				self.skip()
		self.skip()
		return array

	def parse_list(self):
		items = []
		while self.next() == ',':
			items.append(self.current())
			self.skip(2)
		items.append(self.current())
		self.skip()
		return items

	def parse_function_call(self):
		function_name = self.current()
		self.skip()

		params = []
		if self.current() == '(':
			self.skip();
			if self.current() == '[':
				params = self.parse_array()
			else:
				params = self.parse_list()
			self.skip()

		# while self.next() != ')':
		#	params.append(self.current())
		#	self.skip()
		# params.append(self.current())
		# self.skip(2)
		# value = function_name + '(' + ''.join(params) + ')'
		return {
			'type': 'function',
			'name': function_name,
			'params': params
		}

	def parse_parameters(self):
		parameters = {}
		while self.next() == ':':
			name = self.current()
			self.skip(2)

			# parse array
			#
			if self.current() == '[':
				value = self.parse_array()			

			# parse parameter list
			#			
			elif self.next() == ',':
				value = self.parse_list()

			# parse function call
			#
			elif self.next() == '(':
				value = self.parse_function_call()

			# parse single value
			#
			else:
				value = self.current()
				self.skip()

			parameters[name] = value
		return parameters

	def parse_transform(self, line):
		self.tokens = self.tokenizer.scan(line)
		self.count = 0
		name = self.current()

		# parse delete transform
		#
		if name == 'Delete':
			parameters = {}
			self.skip()

			parameters['target'] = self.current()
			self.skip()

			if self.current() == 'with':
				self.skip()
				if self.current() == 'missing':
					self.skip()
					if self.current() == 'values':
						self.skip()
						parameters['with'] = 'missing values'

			if self.current() == 'in':
				self.skip()
				parameters['in'] = self.current()
				self.skip()

		# parse other transforms
		#
		else:
			self.skip()
			parameters = self.parse_parameters()

		return {
			'transform': name,
			'parameters': parameters
		}

	#
	# file parsing methods
	#

	def read(self, filename):
		transforms = []
		with open(filename, 'r') as file:
			for line in file:
				transforms.append(self.parse_transform(line))
		return transforms
