% BiCopter Simulation Height Only
%   Austin Chun
%   August 2017

% Define constants for the simulation
m = 5; % kg
L = 0.5; % m
H = 0.1; 
I = m/12 * (L^2 + H^2);
g = 9.81;

c = 0.04;

%% Define matrices
A = [0 1;
     0 -c/m];
B = [0; 2/m];
C = [1 1];
D = 0;

p = [-12 -1];
K = place(A,B,p)
size(C*(A-B*K)*B)
Kr = -inv( (C-D*K)*inv(A-B*K)*B - D)

C = eye(2);
D = [0; 0];

r = 2;
tstop = 5;
[t,x] = sim('BiCopter_Height',tstop);

figure(1)
plot(t,x)


