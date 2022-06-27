#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
double bg_fit(double *x, double *par) {
	return par[0] - par[1]*TMath::Exp(-abs(par[2])*x[0]);
}

void corr_d_eff_45() {
  const int n = 32;
  double X[n] = {0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8};
  double Y_sig[n] = {17.3428, 20.732, 23.8188, 26.704, 29.0349, 31.2461, 33.3753, 35.4857, 37.3315, 39.171, 41.0672, 42.7114, 44.3304, 45.9116, 47.2723, 48.4566, 49.7165, 51.1906, 52.4316, 53.6979, 54.9893, 55.9909, 56.9422, 57.9186, 58.8824, 59.903, 60.8983, 61.8118, 62.6622, 63.4119, 64.193, 64.9553};
  double Y_rat[n] = {0.353311, 0.491178, 0.625744, 0.755758, 0.86825, 0.956794, 1.02507, 1.07565, 1.11521, 1.14361, 1.16024, 1.17196, 1.17643, 1.17653, 1.17633, 1.1756, 1.17043, 1.15776, 1.14813, 1.13558, 1.12007, 1.1114, 1.10216, 1.09092, 1.07928, 1.06608, 1.05113, 1.03741, 1.02477, 1.01409, 1.00216, 0.990379};
  double Y_bkg_w[n] = {93.3035, 95.0172, 95.805, 96.2972, 96.5505, 96.6895, 96.7735, 96.8361, 96.8842, 96.9304, 96.9697, 97.0023, 97.0317, 97.0622, 97.0902, 97.1136, 97.1386, 97.1661, 97.1934, 97.2171, 97.2395, 97.2659, 97.2902, 97.3136, 97.3373, 97.3635, 97.3847, 97.4046, 97.4239, 97.4427, 97.4624, 97.4821};
  double Y_bkg_tt[n] = {83.4703, 88.9289, 92.0358, 93.9757, 95.2123, 96.0339, 96.615, 97.0384, 97.3565, 97.602, 97.7953, 97.9483, 98.0707, 98.1718, 98.2561, 98.3285, 98.3903, 98.442, 98.4869, 98.5282, 98.5639, 98.5966, 98.6256, 98.6517, 98.6761, 98.6991, 98.7194, 98.7386, 98.7572, 98.7743, 98.7902, 98.8055};
  double Y_bkg_total[n] = {87.9975, 91.7319, 93.7711, 95.0445, 95.8284, 96.3357, 96.688, 96.9453, 97.1391, 97.2928, 97.4152, 97.5127, 97.5923, 97.6609, 97.7194, 97.7692, 97.814, 97.8546, 97.8914, 97.9246, 97.9542, 97.9839, 98.0108, 98.0357, 98.0597, 98.0842, 98.1049, 98.1244, 98.1433, 98.1612, 98.1789, 98.1962};

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
  gr_sig->SetTitle("\\mbox{Signal Efficiency-Distance dependence } e_{40}; d \\mbox{(cm)}; e_{40} \\mbox{ (%)}");

  gr_rat->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_rat->SetMarkerStyle(20);
  gr_rat->SetMarkerSize(1);
  gr_rat->SetMarkerColor(kRed+2);
  gr_rat->SetName("gr_rat");
  gr_rat->SetTitle("\\mbox{Signal Density } k_4; d \\mbox{ (cm)}; k_4 \\mbox{ (%)}");

  gr_bkg_w->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(1);
  gr_bkg_w->SetMarkerColor(kBlue+1);
  gr_bkg_w->SetName("gr_bkg_w");
  gr_bkg_w->SetTitle("WJets Efficiency-Distance dependence; d \\mbox{(cm)}; eff (%)");

  gr_bkg_tt->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_tt->SetMarkerStyle(20);
  gr_bkg_tt->SetMarkerSize(1);
  gr_bkg_tt->SetMarkerColor(kYellow+1);
  gr_bkg_tt->SetName("gr_bkg_tt");
  gr_bkg_tt->SetTitle("TTJets Efficiency-Distance dependence; d \\mbox{ (cm)}; eff (%)");

  gr_bkg_total->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_total->SetMarkerStyle(20);
  gr_bkg_total->SetMarkerSize(1);
  gr_bkg_total->SetMarkerColor(kGreen+1);
  gr_bkg_total->SetName("gr_bkg_total");
  gr_bkg_total->SetTitle("Total Efficiency-Distance dependence; d \\mbox{ (cm)}; eff (%)");

  TMultiGraph *mg_bkg = new TMultiGraph();
  mg_bkg->SetTitle("\\mbox{Background Efficiency-Distance dependence } e_{4j}; d \\mbox{ (cm)}; e_{4j} \\mbox{ (%)}");
  mg_bkg->Add(gr_bkg_w);
  mg_bkg->Add(gr_bkg_tt);
  mg_bkg->Add(gr_bkg_total);

  auto leg_sig = new TLegend(0.65,0.83,0.9,0.9);
  leg_sig->AddEntry(gr_sig,"Signal Efficiency e_{40}","p");
  leg_sig->SetTextSize(0.03);
  auto leg_rat = new TLegend(0.65,0.83,0.9,0.9);
  leg_rat->AddEntry(gr_rat,"Signal Density k_{4}","p");
  leg_rat->SetTextSize(0.035);
  auto leg_bkg = new TLegend(0.65,0.1,0.9,0.25);
  leg_bkg->AddEntry(gr_bkg_w,"WJets Background e_{4W}","p");
  leg_bkg->AddEntry(gr_bkg_tt,"TTJets Background e_{4T}","p");
  leg_bkg->AddEntry(gr_bkg_total,"Total Background e_{4}","p");
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
  c_corr->SaveAs("corr_d_eff_sig_45.png");
  gr_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat_45.png");
  mg_bkg->Draw("AP");
  leg_bkg->Draw();
  c_corr->SaveAs("corr_d_eff_total_45.png");
}
