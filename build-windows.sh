#!/bin/bash

#################
# CONFIGURATION #
#################
script_name="main.py"
program_name="PLAATO_Serial_Logger-win"
dist_dir="dist/${program_name}"
#################

# Recreate the dist directory and station directories
rm -r $dist_dir
mkdir -p $dist_dir
mkdir "${dist_dir}/output"

# Create a base executable file for the program
wine ~/.wine/drive_c/Python39/Scripts/pyinstaller.exe --onefile --distpath $dist_dir --name "${program_name}" $script_name
# Copy over assets
echo $dist_dir | xargs -n 1 cp -r ./files