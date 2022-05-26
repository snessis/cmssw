#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void attach_x27() {
double N1 = 748300; //HT 100 to 200
double N1_a = 70267;
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
double XSEC1 = 1395;
double XSEC2 = 408.7;
double XSEC3 = 57.52;
double XSEC4 = 12.78;
double XSEC5 = 5.246;
double XSEC6 = 1.071;
double XSEC7 = 0.00819;
double L = 1.17;
double SF1 = N1 / 29521158;
double SF2 = N2 / 25468933;
double SF3 = N3 / 5932701;
double SF4 = N4 / 19771294;
double SF5 = N5 / 8402687;
double SF6 = N6 / 7633949;
double SF7 = N7 / 3273980;
double BR = 0.11;
double fake_scale = 1;

TFile *f1 = new TFile("x27_1.root");
TFile *f2 = new TFile("x27_2.root");
TFile *f3 = new TFile("x27_3.root");
TFile *f4 = new TFile("x27_4.root");
TFile *f5 = new TFile("x27_5.root");
TFile *f6 = new TFile("x27_6.root");
TFile *f7 = new TFile("x27_7.root");

TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
TH1F *h3 = (TH1F*)f3->Get("plots/jetht");
TH1F *h4 = (TH1F*)f4->Get("plots/jetht");
TH1F *h5 = (TH1F*)f5->Get("plots/jetht");
TH1F *h6 = (TH1F*)f6->Get("plots/jetht");
TH1F *h7 = (TH1F*)f7->Get("plots/jetht");
TH1F *h_total = new TH1F("total_jetht", "\\mbox{Total Jet } HT", 150, 0, 2000);

TH1F *l1 = (TH1F*)f1->Get("plots/lheht");
TH1F *l2 = (TH1F*)f2->Get("plots/lheht");
TH1F *l3 = (TH1F*)f3->Get("plots/lheht");
TH1F *l4 = (TH1F*)f4->Get("plots/lheht");
TH1F *l5 = (TH1F*)f5->Get("plots/lheht");
TH1F *l6 = (TH1F*)f6->Get("plots/lheht");
TH1F *l7 = (TH1F*)f7->Get("plots/lheht");
TH1F *l_total = new TH1F("total_lheht", "\\mbox{Total Jet } LHE", 100, 0, 3500);

h1->Scale(1/N1*XSEC1*L*SF1*BR*fake_scale);
h2->Scale(1/N2*XSEC2*L*SF2*BR*fake_scale);
h3->Scale(1/N3*XSEC3*L*SF3*BR*fake_scale);
h4->Scale(1/N4*XSEC4*L*SF4*BR*fake_scale);
h5->Scale(1/N5*XSEC5*L*SF5*BR*fake_scale);
h6->Scale(1/N6*XSEC6*L*SF6*BR*fake_scale);
h7->Scale(1/N7*XSEC7*L*SF7*BR*fake_scale);

l1->Scale(1/N1*XSEC1*L*SF1*BR*fake_scale);
l2->Scale(1/N2*XSEC2*L*SF2*BR*fake_scale);
l3->Scale(1/N3*XSEC3*L*SF3*BR*fake_scale);
l4->Scale(1/N4*XSEC4*L*SF4*BR*fake_scale);
l5->Scale(1/N5*XSEC5*L*SF5*BR*fake_scale);
l6->Scale(1/N6*XSEC6*L*SF6*BR*fake_scale*1000000);
l7->Scale(1/N7*XSEC7*L*SF7*BR*fake_scale);

h_total->Add(h1);
h_total->Add(h2);
h_total->Add(h3);
h_total->Add(h4);
h_total->Add(h5);
h_total->Add(h6);
h_total->Add(h7);

l_total->Add(l1);
l_total->Add(l2);
l_total->Add(l3);
l_total->Add(l4);
l_total->Add(l5);
l_total->Add(l6);
l_total->Add(l7);

TCanvas* c = new TCanvas("canv", "The Canvas (post-analysis)", 1200, 800);
gStyle->SetOptStat(1110);
gStyle->SetStatColor(18);
h_total->SetLineColor(38);
h_total->GetXaxis()->SetTitle("p_t \\mbox{ (GeV)}");
h_total->GetXaxis()->CenterTitle(true);
h_total->GetYaxis()->SetTitle("Counts");
h_total->GetYaxis()->CenterTitle(true);
l_total->SetLineColor(38);
l_total->GetXaxis()->SetTitle("\\mbox{LHE (GeV)}");
l_total->GetXaxis()->CenterTitle(true);
l_total->GetYaxis()->SetTitle("Counts");
l_total->GetYaxis()->CenterTitle(true);
h_total->Draw("HIST");
c->SaveAs("attach_x27_jetht.png");
l_total->Draw("HIST");
c->SaveAs("attach_x27_lheht.png");
}
