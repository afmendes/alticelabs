function [y, time_array] = segment_data(data, time, windowSize, windowRoll)
L = length(data);
%Ignore extra data
n = floor(L/windowRoll);
data = data(1:n*windowRoll + 1);
time = time(1:n*windowRoll + 1);
y = zeros(windowSize, n-4);
time_array = zeros(windowSize, n-4);
for count = 1:(n-4)
    time_array(:,count) = time(1+(count-1)*windowRoll:(windowSize+(count-1)*windowRoll));
    y(:,count) = data(1+(count-1)*windowRoll:(windowSize+(count-1)*windowRoll));
end
