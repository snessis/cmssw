#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void attach_x28() {
  double N1 = 748300; //HT 100 to 200
  double N1_a = 70290;
  double N2 = 1248911; //HT 200 to 400
  double N2_a = 202208;
  double N3 = 411531; //HT 400 to 600
  double N3_a = 85192;
  double N4 = 1560343; //HT 600 to 800
  double N4_a = 339364;
  double N5 = 737750; //HT 800 to 1200
  double N5_a = 168321;
  double N6 = 775061; //HT 1200 to 2500
  double N6_a = 182698;
  double N7 = 429253; //HT 2500 to Inf
  double N7_a = 114025;
  double N_ch = 711;
  double XSEC1 = 1395*1.17;
  double XSEC2 = 408.7*1.17;
  double XSEC3 = 57.52*1.17;
  double XSEC4 = 12.78*1.17;
  double XSEC5 = 5.246*1.17;
  double XSEC6 = 1.071*1.17;
  double XSEC7 = 0.00819*1.17;
  double XSECCH = 0.902569;
  double L = 1;
  double SF1 = N1_a / 29521158;
  double SF2 = N2_a / 25468933;
  double SF3 = N3_a / 5932701;
  double SF4 = N4_a / 19771294;
  double SF5 = N5_a / 8402687;
  double SF6 = N6_a / 7633949;
  double SF7 = N7_a / 3273980;
  double SFCH = N_ch / 539666;
  double BR = 0.1063; //W -> muonic
  double fake_scale = 1;

  TFile *f1 = new TFile("x27_1.root");
  TFile *f2 = new TFile("x27_2.root");
  TFile *f3 = new TFile("x27_3.root");
  TFile *f4 = new TFile("x27_4.root");
  TFile *f5 = new TFile("x27_5.root");
  TFile *f6 = new TFile("x27_6.root");
  TFile *f7 = new TFile("x27_7.root");
  TFile *fch = new TFile("x28.root");

  TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
  TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
  TH1F *h3 = (TH1F*)f3->Get("plots/jetht");
  TH1F *h4 = (TH1F*)f4->Get("plots/jetht");
  TH1F *h5 = (TH1F*)f5->Get("plots/jetht");
  TH1F *h6 = (TH1F*)f6->Get("plots/jetht");
  TH1F *h7 = (TH1F*)f7->Get("plots/jetht");
  TH1F *hch = (TH1F*)fch->Get("plots/jetht");
  TH1F *h_total = new TH1F("total_jetht", "\\mbox{Total Jet HT}", 100, 0, 3500);
  TH1F *h_ttotal = new TH1F("ttotal_jetht", "\\mbox{Total Jet HT (plus chargino)}", 100, 0, 3500);
  TH1F *h_acc = new TH1F("ttotal_acc", "\\mbox{Total Jet HT Acceptance (chargino/all)}", 100, 0, 3500);

  TH1F *l1 = (TH1F*)f1->Get("plots/lheht");
  TH1F *l2 = (TH1F*)f2->Get("plots/lheht");
  TH1F *l3 = (TH1F*)f3->Get("plots/lheht");
  TH1F *l4 = (TH1F*)f4->Get("plots/lheht");
  TH1F *l5 = (TH1F*)f5->Get("plots/lheht");
  TH1F *l6 = (TH1F*)f6->Get("plots/lheht");
  TH1F *l7 = (TH1F*)f7->Get("plots/lheht");
  TH1F *l_total = new TH1F("total_lheht", "\\mbox{Total Jet LHE HT}", 100, 0, 3500);

  h1->Scale(1/N1_a*XSEC1*L*SF1*BR*fake_scale);
  h2->Scale(1/N2_a*XSEC2*L*SF2*BR*fake_scale);
  h3->Scale(1/N3_a*XSEC3*L*SF3*BR*fake_scale);
  h4->Scale(1/N4_a*XSEC4*L*SF4*BR*fake_scale);
  h5->Scale(1/N5_a*XSEC5*L*SF5*BR*fake_scale);
  h6->Scale(1/N6_a*XSEC6*L*SF6*BR*fake_scale);
  h7->Scale(1/N7_a*XSEC7*L*SF7*BR*fake_scale);
  hch->Scale(1/N_ch*XSECCH*L*SFCH*BR*fake_scale);

  l1->Scale(1/N1_a*XSEC1*L*SF1*BR*fake_scale);
  l2->Scale(1/N2_a*XSEC2*L*SF2*BR*fake_scale);
  l3->Scale(1/N3_a*XSEC3*L*SF3*BR*fake_scale);
  l4->Scale(1/N4_a*XSEC4*L*SF4*BR*fake_scale);
  l5->Scale(1/N5_a*XSEC5*L*SF5*BR*fake_scale);
  l6->Scale(1/N6_a*XSEC6*L*SF6*BR*fake_scale);
  l7->Scale(1/N7_a*XSEC7*L*SF7*BR*fake_scale);

  h_total->Add(h1);
  h_total->Add(h2);
  h_total->Add(h3);
  h_total->Add(h4);
  h_total->Add(h5);
  h_total->Add(h6);
  h_total->Add(h7);
  h_ttotal->Add(h_total);
  h_ttotal->Add(hch);
  h_acc->Add(hch);
  h_acc->Divide(h_ttotal);

  l_total->Add(l1);
  l_total->Add(l2);
  l_total->Add(l3);
  l_total->Add(l4);
  l_total->Add(l5);
  l_total->Add(l6);
  l_total->Add(l7);

  double h_area = h_total->Integral();
  double hh_area = h_ttotal->Integral();
  double hh_area_acc = h_acc->Integral();
  double l_area = l_total->Integral();

  cout << "HT integral (area) = " << h_area << endl;
  cout << "HT integral w/ chargino (area) = " << hh_area << endl;
  cout << "HT integral w/ chargino acceptance (area) = " << hh_area_acc << endl;
  cout << "LHE HT integral (area) = " << l_area << endl;

  TCanvas* c = new TCanvas("canv", "The Canvas (post-analysis)", 1200, 800);
  gStyle->SetOptStat(1110);
  gStyle->SetStatColor(18);
  h_total->SetLineColor(38);
  h_total->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  h_total->GetXaxis()->CenterTitle(true);
  h_total->GetYaxis()->SetTitle("Counts");
  h_total->GetYaxis()->CenterTitle(true);
  h_ttotal->SetLineColor(38);
  h_ttotal->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  h_ttotal->GetXaxis()->CenterTitle(true);
  h_ttotal->GetYaxis()->SetTitle("Counts");
  h_ttotal->GetYaxis()->CenterTitle(true);
  h_acc->SetLineColor(38);
  h_acc->GetXaxis()->SetTitle("\\mbox{ch HT (GeV)}");
  h_acc->GetXaxis()->CenterTitle(true);
  h_acc->GetYaxis()->SetTitle("Ratio");
  h_acc->GetYaxis()->CenterTitle(true);
  l_total->SetLineColor(38);
  l_total->GetXaxis()->SetTitle("\\mbox{LHE HT (GeV)}");
  l_total->GetXaxis()->CenterTitle(true);
  l_total->GetYaxis()->SetTitle("Counts");
  l_total->GetYaxis()->CenterTitle(true);
  l_total->Draw("HIST");
  c->SaveAs("attach_x27_lheht.png");
  h_total->Draw("HIST");
  c->SaveAs("attach_x27_jetht.png");
  h_ttotal->Draw("HIST");
  c->SaveAs("attach_x27_jetht_sig.png");
  h_acc->Draw("HIST");
  c->SaveAs("attach_x27_jetht_acc.png");
}
