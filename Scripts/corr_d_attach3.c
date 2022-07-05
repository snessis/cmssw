#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void corr_d_attach3() {
  const int n3 = 25;
  double X3[n3] = {0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675};
  double Y3_sig[n3] = {42.6106, 47.5495, 51.8899, 55.5122, 58.9139, 61.7551, 64.3505, 66.8263, 68.8925, 70.7005, 72.477, 74.0771, 75.463, 76.7418, 78.2474, 79.4633, 80.6413, 81.7941, 82.8147, 83.6777, 84.4904, 85.3408, 86.0086, 86.6826, 87.3945};
  double Y3_rat[n3] = {1.91031, 2.65153, 3.41285, 4.17804, 4.89096, 5.54217, 6.09007, 6.513, 6.90085, 7.24113, 7.48959, 7.67483, 7.82832, 7.98967, 7.96348, 7.96381, 7.97872, 7.90201, 7.87612, 7.84557, 7.79378, 7.75416, 7.7255, 7.6889, 7.58026};
  double Y3_bkg_w[n3] = {99.5262, 99.6331, 99.6926, 99.7314, 99.7609, 99.7806, 99.7968, 99.8088, 99.8215, 99.8315, 99.8407, 99.8497, 99.8577, 99.8656, 99.8714, 99.8768, 99.8832, 99.8879, 99.8933, 99.8976, 99.9008, 99.9056, 99.9091, 99.9128, 99.9155};
  double Y3_bkg_tt[n3] = {97.5926, 98.4757, 98.9631, 99.2557, 99.4417, 99.5653, 99.6488, 99.7088, 99.7519, 99.7857, 99.8116, 99.8307, 99.8458, 99.8591, 99.8699, 99.8787, 99.8866, 99.8932, 99.8993, 99.9044, 99.9096, 99.9142, 99.9181, 99.9218, 99.9255};
  double Y3_bkg_total[n3] = {98.4828, 99.0086, 99.299, 99.4747, 99.5887, 99.6644, 99.717, 99.7548, 99.7839, 99.8068, 99.825, 99.8394, 99.8513, 99.8621, 99.8706, 99.8778, 99.885, 99.8908, 99.8965, 99.9013, 99.9055, 99.9102, 99.914, 99.9177, 99.9209};

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
  gr_sig3->SetMarkerStyle(21);
  gr_sig3->SetMarkerSize(1);
  gr_sig3->SetMarkerColor(kViolet-3);
  gr_sig3->SetName("gr_sig3");
  gr_sig3->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{30}; d \\mbox{(cm)}; e_{30} \\mbox{ (%)}");

  gr_rat3->GetXaxis()->SetRangeUser(0,X3[n3-1]);
  gr_rat3->SetMarkerStyle(21);
  gr_rat3->SetMarkerSize(1);
  gr_rat3->SetMarkerColor(kViolet-3);
  gr_rat3->SetName("gr_rat3");
  gr_rat3->SetTitle("\\mbox{Signal Density-Displacement dependence} k_3; d \\mbox{ (cm)}; k_3 \\mbox{ (%)}");

  gr_sig4->GetXaxis()->SetRangeUser(0,X4[n4-1]);
  gr_sig4->GetYaxis()->SetRangeUser(0,100);
  gr_sig4->SetMarkerStyle(20);
  gr_sig4->SetMarkerSize(1);
  gr_sig4->SetMarkerColor(kMagenta+1);
  gr_sig4->SetName("gr_sig4");
  gr_sig4->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{50}; d \\mbox{(cm)}; e_{50} \\mbox{ (%)}");

  gr_rat4->GetXaxis()->SetRangeUser(0,X4[n4-1]);
  gr_rat4->SetMarkerStyle(20);
  gr_rat4->SetMarkerSize(1);
  gr_rat4->SetMarkerColor(kMagenta+1);
  gr_rat4->SetName("gr_rat4");
  gr_rat4->SetTitle("\\mbox{Signal Density-Displacement dependence } k_5; d \\mbox{ (cm)}; k_5 \\mbox{ (%)}");

  TMultiGraph *mg_sig = new TMultiGraph();
  mg_sig->SetTitle("\\mbox{Signal Rejection Efficiency-Displacement dependence } e_{i0}; d \\mbox{ (cm)}; e_{i0} \\mbox{ (%)}");
  mg_sig->Add(gr_sig3);
  mg_sig->Add(gr_sig4);

  TMultiGraph *mg_rat = new TMultiGraph();
  mg_rat->SetTitle("\\mbox{Signal Density-Displacement dependence } k_{i}; d \\mbox{ (cm)}; k_{i} \\mbox{ (%)}");
  mg_rat->Add(gr_rat3);
  mg_rat->Add(gr_rat4);

  auto leg_sig = new TLegend(0.65,0.1,0.9,0.25);
  leg_sig->SetTextSize(0.035);
  leg_sig->AddEntry(gr_sig3,"STATE3 Signal e_{30}","p");
  leg_sig->AddEntry(gr_sig4,"STATE5 Signal e_{50}","p");
  auto leg_rat = new TLegend(0.65,0.4,0.9,0.55);
  leg_sig->SetTextSize(0.035);
  leg_rat->AddEntry(gr_rat3,"STATE3 Signal k_{3}","p");
  leg_rat->AddEntry(gr_rat4,"STATE5 Signal k_{5}","p");
  c_corr->SetGridx();
  c_corr->SetGridy();
  c_corr->GetFrame()->SetFillColor(26);
  c_corr->GetFrame()->SetBorderMode(-1);
  c_corr->GetFrame()->SetBorderSize(5);

  mg_sig->Draw("AP");
  leg_sig->Draw();
  c_corr->SaveAs("corr_d_eff_sig_attach3.png");
  mg_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_attach3.png");


}
