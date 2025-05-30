<p align="center">
  <div align="center">
    <img src="./images/logos/logo.svg" alt="Logo" style="width:200px">
  </div>
</p>

# Mosquito Dashboard Data Pipeline
The Mosquito Dashboard Data Pipeline is a mechanism for:
1) importing data from a variety of data sources
2) transforming it to a target format, and 
3) exporting it to the [Global Mosquito Observations Dashboard](https://mosquitodashboard.org) for storage and display.

## The Global Mosquito Observations Dashboard
The Global Mosquito Observations Dashboard is a project by the [University of Wisconsin](http://wisc.edu) and the [University of South Florida](https://www.usf.edu/) to build a platform to allow a comprehensive mapping of global mosquito observations.   It is funded by the [National Science Foundation](https://www.nsf.gov/).

![Screen Shot](images/screen-shots/mosquito-dashboard.png)
Global Mosquito Observations Dashboard

## Requirements

### 1. Python3

The transformation scripts rely upon the Python3 platform.

## Instructions

To run the data transformation scripts, simply run the appropriate 'parser.py' for the data source that you are interested in using the python3 interpreter followed by the path to the input file that you would like to transform and then the path to the desired output file where you would like the transformed data to be written.

```
python3 src/habitat-mapper/parser.py \
  data/habitat-mapper/input/input.csv \
  data/habitat-mapper/output/output.csv

python3 src/inaturalist/parser.py \
  data/inaturalist/input/input.json \
  data/inaturalist/output/output.csv

python3 src/land-cover/parser.py \
  data/land-cover/input/input.csv \
  data/land-cover/output/output.csv

python3 src/mosquito-alert/parser.py \
  data/mosquito-alert/input/input.json \
  data/mosquito-alert/output/output.csv
```

There is also a utility to convert Trifacta recipes from text to json format to make them easier to read.  To run this utility run the file 'parser.py' in the src/trifacta directory using the python3 interpreter and give it the paths to the desired input and output files.

```
python3 src/trifacta/parser.py \
  src/habitat-mapper/recipe.txt \
  src/habitat-mapper/recipie.json

python3 src/trifacta/parser.py \
  src/inaturalist/recipe.txt \
  src/inaturalist/recipie.json

python3 src/trifacta/parser.py \
  src/land-cover/recipe.txt \
  src/land-cover/recipie.json

python3 src/trifacta/parser.py \
  src/mosquito-alert/recipe.txt \
  src/mosquito-alert/recipie.json
```

<!-- CONTACT -->
## Contact

Abe Megahed - (mailto:amegahed@wisc.edu) - email
