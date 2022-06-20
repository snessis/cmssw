#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
void corr_d_eff() {
  int n = 15;
  double X[15] = {0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55};
  double Y_sig[15] = {35.4857, 37.3315, 39.171, 41.0672, 42.7114, 44.3304, 45.9116, 47.2723, 48.4566, 49.7165, 51.1906, 52.4316, 53.6979, 54.9893, 55.9909};
  double Y_rat[15] = {1.07565, 1.11521, 1.14361, 1.16024, 1.17196, 1.17643, 1.17653, 1.17633, 1.1756, 1.17043, 1.15776, 1.14813, 1.13558, 1.12007, 1.1114};
  double Y_bkg_w[15] = {96.8361, 96.8842, 96.9304, 96.9697, 97.0023, 97.0317, 97.0622, 97.0902, 97.1136, 97.1386, 97.1661, 97.1934, 97.2171, 97.2395, 97.2659};
  double Y_bkg_tt[15] = {97.0384, 97.3565, 97.602, 97.7953, 97.9483, 98.0707, 98.1718, 98.2561, 98.3285, 98.3903, 98.442, 98.4869, 98.5282, 98.5639, 98.5966};
  double Y_bkg_total[15] = {96.9453, 97.1391, 97.2928, 97.4152, 97.5127, 97.5923, 97.6609, 97.7194, 97.7692, 97.814, 97.8546, 97.8914, 97.9246, 97.9542, 97.9839};

  TCanvas *c_corr = new TCanvas("c_corr", "Correlation Canvas", 1000, 700);
  TGraph *gr_sig = new TGraph(n, X, Y_sig);
  TGraph *gr_rat = new TGraph(n, X, Y_rat);
  TGraph *gr_bkg_w = new TGraph(n, X, Y_bkg_w);
  TGraph *gr_bkg_tt = new TGraph(n, X, Y_bkg_tt);
  TGraph *gr_bkg_total = new TGraph(n, X, Y_bkg_total);

  gr_sig->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_sig->GetYaxis()->SetRangeUser(0,100);
  gr_sig->SetMarkerStyle(20);
  gr_sig->SetMarkerSize(1);
  gr_sig->SetMarkerColor(kRed+2);
  gr_sig->SetName("gr_sig");
  gr_sig->SetTitle("Signal Efficiency-Distance dependence; d \\mbox{(cm)}; eff (%)");

  gr_rat->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_rat->SetMarkerStyle(20);
  gr_rat->SetMarkerSize(1);
  gr_rat->SetMarkerColor(kRed+2);
  gr_rat->SetName("gr_rat");
  gr_rat->SetTitle("Signal over Sig+Bkg; #d (cm); ratio (%)");

  gr_bkg_w->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(1);
  gr_bkg_w->SetMarkerColor(kBlue+1);
  gr_bkg_w->SetName("gr_bkg_w");
  gr_bkg_w->SetTitle("WJets Efficiency-Distance dependence; d \\mbox{(cm)}; eff (%)");

  gr_bkg_tt->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_bkg_tt->SetMarkerStyle(20);
  gr_bkg_tt->SetMarkerSize(1);
  gr_bkg_tt->SetMarkerColor(kYellow+1);
  gr_bkg_tt->SetName("gr_bkg_tt");
  gr_bkg_tt->SetTitle("TTJets Efficiency-Distance dependence; d \\mbox{(cm)}; eff (%)");

  gr_bkg_total->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_bkg_total->SetMarkerStyle(20);
  gr_bkg_total->SetMarkerSize(1);
  gr_bkg_total->SetMarkerColor(kGreen+1);
  gr_bkg_total->SetName("gr_bkg_total");
  gr_bkg_total->SetTitle("Total Efficiency-Distance dependence; d \\mbox{(cm)}; eff (%)");

  TMultiGraph *mg_bkg = new TMultiGraph();
  mg_bkg->SetTitle("Background Efficiency-Distance dependence; d \\mbox{(cm)}; eff (%)");
  mg_bkg->Add(gr_bkg_w);
  mg_bkg->Add(gr_bkg_tt);
  mg_bkg->Add(gr_bkg_total);

  auto leg_sig = new TLegend(0.7,0.85,0.9,0.9);
  leg_sig->AddEntry(gr_sig,"Signal Efficiency","p");
  leg_sig->SetTextSize(0.035);
  auto leg_rat = new TLegend(0.7,0.85,0.9,0.9);
  leg_rat->AddEntry(gr_rat,"Signal Ratio","p");
  leg_rat->SetTextSize(0.035);
  auto leg_bkg = new TLegend(0.65,0.75,0.9,0.9);
  leg_bkg->AddEntry(gr_bkg_w,"WJets Background","p");
  leg_bkg->AddEntry(gr_bkg_tt,"TTJets Background","p");
  leg_bkg->AddEntry(gr_bkg_total,"Total Background","p");

  gr_sig->Draw("AP");
  leg_sig->Draw();
  c_corr->SaveAs("corr_d_eff_sig.png");
  gr_rat->Draw("AP");
  leg_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat.png");
  mg_bkg->Draw("AP");
  leg_bkg->Draw();
  c_corr->SaveAs("corr_d_eff_total.png");
}
