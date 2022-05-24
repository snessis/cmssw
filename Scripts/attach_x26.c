#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TArrow.h"
#include "TLatex.h"

void attach_x26() {
//    gROOT->SetStyle("Plain");   // set plain TStyle
  //  gStyle->SetOptStat(111111); // draw statistics on plots,
                            // (0) for no output
//    gStyle->SetOptFit(1111);    // draw fit results on plot,
                            // (0) for no ouput
    //gStyle->SetPalette(57);     // set color map
  //  gStyle->SetOptTitle(0);     // suppress title box


TFile *f1 = new TFile("x26_1.root");
TFile *f2 = new TFile("x26_2.root");
//TFile *f1 = new TFile("../x26_1/x26_1_h_jetht.root");
//TFile *f2 = new TFile("../x26_2/x26_2_h_jetht.root");
f1->ls();
f2->ls();

TH1F *h1 = (TH1F*)f1->Get("plots/jetht");
TH1F *h2 = (TH1F*)f2->Get("plots/jetht");
TH1F *h3 = new TH1F("total_jetht", "Total Jet HT", 100, 0, 1500);
h3->Add(h1);
h3->Add(h2);

TCanvas c("canv", "The Canvas (post-analysis)", 700, 1000); // create a canvas, specify position and size in pixels
h3->Draw();
}
