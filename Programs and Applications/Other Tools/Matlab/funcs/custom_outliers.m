function cleanedData = custom_outliers(data,time)
% Fill outliers
[cleanedData,outlierIndices,thresholdLow,thresholdHigh,center] = ...
    filloutliers(data,"linear","movmedian",5.8e-06,"SamplePoints",time);

% Display results
clf
plot(time,data,"Color",[77 190 238]/255,"DisplayName","Input data")
hold on
plot(time,cleanedData,"Color",[0 114 189]/255,"LineWidth",1.5,...
    "DisplayName","Cleaned data")

% Plot outliers
plot(time(outlierIndices),data(outlierIndices),"x","Color",[64 64 64]/255,...
    "DisplayName","Outliers")
title("Number of outliers: " + nnz(outlierIndices))

% Plot filled outliers
plot(time(outlierIndices),cleanedData(outlierIndices),".","MarkerSize",12,...
    "Color",[217 83 25]/255,"DisplayName","Filled outliers")

% Plot outlier thresholds
plot([time(:); missing; time(:)],[thresholdHigh(:); missing; thresholdLow(:)],...
    "Color",[145 145 145]/255,"DisplayName","Outlier thresholds")

% Plot outlier center
plot(time,center,"k","LineWidth",2,"DisplayName","Outlier center")

hold off
legend
xlabel("Tempo (s)")
ylabel("U.A.")
clear outlierIndices thresholdLow thresholdHigh center