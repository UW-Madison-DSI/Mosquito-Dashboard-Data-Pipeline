################################################################################
#                                                                              #
#                                 tokenizer.py                                 #
#                                                                              #
################################################################################
#                                                                              #
#        This is a utility for tokenizing a Wrangle recipe.                    #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#     Copyright (C) 2025, Data Science Institute, University of Wisconsin      #
################################################################################

#
# class definition
#

class Tokenizer:

	#
	# constructor
	#

	def __init__(self):
		self.chars = []
		self.count = 0

	#
	# helper methods
	#

	def start(self, chars = None):
		self.count = 0
		if chars:
			self.chars = chars

	def current(self):
		return self.chars[self.count] if (self.count < len(self.chars)) else None

	def next(self):
		return self.chars[self.count + 1] if (self.count < len(self.chars) - 1) else None

	def skip(self, number = 1):
		self.count += number

	def finished(self):
		return self.count == len(self.chars) - 1

	#
	# scanning functions
	#

	def scan_whitespace(self):
		while self.current() == ' ':
			self.skip()

	def scan_object(self):
		string = ''
		while self.current() != '}':
			string += self.current()
			self.skip()
		string += self.current()
		self.skip()

		return string

	def scan_single_quoted_string(self):
		string = ''
		self.skip()
		while self.current() != "'" and not self.finished():
			if self.current() == '\\':
				self.skip()
				string += self.current()
				self.skip()
			else:
				string += self.current()
				self.skip()
		self.skip()
		return "'" + string + "'"

	def scan_double_quoted_string(self):
		string = ''
		self.skip()
		while self.current() != '"':
			string += self.current()
			self.skip()
		self.skip()

		return '"' + string + '"'

	def scan_pattern(self):
		string = ''
		self.skip()
		while self.current() != "`":
			string += self.current()
			self.skip()
		self.skip()

		return "`" + string + "`"

	def scan_identifier(self):
		string = ''
		self.skip
		char = self.current()
		while char != None and (char.isalpha() or char.isdigit() or char == '_'):
			string += char
			self.skip()
			char = self.current()

		if (string == 'true'):
			return True
		elif (string == 'false'):
			return False
		else:
			return string

	def scan_symbol(self):
		token = None
		if (self.current() != "\n"):
			token = self.current()
		self.skip()
		return token

	#
	# scanning methods
	#

	def scan(self, line):
		tokens = []

		# start
		#
		self.start(line)

		# scan chars
		#
		while not self.finished():
			token = None

			# scan through whitespace
			#
			self.scan_whitespace()

			# scan items
			#
			char = self.current()
			if char == None:
				break;
			elif char == '{':
				token = self.scan_object()
			elif char == "'":
				token = self.scan_single_quoted_string()
			elif char == '"':
				token = self.scan_double_quoted_string()
			elif char == "`":
				token = self.scan_pattern()
			elif char.isalpha() or char == '_':
				token = self.scan_identifier()
			else:
				token = self.scan_symbol()

			# add to tokens
			#
			if token:
				tokens.append(token)

		return tokens

	def echo(self, filename):
		with open(filename, 'r') as file:
			self.start(file.read())
			while not self.finished():
				print('ch = ', self.current(), sep='')
				self.skip()

	#
	# file reading methods
	#

	def read(self, filename):
		tokens = []
		with open(filename, 'r') as file:
			tokens = self.scan(file.read())
		return tokens
