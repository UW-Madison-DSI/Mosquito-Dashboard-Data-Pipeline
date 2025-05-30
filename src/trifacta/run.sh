echo "Converthing Habitat Mapper recipe to json"
python3 parse_recipe.py ../habitat-mapper/recipe.txt ../habitat-mapper/recipe.json

echo "Converthing iNaturalist recipe to json"
python3 parse_recipe.py ../inaturalist/recipe.txt ../inaturalist/recipe.json

echo "Converthing Land Cover recipe to json"
python3 parse_recipe.py ../land-cover/recipe.txt ../land-cover/recipe.json

echo "Converthing Mosquito Alert recipe to json"
python3 parse_recipe.py ../mosquito-alert/recipe.txt ../mosquito-alert/recipe.json