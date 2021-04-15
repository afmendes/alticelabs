clearvars, clc, close all

pesos = [1160,5435,8205,9545,12245,15155,20580,24745]'/1000;
frente_dir = [40000,200000,337000,397000,548000,598000,727000,840000]';
frente_esq = [52.5  230 335 390 482 547 633 780]'*1000;
traseira_esq = [46800,220000,352000,380000,433000,511000,560000,740000]';
traseira_dir = [1000,166000,253000,287000,321000,362000,470000,536000]';

figure,
hold on
plot(pesos,frente_dir,"b.","MarkerSize",15)
plot(pesos,frente_esq,"r.","MarkerSize",15)
plot(pesos,traseira_esq,"k.","MarkerSize",15)
plot(pesos,traseira_dir,"g.","MarkerSize",15)

m = 3.389e4;
b = 4.962e4;
plot([0 24.745],[b m*24.745+b],"b")

m = 2.915e4;
b = 7.746e4;
plot([0 24.745],[b m*24.745+b],"r")

m = 2.647e4;
b = 8.42e4;
plot([0 24.745],[b m*24.745+b],"k")

m = 2.108e4;
b = 4.367e4;
plot([0 24.745],[b m*24.745+b],"g")


legend("Frente Esquerda","Frente Direita",...
    "Traseira Esquerda","Traseira Direita","","","","")

xlabel("Massa (Kg)")
ylabel("U.A.")