function conf = confidence(data_fft, f, lower_lim, upper_lim)
indexes = f > lower_lim & f < upper_lim;

[M, ~] = max(abs(data_fft(indexes)).*2);

trap = (trapz(f(indexes),abs(data_fft(indexes)).*2));
conf = M / ((trap)/9.3);
