clear; clc; close all; addpath(genpath('../'));
dataset_name = 'motorcycle';
experiment_name = 'esann_2019';
% load(sprintf('../experiments/dataset_divisions/%s_%s.mat',experiment_name, dataset_name));

mkdir('../experiments/plots');
mkdir(sprintf('../experiments/plots/%s',experiment_name));
% X = dataset(:,1);
% y = dataset(:,2);


X = linspace(-3*pi,3*pi,200)';
ruido = 0.3 * rand(size(X,1),1);
ruido = ruido - mean(ruido);

y =  sin(X)./X + ruido;

%% save data
dlmwrite(sprintf('../experiments/plots/%s/data.csv',experiment_name),[X y]);

%% M-FOCUSS MLM
clf1 = MF_MLM(struct('lambda', 0.0001,'p',0.0001,'selection_type',2));
clf1.fit(X,y);
% save reference points
dlmwrite(sprintf('../experiments/plots/%s/rp_rmf_mlm.csv',experiment_name),[X(clf1.parameters.rp_index_in) y(clf1.parameters.rp_index_in)]);
dlmwrite(sprintf('../experiments/plots/%s/data_rmf_mlm.csv',experiment_name),[X clf1.predict(X)]);
figure,clf1.plot();


%% RANDOM MLM
clf2 = MLM(struct('selection_type',4));
clf2.fit(X,y);
% save reference points
dlmwrite(sprintf('../experiments/plots/%s/rp_fl_mlm.csv',experiment_name),[X(clf2.parameters.rp_index_in) y(clf2.parameters.rp_index_in)]);
X_ = [linspace(min(X),max(X),500)]';
dlmwrite(sprintf('../experiments/plots/%s/data_fl_mlm.csv',experiment_name),[X_ clf2.predict(X_)]);
figure,clf2.plot();

%% RANDOM MLM
clf3 = MLM(struct('M',size(clf1.parameters.rp_index_in,1),'selection_type',2));
clf3.fit(X,y);
%% save reference points (proposal)
dlmwrite(sprintf('../experiments/plots/%s/rp_rn_mlm.csv',experiment_name),[X(clf3.parameters.rp_index_in) y(clf3.parameters.rp_index_in)]);
dlmwrite(sprintf('../experiments/plots/%s/data_rn_mlm.csv',experiment_name),[X clf3.predict(X)]);
figure,clf3.plot();



% clf.plot();
% figure
% clf2.plot();
