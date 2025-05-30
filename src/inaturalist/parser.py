################################################################################
#                                                                              #
#                                  parser.py                                   #
#                                                                              #
################################################################################
#                                                                              #
#        This is a utility for parsing a iNaturalist data.                     #
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
import json
import csv

#
# globals
#

schema = '../../data/inaturalist/output/schema.txt'
columns = []

#
# parsing functions
#

def get_observation_value(observation, key):
	match key:

		case 'OBJECTID':
			return observation['id']

		case 'title':
			return 'Citizen·science·data·on·mosquitos·from·iNaturalist·with·additional·automated·ID'

		case 'description':
			return 'Data·is·generated·from·the·iNaturalist·database·filtered·by·Mosquitoes·and·quality·grade·before·additional·automated·identifications·are·added'

		case 'dataStreamName':
			return '·Research·grade·mosquito·species·occurrence·data·from·user·cell·phone'

		case 'dataStreamDescription':
			return 'All·species·occurrence·observations·from·a·particular·user·taken·with·a·sensor·or·manually'

		case 'dataStreamObsType':
			return 'category observation'

		case 'dataStreamUniCategory':
			return {
				"Type": "Annotations potentially including lifecycle phase",
				"Identified by Human": "Annotations potentially including lifecycle phase",
				"Identified by Machine": "Annotations potentially including lifecycle phase"
			}

		case 'observationProObsUID':
			return observation['uuid']

		case 'observationResCatObsPheTime':
			return observation['time_observed_at']

		case 'observationResCatObsResTime':
			return ''

		case 'observationResCatObsResult':
			return {
				'Type': 'adult',
				'Human ID': observation['taxon']['name'],
				'Automated ID': []
			}

		case 'obsResCatObsResult_Type':
			return 'adult'

		case 'Identified by Human' | 'Indentified by Human':
			return observation['taxon']['name']

		case 'Identified by Machine' | 'Identified by Machine':
			return ''

		case 'observationResCatObsSubTime':
			return ''

		case 'observationImaImaStatus':
			return 1 if observation['observation_photos'] else 0

		case 'observationImaImaResult':
			photos = observation['observation_photos']
			if photos:
				return photos[0]['photo']['url']

		case 'observationConParameters':
			return {
				'captive': observation['captive'],
				'comments': observation['comments'],
				'time_zone_offset': observation['time_zone_offset'],
				'uri': observation['uri'],
				'icon_url': observation['user']['icon_url'],
				'sounds': observation['sounds']
			}

		case 'Aegypti_Certainty':
			return ''

		case 'Tiger_Certainty':
			return ''

		case 'omProcessLicLicName':
			return observation['taxon']['default_photo']['license_code']

		case 'omProcessLicLicURI':
			return ''

		case 'omProcessLicLicAttSource':
			return ''

		case 'omProcessLicLicAttAggregator':
			return 'iNaturalist'

		case 'omProcessProType' | 'omPrcoessProType':
			return 'Sensor'

		case 'omProcessProReference':
			return 'https://www.inaturalist.org/pages/help'

		case 'omProcessResQuaValStatus' | 'omPrcoessResQuaValStatus':
			return 1

		case 'omProcessResQuaValMethod' | 'omPrcoessResQuaValMethod':
			return 'Human expert validation'

		case 'omProcessResQuaValResult' | 'omPrcoessResQuaValResult':
			return 1

		case 'omProcessResQuaQuaGrade' | 'omPrcoessResQuaQuaGrade':
			return observation['quality_grade']

		case 'observedProName':
			return 'Species occurrence'

		case 'observedProDescription':
			return 'Whether a species is observed at a location'

		case 'observedProDefinition':
			return 'https://www.sciencedirect.com/topics/earth-and-planetary-sciences/species-occurrence'

		case 'sensorName':
			return observation['uuid']

		case 'sensorDescription':
			return 'Observation take by mobile phone of user: ' + observation['uuid']

		case 'sensorEncType':
			return 'NC'

		case 'locationName':
			return 'Anonymous location'

		case 'locationDescription':
			return 'location.name'

		case 'locationEncType':
			return 'GeoJSON Point'

		case 'latitude':
			location = observation['location']
			return location.split(',')[0] if location else None

		case 'longitude':
			location = observation['location']
			return location.split(',')[1] if location else None

		case 'thingName':
			return 'sensor.name'

		case 'thingDescription':
			return 'sensor.description'

		case 'featureIntName':
			return 'location.name'

		case 'featureIntDescription':
			return 'location.description'

		case 'featureIntEncType':
			return 'GeoJSON Point'

		case 'featureIntLocation':
			return 'latitude, longitude'

		case 'type':
			return 'FeatureCollection'

		case 'coordinates':
			return '[' + observation['location'] + ']' if observation['location'] else ''

		case 'nuts_3':
			return ''

		case 'nuts_2':
			return ''

		case 'X':
			return ''

		case 'Y':
			return ''

		case _:
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

	# parse data from observations
	#
	data = json.loads(read_file(filename))
	observations = data['results']

	# write transformed data to csv file
	#
	write_csv(outfilename, observations)