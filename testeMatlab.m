close all; clear; clc;

load('v2');
load('x2');
load('stim_times');

figure;
hold on;
%plot(v,'r');
plot(x);

%plot(stim_times, ones(length(stim_times)),'r*');

hold off;