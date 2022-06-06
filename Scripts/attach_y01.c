#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
//NO CUTS:

void attach_y01() {
  double N1 = 748300; //HT 100 to 200
  double N2 = 1248911; //HT 200 to 400
  double N3 = 411531; //HT 400 to 600
  double N4 = 1560343; //HT 600 to 800
  double N5 = 737750; //HT 800 to 1200
  double N6 = 775061; //HT 1200 to 2500
  double N7 = 429253; //HT 2500 to Inf
  double N = 556249; // 200_195_10
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
  double SFCH = 1;
  double BR = 0.1063; //W -> muonic

  TFile *f1 = new TFile("y01_1.root");
  TFile *f2 = new TFile("x01_2.root");
  TFile *f3 = new TFile("x01_3.root");
  TFile *f4 = new TFile("x01_4.root");
  TFile *f5 = new TFile("x05_5.root");
  TFile *f6 = new TFile("x01_6.root");
  TFile *f7 = new TFile("x01_7.root");
  TFile *fch = new TFile("y01.root");

  TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
  TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
  TH1F *h3 = (TH1F*)f3->Get("plots/jetht");
  TH1F *h4 = (TH1F*)f4->Get("plots/jetht");
  TH1F *h5 = (TH1F*)f5->Get("plots/jetht");
  TH1F *h6 = (TH1F*)f6->Get("plots/jetht");
  TH1F *h7 = (TH1F*)f7->Get("plots/jetht");
  TH1F *hch = (TH1F*)fch->Get("plots/jetht");
  TH1F *hbg = new TH1F("bg_jetht", "\\mbox{Total Jet HT (background)}", 100, 0, 3500);
  TH1F *htotal = new TH1F("total_jetht", "\\mbox{Total Jet HT (plus chargino)}", 100, 0, 3500);

  TH1F *met1 = (TH1F*)f1->Get("plots/metpt");
  TH1F *met2 = (TH1F*)f2->Get("plots/metpt");
  TH1F *met3 = (TH1F*)f3->Get("plots/metpt");
  TH1F *met4 = (TH1F*)f4->Get("plots/metpt");
  TH1F *met5 = (TH1F*)f5->Get("plots/metpt");
  TH1F *met6 = (TH1F*)f6->Get("plots/metpt");
  TH1F *met7 = (TH1F*)f7->Get("plots/metpt");
  TH1F *metch = (TH1F*)fch->Get("plots/metpt");
  TH1F *metbg= new TH1F("bg_met", "\\mbox{MET (background)}", 100, 0, 400);

  h1->Scale(1/N1*XSEC1*L*SF1*BR);
  h2->Scale(1/N2*XSEC2*L*SF2*BR);
  h3->Scale(1/N3*XSEC3*L*SF3*BR);
  h4->Scale(1/N4*XSEC4*L*SF4*BR);
  h5->Scale(1/N5*XSEC5*L*SF5*BR);
  h6->Scale(1/N6*XSEC6*L*SF6*BR);
  h7->Scale(1/N7*XSEC7*L*SF7*BR);
  hch->Scale(1/N*XSECCH*L*BR);

  met1->Scale(1/N1*XSEC1*L*SF1*BR);
  met2->Scale(1/N2*XSEC2*L*SF2*BR);
  met3->Scale(1/N3*XSEC3*L*SF3*BR);
  met4->Scale(1/N4*XSEC4*L*SF4*BR);
  met5->Scale(1/N5*XSEC5*L*SF5*BR);
  met6->Scale(1/N6*XSEC6*L*SF6*BR);
  met7->Scale(1/N7*XSEC7*L*SF7*BR);
  metch->Scale(1/N*XSECCH*L*SFCH*BR);

  hbg->Add(h1);
  hbg->Add(h2);
  hbg->Add(h3);
  hbg->Add(h4);
  hbg->Add(h5);
  hbg->Add(h6);
  hbg->Add(h7);
  htotal->Add(hbg);
  htotal->Add(hch);

  metbg->Add(met1);
  metbg->Add(met2);
  metbg->Add(met3);
  metbg->Add(met4);
  metbg->Add(met5);
  metbg->Add(met6);
  metbg->Add(met7);

  double hbg_area = hbg->Integral();
  double hch_area = hch->Integral();
  double htotal_area = htotal->Integral();
  double metbg_area = metbg->Integral();
  double metch_area = metch->Integral();
  cout << "HT integral (area) = " << hbg_area << endl;
  cout << "HT integral chargino only (area) = " << hch_area << endl;
  cout << "HT integral w/ chargino (area) = " << htotal_area << endl;
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
  htotal->SetLineColor(38);
  htotal->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  htotal->GetXaxis()->CenterTitle(true);
  htotal->GetYaxis()->SetTitle("Counts");
  htotal->GetYaxis()->CenterTitle(true);
  hbg->Draw("HIST");
  c->SaveAs("attach_x35_bg_jetht.png");
  metbg->Draw("HIST");
  c->SaveAs("attach_x35_bg_met.png");
  metch->Draw("HIST");
  c->SaveAs("attach_x35_ch_met.png");
  hch->Draw("HIST");
  c->SaveAs("attach_x35_ch_jetht.png");
  htotal->Draw("HIST");
  c->SaveAs("attach_x35_total_jetht.png");
}
