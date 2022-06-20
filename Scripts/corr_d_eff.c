#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
void corr_d_eff() {
  int n = 10;
  double X[10] = {0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425};//, 0.45, 0.475, 0.5, 0.525, 0.55];
  double Y_sig[10] = {35.4857, 37.3315, 39.171, 41.0672, 42.7114, 44.3304, 45.9116, 47.2723, 48.4566, 49.7165};
  double Y_rat[10] = {1.07565, 1.11521, 1.14361, 1.16024, 1.17196, 1.17643, 1.17653, 1.17633, 1.1756, 1.17043};
  double Y_bkg_w[10] = {96.8361, 96.8842, 96.9304, 96.9697, 97.0023, 97.0317, 97.0622, 97.0902, 97.1136, 97.1386};
  double Y_bkg_tt[10] = {97.0384, 97.3565, 97.602, 97.7953, 97.9483, 98.0707, 98.1718, 98.2561, 98.3285, 98.3903};
  double Y_bkg_total[10] = {96.9453, 97.1391, 97.2928, 97.4152, 97.5127, 97.5923, 97.6609, 97.7194, 97.7692, 97.814};

  TCanvas *c_corr = new TCanvas("c_corr", "c1", 1000, 700);
  TGraph *gr_sig = new TGraph(n, X, Y_sig);
  TGraph *gr_rat = new TGraph(n, X, Y_rat);
  TGraph *gr_bkg_w = new TGraph(n, X, Y_bkg_w);
  TGraph *gr_bkg_tt = new TGraph(n, X, Y_bkg_tt);
  TGraph *gr_bkg_total = new TGraph(n, X, Y_bkg_total);

  gr_sig->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_sig->GetYaxis()->SetRangeUser(0,100);
  gr_sig->SetMarkerStyle(20);
  gr_sig->SetMarkerSize(0.5);
  gr_sig->SetTitle("Signal Efficiency-#d dependence; #d (cm); eff (%)");

  gr_rat->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_rat->GetYaxis()->SetRangeUser(0,100);
  gr_rat->SetMarkerStyle(20);
  gr_rat->SetMarkerSize(0.5);
  gr_rat->SetTitle("Signal over Sig+Bkg; #d (cm); ratio (%)");

  gr_bkg_w->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_bkg_w->GetYaxis()->SetRangeUser(0,100);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(0.5);
  gr_bkg_w->SetTitle("WJets Efficiency-#d dependence; #d (cm); eff (%)");

  gr_bkg_tt->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_bkg_tt->GetYaxis()->SetRangeUser(0,100);
  gr_bkg_tt->SetMarkerStyle(20);
  gr_bkg_tt->SetMarkerSize(0.5);
  gr_bkg_tt->SetTitle("TTJets Efficiency-#d dependence; #d (cm); eff (%)");

  gr_bkg_total->GetXaxis()->SetRangeUser(0.2,X[n]);
  gr_bkg_total->GetYaxis()->SetRangeUser(0,100);
  gr_bkg_total->SetMarkerStyle(20);
  gr_bkg_total->SetMarkerSize(0.5);
  gr_bkg_total->SetTitle("Total Efficiency-#d dependence; #d (cm); eff (%)");

  gr_sig->Draw();
  c_corr->SaveAs("corr_d_eff_sig");
  gr_rat->Draw();
  c_corr->SaveAs("corr_d_eff_rat");
  gr_bkg_w->Draw();
  c_corr->SaveAs("corr_d_eff_w");
  gr_bkg_tt->Draw();
  c_corr->SaveAs("corr_d_eff_tt");
  gr_bkg_total->Draw();
  c_corr->SaveAs("corr_d_eff_total");
}
