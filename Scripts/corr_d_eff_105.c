#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
double bg_fit(double *x, double *par) {
	return par[0] - par[1]*TMath::Exp(-abs(par[2])*x[0]);
}

void corr_d_eff_105() {
	const int n = 25;
	double X[n] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375 ,0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625};
  double Y_sig[n] = {49.5716, 55.2665, 59.4872, 62.9772, 65.8876, 68.3697, 70.669, 72.5904, 74.2598, 75.9166, 77.2647, 78.5498, 79.8224, 80.9941, 82.0209, 82.9785, 84.0179, 84.9061, 85.7251, 86.5881, 87.3567, 87.9488, 88.4969, 89.1206, 89.6308};
  double Y_rat[n] = {0.747159, 1.3005, 1.98684, 2.79861, 3.681, 4.58607, 5.48316, 6.37937, 7.19752, 7.88509, 8.56251, 9.17425, 9.63983, 10.0484, 10.3915, 10.7372, 10.8352, 10.8951, 10.9835, 10.9204, 10.9022, 10.9489, 10.9893, 11.0466, 10.993};
  double Y_bkg_w[n] = {99.2684, 99.6147, 99.7424, 99.806, 99.8416, 99.8618, 99.8781, 99.8903, 99.8995, 99.9067, 99.9136, 99.9196, 99.9246, 99.9303, 99.9349, 99.9394, 99.9422, 99.9443, 99.9472, 99.949};
  double Y_bkg_tt[n] = {94.2326, 97.0895, 98.3129, 98.9386, 99.2835, 99.49, 99.6216, 99.7098, 99.7691, 99.8111, 99.8421, 99.866, 99.8839, 99.8972, 99.9077, 99.9167, 99.9238, 99.9297, 99.9347, 99.9391};
  double Y_bkg_total[n] = {96.551, 98.2521, 98.971, 99.338, 99.5404, 99.6612, 99.7397, 99.7929, 99.8291, 99.8551, 99.875, 99.8907, 99.9026, 99.9124, 99.9202, 99.9271, 99.9323, 99.9364, 99.9404, 99.9437};

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
  gr_sig->SetMarkerColor(kMagenta+1);
  gr_sig->SetName("gr_sig");
  gr_sig->SetTitle("\\mbox{Signal Efficiency-Displacement dependence } e_{70}; d \\mbox{ (cm)}; e_{70} \\mbox{ (%)}");

  gr_rat->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_rat->SetMarkerStyle(20);
  gr_rat->SetMarkerSize(1);
  gr_rat->SetMarkerColor(kMagenta+1);
  gr_rat->SetName("gr_rat");
  gr_rat->SetTitle("\\mbox{Signal Density-Displacement dependence } k_7; d \\mbox{ (cm)}; k_7 \\mbox{ (%)}");

  gr_bkg_w->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(1);
  gr_bkg_w->SetMarkerColor(kBlue+1);
  gr_bkg_w->SetName("gr_bkg_w");
  gr_bkg_w->SetTitle("WJets Efficiency-Displacement dependence; d \\mbox{ (cm)}; eff (%)");

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
  mg_bkg->SetTitle("\\mbox{Background Efficiency-Displacement dependence } e_{7j}; d \\mbox{ (cm)}; e_{7j} \\mbox{ (%)}");
  mg_bkg->Add(gr_bkg_w);
  mg_bkg->Add(gr_bkg_tt);
  mg_bkg->Add(gr_bkg_total);

  auto leg_sig = new TLegend(0.65,0.83,0.9,0.9);
  leg_sig->AddEntry(gr_sig,"Signal Efficiency e_{70}","p");
  leg_sig->SetTextSize(0.03);
  auto leg_rat = new TLegend(0.1,0.83,0.35,0.9);
  leg_rat->AddEntry(gr_rat,"Signal Density k_{7}","p");
  leg_rat->SetTextSize(0.035);
  auto leg_bkg = new TLegend(0.65,0.1,0.9,0.25);
  leg_bkg->AddEntry(gr_bkg_w,"WJets Background e_{7W}","p");
  leg_bkg->AddEntry(gr_bkg_tt,"TTJets Background e_{7T}","p");
  leg_bkg->AddEntry(gr_bkg_total,"Total Background e_{7}","p");
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
  c_corr->SaveAs("corr_d_eff_sig_105.png");
  gr_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_105.png");
  mg_bkg->Draw("AP");
  leg_bkg->Draw();
  c_corr->SaveAs("corr_d_eff_total_105.png");
}
