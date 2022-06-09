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
  TFile *f2 = new TFile("y01_2.root");
  TFile *f3 = new TFile("y01_3.root");
  TFile *f4 = new TFile("y01_4.root");
  TFile *f5 = new TFile("y01_5.root");
  TFile *f6 = new TFile("y01_6.root");
  TFile *f7 = new TFile("y01_7.root");
  TFile *fch = new TFile("y01.root");

  TH1F *met1 = (TH1F*)f1->Get("plots/metpt");
  TH1F *met2 = (TH1F*)f2->Get("plots/metpt");
  TH1F *met3 = (TH1F*)f3->Get("plots/metpt");
  TH1F *met4 = (TH1F*)f4->Get("plots/metpt");
  TH1F *met5 = (TH1F*)f5->Get("plots/metpt");
  TH1F *met6 = (TH1F*)f6->Get("plots/metpt");
  TH1F *met7 = (TH1F*)f7->Get("plots/metpt");
  TH1F *metch = (TH1F*)fch->Get("plots/metpt");
  TH1F *metbg = new TH1F("bg_met", "\\mbox{MET (background)}", 100, 0, 400);

  TH1F *h1_1 = (TH1F*)f1->Get("plots/jetht1");
  TH1F *h2_1 = (TH1F*)f2->Get("plots/jetht1");
  TH1F *h3_1 = (TH1F*)f3->Get("plots/jetht1");
  TH1F *h4_1 = (TH1F*)f4->Get("plots/jetht1");
  TH1F *h5_1 = (TH1F*)f5->Get("plots/jetht1");
  TH1F *h6_1 = (TH1F*)f6->Get("plots/jetht1");
  TH1F *h7_1 = (TH1F*)f7->Get("plots/jetht1");
  TH1F *hch_1 = (TH1F*)fch->Get("plots/jetht1");
  TH1F *hbg_1 = new TH1F("bg_jetht1", "\\mbox{Total Jet HT (background) for length cut } d_1", 120, 0, 3500);
  TH1F *htotal_1 = new TH1F("total_jetht1", "\\mbox{Total Jet HT (plus chargino) for length cut } d_1", 120, 0, 3500);

  TH1F *h1_2 = (TH1F*)f1->Get("plots/jetht2");
  TH1F *h2_2 = (TH1F*)f2->Get("plots/jetht2");
  TH1F *h3_2 = (TH1F*)f3->Get("plots/jetht2");
  TH1F *h4_2 = (TH1F*)f4->Get("plots/jetht2");
  TH1F *h5_2 = (TH1F*)f5->Get("plots/jetht2");
  TH1F *h6_2 = (TH1F*)f6->Get("plots/jetht2");
  TH1F *h7_2 = (TH1F*)f7->Get("plots/jetht2");
  TH1F *hch_2 = (TH1F*)fch->Get("plots/jetht2");
  TH1F *hbg_2 = new TH1F("bg_jetht2", "\\mbox{Total Jet HT (background) for length cut } d_2", 120, 0, 3500);
  TH1F *htotal_2 = new TH1F("total_jetht2", "\\mbox{Total Jet HT (plus chargino) for length cut } d_2", 120, 0, 3500);

  TH1F *h1_3 = (TH1F*)f1->Get("plots/jetht3");
  TH1F *h2_3 = (TH1F*)f2->Get("plots/jetht3");
  TH1F *h3_3 = (TH1F*)f3->Get("plots/jetht3");
  TH1F *h4_3 = (TH1F*)f4->Get("plots/jetht3");
  TH1F *h5_3 = (TH1F*)f5->Get("plots/jetht3");
  TH1F *h6_3 = (TH1F*)f6->Get("plots/jetht3");
  TH1F *h7_3 = (TH1F*)f7->Get("plots/jetht3");
  TH1F *hch_3 = (TH1F*)fch->Get("plots/jetht3");
  TH1F *hbg_3 = new TH1F("bg_jetht3", "\\mbox{Total Jet HT (background) for length cut } d_3", 120, 0, 3500);
  TH1F *htotal_3 = new TH1F("total_jetht3", "\\mbox{Total Jet HT (plus chargino) for length cut } d_3", 120, 0, 3500);

  TH1F *h1_4 = (TH1F*)f1->Get("plots/jetht4");
  TH1F *h2_4 = (TH1F*)f2->Get("plots/jetht4");
  TH1F *h3_4 = (TH1F*)f3->Get("plots/jetht4");
  TH1F *h4_4 = (TH1F*)f4->Get("plots/jetht4");
  TH1F *h5_4 = (TH1F*)f5->Get("plots/jetht4");
  TH1F *h6_4 = (TH1F*)f6->Get("plots/jetht4");
  TH1F *h7_4 = (TH1F*)f7->Get("plots/jetht4");
  TH1F *hch_4 = (TH1F*)fch->Get("plots/jetht4");
  TH1F *hbg_4 = new TH1F("bg_jetht4", "\\mbox{Total Jet HT (background) for length cut } d_4", 120, 0, 3500);
  TH1F *htotal_4 = new TH1F("total_jetht4", "\\mbox{Total Jet HT (plus chargino) for length cut } d_4", 120, 0, 3500);

  TH1F *h1_5 = (TH1F*)f1->Get("plots/jetht5");
  TH1F *h2_5 = (TH1F*)f2->Get("plots/jetht5");
  TH1F *h3_5 = (TH1F*)f3->Get("plots/jetht5");
  TH1F *h4_5 = (TH1F*)f4->Get("plots/jetht5");
  TH1F *h5_5 = (TH1F*)f5->Get("plots/jetht5");
  TH1F *h6_5 = (TH1F*)f6->Get("plots/jetht5");
  TH1F *h7_5 = (TH1F*)f7->Get("plots/jetht5");
  TH1F *hch_5 = (TH1F*)fch->Get("plots/jetht5");
  TH1F *hbg_5 = new TH1F("bg_jetht5", "\\mbox{Total Jet HT (background) for length cut } d_5", 120, 0, 3500);
  TH1F *htotal_5 = new TH1F("total_jetht5", "\\mbox{Total Jet HT (plus chargino) for length cut } d_5", 120, 0, 3500);

  met1->Scale(1/N1*XSEC1*L*SF1*BR);
  met2->Scale(1/N2*XSEC2*L*SF2*BR);
  met3->Scale(1/N3*XSEC3*L*SF3*BR);
  met4->Scale(1/N4*XSEC4*L*SF4*BR);
  met5->Scale(1/N5*XSEC5*L*SF5*BR);
  met6->Scale(1/N6*XSEC6*L*SF6*BR);
  met7->Scale(1/N7*XSEC7*L*SF7*BR);
  metch->Scale(1/N*XSECCH*L*SFCH*BR);

  h1_1->Scale(1/N1*XSEC1*L*SF1*BR);
  h2_1->Scale(1/N2*XSEC2*L*SF2*BR);
  h3_1->Scale(1/N3*XSEC3*L*SF3*BR);
  h4_1->Scale(1/N4*XSEC4*L*SF4*BR);
  h5_1->Scale(1/N5*XSEC5*L*SF5*BR);
  h6_1->Scale(1/N6*XSEC6*L*SF6*BR);
  h7_1->Scale(1/N7*XSEC7*L*SF7*BR);
  hch_1->Scale(1/N*XSECCH*L*SFCH*BR);

  h1_2->Scale(1/N1*XSEC1*L*SF1*BR);
  h2_2->Scale(1/N2*XSEC2*L*SF2*BR);
  h3_2->Scale(1/N3*XSEC3*L*SF3*BR);
  h4_2->Scale(1/N4*XSEC4*L*SF4*BR);
  h5_2->Scale(1/N5*XSEC5*L*SF5*BR);
  h6_2->Scale(1/N6*XSEC6*L*SF6*BR);
  h7_2->Scale(1/N7*XSEC7*L*SF7*BR);
  hch_2->Scale(1/N*XSECCH*L*SFCH*BR);

  h1_3->Scale(1/N1*XSEC1*L*SF1*BR);
  h2_3->Scale(1/N2*XSEC2*L*SF2*BR);
  h3_3->Scale(1/N3*XSEC3*L*SF3*BR);
  h4_3->Scale(1/N4*XSEC4*L*SF4*BR);
  h5_3->Scale(1/N5*XSEC5*L*SF5*BR);
  h6_3->Scale(1/N6*XSEC6*L*SF6*BR);
  h7_3->Scale(1/N7*XSEC7*L*SF7*BR);
  hch_3->Scale(1/N*XSECCH*L*SFCH*BR);

  h1_4->Scale(1/N1*XSEC1*L*SF1*BR);
  h2_4->Scale(1/N2*XSEC2*L*SF2*BR);
  h3_4->Scale(1/N3*XSEC3*L*SF3*BR);
  h4_4->Scale(1/N4*XSEC4*L*SF4*BR);
  h5_4->Scale(1/N5*XSEC5*L*SF5*BR);
  h6_4->Scale(1/N6*XSEC6*L*SF6*BR);
  h7_4->Scale(1/N7*XSEC7*L*SF7*BR);
  hch_4->Scale(1/N*XSECCH*L*SFCH*BR);

  h1_5->Scale(1/N1*XSEC1*L*SF1*BR);
  h2_5->Scale(1/N2*XSEC2*L*SF2*BR);
  h3_5->Scale(1/N3*XSEC3*L*SF3*BR);
  h4_5->Scale(1/N4*XSEC4*L*SF4*BR);
  h5_5->Scale(1/N5*XSEC5*L*SF5*BR);
  h6_5->Scale(1/N6*XSEC6*L*SF6*BR);
  h7_5->Scale(1/N7*XSEC7*L*SF7*BR);
  hch_5->Scale(1/N*XSECCH*L*SFCH*BR);

  metbg->Add(met1);
  metbg->Add(met2);
  metbg->Add(met3);
  metbg->Add(met4);
  metbg->Add(met5);
  metbg->Add(met6);
  metbg->Add(met7);

  hbg_1->Add(h1_1);
  hbg_1->Add(h2_1);
  hbg_1->Add(h3_1);
  hbg_1->Add(h4_1);
  hbg_1->Add(h5_1);
  hbg_1->Add(h6_1);
  hbg_1->Add(h7_1);
  htotal_1->Add(hbg_1);
  htotal_1->Add(hch_1);

  hbg_2->Add(h1_2);
  hbg_2->Add(h2_2);
  hbg_2->Add(h3_2);
  hbg_2->Add(h4_2);
  hbg_2->Add(h5_2);
  hbg_2->Add(h6_2);
  hbg_2->Add(h7_2);
  htotal_2->Add(hbg_2);
  htotal_2->Add(hch_2);

  hbg_3->Add(h1_3);
  hbg_3->Add(h2_3);
  hbg_3->Add(h3_3);
  hbg_3->Add(h4_3);
  hbg_3->Add(h5_3);
  hbg_3->Add(h6_3);
  hbg_3->Add(h7_3);
  htotal_3->Add(hbg_3);
  htotal_3->Add(hch_3);

  hbg_4->Add(h1_4);
  hbg_4->Add(h2_4);
  hbg_4->Add(h3_4);
  hbg_4->Add(h4_4);
  hbg_4->Add(h5_4);
  hbg_4->Add(h6_4);
  hbg_4->Add(h7_4);
  htotal_4->Add(hbg_4);
  htotal_4->Add(hch_4);

  hbg_5->Add(h1_5);
  hbg_5->Add(h2_5);
  hbg_5->Add(h3_5);
  hbg_5->Add(h4_5);
  hbg_5->Add(h5_5);
  hbg_5->Add(h6_5);
  hbg_5->Add(h7_5);
  htotal_5->Add(hbg_5);
  htotal_5->Add(hch_5);

  double hbg_1_area = hbg_1->Integral();
  double hbg_2_area = hbg_2->Integral();
  double hbg_3_area = hbg_3->Integral();
  double hbg_4_area = hbg_4->Integral();
  double hbg_5_area = hbg_5->Integral();
  double hch_1_area = hch_1->Integral();
  double hch_2_area = hch_2->Integral();
  double hch_3_area = hch_3->Integral();
  double hch_4_area = hch_4->Integral();
  double hch_5_area = hch_5->Integral();
  double htotal_1_area = htotal_1->Integral();
  double htotal_2_area = htotal_2->Integral();
  double htotal_3_area = htotal_3->Integral();
  double htotal_4_area = htotal_4->Integral();
  double htotal_5_area = htotal_5->Integral();
  double metbg_area = metbg->Integral();
  double metch_area = metch->Integral();

  cout << "MET integral background = " << metbg_area << endl;
  cout << "HT integral background (d1) = " << hbg_1_area << endl;
  cout << "HT integral background (d2) = " << hbg_2_area << endl;
  cout << "HT integral background (d3) = " << hbg_3_area << endl;
  cout << "HT integral background (d4) = " << hbg_4_area << endl;
  cout << "HT integral background (d5) = " << hbg_5_area << endl;
  cout << "MET integral chargino only = " << metch_area << endl;
  cout << "HT integral chargino only (d1) = " << hch_1_area << endl;
  cout << "HT integral chargino only (d2) = " << hch_2_area << endl;
  cout << "HT integral chargino only (d3) = " << hch_3_area << endl;
  cout << "HT integral chargino only (d4) = " << hch_4_area << endl;
  cout << "HT integral chargino only (d5) = " << hch_5_area << endl;
  cout << "HT integral total (d1) = " << htotal_1_area << endl;
  cout << "HT integral total (d2) = " << htotal_2_area << endl;
  cout << "HT integral total (d3) = " << htotal_3_area << endl;
  cout << "HT integral total (d4) = " << htotal_4_area << endl;
  cout << "HT integral total (d5) = " << htotal_5_area << endl;

  TCanvas* c = new TCanvas("canv", "The Canvas (post-analysis)", 1200, 800);
  gStyle->SetOptStat(1110);
  gStyle->SetStatColor(18);
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
  hbg_1->SetLineColor(38);
  hbg_1->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hbg_1->GetXaxis()->CenterTitle(true);
  hbg_1->GetYaxis()->SetTitle("Counts");
  hbg_1->GetYaxis()->CenterTitle(true);
  hbg_2->SetLineColor(38);
  hbg_2->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hbg_2->GetXaxis()->CenterTitle(true);
  hbg_2->GetYaxis()->SetTitle("Counts");
  hbg_2->GetYaxis()->CenterTitle(true);
  hbg_3->SetLineColor(38);
  hbg_3->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hbg_3->GetXaxis()->CenterTitle(true);
  hbg_3->GetYaxis()->SetTitle("Counts");
  hbg_3->GetYaxis()->CenterTitle(true);
  hbg_4->SetLineColor(38);
  hbg_4->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hbg_4->GetXaxis()->CenterTitle(true);
  hbg_4->GetYaxis()->SetTitle("Counts");
  hbg_4->GetYaxis()->CenterTitle(true);
  hbg_5->SetLineColor(38);
  hbg_5->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hbg_5->GetXaxis()->CenterTitle(true);
  hbg_5->GetYaxis()->SetTitle("Counts");
  hbg_5->GetYaxis()->CenterTitle(true);
  hch_1->SetLineColor(38);
  hch_1->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch_1->GetXaxis()->CenterTitle(true);
  hch_1->GetYaxis()->SetTitle("Counts");
  hch_1->GetYaxis()->CenterTitle(true);
  hch_2->SetLineColor(38);
  hch_2->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch_2->GetXaxis()->CenterTitle(true);
  hch_2->GetYaxis()->SetTitle("Counts");
  hch_2->GetYaxis()->CenterTitle(true);
  hch_3->SetLineColor(38);
  hch_3->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch_3->GetXaxis()->CenterTitle(true);
  hch_3->GetYaxis()->SetTitle("Counts");
  hch_3->GetYaxis()->CenterTitle(true);
  hch_4->SetLineColor(38);
  hch_4->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch_4->GetXaxis()->CenterTitle(true);
  hch_4->GetYaxis()->SetTitle("Counts");
  hch_4->GetYaxis()->CenterTitle(true);
  hch_5->SetLineColor(38);
  hch_5->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  hch_5->GetXaxis()->CenterTitle(true);
  hch_5->GetYaxis()->SetTitle("Counts");
  hch_5->GetYaxis()->CenterTitle(true);
  htotal_1->SetLineColor(38);
  htotal_1->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  htotal_1->GetXaxis()->CenterTitle(true);
  htotal_1->GetYaxis()->SetTitle("Counts");
  htotal_1->GetYaxis()->CenterTitle(true);
  htotal_1->SetLineColor(38);
  htotal_2->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  htotal_2->GetXaxis()->CenterTitle(true);
  htotal_2->GetYaxis()->SetTitle("Counts");
  htotal_2->GetYaxis()->CenterTitle(true);
  htotal_3->SetLineColor(38);
  htotal_3->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  htotal_3->GetXaxis()->CenterTitle(true);
  htotal_3->GetYaxis()->SetTitle("Counts");
  htotal_3->GetYaxis()->CenterTitle(true);
  htotal_4->SetLineColor(38);
  htotal_4->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  htotal_4->GetXaxis()->CenterTitle(true);
  htotal_4->GetYaxis()->SetTitle("Counts");
  htotal_4->GetYaxis()->CenterTitle(true);
  htotal_5->SetLineColor(38);
  htotal_5->GetXaxis()->SetTitle("\\mbox{HT (GeV)}");
  htotal_5->GetXaxis()->CenterTitle(true);
  htotal_5->GetYaxis()->SetTitle("Counts");
  htotal_5->GetYaxis()->CenterTitle(true);
  metbg->Draw("HIST");
  c->SaveAs("attach_y01_bg_met.png");
  metch->Draw("HIST");
  c->SaveAs("attach_y01_ch_met.png");
  hbg_1->Draw("HIST");
  c->SaveAs("attach_y01_d1_bg_jetht.png");
  hch_1->Draw("HIST");
  c->SaveAs("attach_y01_d1_ch_jetht.png");
  htotal_1->Draw("HIST");
  c->SaveAs("attach_y01_d1_total_jetht.png");
  hbg_2->Draw("HIST");
  c->SaveAs("attach_y01_d2_bg_jetht.png");
  hch_2->Draw("HIST");
  c->SaveAs("attach_y01_d2_ch_jetht.png");
  htotal_2->Draw("HIST");
  c->SaveAs("attach_y01_d2_total_jetht.png");
  hbg_3->Draw("HIST");
  c->SaveAs("attach_y01_d3_bg_jetht.png");
  hch_3->Draw("HIST");
  c->SaveAs("attach_y01_d3_ch_jetht.png");
  htotal_3->Draw("HIST");
  c->SaveAs("attach_y01_d3_total_jetht.png");
  hbg_4->Draw("HIST");
  c->SaveAs("attach_y01_d4_bg_jetht.png");
  hch_4->Draw("HIST");
  c->SaveAs("attach_y01_d4_ch_jetht.png");
  htotal_4->Draw("HIST");
  c->SaveAs("attach_y01_d4_total_jetht.png");
  hbg_5->Draw("HIST");
  c->SaveAs("attach_y01_d5_bg_jetht.png");
  hch_5->Draw("HIST");
  c->SaveAs("attach_y01_d5_ch_jetht.png");
  htotal_5->Draw("HIST");
  c->SaveAs("attach_y01_d5_total_jetht.png");
}
