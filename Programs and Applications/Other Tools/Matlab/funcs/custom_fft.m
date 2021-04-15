function custom_fft(data, time, Fs, title_text, type)
L = length(data);
f = Fs*(0:(L/2))/L;

data_fft = fft(data);
data_fft_cut = abs(data_fft(1:numel(f))).*2;

switch type
    case "BPM"
        lower_lim = 0.7;
        upper_lim = 2;

        lower_lim_index = find(f>lower_lim,1,"first");
        upper_lim_index = find(f<upper_lim,1,"last");

        [M, I] = max(data_fft_cut(lower_lim_index:upper_lim_index));
        I = I + lower_lim_index - 1;
        
        fig = figure;
        subplot(211),plot(time, data)
        title(title_text),
        xlabel("T(s)")
        subplot(212),plot(f, data_fft_cut)
        title("FFT - estimated BPM: "+f(I)*60)
        xlim([lower_lim, upper_lim])
        xlabel("Hz")
        hold on
        plot(f(I), M, 'o', 'MarkerSize', 10)
    case "RR"
        lower_lim = 0.1;
        upper_lim = 0.6;

        lower_lim_index = find(f>lower_lim,1,"first");
        upper_lim_index = find(f<upper_lim,1,"last");

        [M, I] = max(data_fft_cut(lower_lim_index:upper_lim_index));
        I = I + lower_lim_index - 1;
        
        fig = figure;
        subplot(211),plot(time, data)
        title(title_text),
        xlabel("T(s)")
        subplot(212),plot(f, data_fft_cut)
        title("FFT - estimated RR: "+f(I)*60)
        xlim([lower_lim, upper_lim])
        xlabel("Hz")
        hold on
        plot(f(I), M, 'o', 'MarkerSize', 10)
    case "ALL"
        lower_lim_rr = 0.1;
        upper_lim_rr = 0.6;

        lower_lim_index_rr = find(f>lower_lim_rr,1,"first");
        upper_lim_index_rr = find(f<upper_lim_rr,1,"last");

        [M_rr, I_rr] = max(data_fft_cut(lower_lim_index_rr:upper_lim_index_rr));
        I_rr = I_rr + lower_lim_index_rr - 1;
        disp("Estimated RR: " + f(I_rr)*60)
        
        lower_lim_bpm = 0.7;
        upper_lim_bpm = 2;

        lower_lim_index_bpm = find(f>lower_lim_bpm,1,"first");
        upper_lim_index_bpm = find(f<upper_lim_bpm,1,"last");

        [M_bpm, I_bpm] = max(data_fft_cut(lower_lim_index_bpm:upper_lim_index_bpm));
        I_bpm = I_bpm + lower_lim_index_bpm - 1;
        disp("Estimated BPM: " + f(I_bpm)*60)
        
        fig = figure;
        subplot(311),plot(time, data)
        title(title_text),
        xlabel("T(s)")
        subplot(312),plot(f, data_fft_cut)
        title("FFT - estimated RR: "+f(I_rr)*60)
        xlim([lower_lim_rr, upper_lim_rr])
        xlabel("Hz")
        hold on
        plot(f(I_rr), M_rr, 'o', 'MarkerSize', 10)
        subplot(313),plot(f, data_fft_cut)
        title("FFT - estimated BPM: "+f(I_bpm)*60)
        xlim([lower_lim_bpm, upper_lim_bpm])
        xlabel("Hz")
        hold on
        plot(f(I_bpm), M_bpm, 'o', 'MarkerSize', 10)
end

saveas(fig,"output/"+title_text+".fig")
saveas(fig,"output/"+title_text+".jpeg")