################################################################################
#                                                                              #
#                                  parser.py                                   #
#                                                                              #
################################################################################
#                                                                              #
#        This is a utility for parsing Habitat Mapper data.                    #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#     Copyright (C) 2025, Data Science Institute, University of Wisconsin      #
################################################################################

import os
import sys
import json
import csv
import uuid

#
# globals
#

current = os.path.dirname(os.path.abspath(__file__))
schema = current + '/../../data/habitat-mapper/output/schema.txt'
columns = []
count = 0

#
# parsing functions
#

def get_observation_value(observation, key):
	global count

	match key:

		case 'OBJECTID':
			count += 1
			return count

		case 'title':
			return 'GLOBE Observer Mosquito Habitats'

		case 'dataStreamName':
			return 'Mosquito Habitats ' + observation['mhm_Userid']

		case 'dataStreamDescription':
			return 'Mosquito Habitats as documented by a photo'

		case 'observationType':
			return 'Sensor'

		case 'unitOfCategory':
			return 'Mosquito Habitat, NA, NC'

		case 'phenomenonTime':
			return observation['mhm_MeasuredAt']

		case 'resultTime':
			return observation['mhm_measuredDate']

		case 'result':
			return observation['mhm_WaterSourcePhotoUrls']

		case 'submitTime':
			return observation['mhm_createDate']

		case 'imageStatus':
			return 1 if observation['mhm_WaterSourcePhotoUrls'] else 0

		case 'parameters':
			return observation['mhm_WaterSourcePhotoUrls']

		case 'licenseName':
			return 'NA'

		case 'licenseURI':
			return 'https://www.globe.gov/documents/10157/2592674/GLOBE+Data+User+Guide_v1_final.pdf/863a971d-95c5-4dd9-b75c-46713f019088'

		case 'attributionDataSource':
			return 'User: ' + observation['mhm_Userid']

		case 'attributionDataAggregator':
			return "Global Learning and Observations to Benefit the Environment (GLOBE)"

		case 'validationStatus':
			return '1'

		case 'validationMethod':
			return "Our Validation method is as follows: 1) GLOBE Observer App has its own validators to ensure the requested data type matches the received value. 2) GLOBE Observer Team validates the photos to ensure they are useful and match the area where the photographer took the photo. 3) Our pre-processing algorithms ensure values entered are appropriate and reasonable. Our code also creates quality assurance flag to allow Users to better summarize the data."

		case 'validationResult':
			return "FALSE (Entries with their photos undergoing GLOBE's validation process will have a 'pending' code for their photos. NOTE: Some entries' photos will be listed as 'rejected'. Photos that pass our validation process will include GLOBE's URL to that photo)"

		case 'qualityDescription':
			return "GLOBE Observer Data Guide: https://www.globe.gov/documents/10157/2592674/GLOBE+Data+User+Guide_v1_final.pdf/863a971d-95c5-4dd9-b75c-46713f019088 (Page 25)"

		case 'qualityGrade':
			return 'research'

		case 'observedPropertyName':
			return 'Mosquito Habitats'

		case 'observedPropertyDescription':
			return 'Mosquito Habitats as documented by a photo'

		case 'observedPropertyDefinition':
			return 'https://observer.globe.gov/toolkit/mosquito-habitat-mapper-toolkit'

		case 'sensorName':
			return 'NA'

		case 'sensorDescription':
			return 'NA'

		case 'sensorEncodingType':
			return 'NA'

		case 'sensorMetadata':
			return 'NA'

		case 'locationName':
			return observation['mhm_siteName']

		case 'locationDescription':
			return observation['mhm_siteId']

		case 'locationEncodingType':
			return 'GeoJSON'

		case 'latitude':
			return observation['mhm_MGRSLatitude']

		case 'longitude':
			return observation['mhm_MGRSLongitude']

		case 'volunteerName':
			return 'User: ' + observation['mhm_Userid']

		case 'volunteerDescription':
			return observation['mhm_organizationName']

		case 'volunteerProperties':
			return observation['mhm_WaterSource']

		case 'featureName':
			return observation['mhm_siteName']

		case 'featureDescription':
			return observation['mhm_siteId']

		case 'featureEncodingType':
			return 'GeoJSON'

		case 'featureLocation':
			return ''

		case 'type':
			return 'Point'

		case 'coordinates':
			return ''

		case 'x':
			return ''

		case 'y':
			return ''

	return ''

def get_observation_values(observation):
	values = []
	for column in columns:
		value = get_observation_value(observation, column)
		values.append(value)
	return values

#
# utility functions
#

def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

def read_observations(filename):
	observations = []
	with open(filename) as csvfile:
		reader = csv.reader(csvfile)
		index = 0
		input_columns = []
		for row in reader:
			index += 1
			if index == 1:
				input_columns = row
			else:
				values = {}
				for i in range(0, len(row)):
					values[input_columns[i]] = row[i]
				observations.append(values)
	return observations

#
# output functions
#

def write_csv(filename, observations):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)

		# add headers
		#
		writer.writerow(columns)

		# add columns
		#
		for observation in observations:
			writer.writerow(get_observation_values(observation))

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

	# parse columns to read from schema
	#
	columns = []
	with open(schema, 'r') as file:
		for line in file:
			columns.append(line.replace(',', '').replace('REQUIRED', '').replace('MANDATORY', '').strip())

	# parse observations
	#
	observations = read_observations(filename)

	# write transformed data to csv file
	#
	write_csv(outfilename, observations)