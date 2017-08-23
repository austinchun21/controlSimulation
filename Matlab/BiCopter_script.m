% BiCopter Simulation (Non-Linear)
%   Austin Chun
%   August 2017

% Define constants for the simulation
m = 0.5; % kg
L = 0.5; % m
H = 0.1; 
I = m/12 * (L^2 + H^2);
g = 9.81;

c = 0.4;
b = 0.4;

%% Run simulation (Non Linear)
%{
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
%}
%% Define state-space (linearized model)

% r = [0; 2; 0; 0; 0; 0];
r = [0; 10];

%x = r;
%u = [1; 1];

A = [0 0 0 1 0 0;
     0 0 0 0 1 0;
     0 0 0 0 0 1;
     0 0 -g -c/m 0 0;
     0 0 0 0 -c/m 0;
     0 0 0 0 0 -b/m];
B = [0 0;
     0 0;
     0 0;
     0 0;
     1/m 1/m;
     -L/(2*I) L/(2*I)];
C = [1 0 0 0 0 0; 
     0 1 0 0 0 0;];
D = 0;

p = -0.5*ones(1,6);
for i = 1:6
    p(i) = p(i) + 0.01*i;
end
%p(5) = -0.001
%p(6) = -0.2

K = place(A,B,p)

%size(K)
%Kr = -inv( (C-D*K)*inv(A-B*K)*B - D)
% inv(A-B*K)*B
Kr = -inv( (C)*inv(A-B*K)*B)

C = zeros(6,6);
C(2,2) = 1;
D = zeros(6,2);

tstop = 100;
[t,pos] = sim('BiCopter_Linear', tstop);

figure(2)
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






