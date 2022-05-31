#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
//NO CUTS:

void attach_x33() {
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

  TFile *f1 = new TFile("x32_1.root");
  TFile *f2 = new TFile("x32_2.root");
  TFile *f3 = new TFile("x32_3.root");
  TFile *f4 = new TFile("x32_4.root");
  TFile *f5 = new TFile("x32_5.root");
  TFile *f6 = new TFile("x32_6.root");
  TFile *f7 = new TFile("x32_7.root");
  TFile *fch = new TFile("x33.root");

  TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
  TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
  TH1F *h3 = (TH1F*)f3->Get("plots/jetht");
  TH1F *h4 = (TH1F*)f4->Get("plots/jetht");
  TH1F *h5 = (TH1F*)f5->Get("plots/jetht");
  TH1F *h6 = (TH1F*)f6->Get("plots/jetht");
  TH1F *h7 = (TH1F*)f7->Get("plots/jetht");
  TH1F *hch = (TH1F*)fch->Get("plots/jetht");
  TH1F *hbg = new TH1F("bg_jetht", "\\mbox{Total Jet HT (background)}", 100, 0, 3500);
  TH1F *h_total = new TH1F("total_jetht", "\\mbox{Total Jet HT (plus chargino)}", 100, 0, 3500);

  TH1F *met1 = (TH1F*)f1->Get("plots/metpt");
  TH1F *met2 = (TH1F*)f2->Get("plots/metpt");
  TH1F *met3 = (TH1F*)f3->Get("plots/metpt");
  TH1F *met4 = (TH1F*)f4->Get("plots/metpt");
  TH1F *met5 = (TH1F*)f5->Get("plots/metpt");
  TH1F *met6 = (TH1F*)f6->Get("plots/metpt");
  TH1F *met7 = (TH1F*)f7->Get("plots/metpt");
  TH1F *metch = (TH1F*)fch->Get("plots/metpt");
  TH1F *metbg= new TH1F("bg_met", "\\mbox{MET (background)}", 100, 0, 400);

  h1->Scale(1/N1*XSEC1*L*SF1*BR*fake_scale);
  h2->Scale(1/N2*XSEC2*L*SF2*BR*fake_scale);
  h3->Scale(1/N3*XSEC3*L*SF3*BR*fake_scale);
  h4->Scale(1/N4*XSEC4*L*SF4*BR*fake_scale);
  h5->Scale(1/N5*XSEC5*L*SF5*BR*fake_scale);
  h6->Scale(1/N6*XSEC6*L*SF6*BR*fake_scale);
  h7->Scale(1/N7*XSEC7*L*SF7*BR*fake_scale);
  hch->Scale(1/N*XSECCH*L*BR*fake_scale);

  met1->Scale(1/N1*XSEC1*L*SF1*BR*fake_scale);
  met2->Scale(1/N2*XSEC2*L*SF2*BR*fake_scale);
  met3->Scale(1/N3*XSEC3*L*SF3*BR*fake_scale);
  met4->Scale(1/N4*XSEC4*L*SF4*BR*fake_scale);
  met5->Scale(1/N5*XSEC5*L*SF5*BR*fake_scale);
  met6->Scale(1/N6*XSEC6*L*SF6*BR*fake_scale);
  met7->Scale(1/N7*XSEC7*L*SF7*BR*fake_scale);
  metch->Scale(1/N*XSECCH*L*BR*fake_scale);

  hbg->Add(h1);
  hbg->Add(h2);
  hbg->Add(h3);
  hbg->Add(h4);
  hbg->Add(h5);
  hbg->Add(h6);
  hbg->Add(h7);
  h_total->Add(h_total);
  h_total->Add(hch);

  metbg->Add(met1);
  metbg->Add(met2);
  metbg->Add(met3);
  metbg->Add(met4);
  metbg->Add(met5);
  metbg->Add(met6);
  metbg->Add(met7);

  double hbg_area = hbg->Integral();
  double hch_area = hch->Integral();
  double hg_area = h_total->Integral();
  double metbg_area = metbg->Integral();
  double metch_area = metch->Integral();
  cout << "HT integral (area) = " << hbg_area << endl;
  cout << "HT integral chargino only (area) = " << hch_area << endl;
  cout << "HT integral w/ chargino (area) = " << hg_area << endl;
  cout << "MET integral background (area) = " << metbg_area << endl;
  cout << "MET integral chargino only (area) = " << metch_area << endl;

  TCanvas* c = new TCanvas("canv", "The Canvas (post-analysis)", 1200, 800);
  gStyle->SetOptStat(1110);
  gStyle->SetStatColor(18);
  hbg->SetLineColor(38);
  hbg->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hbg->GetXaxis()->CenterTitle(true);
  hbg->GetYaxis()->SetTitle("Counts");
  hbg->GetYaxis()->CenterTitle(true);
  metch->SetLineColor(38);
  metch->GetXaxis()->SetTitle("\\mbox{MET (GeV)}");
  metch->GetXaxis()->CenterTitle(true);
  metch->GetYaxis()->SetTitle("Counts");
  metch->GetYaxis()->CenterTitle(true);
  metbg->SetLineColor(38);
  metbg->GetXaxis()->SetTitle("\\mbox{MET (GeV)}");
  metbg->GetXaxis()->CenterTitle(true);
  metbg->GetYaxis()->SetTitle("Counts");
  metbg->GetYaxis()->CenterTitle(true);
  hch->SetLineColor(38);
  hch->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch->GetXaxis()->CenterTitle(true);
  hch->GetYaxis()->SetTitle("Counts");
  hch->GetYaxis()->CenterTitle(true);
  h_total->SetLineColor(38);
  h_total->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  h_total->GetXaxis()->CenterTitle(true);
  h_total->GetYaxis()->SetTitle("Counts");
  h_total->GetYaxis()->CenterTitle(true);
  hbg->Draw("HIST");
  c->SaveAs("attach_x32_bg_jetht.png");
  metbg->Draw("HIST");
  c->SaveAs("attach_x32_bg_met.png");
  metch->Draw("HIST");
  c->SaveAs("attach_x32_ch_met.png");
  hch->Draw("HIST");
  c->SaveAs("attach_x32_ch_jetht.png");
  h_total->Draw("HIST");
  c->SaveAs("attach_x32_total_jetht.png");
}
