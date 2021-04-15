clearvars, clc

data = readtable("Readings.csv","VariableNamingRule","preserve");
raw_data = table2array(data(:,"z_accel"));

clear data

[respiratory_rate, hearth_rate, valid_hr] = freq_proc(raw_data);