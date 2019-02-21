clear all
close all

% Wavelength (in nm)
wvl = 1000;

% Refractive indices
n2 = 1.38;
n1 = 2.32;
n0 = 1;
ns = 1.5;

% Number of layers
Nstk = 4;

% Mirror stack n and width
Mirrn = [repmat([n1,n2],1,Nstk)];
Mirrw = [repmat([wvl/(4*n1),wvl/(4*n2)],1,Nstk)];

% Add air and substrate
fulln = [1,n0,Mirrn,ns];
fullw = [0,wvl/n0,Mirrw,wvl/ns];

% Run transfer matrix function
[r,t,x,Nn,E] = tmm(wvl,fulln, fullw);

% Units in um and offset
x = x/1e3-1;

% Plot n and E
figure(1)
subplot(2,1,1)
plot(x,Nn,'Color','blue')
ylabel('Refractive index n')
xlabel('Distance (um)')
xlim([min(x),max(x)])
title(['r = ', sprintf('%.5f', r) ,', t = ', sprintf('%.5f', t)])
subplot(2,1,2)
plot(x,abs(E).^2,'Color','red')
ylabel('Normalized |E|^2')
xlabel('Distance (um)')
xlim([min(x),max(x)])

% Save plot as png
saveas(gcf,'example_dbr.png')

% Redefine (fixed) mirror
Mirrw = [repmat([107.7586,181.1594],1,Nstk)];
fullw = [0,1000,Mirrw,666.6667];

% Wavelengths array
wvls = linspace(wvl-600,wvl+600,301);

% Loop through wavelengths
for ii=1:length(wvls)
   [r,t,x,Nn,E] = tmm(wvls(ii),fulln, fullw);
   R(ii) = abs(r)^2 * 100;
end

% Plot reflectance vs wvls
figure(2)
plot(wvls,R,'Color','blue')
ylabel('Reflectance (%)')
xlabel('Wavelength (nm)')
