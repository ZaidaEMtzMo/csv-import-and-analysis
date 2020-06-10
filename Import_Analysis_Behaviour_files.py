# -*- coding: utf-8 -*-
"""
Before running this code, it is necessary to run codes:
    - In unix terminal: Organizing_files.sh
    - In MatLab: Export_csv_files.m
    - In unix terminal: Organizing_files.sh (again to include files created by MatLab)

and to update the main_dir variable.

@author: Zaida Escila Martinez Moreno
@date: June 2020
"""

# Import all necessary libraries

import os     # To navigate through directories
from datetime import datetime,timedelta      # To get date of creation of files
import numpy as np
import pandas as pd     # To import .csv files
import seaborn as sns    # To help with plots
import matplotlib.pyplot as plt
# import json
# import matplotlib.colors as clrs
# import math




# Defining functions that will be necessary

def find_duplicates(test_list):
    """
    Finds elements that are duplicated in a list.

    Parameters
    ----------
    test_list : LIST

    Returns
    -------
    dup_list : LIST
        List of duplicated elements.

    """
    dup_list = []   # Container list
    for elem in test_list:
        if test_list.count(elem) > 1:   # If there any element is repeated...
            if elem not in dup_list:    # Avoids duplicating an element in dup_list
                dup_list.append(elem)
    return dup_list




def read_simple_txt(filename,header=False,delimiter=False,delim=','):
    """
    Read simple text file to list.

    Parameters
    ----------
    filename : STRING
        Contains the name of the file that will be imported.
    header : BOOLEAN
        Indicates if first line of file is header.
    delimiter : BOOLEAN
        Indicates if the data should be separated.
    delim : STRING
        Indicates the delimiter in the datafile.
        
    Returns
    -------
    List of strings. One string per line in filename.

    """
    
    f = open(filename, 'r')     # Open chosen file
    
    list_strings = []   # Empty container
    
    # When there is a header, send it to another variable (column_headers)
    if header:
        line = f.readline()
        column_headers = line.rstrip("\n").split(delim)
    
    # Loop while there are lines in the file
    while True:
        line = f.readline()
        if line == "":   # End of the file
            break
        
        if delimiter:    # When there is a delimiter, strip the 'next line chr'
                         #      and split the list by delimiters
            list_strings.append(line.rstrip("\n").split(delim))
        
        else:            # When there is no delimiter, just strip 'next line' and '/'
            list_strings.append(line.rstrip("/\n"))
    f.close()
    
    if header:     # Return headers and list
        return column_headers, list_strings
    else:          # or just the list
        return list_strings




def convert_month2number(month):
    """
    Converts a three letter month into the right number.
    
    
    Parameters
    -------
    ----------
    month : STRING
        In the format: 'Jan', 'Feb', etc.

    Returns
    -------
    month_number : INT

    """
    months_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep',
                   'Oct','Nov','Dec']
    if month in months_list:
        month_number = months_list.index(month) +1  # Add 1 to avoid month 00
    else:
        print(month,'is an invalid input.')    # Check validity of month
    return month_number



    
def n_days_dict(filenames_list, dates_list, days=12):
    """
    Receives two sorted-by-date lists. Creates a 12 day array and assigns day 
    number to each filename.
    
    Parameters
    ----------
    filenames_list : LIST
        List of filenames.
    dates_list : LIST
        List of dates extracted from those filenames.
    days : INT
        Number of days that the array should have. Default is 12.

    Returns
    -------
    dict_of_dates : TYPE
        DESCRIPTION.

    """
    # Take first date and creates a list of that day plus n others
    #   Uses datetime.timedelta to sum days
    days_list = [ dates_list[0] + timedelta(days=x) for x in range(days)]
    
    # Create empty dictionary with filenames as keys
    dict_of_dates = dict.fromkeys(filenames_list,'')
    
    # Per each paired date and filename
    for date, filename in zip(dates_list, filenames_list):
        day_number = days_list.index(date) + 1  # Avoids Day 00
        
        # Associates filename with the corresponding day number
        dict_of_dates[filename] = '{}'.format(str(day_number)
                                              .zfill(2))  # Num format: 00, 01...
    return dict_of_dates




def sort_by_date(filenames_list):
    """
    Given a list of files in the format "Subject_D-M-YYYY_complement",
    extracts date string and sorts the files depending on their date.

    Parameters
    ----------
    filenames_list : LIST
        List of filenames that contain a date between two underscores 
        (Subject_date_info.ext) or three underscores (Subject_nScan_date_info.ext).

    Returns
    -------
    List of filenames sorted by the date.

    """
    # Empty containers
    dates_list = []
    sorted_files = []
    
    
    for file in filenames_list:
        
        # Extract string of date from filename
        if file.count('_') == 2: # Subject_date_info.ext
            date_per_file = file.split('_')[1] # Takes second string
            
        elif file.count('_') == 3: # Subject_nScan_date_info.ext
            date_per_file = file.split('_')[2] # Takes third string
            
        # Convert string of date [DD-MM-YYYY] to list of integers: [DD, MM, YYYY]
        date_DMY = date_per_file.split('-')  # Separate date string in [dd, mm, yyyy]
        
        if not ( date_DMY[1].isdigit() ):   # If month is NOT a digit (Jan,Feb,Mar...)
            date_DMY[1] = convert_month2number(date_DMY[1])   # Convert month to digit
        
        # Convert from strings to integers in date
        date_DMY = [ int(date_DMY[index]) for index in range(len(date_DMY)) ]
        dates_list.append(date_DMY)
        
    # Convert integers to "true dates" with datetime library
    datetime_list = [ datetime(year=date[2], month=date[1], day=date[0]) 
                     for date in dates_list ]
        
    # Sort list of filenames depending on the date using "decorate, sort, undecorate" idiom and args (*).
    # Taken from: https://stackoverflow.com/questions/9764298/how-to-sort-two-lists-which-reference-each-other-in-the-exact-same-way
    
    datetime_list, sorted_files = (list(file) for file in zip
                                   (*sorted(zip(datetime_list, filenames_list))))
    
    # Create dictionary that relates the sorted files with their date
    dates_dict = n_days_dict(sorted_files, datetime_list)
        
    return sorted_files, dates_dict

def find_subject(subjectID,subjects_info,header_info):
    """
    Given a file containing info of each subject, this function finds any 
    given SubjectID inside that subjects_info, and returns the position on
    that list where it found it and the group that subject belongs to.

    Parameters
    ----------
    subjectID : STRING
        Name of subject in the format 'Subject01'.
    subjects_info : LIST OF LISTS
        List containing a list per each line of the Subjects_info.csv file.
    header_info : LIST
        List containing the header of Subjects_info.csv.

    Returns
    -------
    index : INT
        Position in subjects_info that contains subjectID.
    group : STRING
        Group where subjectID belongs.

    """
    # Loops through the array of lists in subjects_info
    for index in range(len(subjects_info)):
        
        # Subject ID must be in first position of list
        if subjectID == subjects_info[index][0]:
            
            # When it finds the right subjectID, outputs the index and the group
            #   it belongs to
            age_group = subjects_info[index][header_info.index('Group')]
            gender = subjects_info[index][header_info.index('Gender')]
            age = subjects_info[index][header_info.index('Age')]
            mus_train = subjects_info[index][header_info.index('Musical training')]
            lat = subjects_info[index][header_info.index('Laterality')]
            nLang = subjects_info[index][header_info.index('Language')]
            edu_class = subjects_info[index][header_info.index('Education')]
            
            return index, age_group, gender, age, mus_train, lat, nLang, edu_class
        

# Directory where all files are
main_dir = "A:\Zaida\OneDrive\CLASSES\Intro_Programming\Project\Tablet_Data"

# Go to main directory. Uses os.system library
os.chdir(main_dir)

# Get the name of all the subjects' folders
subjects_list = read_simple_txt('Subjects.txt')     # Get list of subjects

# Get the info from each subject into a variable
header_info, subjects_info = read_simple_txt('Subjects_info.csv',header=True,
                                             delimiter=True,delim=',')

# Create DataFrame with info from subjects
subjects_info_df = pd.DataFrame.from_records(subjects_info)   # Convert to DataFrame
subjects_info_df.columns = header_info
subjects_info_df=subjects_info_df.set_index('Subjects')

# Get some data from info
#**Organize data to make it possible
subjects_info_df=subjects_info_df.replace('','-1')
subjects_info_df['Age']=subjects_info_df['Age'].astype(int)
subjects_info_df['MTcode']=subjects_info_df['MTcode'].astype(int)
subjects_info_df['Language']=subjects_info_df['Language'].astype(int)
subjects_info_df=subjects_info_df.replace('-1',np.nan)
subjects_info_df=subjects_info_df.replace(-1,np.nan)


#**Mean per age group
mean_pergroup=subjects_info_df.groupby('Group')['Age'].mean()
max_pergroup=subjects_info_df.groupby('Group')['Age'].max()
min_pergroup=subjects_info_df.groupby('Group')['Age'].min()

# Initialize list: will contain a list of DataFrames
dataset_per_subject = []

# Headers for the DataFrame
headers_df = ['Username','Timer (s)','Trial','Level','Target?','StimID',
              'Response','Position_1','Position_2','Position_3','Position_4',
              'Freq_1','Freq_2','Freq_3','Freq_4','S.loud_1','S.loud_2',
              'S.loud_3','F0']

# Iterates through each subject
for subject in subjects_list:
    file_loc = '{}/filenames.txt'.format(subject)   # Get string with file location
    filenames_list = read_simple_txt(file_loc)   # Get list of files to import per subject
    
    # Organizes the filenames per date and creates a dictionary that pairs each
    #   filename with the appropiate day number
    file_list, date_dict = sort_by_date(filenames_list)
    
    # Extracts the values (days of training) of the dictionary and adds them to a list
    values_dict = list(date_dict.values())
    
    # Assess if there is any training day that was repeated. If so, let know to user
    if len(values_dict) != len(set(values_dict)):
        print("{} are repeated in {}. Check out and correct manually.\n{}\n\n"
              .format((find_duplicates(values_dict)),subject,date_dict))
    
    # Iterates through each file that corresponds to a training day
    for file in file_list:
        file_loc = '{}/{}'.format(subject,file)     # Creates string with path to file
        
        # To import to pandas, it needs to be a .csv
        #   All files should be due to the creation of 'filenames.txt' in bash,
        #   but just avoids future errors.
        if ".csv" in file:
            dataset_per_day = pd.read_csv(file_loc)
        else:
            print("{} is not a valid file to input to pandas.".format(file))
        
        # Make sure that headlines of all columns are the same to avoid creation
        #   of new columns
        dataset_per_day.columns = headers_df

        # Identify which groups each subject belongs to
        index_subjectinfo, age_group, gender, age, mus_train, lat, \
            nLang, edu_class = find_subject(subject,subjects_info,header_info)


        # Add columns that will serve to identify and analyze the data
        dataset_per_day['Day'] = date_dict[file]
        dataset_per_day['Subject'] = subject
        dataset_per_day['Age group'] = age_group
        dataset_per_day['Gender'] = gender
        dataset_per_day['Age'] = age
        dataset_per_day['Musical training'] = mus_train
        dataset_per_day['Laterality'] = lat
        dataset_per_day['Spoken languages'] = nLang
        dataset_per_day['Education level'] = edu_class
        

        # Join DataFrames from each day in a list of DataFrames
        dataset_per_subject.append(dataset_per_day)
        
        # Erase DataFrame variable to avoid size problems when assigning headers
        del dataset_per_day
        
# Join all the DataFrames in just one DataFrame
full_dataset = pd.concat(dataset_per_subject)

# Export the dataset to a file
full_dataset.to_csv('Tablet_training_FULLresults.csv')

# Use columns Day, Group and Subject as indices.
# Organize the dataset by them.
indexed_dataset = full_dataset.set_index(['Day','Age group','Subject',
                                          'Age', 'Gender', 'Musical training', 
                                          'Laterality', 'Spoken languages',
                                          'Education level'])

# Calculate max level in the dataset when grouped by Day(0),Group(1),Subject(2)
max_level_byGroups = indexed_dataset['Level'].groupby(level=(0,1,2,3,4,5,6,7,8)).max()

# Convert indexed columns into normal columns
max_level_byGroups = max_level_byGroups.reset_index()

# Change empty cells to NaN
max_level_byGroups = max_level_byGroups.replace(r'', np.nan)


# Plot: https://seaborn.pydata.org/generated/seaborn.relplot.html

# sns.relplot(x="Day", y="Level", style="Age group", col="Age group", 
#               hue="Age group", kind="line", data=max_level_byGroups)
    # x -> Data in x axis
    # y -> Data in y axis
    # col -> Divide in columns by input
    # kind -> Plots it as a line
    # data -> Inputs the matrix where the data is
    # style -> Changes style depending on input
    # hue -> Changes color depending on input
            

#************ Plot the maximum level reach in the tablet by: *************#

#~~~~~ Age group separated
sns.relplot(x="Day", y="Level", style="Age group", col="Age group", 
            hue="Age group", kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_YoungVsOld_sep.png", dpi=300)

#~~~~~ Age group together
sns.relplot(x="Day", y="Level", style="Age group", hue="Age group", 
            kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_YoungVsOld_tog.png", dpi=300)

#~~~~~ Gender separated
sns.relplot(x="Day", y="Level", style="Gender", col="Gender", 
            hue="Gender", kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Gender_sep.png", dpi=300)

#~~~~~ Gender together
sns.relplot(x="Day", y="Level", style="Gender", hue="Gender", 
            kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Gender_tog.png", dpi=300)

#~~~~~ Musical training separated
sns.relplot(x="Day", y="Level", style="Musical training", col="Musical training", 
            hue="Musical training", kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Musical_training_sep.png", dpi=300)

#~~~~~ Musical training together
sns.relplot(x="Day", y="Level", style="Musical training", hue="Musical training", 
            kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Musical_training_tog.png", dpi=300)

#~~~~~ Laterality separated
sns.relplot(x="Day", y="Level", style="Laterality", col="Laterality", 
            hue="Laterality", kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Laterality_sep.png", dpi=300)

#~~~~~ Laterality together
sns.relplot(x="Day", y="Level", style="Laterality", hue="Laterality", 
            kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Laterality_tog.png", dpi=300)

#~~~~~ Spoken languages separated
sns.relplot(x="Day", y="Level", style="Spoken languages", col="Spoken languages", 
            hue="Spoken languages", kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_SpokenLanguages_sep.png", dpi=300)

#~~~~~ Spoken languages together
sns.relplot(x="Day", y="Level", style="Spoken languages", hue="Spoken languages", 
            kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_SpokenLanguages_tog.png", dpi=300)

#~~~~~ Education level separated
sns.relplot(x="Day", y="Level", style="Education level", col="Education level", 
            hue="Education level", kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Education_level_sep.png", dpi=300)

#~~~~~ Education level together
sns.relplot(x="Day", y="Level", style="Education level", hue="Education level", 
            kind="line", data=max_level_byGroups)
plt.savefig("MaxLevel_Education_level_tog.png", dpi=300)


# #~~~~~ XXXXXXXXX separated
# sns.relplot(x="Day", y="Level", style="XXXXXXXXX", col="XXXXXXXXX", 
#             hue="XXXXXXXXX", kind="line", data=max_level_byGroups)
# #plt.savefig("MaxLevel_XXXXXXXXX_sep.png", dpi=300)

# #~~~~~ XXXXXXXXX together
# sns.relplot(x="Day", y="Level", style="XXXXXXXXX", hue="XXXXXXXXX", 
#             kind="line", data=max_level_byGroups)
# #plt.savefig("MaxLevel_XXXXXXXXX_tog.png", dpi=300)

