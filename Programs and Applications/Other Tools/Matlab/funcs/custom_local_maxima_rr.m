function maxIndices = custom_local_maxima_rr(data,time)
% Find local maxima
maxIndices = islocalmax(data,"MinSeparation",3,"SamplePoints",time);
%maxIndices = maxIndices & (data > 0);
% Display results
clf
plot(time,data,"Color",[77 190 238]/255,"DisplayName","Input data")
hold on

% Plot local maxima
plot(time(maxIndices),data(maxIndices),"^","Color",[217 83 25]/255,...
    "MarkerFaceColor",[217 83 25]/255,"DisplayName","Local maxima")
title("Number of extrema: " + nnz(maxIndices) + " - Average respiration rate: " + nnz(maxIndices)/max(time)*60)
hold off
legend
xlabel("time")