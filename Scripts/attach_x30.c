#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void attach_x30() {
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
  double N = 539666;
  double N_ch = 711;
  double XSEC1 = 1395*1.17*1000;
  double XSEC2 = 408.7*1.17*1000;
  double XSEC3 = 57.52*1.17*1000;
  double XSEC4 = 12.78*1.17*1000;
  double XSEC5 = 5.246*1.17*1000;
  double XSEC6 = 1.071*1.17*1000;
  double XSEC7 = 0.00819*1.17*1000;
  double XSECCH = 0.902569*1000;
  double L = 60;
  double SF1 = N1 / 29521158;
  double SF2 = N2 / 25468933;
  double SF3 = N3 / 5932701;
  double SF4 = N4 / 19771294;
  double SF5 = N5 / 8402687;
  double SF6 = N6 / 7633949;
  double SF7 = N7 / 3273980;
  double SFCH = N / 539666;
  double BR = 0.1063; //W -> muonic
  double fake_scale = 1;

  TFile *f1 = new TFile("x27_1.root");
  TFile *f2 = new TFile("x27_2.root");
  TFile *f3 = new TFile("x27_3.root");
  TFile *f4 = new TFile("x27_4.root");
  TFile *f5 = new TFile("x27_5.root");
  TFile *f6 = new TFile("x27_6.root");
  TFile *f7 = new TFile("x27_7.root");
  TFile *fch = new TFile("x30.root");

  TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
  TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
  TH1F *h3 = (TH1F*)f3->Get("plots/jetht");
  TH1F *h4 = (TH1F*)f4->Get("plots/jetht");
  TH1F *h5 = (TH1F*)f5->Get("plots/jetht");
  TH1F *h6 = (TH1F*)f6->Get("plots/jetht");
  TH1F *h7 = (TH1F*)f7->Get("plots/jetht");
  TH1F *hch = (TH1F*)fch->Get("plots/jetht");
  TH1F *hmetch = (TH1F*)fch->Get("plots/metpt");
  TH1F *h_total = new TH1F("total_jetht", "\\mbox{Total Jet HT}", 100, 0, 3500);
  TH1F *h_ttotal = new TH1F("ttotal_jetht", "\\mbox{Total Jet HT (plus chargino)}", 100, 0, 3500);
  //TH1F *h_met_sig = new TH1F("total_met_sig", "\\mbox{MET chargino}", 100, 0, 3500);

  h1->Scale(1/N1*XSEC1*L*SF1*BR*fake_scale);
  h2->Scale(1/N2*XSEC2*L*SF2*BR*fake_scale);
  h3->Scale(1/N3*XSEC3*L*SF3*BR*fake_scale);
  h4->Scale(1/N4*XSEC4*L*SF4*BR*fake_scale);
  h5->Scale(1/N5*XSEC5*L*SF5*BR*fake_scale);
  h6->Scale(1/N6*XSEC6*L*SF6*BR*fake_scale);
  h7->Scale(1/N7*XSEC7*L*SF7*BR*fake_scale);
  hch->Scale(1/N*XSECCH*L*BR*fake_scale);
  metch->Scale(1/N*XSECCH*L*BR*fake_scale);

  h_total->Add(h1);
  h_total->Add(h2);
  h_total->Add(h3);
  h_total->Add(h4);
  h_total->Add(h5);
  h_total->Add(h6);
  h_total->Add(h7);
  h_ttotal->Add(h_total);
  h_ttotal->Add(hch);

  double h_area = h_total->Integral();
  double h_charea = hch->Integral();
  double hh_area = h_ttotal->Integral();
  double met_area = metch->Integral();
  cout << "HT integral (area) = " << h_area << endl;
  cout << "HT integral chargino only (area) = " << h_charea << endl;
  cout << "HT integral w/ chargino (area) = " << hh_area << endl;
  cout << "MET chargino only (area) = " << met_area << endl;

  TCanvas* c = new TCanvas("canv", "The Canvas (post-analysis)", 1200, 800);
  gStyle->SetOptStat(1110);
  gStyle->SetStatColor(18);
  h_total->SetLineColor(38);
  h_total->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  h_total->GetXaxis()->CenterTitle(true);
  h_total->GetYaxis()->SetTitle("Counts");
  h_total->GetYaxis()->CenterTitle(true);
  metch->SetLineColor(38);
  metch->GetXaxis()->SetTitle("\\mbox{MET (GeV)}");
  metch->GetXaxis()->CenterTitle(true);
  metch->GetYaxis()->SetTitle("Counts");
  metch->GetYaxis()->CenterTitle(true);
  hch->SetLineColor(38);
  hch->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch->GetXaxis()->CenterTitle(true);
  hch->GetYaxis()->SetTitle("Counts");
  hch->GetYaxis()->CenterTitle(true);
  h_ttotal->SetLineColor(38);
  h_ttotal->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  h_ttotal->GetXaxis()->CenterTitle(true);
  h_ttotal->GetYaxis()->SetTitle("Counts");
  h_ttotal->GetYaxis()->CenterTitle(true);
  h_total->Draw("HIST");
  c->SaveAs("attach_x30_jetht.png");
  metch->Draw("HIST");
  c->SaveAs("attach_x30_metch.png");
  hch->Draw("HIST");
  c->SaveAs("attach_x30_jetht_ch.png");
  h_ttotal->Draw("HIST");
  c->SaveAs("attach_x30_jetht_sig.png");
}
