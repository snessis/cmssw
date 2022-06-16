#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TLatex.h"
void ssattach() {
  double N1 = 748300; //HT 100 to 200
  double N2 = 1248911; //HT 200 to 400
  double N3 = 411531; //HT 400 to 600
  double N4 = 1560343; //HT 600 to 800
  double N5 = 737750; //HT 800 to 1200
  double N6 = 775061; //HT 1200 to 2500
  double N7 = 429253; //HT 2500 to Inf
  double N8 = 4500552; //Dilepton
  double N9 = 3977039; //tt
  double N10 = 4164133; //ttbar
  double N = 528605; // 200_185_10
  double XSEC1 = 1395*1.17*1000;
  double XSEC2 = 408.7*1.17*1000;
  double XSEC3 = 57.52*1.17*1000;
  double XSEC4 = 12.78*1.17*1000;
  double XSEC5 = 5.246*1.17*1000;
  double XSEC6 = 1.071*1.17*1000;
  double XSEC7 = 0.00819*1.17*1000;
  double XSEC8 = 831.76*((3*0.108)*(3*0.108))*1000;
  double XSEC9 = 831.76*(3*0.108)*(1-3*0.108)*1000;
  double XSEC10 = 831.76*(3*0.108)*(1-3*0.108)*1000;
  double XSECCH = 0.902569*1000;
  double L = 60;
  double SF1 = N1 / 29521158;
  double SF2 = N2 / 25468933;
  double SF3 = N3 / 5932701;
  double SF4 = N4 / 19771294;
  double SF5 = N5 / 8402687;
  double SF6 = N6 / 7633949;
  double SF7 = N7 / 3273980;
  double SF8 = N8 / 28701360;
  double SF9 = N9 / 57259880;
  double SF10 = N10 / 59929205;
  double SFCH = 1;
  double BR = 0.1063; //W -> muonic

  TFile *f1 = new TFile("y04_1.root");
  TFile *f2 = new TFile("y04_2.root");
  TFile *f3 = new TFile("y04_3.root");
  TFile *f4 = new TFile("y04_4.root");
  TFile *f5 = new TFile("y04_5.root");
  TFile *f6 = new TFile("y04_6.root");
  TFile *f7 = new TFile("y04_7.root");
  TFile *f8 = new TFile("y04_8.root");
  TFile *f9 = new TFile("y04_9.root");
  TFile *f10 = new TFile("y04_10.root");
  TFile *fch = new TFile("y04.root");

  TFile *g1 = new TFile("y05_1.root");
  TFile *g2 = new TFile("y05_2.root");
  TFile *g3 = new TFile("y05_3.root");
  TFile *g4 = new TFile("y05_4.root");
  TFile *g5 = new TFile("y05_5.root");
  TFile *g6 = new TFile("y05_6.root");
  TFile *g7 = new TFile("y05_7.root");
  TFile *g8 = new TFile("y05_8.root");
  TFile *g9 = new TFile("y05_9.root");
  TFile *g10 = new TFile("y05_10.root");
  TFile *gch = new TFile("y05.root");

  TH1F *fn1 = (TH1F*)f1->Get("plots/N");
  TH1F *fn2 = (TH1F*)f2->Get("plots/N");
  TH1F *fn3 = (TH1F*)f3->Get("plots/N");
  TH1F *fn4 = (TH1F*)f4->Get("plots/N");
  TH1F *fn5 = (TH1F*)f5->Get("plots/N");
  TH1F *fn6 = (TH1F*)f6->Get("plots/N");
  TH1F *fn7 = (TH1F*)f7->Get("plots/N");
  TH1F *fn8 = (TH1F*)f8->Get("plots/N");
  TH1F *fn9 = (TH1F*)f9->Get("plots/N");
  TH1F *fn10 = (TH1F*)f10->Get("plots/N");
  TH1F *fnch = (TH1F*)fch->Get("plots/N");

  double fn1_entries = fn1->GetEntries()*1/N1*XSEC1*L*SF1*BR;
  double fn2_entries = fn2->GetEntries()*1/N2*XSEC2*L*SF2*BR;
  double fn3_entries = fn3->GetEntries()*1/N3*XSEC3*L*SF3*BR;
  double fn4_entries = fn4->GetEntries()*1/N4*XSEC4*L*SF4*BR;
  double fn5_entries = fn5->GetEntries()*1/N5*XSEC5*L*SF5*BR;
  double fn6_entries = fn6->GetEntries()*1/N6*XSEC6*L*SF6*BR;
  double fn7_entries = fn7->GetEntries()*1/N7*XSEC7*L*SF7*BR;
  double fn8_entries = fn8->GetEntries()*1/N8*XSEC8*L*SF8*BR;
  double fn9_entries = fn9->GetEntries()*1/N9*XSEC9*L*SF9*BR;
  double fn10_entries = fn10->GetEntries()*1/N10*XSEC10*L*SF10*BR;
  double fnch_entries = fnch->GetEntries()*1/N*XSECCH*L*SFCH*BR;
  double fnbg_entries = 0;
  double fnbg_w_entries = 0;
  double fnbg_tt_entries = 0;

  TH1F *gn1 = (TH1F*)g1->Get("plots/N");
  TH1F *gn2 = (TH1F*)g2->Get("plots/N");
  TH1F *gn3 = (TH1F*)g3->Get("plots/N");
  TH1F *gn4 = (TH1F*)g4->Get("plots/N");
  TH1F *gn5 = (TH1F*)g5->Get("plots/N");
  TH1F *gn6 = (TH1F*)g6->Get("plots/N");
  TH1F *gn7 = (TH1F*)g7->Get("plots/N");
  TH1F *gn8 = (TH1F*)g8->Get("plots/N");
  TH1F *gn9 = (TH1F*)g9->Get("plots/N");
  TH1F *gn10 = (TH1F*)g10->Get("plots/N");
  TH1F *gnch = (TH1F*)gch->Get("plots/N");

  double gn1_entries = gn1->GetEntries()*1/N1*XSEC1*L*SF1*BR;
  double gn2_entries = gn2->GetEntries()*1/N2*XSEC2*L*SF2*BR;
  double gn3_entries = gn3->GetEntries()*1/N3*XSEC3*L*SF3*BR;
  double gn4_entries = gn4->GetEntries()*1/N4*XSEC4*L*SF4*BR;
  double gn5_entries = gn5->GetEntries()*1/N5*XSEC5*L*SF5*BR;
  double gn6_entries = gn6->GetEntries()*1/N6*XSEC6*L*SF6*BR;
  double gn7_entries = gn7->GetEntries()*1/N7*XSEC7*L*SF7*BR;
  double gn8_entries = gn8->GetEntries()*1/N8*XSEC8*L*SF8*BR;
  double gn9_entries = gn9->GetEntries()*1/N9*XSEC9*L*SF9*BR;
  double gn10_entries = gn10->GetEntries()*1/N10*XSEC10*L*SF10*BR;
  double gnch_entries = gnch->GetEntries()*1/N*XSECCH*L*SFCH*BR;
  double gnbg_entries = 0;
  double gnbg_w_entries = 0;
  double gnbg_tt_entries = 0;

  fnbg_entries += fn1_entries;
  fnbg_entries += fn2_entries;
  fnbg_entries += fn3_entries;
  fnbg_entries += fn4_entries;
  fnbg_entries += fn5_entries;
  fnbg_entries += fn6_entries;
  fnbg_entries += fn7_entries;
  fnbg_entries += fn8_entries;
  fnbg_entries += fn9_entries;
  fnbg_entries += fn10_entries;
  fnbg_w_entries += fn1_entries;
  fnbg_w_entries += fn2_entries;
  fnbg_w_entries += fn3_entries;
  fnbg_w_entries += fn4_entries;
  fnbg_w_entries += fn5_entries;
  fnbg_w_entries += fn6_entries;
  fnbg_w_entries += fn7_entries;
  fnbg_tt_entries += fn8_entries;
  fnbg_tt_entries += fn9_entries;
  fnbg_tt_entries += fn10_entries;

  gnbg_entries += gn1_entries;
  gnbg_entries += gn2_entries;
  gnbg_entries += gn3_entries;
  gnbg_entries += gn4_entries;
  gnbg_entries += gn5_entries;
  gnbg_entries += gn6_entries;
  gnbg_entries += gn7_entries;
  gnbg_entries += gn8_entries;
  gnbg_entries += gn9_entries;
  gnbg_entries += gn10_entries;
  gnbg_w_entries += gn1_entries;
  gnbg_w_entries += gn2_entries;
  gnbg_w_entries += gn3_entries;
  gnbg_w_entries += gn4_entries;
  gnbg_w_entries += gn5_entries;
  gnbg_w_entries += gn6_entries;
  gnbg_w_entries += gn7_entries;
  gnbg_tt_entries += gn8_entries;
  gnbg_tt_entries += gn9_entries;
  gnbg_tt_entries += gn10_entries;

  cout << "-----" << endl;
  cout << "y04: Chargino Physical Events (best accuracy) = " << fnch_entries << endl;
  cout << "y04: Background Total Physical Events (best accuracy) = " << fnbg_entries<< endl;
  cout << "y04: Background WJets Physical Events (best accuracy) = " << fnbg_w_entries << endl;
  cout << "y04: Background TTJets Physical Events (best accuracy) = " << fnbg_tt_entries << endl;
  cout << "y05: Chargino Physical Events (best accuracy) = " << gnch_entries << endl;
  cout << "y05: Background Total Physical Events (best accuracy) = " << gnbg_entries<< endl;
  cout << "y05: Background WJets Physical Events (best accuracy) = " << gnbg_w_entries << endl;
  cout << "y05: Background TTJets Physical Events (best accuracy) = " << gnbg_tt_entries << endl;
  cout << "-----" << endl;
  cout << "y05-y04: Chargino Physical Events Difference (best accuracy) = " << gnch_entries - fnch_entries << endl;
  cout << "y05-y04: Background Total Physical Events Difference (best accuracy) = " <<  gnbg_entries - fnbg_entries<< endl;
  cout << "y05-y04: Background WJets Physical Events Difference (best accuracy) = " << gnbg_w_entries - fnbg_w_entries << endl;
  cout << "y05-y04: Background TTJets Physical Events Difference (best accuracy) = " << gnbg_tt_entries - fnbg_tt_entries<< endl;
  cout << "-----" << endl;
  cout << "y05-y04: Chargino Cut Efficiency % (best accuracy) = " << (gnch_entries - fnch_entries) / gnch_entries * 100 << endl;
  cout << "y05-y04: Background Total Cut Efficiency % (best accuracy) = " << (gnbg_entries - fnbg_entries) / gnbg_entries * 100 << endl;
  cout << "y05-y04: Background WJets Cut Efficiency % (best accuracy) = " << (gnbg_w_entries - fnbg_w_entries) / gnbg_w_entries * 100 << endl;
  cout << "y05-y04: Background TTJets Cut Efficiency % (best accuracy) = " << (gnbg_tt_entries - fnbg_tt_entries) / gnbg_tt_entries * 100 << endl;

}
