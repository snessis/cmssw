#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
double bg_fit(double *x, double *par) {
	return par[0] - par[1]*TMath::Exp(-abs(par[2])*x[0]);
}

void corr_d_eff_75() {
  const int n = 10;
  double X[n] = {0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425};
  double Y_sig[n] = {61.7551, 64.3505, 66.8263, 68.8925, 70.7005};
  double Y_rat[n] = {5.54217, 6.09007, 6.513, 6.90085, 7.24113};
  double Y_bkg_w[n] = {99.7806, 99.7968, 99.8088, 99.8215, 99.8315};
  double Y_bkg_tt[n] = {99.5653, 99.6488, 99.7088, 99.7519, 99.7857};
  double Y_bkg_total[n] = {99.6644, 99.717, 99.7548, 99.7839, 99.8068};

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
  gr_sig->SetTitle("\\mbox{Signal Efficiency-Distance dependence } e_{30}; d \\mbox{(cm)}; e_{30} \\mbox{ (%)}");

  gr_rat->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_rat->SetMarkerStyle(20);
  gr_rat->SetMarkerSize(1);
  gr_rat->SetMarkerColor(kRed+2);
  gr_rat->SetName("gr_rat");
  gr_rat->SetTitle("\\mbox{Signal Density } k_3; d \\mbox{ (cm)}; k_3 \\mbox{ (%)}");

  gr_bkg_w->GetXaxis()->SetRangeUser(0,X[n-1]);
  gr_bkg_w->SetMarkerStyle(20);
  gr_bkg_w->SetMarkerSize(1);
  gr_bkg_w->SetMarkerColor(kBlue+1);
  gr_bkg_w->SetName("gr_bkg_w");
  gr_bkg_w->SetTitle("WJets Efficiency-Distance dependence; d \\mbox{ (cm)}; eff (%)");

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
  mg_bkg->SetTitle("\\mbox{Background Efficiency-Distance dependence } e_{3j}; d \\mbox{ (cm)}; e_{3j} (%)");
  mg_bkg->Add(gr_bkg_w);
  mg_bkg->Add(gr_bkg_tt);
  mg_bkg->Add(gr_bkg_total);

  auto leg_sig = new TLegend(0.65,0.85,0.9,0.9);
  leg_sig->AddEntry(gr_sig,"Signal Efficiency e_{30}","p");
  leg_sig->SetTextSize(0.03);
  auto leg_rat = new TLegend(0.65,0.85,0.9,0.9);
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
