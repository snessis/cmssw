#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"

void attach_x26() {
TFile *f1 = new TFile("x26_1.root");
TFile *f2 = new TFile("x26_2.root");
TFile *f3 = new TFile("x26_2.root");
TFile *f4 = new TFile("x26_2.root");
TFile *f5 = new TFile("x26_2.root");
TFile *f6 = new TFile("x26_2.root");
TFile *f7 = new TFile("x26_2.root");

TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
TH1F *h3 = (TH1F*)f2->Get("plots/jetht");
TH1F *h4 = (TH1F*)f2->Get("plots/jetht");
TH1F *h5 = (TH1F*)f2->Get("plots/jetht");
TH1F *h6 = (TH1F*)f2->Get("plots/jetht");
TH1F *h7 = (TH1F*)f2->Get("plots/jetht");
TH1F *h_total = new TH1F("total_jetht", "\\mbox{Jet } HT", 100, 0, 3500);

h_total->Add(h1);
h_total->Add(h2);
h_total->Add(h3);
h_total->Add(h4);
h_total->Add(h5);
h_total->Add(h6);
h_total->Add(h7);

TCanvas* c = new TCanvas("canv", "The Canvas (post-analysis)", 1200, 800);
gStyle->SetOptStat(1110);
gStyle->SetStatColor(18);
h_total->SetLineColor(38);
h_total->GetXaxis()->SetTitle("E_t \\mbox{ (GeV)}");
h_total->GetXaxis()->CenterTitle(true);
h_total->GetYaxis()->SetTitle("Counts");
h_total->GetYaxis()->CenterTitle(true);
h_total->Draw();
c->SaveAs("attach_x26_output.png");
}
