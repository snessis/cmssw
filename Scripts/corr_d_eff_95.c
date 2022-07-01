#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
double bg_fit(double *x, double *par) {
	return par[0] - par[1]*TMath::Exp(-abs(par[2])*x[0]);
}

void corr_d_eff_95() {
	const int n = 30;
	double X[n] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375 ,0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75};
  double Y_sig[n] = {43.0389, 45.5147, 47.9715, 50.0567, 51.808, 53.5656, 55.109, 56.7469, 58.1517, 59.5061, 60.9676, 62.1393, 63.3489, 64.4702, 65.434, 66.379, 67.1979, 68.2563, 69.1697, 70.1462, 71.11, 71.8281, 72.5589, 73.2708, 73.9259, 74.6504, 75.337, 75.9859, 76.5718, 77.0757};
  double Y_rat[n] = {0.430507, 0.62169, 0.815925, 1.00466, 1.17674, 1.31538, 1.42621, 1.5012, 1.55624, 1.59384, 1.60864, 1.61969, 1.61541, 1.60939, 1.60175, 1.58949, 1.57825, 1.55264, 1.53221, 1.50381, 1.47432, 1.45573, 1.43635, 1.41482, 1.39421, 1.37127, 1.34837, 1.32533, 1.30461, 1.28774};
  double Y_bkg_w[n] = {97.3824, 97.8908, 98.1217, 98.2512, 98.3343, 98.3915, 98.4292, 98.4559, 98.4764, 98.4975, 98.515, 98.5315, 98.5439, 98.5592, 98.5726, 98.5849, 98.5964, 98.6097, 98.6245, 98.6349, 98.6468, 98.6581, 98.6718, 98.683, 98.6928, 98.7059, 98.718, 98.7274, 98.7357, 98.7446};
  double Y_bkg_tt[n] = {89.6634, 93.4895, 95.5681, 96.7966, 97.5596, 98.0484, 98.3799, 98.6096, 98.7742, 98.8964, 98.9892, 99.0587, 99.1126, 99.1568, 99.1918, 99.2212, 99.2458, 99.2658, 99.2831, 99.299, 99.3125, 99.3253, 99.3366, 99.3466, 99.3558, 99.3645, 99.3721, 99.3798, 99.3876, 99.3945};
  double Y_bkg_total[n] = {93.2172, 95.5158, 96.7437, 97.4663, 97.9163, 98.2064, 98.4026, 98.5388, 98.6371, 98.7128, 98.7708, 98.816, 98.8507, 98.8817, 98.9067, 98.9283, 98.9468, 98.9637, 98.9799, 98.9933, 99.006, 99.0181, 99.0305, 99.0411, 99.0506, 99.0613, 99.071, 99.0795, 99.0875, 99.0953};

  TCanvas *c_corr = new TCanvas("c_corr", "Correlation Canvas", 1000, 700);
  TGraph *gr_sig = new TGraph(n, X, Y_sig);
  TGraph *gr_rat = new TGraph(n, X, Y_rat);
  TGraph *gr_bkg_w = new TGraph(n, X, Y_bkg_w);
  TGraph *gr_bkg_tt = new TGraph(n, X, Y_bkg_tt);
  TGraph *gr_bkg_total = new TGraph(n, X, Y_bkg_total);

  gr_sig->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_sig->GetYaxis()->SetRangeUser(0,100);
  gr_sig->SetMarkerStyle(20);
  gr_sig->SetMarkerSize(1);
  gr_sig->SetMarkerColor(kRed+2);
  gr_sig->SetName("gr_sig");
  gr_sig->SetTitle("\\mbox{Signal Efficiency-Displacement dependence } e_{60}; d \\mbox{ (cm)}; e_{60} \\mbox{ (%)}");

  gr_rat->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_rat->SetMarkerStyle(20);
  gr_rat->SetMarkerSize(1);
  gr_rat->SetMarkerColor(kRed+2);
  gr_rat->SetName("gr_rat");
  gr_rat->SetTitle("\\mbox{Signal Density-Displacement dependence } k_6; d \\mbox{ (cm)}; k_6 \\mbox{ (%)}");

  gr_bkg_w->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(1);
  gr_bkg_w->SetMarkerColor(kBlue+1);
  gr_bkg_w->SetName("gr_bkg_w");
  gr_bkg_w->SetTitle("WJets Efficiency-Displacementdependence; d \\mbox{(cm)}; eff (%)");

  gr_bkg_tt->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_tt->SetMarkerStyle(20);
  gr_bkg_tt->SetMarkerSize(1);
  gr_bkg_tt->SetMarkerColor(kYellow+1);
  gr_bkg_tt->SetName("gr_bkg_tt");
  gr_bkg_tt->SetTitle("TTJets Efficiency-Displacement dependence; d \\mbox{ (cm)}; eff (%)");

  gr_bkg_total->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_total->SetMarkerStyle(20);
  gr_bkg_total->SetMarkerSize(1);
  gr_bkg_total->SetMarkerColor(kGreen+1);
  gr_bkg_total->SetName("gr_bkg_total");
  gr_bkg_total->SetTitle("Total Efficiency-Displacement dependence; d \\mbox{ (cm)}; eff (%)");

  TMultiGraph *mg_bkg = new TMultiGraph();
  mg_bkg->SetTitle("\\mbox{Background Efficiency-Displacement dependence } e_{6j}; d \\mbox{ (cm)}; e_{6j} \\mbox{ (%)}");
  mg_bkg->Add(gr_bkg_w);
  mg_bkg->Add(gr_bkg_tt);
  mg_bkg->Add(gr_bkg_total);

  auto leg_sig = new TLegend(0.65,0.83,0.9,0.9);
  leg_sig->AddEntry(gr_sig,"Signal Efficiency e_{60}","p");
  leg_sig->SetTextSize(0.03);
  auto leg_rat = new TLegend(0.65,0.83,0.9,0.9);
  leg_rat->AddEntry(gr_rat,"Signal Density k_{6}","p");
  leg_rat->SetTextSize(0.035);
  auto leg_bkg = new TLegend(0.65,0.1,0.9,0.25);
  leg_bkg->AddEntry(gr_bkg_w,"WJets Background e_{6W}","p");
  leg_bkg->AddEntry(gr_bkg_tt,"TTJets Background e_{6T}","p");
  leg_bkg->AddEntry(gr_bkg_total,"Total Background e_{6}","p");
  c_corr->SetGridx();
  c_corr->SetGridy();
  c_corr->GetFrame()->SetFillColor(21);
  c_corr->GetFrame()->SetBorderMode(-1);
  c_corr->GetFrame()->SetBorderSize(5);
  TF1 *bg_fit_func = new TF1("bg_fit_func",bg_fit,0.01,0.7,3);
  bg_fit_func->SetParameters(98,1,20);
  //gr_bkg_total->Fit("bg_fit_func");

  gr_sig->Draw("AP");
  leg_sig->Draw();
  c_corr->SaveAs("corr_d_eff_sig_95.png");
  gr_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_95.png");
  mg_bkg->Draw("AP");
  leg_bkg->Draw();
  c_corr->SaveAs("corr_d_eff_total_95.png");
}
