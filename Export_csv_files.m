%% Export .mat files to .txt files for Python

% Declare the initial path
orig_path = "A:\Zaida\OneDrive\CLASSES\Intro_Programming\Project\Tablet_Data";

% Change directory to initial path
cd(orig_path)

%% Get list of subject's folders
working_directory = dir();

% Obtained from: https://www.mathworks.com/matlabcentral/answers/166629-is-there-any-way-to-list-all-folders-only-in-the-level-directly-below-a-selected-directory

% Add directories ONLY to the loop
dirFlags = [ working_directory.isdir ];
wd_onlyfolders = working_directory(dirFlags);

% Create empty cell 
subjects = cell(length(wd_onlyfolders)-2,1);

% Append folders to empty cell and omit first two folders ('.', '..')
for index = 1:(length(wd_onlyfolders)-2)
    subjects{index} = wd_onlyfolders(index+2).name;
end

%% Export file

% Loop through subjects' folders
for folder = 1:length(subjects)
    cd(subjects{folder})  % Enter subject's directory
    subject_directory = dir('*.mat');  % List of .mat files ONLY
    days = cell(length(subject_directory),1);  % Empty cell
    
    % Append filenames to empty cell
    for index = 1:(length(subject_directory))
        days{index} = subject_directory(index).name;  % Cell with filenames
    end
    
    % When there are not .mat files in subject's directory, go back to
    % orig_path and exit to parent loop
    if isempty(days)
        cd(orig_path)
        continue
    else % when there are .mat files
        
        % Loop through files per day
        for day = 1:length(days)
            % Get the filename in char array and load
            input_filename = char(days(day));
            load(input_filename)
            fprintf('Currently working in: %s\n', input_filename)
            
            % Split column 10 in three cells
            column_ten = cellfun(@(x) strsplit(x,'     '), S.testlog(:,10), 'UniformOutput', false);
            
            % Convert column 10 in doubles
            export_file = cellfun(@(x) str2double(x), column_ten, 'UniformOutput', false);
            
            % Substitute original column 10 with edited one
            export_file{1,1}='S.loud'; % Add header that was erased from column 10
            empty = [];
            S.testlog(:,10)=export_file; % Substitute column
            
            % Erase useless data
            S.testlog{11,1}=empty; 
            S.testlog{12,1}=empty;

            % Convert cell array to table
            table_per_day=cell2table(S.testlog(:,:));

            % Erase 'Response Time' column
            short_table_per_day = removevars(table_per_day,{'Var12'});
            
            % Create .txt filename
            output_filename = [input_filename(1:end-4) '.csv'];

            % Export table to .txt file, using delimiter ',' and omiting
            % headers
            writetable(short_table_per_day,output_filename,'WriteVariableNames', 0, 'Delimiter', ',')

        end
    end
    
    % Return to original path
    cd(orig_path)
    
end

