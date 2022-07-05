#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
double bg_fit(double *x, double *par) {
	return par[0] - par[1]*TMath::Exp(-abs(par[2])*x[0]);
}

void corr_d_eff_75() {
  const int n = 25;
  double X[n] = {0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675};
  double Y_sig[n] = {42.6106, 47.5495, 51.8899, 55.5122, 58.9139, 61.7551, 64.3505, 66.8263, 68.8925, 70.7005, 72.477, 74.0771, 75.463, 76.7418, 78.2474, 79.4633, 80.6413, 81.7941, 82.8147, 83.6777, 84.4904, 85.3408, 86.0086, 86.6826, 87.3945};
  double Y_rat[n] = {1.91031, 2.65153, 3.41285, 4.17804, 4.89096, 5.54217, 6.09007, 6.513, 6.90085, 7.24113, 7.48959, 7.67483, 7.82832, 7.98967, 7.96348, 7.96381, 7.97872, 7.90201, 7.87612, 7.84557, 7.79378, 7.75416, 7.7255, 7.6889, 7.58026};
  double Y_bkg_w[n] = {99.5262, 99.6331, 99.6926, 99.7314, 99.7609, 99.7806, 99.7968, 99.8088, 99.8215, 99.8315, 99.8407, 99.8497, 99.8577, 99.8656, 99.8714, 99.8768, 99.8832, 99.8879, 99.8933, 99.8976, 99.9008, 99.9056, 99.9091, 99.9128, 99.9155};
  double Y_bkg_tt[n] = {97.5926, 98.4757, 98.9631, 99.2557, 99.4417, 99.5653, 99.6488, 99.7088, 99.7519, 99.7857, 99.8116, 99.8307, 99.8458, 99.8591, 99.8699, 99.8787, 99.8866, 99.8932, 99.8993, 99.9044, 99.9096, 99.9142, 99.9181, 99.9218, 99.9255};
  double Y_bkg_total[n] = {98.4828, 99.0086, 99.299, 99.4747, 99.5887, 99.6644, 99.717, 99.7548, 99.7839, 99.8068, 99.825, 99.8394, 99.8513, 99.8621, 99.8706, 99.8778, 99.885, 99.8908, 99.8965, 99.9013, 99.9055, 99.9102, 99.914, 99.9177, 99.9209};

  TCanvas *c_corr = new TCanvas("c_corr", "Correlation Canvas", 1000, 700);
  TGraph *gr_sig = new TGraph(n, X, Y_sig);
  TGraph *gr_rat = new TGraph(n, X, Y_rat);
  TGraph *gr_bkg_w = new TGraph(n, X, Y_bkg_w);
  TGraph *gr_bkg_tt = new TGraph(n, X, Y_bkg_tt);
  TGraph *gr_bkg_total = new TGraph(n, X, Y_bkg_total);

  gr_sig->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_sig->GetYaxis()->SetRangeUser(0,100);
  gr_sig->SetMarkerStyle(21);
  gr_sig->SetMarkerSize(1);
  gr_sig->SetMarkerColor(kViolet-3);
  gr_sig->SetName("gr_sig");
  gr_sig->SetTitle("\\mbox{Signal Efficiency-Displacement dependence } e_{30}; d_t \\mbox{ (cm)}; e_{30} \\mbox{ (%)}");

  gr_rat->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_rat->SetMarkerStyle(21);
  gr_rat->SetMarkerSize(1);
  gr_rat->SetMarkerColor(kViolet-3);
  gr_rat->SetName("gr_rat");
  gr_rat->SetTitle("\\mbox{Signal Density-Displacement dependence } k_3; d_t \\mbox{ (cm)}; k_3 \\mbox{ (%)}");

  gr_bkg_w->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_w->SetMarkerStyle(21);
  gr_bkg_w->SetMarkerSize(1);
  gr_bkg_w->SetMarkerColor(kBlue+1);
  gr_bkg_w->SetName("gr_bkg_w");
  gr_bkg_w->SetTitle("WJets Efficiency-Displacement dependence; d_t \\mbox{ (cm)}; eff (%)");

  gr_bkg_tt->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_tt->SetMarkerStyle(21);
  gr_bkg_tt->SetMarkerSize(1);
  gr_bkg_tt->SetMarkerColor(kYellow+1);
  gr_bkg_tt->SetName("gr_bkg_tt");
  gr_bkg_tt->SetTitle("TTJets Efficiency-Displacement dependence; d_t \\mbox{ (cm)}; eff (%)");

  gr_bkg_total->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_total->SetMarkerStyle(21);
  gr_bkg_total->SetMarkerSize(1);
  gr_bkg_total->SetMarkerColor(kGreen+1);
  gr_bkg_total->SetName("gr_bkg_total");
  gr_bkg_total->SetTitle("Total Efficiency-Displacement dependence; d_t \\mbox{ (cm)}; eff (%)");

  TMultiGraph *mg_bkg = new TMultiGraph();
  mg_bkg->SetTitle("\\mbox{Background Rejection Efficiency-Displacement dependence } e_{3j}; d_t \\mbox{ (cm)}; e_{3j} \\mbox{ (%)}");
  mg_bkg->Add(gr_bkg_w);
  mg_bkg->Add(gr_bkg_tt);
  mg_bkg->Add(gr_bkg_total);

  auto leg_sig = new TLegend(0.65,0.83,0.9,0.9);
  leg_sig->AddEntry(gr_sig,"Signal Efficiency e_{30}","p");
  leg_sig->SetTextSize(0.03);
  auto leg_rat = new TLegend(0.1,0.83,0.35,0.9);
  leg_rat->AddEntry(gr_rat,"Signal Density k_{3}","p");
  leg_rat->SetTextSize(0.035);
  auto leg_bkg = new TLegend(0.65,0.1,0.9,0.25);
  leg_bkg->AddEntry(gr_bkg_w,"WJets Background e_{3W}","p");
  leg_bkg->AddEntry(gr_bkg_tt,"TTJets Background e_{3T}","p");
  leg_bkg->AddEntry(gr_bkg_total,"Total Background e_{3}","p");
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
  c_corr->SaveAs("corr_d_eff_sig_75.png");
  gr_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_75.png");
  mg_bkg->Draw("AP");
  leg_bkg->Draw();
  c_corr->SaveAs("corr_d_eff_total_75.png");
}
