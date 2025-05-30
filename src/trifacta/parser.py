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

import sys
from utilities.parser import Parser
import json

#
# main
#

if __name__ == '__main__':

	# parse arguments
	#
	if (len(sys.argv) < 3):
		print("Usage: python3 parser.py <input-file-name> <output-file-name");
		exit();

	# get command line arguments
	#
	filename = sys.argv[1]
	outfilename = sys.argv[2]

	# parse input file
	#
	parser = Parser()
	transforms = parser.read(filename)

	# write output file
	#
	with open(outfilename, "w") as file:
		file.write(json.dumps(transforms, indent=4))