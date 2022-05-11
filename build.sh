#!/bin/bash

#################
# CONFIGURATION #
#################
script_name="main.py"
program_name="PLAATO_Serial_Logger"
dist_dir="./dist/${program_name}"
#################

# Recreate the dist directory and station directories
rm -r ./dist
mkdir -p $dist_dir
mkdir "${dist_dir}/output"

# Create a base executable file for the program
pyinstaller --onefile --distpath $dist_dir --name "${program_name}" $script_name
# Copy over assets
echo $dist_dir | xargs -n 1 cp -r ./files