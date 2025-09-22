# This file is the bash script for creating the folder structure of a new project.

# Creing the folders with the mkdir command.
mkdir -p src
mkdir -p research


# Creating the files with the touch command.
touch src/__init__.py
touch src/helper.py
touch src/prompt.py
touch .env
touch setup.py
touch app.py
touch research/trialts.ipynb
touch requirements.txt


# When aLL the folders and files are created, print a message to the user.
echo "Project structure created successfully!"

