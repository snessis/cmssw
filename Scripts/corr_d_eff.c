#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
void corr_d_eff() {
  int n = 10;
  double X[n] = [];
  double Y_sig[n] = [];
  double Y_bkg_w[n] = [];
  double Y_bkg_tt[n] = [];
  double Y_bkg_total[n] = [];

  TCanvas *c_corr = new TCanvas("c_corr", "c1", 1000, 700);
  TGraph *gr_sig = new TGraph(n, X, Y_sig);
  TGraph *gr_bkg_w = new TGraph(n, X, Y_bkg_w);
  TGraph *gr_bkg_tt = new TGraph(n, X, Y_bkg_tt);
  TGraph *gr_bkg_total = new TGraph(n, X, Y_bkg_total);

  gr_sig->GetXaxis()->SetRangeUser(0,);
  gr_sig->GetYaxis()->SetRangeUser(0,100);
  gr_sig->SetMarkerStyle(20);
  gr_sig->SetMarkerSize(0.5);
  gr_sig->SetTitle("Signal Efficiency-#d dependence; #d (cm); eff (%)");

  gr_bkg_w->GetXaxis()->SetRangeUser(0,);
  gr_bkg_w->GetYaxis()->SetRangeUser(0,100);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(0.5);
  gr_bkg_w->SetTitle("WJets Efficiency-#d dependence; #d (cm); eff (%)");

  gr_bkg_tt->GetXaxis()->SetRangeUser(0,);
  gr_bkg_tt->GetYaxis()->SetRangeUser(0,100);
  gr_bkg_tt->SetMarkerStyle(20);
  gr_bkg_tt->SetMarkerSize(0.5);
  gr_bkg_tt->SetTitle("TTJets Efficiency-#d dependence; #d (cm); eff (%)");

  gr_bkg_total->GetXaxis()->SetRangeUser(0,);
  gr_bkg_total->GetYaxis()->SetRangeUser(0,100);
  gr_bkg_total->SetMarkerStyle(20);
  gr_bkg_total->SetMarkerSize(0.5);
  gr_bkg_total->SetTitle("Total Efficiency-#d dependence; #d (cm); eff (%)");
}
