orig_path=/mnt/a/Zaida/OneDrive/PhD/Project_Training/AllTrainingData
dest_path=/mnt/a/Zaida/OneDrive/CLASSES/Intro_Programming/Project/Tablet_Data

cd $orig_path
rm $dest_path/Subjects.txt   # Delete file if it exists

## ITERATES IN ORIGIN PATH (BACKUP FOLDERS AND FILES) - DOES NOT MODIFY IT

for folder in $(ls -d */)   # Loops through each folder in origin directory (orig_path)
do
    mkdir -p $dest_path/$folder  # Creates folder if not existing
    printf "$folder\n" >> $dest_path/Subjects.txt   # Add names of every folder to a file.
    cd $folder

        if ls *.csv 1> /dev/null 2>&1; then   # Test if .csv files are present. /dev/null ... redirects output of ls to make it silent.
                                              # Taken from: https://stackoverflow.com/questions/6363441/check-if-a-file-exists-with-wildcard-in-shell-script
            cp -pu *.csv $dest_path/$folder/     # Copy .csv files to dest_path
        else
            printf ".csv files are missing in $folder\n"
        fi

        if ls *.mat 1> /dev/null 2>&1; then   # Test if .mat files are present
            cp -pu *.mat $dest_path/$folder/     # Copy .mat files to dest_path
        else
            printf ".mat files are missing in $folder\n"
        fi

    cd $orig_path   # Return to main path to continue iteration
done

## ITERATES IN DESTINATION PATH (NEW FOLDER AND FILES)

# Create .txt files containing list of .csv and .mat files in dest_path
cd $dest_path

for folder in $(ls -d */)   # Loops through each folder in dest directory (dest_path)
do
    cd $folder
        rm filenames.txt    # Delete if file exists
        for datafile in $(ls *.csv); do
            printf "$datafile\n" >> filenames.txt   # Add filenames to txt file that Python will import
        done
    cd $dest_path   # Return to main path to continue iteration
done
