#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void corr_d_attach2() {
  const int n3 = 30;
  double X3[n3] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375 ,0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75};
  double Y3_sig[n3] = {43.0389, 45.5147, 47.9715, 50.0567, 51.808, 53.5656, 55.109, 56.7469, 58.1517, 59.5061, 60.9676, 62.1393, 63.3489, 64.4702, 65.434, 66.379, 67.1979, 68.2563, 69.1697, 70.1462, 71.11, 71.8281, 72.5589, 73.2708, 73.9259, 74.6504, 75.337, 75.9859, 76.5718, 77.0757};
  double Y3_rat[n3] = {0.430507, 0.62169, 0.815925, 1.00466, 1.17674, 1.31538, 1.42621, 1.5012, 1.55624, 1.59384, 1.60864, 1.61969, 1.61541, 1.60939, 1.60175, 1.58949, 1.57825, 1.55264, 1.53221, 1.50381, 1.47432, 1.45573, 1.43635, 1.41482, 1.39421, 1.37127, 1.34837, 1.32533, 1.30461, 1.28774};
  double Y3_bkg_w[n3] = {97.3824, 97.8908, 98.1217, 98.2512, 98.3343, 98.3915, 98.4292, 98.4559, 98.4764, 98.4975, 98.515, 98.5315, 98.5439, 98.5592, 98.5726, 98.5849, 98.5964, 98.6097, 98.6245, 98.6349, 98.6468, 98.6581, 98.6718, 98.683, 98.6928, 98.7059, 98.718, 98.7274, 98.7357, 98.7446};
  double Y3_bkg_tt[n3] = {89.6634, 93.4895, 95.5681, 96.7966, 97.5596, 98.0484, 98.3799, 98.6096, 98.7742, 98.8964, 98.9892, 99.0587, 99.1126, 99.1568, 99.1918, 99.2212, 99.2458, 99.2658, 99.2831, 99.299, 99.3125, 99.3253, 99.3366, 99.3466, 99.3558, 99.3645, 99.3721, 99.3798, 99.3876, 99.3945};
  double Y3_bkg_total[n3] = {93.2172, 95.5158, 96.7437, 97.4663, 97.9163, 98.2064, 98.4026, 98.5388, 98.6371, 98.7128, 98.7708, 98.816, 98.8507, 98.8817, 98.9067, 98.9283, 98.9468, 98.9637, 98.9799, 98.9933, 99.006, 99.0181, 99.0305, 99.0411, 99.0506, 99.0613, 99.071, 99.0795, 99.0875, 99.0953};

  const int n4 = 30;
  double X4[n4] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375 ,0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75};
  double Y4_sig[n4] = {49.5716, 55.2665, 59.4872, 62.9772, 65.8876, 68.3697, 70.669, 72.5904, 74.2598, 75.9166, 77.2647, 78.5498, 79.8224, 80.9941, 82.0209, 82.9785, 84.0179, 84.9061, 85.7251, 86.5881, 87.3567, 87.9488, 88.4969, 89.1206, 89.6308, 90.1222, 90.6262, 91.0609, 91.3758, 91.7349};
  double Y4_rat[n4] = {0.747159, 1.3005, 1.98684, 2.79861, 3.681, 4.58607, 5.48316, 6.37937, 7.19752, 7.88509, 8.56251, 9.17425, 9.63983, 10.0484, 10.3915, 10.7372, 10.8352, 10.8951, 10.9835, 10.9204, 10.9022, 10.9489, 10.9893, 11.0466, 10.993, 11.0518, 10.9678, 11.0078, 11.1186, 11.0072};
  double Y4_bkg_w[n4] = {99.2684, 99.6147, 99.7424, 99.806, 99.8416, 99.8618, 99.8781, 99.8903, 99.8995, 99.9067, 99.9136, 99.9196, 99.9246, 99.9303, 99.9349, 99.9394, 99.9422, 99.9443, 99.9472, 99.949, 99.9513, 99.9534, 99.9549, 99.9579, 99.9591, 99.9612, 99.9625, 99.9645, 99.9661, 99.9667};
  double Y4_bkg_tt[n4] = {94.2326, 97.0895, 98.3129, 98.9386, 99.2835, 99.49, 99.6216, 99.7098, 99.7691, 99.8111, 99.8421, 99.866, 99.8839, 99.8972, 99.9077, 99.9167, 99.9238, 99.9297, 99.9347, 99.9391, 99.943, 99.9462, 99.9495, 99.9524, 99.9548, 99.9573, 99.9594, 99.9613, 99.9631, 99.9646};
  double Y4_bkg_total[n4] = {96.551, 98.2521, 98.971, 99.338, 99.5404, 99.6612, 99.7397, 99.7929, 99.8291, 99.8551, 99.875, 99.8907, 99.9026, 99.9124, 99.9202, 99.9271, 99.9323, 99.9364, 99.9404, 99.9437, 99.9468, 99.9495, 99.952, 99.9549, 99.9568, 99.9591, 99.9608, 99.9628, 99.9645, 99.9656};

  TCanvas *c_corr = new TCanvas("c_corr", "Correlation Canvas Attach", 1000, 700);
  TGraph *gr_sig3 = new TGraph(n3, X3, Y3_sig);
  TGraph *gr_rat3 = new TGraph(n3, X3, Y3_rat);
  TGraph *gr_sig4 = new TGraph(n4, X4, Y4_sig);
  TGraph *gr_rat4 = new TGraph(n4, X4, Y4_rat);

  gr_sig3->GetXaxis()->SetRangeUser(0,X3[n3-1]);
  gr_sig3->GetYaxis()->SetRangeUser(0,100);
  gr_sig3->SetMarkerStyle(20);
  gr_sig3->SetMarkerSize(1);
  gr_sig3->SetMarkerColor(kMagenta+1);
  gr_sig3->SetName("gr_sig3");
  gr_sig3->SetTitle("\\mbox{Signal Efficiency-Distance dependence } e_{60}; d \\mbox{(cm)}; e_{60} \\mbox{ (%)}");

  gr_rat3->GetXaxis()->SetRangeUser(0,X3[n3-1]);
  gr_rat3->SetMarkerStyle(20);
  gr_rat3->SetMarkerSize(1);
  gr_rat3->SetMarkerColor(kMagenta+1);
  gr_rat3->SetName("gr_rat3");
  gr_rat3->SetTitle("\\mbox{Signal Density } k_6; d \\mbox{ (cm)}; k_6 \\mbox{ (%)}");

  gr_sig4->GetXaxis()->SetRangeUser(0,X4[n4-1]);
  gr_sig4->GetYaxis()->SetRangeUser(0,100);
  gr_sig4->SetMarkerStyle(20);
  gr_sig4->SetMarkerSize(1);
  gr_sig4->SetMarkerColor(kRed+2);
  gr_sig4->SetName("gr_sig4");
  gr_sig4->SetTitle("\\mbox{Signal Efficiency-Distance dependence } e_{50}; d \\mbox{(cm)}; e_{50} \\mbox{ (%)}");

  gr_rat4->GetXaxis()->SetRangeUser(0,X4[n4-1]);
  gr_rat4->SetMarkerStyle(20);
  gr_rat4->SetMarkerSize(1);
  gr_rat4->SetMarkerColor(kRed+2);
  gr_rat4->SetName("gr_rat4");
  gr_rat4->SetTitle("\\mbox{Signal Density } k_5; d \\mbox{ (cm)}; k_5 \\mbox{ (%)}");

  TMultiGraph *mg_sig = new TMultiGraph();
  mg_sig->SetTitle("\\mbox{Signal Efficiency-Distance dependence } e_{i0}; d \\mbox{ (cm)}; e_{i0} \\mbox{ (%)}");
  mg_sig->Add(gr_sig3);
  mg_sig->Add(gr_sig4);

  TMultiGraph *mg_rat = new TMultiGraph();
  mg_rat->SetTitle("\\mbox{Signal Density } k_{i}; d \\mbox{ (cm)}; k_{i} \\mbox{ (%)}");
  mg_rat->Add(gr_rat3);
  mg_rat->Add(gr_rat4);

  auto leg_sig = new TLegend(0.65,0.1,0.9,0.25);
  leg_sig->SetTextSize(0.035);
  leg_sig->AddEntry(gr_sig3,"STATE6 Signal e_{60}","p");
  leg_sig->AddEntry(gr_sig4,"STATE6 Signal e_{50}","p");
  auto leg_rat = new TLegend(0.65,0.4,0.9,0.55);
  leg_sig->SetTextSize(0.035);
  leg_rat->AddEntry(gr_rat3,"STATE5 Signal k_{6}","p");
  leg_rat->AddEntry(gr_rat4,"STATE6 Signal k_{5}","p");
  c_corr->SetGridx();
  c_corr->SetGridy();
  c_corr->GetFrame()->SetFillColor(21);
  c_corr->GetFrame()->SetBorderMode(-1);
  c_corr->GetFrame()->SetBorderSize(5);

  mg_sig->Draw("AP");
  leg_sig->Draw();
  c_corr->SaveAs("corr_d_eff_sig_attach2.png");
  mg_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_attach2.png");


}
