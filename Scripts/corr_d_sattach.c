#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void corr_d_sattach() {
	const int n3 = 25;
  double X3[n3] = {0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675};
  double Y3_sig[n3] = {42.6106, 47.5495, 51.8899, 55.5122, 58.9139, 61.7551, 64.3505, 66.8263, 68.8925, 70.7005, 72.477, 74.0771, 75.463, 76.7418, 78.2474, 79.4633, 80.6413, 81.7941, 82.8147, 83.6777, 84.4904, 85.3408, 86.0086, 86.6826, 87.3945};
  double Y3_rat[n3] = {1.91031, 2.65153, 3.41285, 4.17804, 4.89096, 5.54217, 6.09007, 6.513, 6.90085, 7.24113, 7.48959, 7.67483, 7.82832, 7.98967, 7.96348, 7.96381, 7.97872, 7.90201, 7.87612, 7.84557, 7.79378, 7.75416, 7.7255, 7.6889, 7.58026};
  double Y3_bkg_w[n3] = {99.5262, 99.6331, 99.6926, 99.7314, 99.7609, 99.7806, 99.7968, 99.8088, 99.8215, 99.8315, 99.8407, 99.8497, 99.8577, 99.8656, 99.8714, 99.8768, 99.8832, 99.8879, 99.8933, 99.8976, 99.9008, 99.9056, 99.9091, 99.9128, 99.9155};
  double Y3_bkg_tt[n3] = {97.5926, 98.4757, 98.9631, 99.2557, 99.4417, 99.5653, 99.6488, 99.7088, 99.7519, 99.7857, 99.8116, 99.8307, 99.8458, 99.8591, 99.8699, 99.8787, 99.8866, 99.8932, 99.8993, 99.9044, 99.9096, 99.9142, 99.9181, 99.9218, 99.9255};
  double Y3_bkg_total[n3] = {98.4828, 99.0086, 99.299, 99.4747, 99.5887, 99.6644, 99.717, 99.7548, 99.7839, 99.8068, 99.825, 99.8394, 99.8513, 99.8621, 99.8706, 99.8778, 99.885, 99.8908, 99.8965, 99.9013, 99.9055, 99.9102, 99.914, 99.9177, 99.9209};

	const int n4 = 32;
  double X4[n4] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8};
  double Y4_sig[n4] = {17.3428, 20.732, 23.8188, 26.704, 29.0349, 31.2461, 33.3753, 35.4857, 37.3315, 39.171, 41.0672, 42.7114, 44.3304, 45.9116, 47.2723, 48.4566, 49.7165, 51.1906, 52.4316, 53.6979, 54.9893, 55.9909, 56.9422, 57.9186, 58.8824, 59.903, 60.8983, 61.8118, 62.6622, 63.4119, 64.193, 64.9553};
  double Y4_rat[n4] = {0.353311, 0.491178, 0.625744, 0.755758, 0.86825, 0.956794, 1.02507, 1.07565, 1.11521, 1.14361, 1.16024, 1.17196, 1.17643, 1.17653, 1.17633, 1.1756, 1.17043, 1.15776, 1.14813, 1.13558, 1.12007, 1.1114, 1.10216, 1.09092, 1.07928, 1.06608, 1.05113, 1.03741, 1.02477, 1.01409, 1.00216, 0.990379};
  double Y4_bkg_w[n4] = {93.3035, 95.0172, 95.805, 96.2972, 96.5505, 96.6895, 96.7735, 96.8361, 96.8842, 96.9304, 96.9697, 97.0023, 97.0317, 97.0622, 97.0902, 97.1136, 97.1386, 97.1661, 97.1934, 97.2171, 97.2395, 97.2659, 97.2902, 97.3136, 97.3373, 97.3635, 97.3847, 97.4046, 97.4239, 97.4427, 97.4624, 97.4821};
  double Y4_bkg_tt[n4] = {83.4703, 88.9289, 92.0358, 93.9757, 95.2123, 96.0339, 96.615, 97.0384, 97.3565, 97.602, 97.7953, 97.9483, 98.0707, 98.1718, 98.2561, 98.3285, 98.3903, 98.442, 98.4869, 98.5282, 98.5639, 98.5966, 98.6256, 98.6517, 98.6761, 98.6991, 98.7194, 98.7386, 98.7572, 98.7743, 98.7902, 98.8055};
  double Y4_bkg_total[n4] = {87.9975, 91.7319, 93.7711, 95.0445, 95.8284, 96.3357, 96.688, 96.9453, 97.1391, 97.2928, 97.4152, 97.5127, 97.5923, 97.6609, 97.7194, 97.7692, 97.814, 97.8546, 97.8914, 97.9246, 97.9542, 97.9839, 98.0108, 98.0357, 98.0597, 98.0842, 98.1049, 98.1244, 98.1433, 98.1612, 98.1789, 98.1962};

	const int n5 = 30;
  double X5[n4] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375 ,0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75};
  double Y5_sig[n5] = {49.5716, 55.2665, 59.4872, 62.9772, 65.8876, 68.3697, 70.669, 72.5904, 74.2598, 75.9166, 77.2647, 78.5498, 79.8224, 80.9941, 82.0209, 82.9785, 84.0179, 84.9061, 85.7251, 86.5881, 87.3567, 87.9488, 88.4969, 89.1206, 89.6308, 90.1222, 90.6262, 91.0609, 91.3758, 91.7349};
  double Y5_rat[n5] = {0.747159, 1.3005, 1.98684, 2.79861, 3.681, 4.58607, 5.48316, 6.37937, 7.19752, 7.88509, 8.56251, 9.17425, 9.63983, 10.0484, 10.3915, 10.7372, 10.8352, 10.8951, 10.9835, 10.9204, 10.9022, 10.9489, 10.9893, 11.0466, 10.993, 11.0518, 10.9678, 11.0078, 11.1186, 11.0072};
  double Y5_bkg_w[n5] = {99.2684, 99.6147, 99.7424, 99.806, 99.8416, 99.8618, 99.8781, 99.8903, 99.8995, 99.9067, 99.9136, 99.9196, 99.9246, 99.9303, 99.9349, 99.9394, 99.9422, 99.9443, 99.9472, 99.949, 99.9513, 99.9534, 99.9549, 99.9579, 99.9591, 99.9612, 99.9625, 99.9645, 99.9661, 99.9667};
  double Y5_bkg_tt[n5] = {94.2326, 97.0895, 98.3129, 98.9386, 99.2835, 99.49, 99.6216, 99.7098, 99.7691, 99.8111, 99.8421, 99.866, 99.8839, 99.8972, 99.9077, 99.9167, 99.9238, 99.9297, 99.9347, 99.9391, 99.943, 99.9462, 99.9495, 99.9524, 99.9548, 99.9573, 99.9594, 99.9613, 99.9631, 99.9646};
  double Y5_bkg_total[n5] = {96.551, 98.2521, 98.971, 99.338, 99.5404, 99.6612, 99.7397, 99.7929, 99.8291, 99.8551, 99.875, 99.8907, 99.9026, 99.9124, 99.9202, 99.9271, 99.9323, 99.9364, 99.9404, 99.9437, 99.9468, 99.9495, 99.952, 99.9549, 99.9568, 99.9591, 99.9608, 99.9628, 99.9645, 99.9656};

	const int n6 = 30;
  double X6[n6] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375 ,0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75};
  double Y6_sig[n6] = {43.0389, 45.5147, 47.9715, 50.0567, 51.808, 53.5656, 55.109, 56.7469, 58.1517, 59.5061, 60.9676, 62.1393, 63.3489, 64.4702, 65.434, 66.379, 67.1979, 68.2563, 69.1697, 70.1462, 71.11, 71.8281, 72.5589, 73.2708, 73.9259, 74.6504, 75.337, 75.9859, 76.5718, 77.0757};
  double Y6_rat[n6] = {0.430507, 0.62169, 0.815925, 1.00466, 1.17674, 1.31538, 1.42621, 1.5012, 1.55624, 1.59384, 1.60864, 1.61969, 1.61541, 1.60939, 1.60175, 1.58949, 1.57825, 1.55264, 1.53221, 1.50381, 1.47432, 1.45573, 1.43635, 1.41482, 1.39421, 1.37127, 1.34837, 1.32533, 1.30461, 1.28774};
  double Y6_bkg_w[n6] = {97.3824, 97.8908, 98.1217, 98.2512, 98.3343, 98.3915, 98.4292, 98.4559, 98.4764, 98.4975, 98.515, 98.5315, 98.5439, 98.5592, 98.5726, 98.5849, 98.5964, 98.6097, 98.6245, 98.6349, 98.6468, 98.6581, 98.6718, 98.683, 98.6928, 98.7059, 98.718, 98.7274, 98.7357, 98.7446};
  double Y6_bkg_tt[n6] = {89.6634, 93.4895, 95.5681, 96.7966, 97.5596, 98.0484, 98.3799, 98.6096, 98.7742, 98.8964, 98.9892, 99.0587, 99.1126, 99.1568, 99.1918, 99.2212, 99.2458, 99.2658, 99.2831, 99.299, 99.3125, 99.3253, 99.3366, 99.3466, 99.3558, 99.3645, 99.3721, 99.3798, 99.3876, 99.3945};
  double Y6_bkg_total[n6] = {93.2172, 95.5158, 96.7437, 97.4663, 97.9163, 98.2064, 98.4026, 98.5388, 98.6371, 98.7128, 98.7708, 98.816, 98.8507, 98.8817, 98.9067, 98.9283, 98.9468, 98.9637, 98.9799, 98.9933, 99.006, 99.0181, 99.0305, 99.0411, 99.0506, 99.0613, 99.071, 99.0795, 99.0875, 99.0953};

  TCanvas *c_corr = new TCanvas("c_scorr", "Correlation Canvas SAttach", 1000, 700);
  TGraph *gr_sig3 = new TGraph(n3, X3, Y3_sig);
  TGraph *gr_rat3 = new TGraph(n3, X3, Y3_rat);
  TGraph *gr_sig4 = new TGraph(n4, X4, Y4_sig);
  TGraph *gr_rat4 = new TGraph(n4, X4, Y4_rat);
	TGraph *gr_sig5 = new TGraph(n5, X5, Y5_sig);
  TGraph *gr_rat5 = new TGraph(n5, X5, Y5_rat);
  TGraph *gr_sig6 = new TGraph(n6, X6, Y6_sig);
  TGraph *gr_rat6 = new TGraph(n6, X6, Y6_rat);

	gr_sig3->GetXaxis()->SetRangeUser(0,X3[n3-1]);
  gr_sig3->GetYaxis()->SetRangeUser(0,100);
  gr_sig3->SetMarkerStyle(21);
  gr_sig3->SetMarkerSize(1);
  gr_sig3->SetMarkerColor(kViolet-6);
  gr_sig3->SetName("gr_sig3");
  gr_sig3->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{30}; d \\mbox{(cm)}; e_{30} \\mbox{ (%)}");

  gr_rat3->GetXaxis()->SetRangeUser(0,X3[n3-1]);
  gr_rat3->SetMarkerStyle(21);
  gr_rat3->SetMarkerSize(1);
  gr_rat3->SetMarkerColor(kViolet-6);
  gr_rat3->SetName("gr_rat3");
  gr_rat3->SetTitle("\\mbox{Signal Density-Displacement dependence} k_3; d \\mbox{ (cm)}; k_3 \\mbox{ (%)}");

  gr_sig4->GetXaxis()->SetRangeUser(0,X4[n4-1]);
  gr_sig4->GetYaxis()->SetRangeUser(0,100);
  gr_sig4->SetMarkerStyle(21);
  gr_sig4->SetMarkerSize(1);
  gr_sig4->SetMarkerColor(kOrange+7);
  gr_sig4->SetName("gr_sig4");
  gr_sig4->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{40}; d \\mbox{(cm)}; e_{40} \\mbox{ (%)}");

  gr_rat4->GetXaxis()->SetRangeUser(0,X4[n4-1]);
  gr_rat4->SetMarkerStyle(21);
  gr_rat4->SetMarkerSize(1);
  gr_rat4->SetMarkerColor(kOrange+7);
  gr_rat4->SetName("gr_rat4");
  gr_rat4->SetTitle("\\mbox{Signal Density-Displacement dependence } k_4; d \\mbox{ (cm)}; k_4 \\mbox{ (%)}");

	gr_sig5->GetXaxis()->SetRangeUser(0,X5[n5-1]);
  gr_sig5->GetYaxis()->SetRangeUser(0,100);
  gr_sig5->SetMarkerStyle(20);
  gr_sig5->SetMarkerSize(1);
  gr_sig5->SetMarkerColor(kMagenta+1);
  gr_sig5->SetName("gr_sig5");
  gr_sig5->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{50}; d \\mbox{(cm)}; e_{50} \\mbox{ (%)}");

  gr_rat5->GetXaxis()->SetRangeUser(0,X5[n5-1]);
  gr_rat5->SetMarkerStyle(20);
  gr_rat5->SetMarkerSize(1);
  gr_rat5->SetMarkerColor(kMagenta+1);
  gr_rat5->SetName("gr_rat5");
  gr_rat5->SetTitle("\\mbox{Signal Density-Displacement dependence } k_5; d \\mbox{ (cm)}; k_5 \\mbox{ (%)}");

  gr_sig6->GetXaxis()->SetRangeUser(0,X6[n6-1]);
  gr_sig6->GetYaxis()->SetRangeUser(0,100);
  gr_sig6->SetMarkerStyle(20);
  gr_sig6->SetMarkerSize(1);
  gr_sig6->SetMarkerColor(kRed+2);
  gr_sig6->SetName("gr_sig6");
  gr_sig6->SetTitle("\\mbox{Rejection Signal Efficiency-Displacement dependence } e_{60}; d \\mbox{(cm)}; e_{60} \\mbox{ (%)}");

  gr_rat6->GetXaxis()->SetRangeUser(0,X6[n6-1]);
  gr_rat6->SetMarkerStyle(20);
  gr_rat6->SetMarkerSize(1);
  gr_rat6->SetMarkerColor(kRed+2);
  gr_rat6->SetName("gr_rat6");
  gr_rat6->SetTitle("\\mbox{Signal Density-Displacement dependence } k_6; d \\mbox{ (cm)}; k_6 \\mbox{ (%)}");

  TMultiGraph *mg_sig = new TMultiGraph();
  mg_sig->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{i0}; d \\mbox{ (cm)}; e_{i0} \\mbox{ (%)}");
  mg_sig->Add(gr_sig3);
  mg_sig->Add(gr_sig4);
	mg_sig->Add(gr_sig5);
  mg_sig->Add(gr_sig6);

  TMultiGraph *mg_rat = new TMultiGraph();
  mg_rat->SetTitle("\\mbox{Signal Density-Displacement dependence } k_{i}; d \\mbox{ (cm)}; k_{i} \\mbox{ (%)}");
  mg_rat->Add(gr_rat3);
  mg_rat->Add(gr_rat4);
	mg_rat->Add(gr_rat5);
  mg_rat->Add(gr_rat6);

  auto leg_sig = new TLegend(0.63,0.14,0.9,0.4);
  leg_sig->SetTextSize(0.035);
	leg_sig->SetFillColor(16);
  leg_sig->AddEntry(gr_sig3,"STATE3 Signal e_{30}","p");
  leg_sig->AddEntry(gr_sig4,"STATE4 Signal e_{40}","p");
	leg_sig->AddEntry(gr_sig5,"STATE5 Signal e_{50}","p");
  leg_sig->AddEntry(gr_sig6,"STATE6 Signal e_{60}","p");
  auto leg_rat = new TLegend(0.63,0.32,0.9,0.56);
  leg_rat->SetTextSize(0.035);
	leg_rat->SetFillColor(16);
  leg_rat->AddEntry(gr_rat3,"STATE3 Signal k_{3}","p");
  leg_rat->AddEntry(gr_rat4,"STATE4 Signal k_{4}","p");
	leg_rat->AddEntry(gr_rat5,"STATE5 Signal k_{5}","p");
	leg_rat->AddEntry(gr_rat6,"STATE6 Signal k_{6}","p");
  c_corr->SetGridx();
  c_corr->SetGridy();
  c_corr->GetFrame()->SetFillColor(26);
  c_corr->GetFrame()->SetBorderMode(-1);
  c_corr->GetFrame()->SetBorderSize(5);
	c_corr->SetFillColor(18);

  mg_sig->Draw("AP");
  leg_sig->Draw();
  c_corr->SaveAs("corr_d_eff_sig_sattach.png");
  mg_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_sattach.png");


}
