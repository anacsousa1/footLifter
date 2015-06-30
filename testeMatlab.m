close all; clear; clc;

load('v');
load('x');

figure;
hold on;
plot(v/norm(v),'r');
plot(x/norm(x));
hold off;