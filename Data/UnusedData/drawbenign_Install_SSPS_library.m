data=xlsread('installforSPSS_benign.xlsx',3,'A2:G1697');
failure_rate=data(:,1);
minsdk=data(:,2);
api=data(:,3);
year=data(:,4);
api_year=data(:,5);
api_minus_year=data(:,6);
api_minus_minsdk=data(:,7);
x=api_minus_minsdk;
y=api_minus_year;
z=failure_rate;

%draw 3D scatter diagram with input data
figure;
scatter3(x,y,z);
%title name may change
title('Library failed installation percentage distribution among different API level');
t1=xlabel('API lapse', 'FontSize',12,'FontWeight','bold','Color','m');
t2=ylabel('App lapse', 'FontSize',12,'FontWeight','bold','Color','r');
zlabel('IIR', 'FontSize',12,'FontWeight','bold','Color','black');



