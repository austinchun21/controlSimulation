% BiCopter Simulation (Non-Linear)
%   Austin Chun
%   August 2017

% Define constants for the simulation
m = 0.5; % kg
L = 0.25; % m
H = 0.05; 
I = m/12 * (L^2 + H^2);
g = 9.81;

%% Run simulation (Non Linear)
tstop = 25; % seconds
[t,pos] = sim('BiCopter',tstop);

x = pos(:,1);
y = pos(:,2);
theta = pos(:,3);
vx = pos(:,4);
vy = pos(:,5);
omega = pos(:,6);


figure(1)
subplot(3,2,1)
plot(t,pos(:,1))
subplot(3,2,2)
plot(t,pos(:,2))
subplot(3,2,3)
plot(t,pos(:,3))
subplot(3,2,4)
plot(t,pos(:,4))
subplot(3,2,5)
plot(t,pos(:,5))
subplot(3,2,6)
plot(t,pos(:,6))