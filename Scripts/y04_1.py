#!/usr/bin/env python
ver = "02_1"
#cuts: met>=100, >=1 muons, muonpt >= 4, muoneta <=2.5
import os, sys, math
if 'CMSSW_VERSION' not in os.environ:
    print("Run 'cmsenv' on ../src/")
    quit(1)
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import ROOT
from ROOT import gStyle, gROOT
from pprint import pprint
ROOT.PyConfig.IgnoreCommandLineOptions = True
#define values here to print in endJob function call
events_recorded = 0
events_passed = 0
events_selected = 0
events_all = 556249
locateFinalStates = [13, 14, 1000022]
leptonic = [13, 14]
hadronic = [1,2,3,4,5,6,21]
d1 = 0
d2 = 0.25
d3 = 0.5
d4 = 0.75
d5 = 1
class ExampleDisplacedAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        print("Creating ROOT objects...")
        # GENERAL
        self.h_metptall = ROOT.TH1F('metptall', '\\mbox{Missing Energy Transverse, all events (MET)}', 100, 0, 400)
        self.h_metpt = ROOT.TH1F('metpt', '\\mbox{Missing Energy Transverse, muon channel (MET)}', 100, 0, 400)
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # JETS
        self.h_jetht1 = ROOT.TH1F('jetht1', '\\mbox{Jet HT (for distance } d_1 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht2 = ROOT.TH1F('jetht2', '\\mbox{Jet HT (for distance } d_2 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht3 = ROOT.TH1F('jetht3', '\\mbox{Jet HT (for distance } d_3 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht4 = ROOT.TH1F('jetht4', '\\mbox{Jet HT (for distance } d_4 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht5 = ROOT.TH1F('jetht5', '\\mbox{Jet HT (for distance } d_5 \\mbox{ cut)}', 100, 0, 3500) #component
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', '\\mbox{Muon Transverse Momentum } p_t', 100, 0, 25)
        self.h_mueta = ROOT.TH1F('mueta', '\\mbox{Muon Pseudorapidity } \\eta', 100, -6, 6)
        self.h_mupvdistancerestrest1 = ROOT.TH1F('mupvdistancerestrest1', '\\mbox{Muon-PV Distance (Lab Frame) } d_1', 120, 0, 15)
        self.h_mupvdistancerestrest2 = ROOT.TH1F('mupvdistancerestrest2', '\\mbox{Muon-PV Distance (Lab Frame) } d_2', 120, 0, 15)
        self.h_mupvdistancerestrest3 = ROOT.TH1F('mupvdistancerestrest3', '\\mbox{Muon-PV Distance (Lab Frame) } d_3', 120, 0, 15)
        self.h_mupvdistancerestrest4 = ROOT.TH1F('mupvdistancerestrest4', '\\mbox{Muon-PV Distance (Lab Frame) } d_4', 120, 0, 15)
        self.h_mupvdistancerestrest5 = ROOT.TH1F('mupvdistancerestrest5', '\\mbox{Muon-PV Distance (Lab Frame) } d_5', 120, 0, 15)
        # 14 - MUON NEUTRINO
        self.h_nmupt = ROOT.TH1F('nmupt', '\\mbox{Muon Neutrino Transverse Momentum } p_t', 100, 0, 25)
        self.h_nmueta = ROOT.TH1F('nmueta', '\\mbox{Muon Neutrino Pseudorapidity } \\eta', 100, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', '\\mbox{Neutralino Transverse Momentum } p_t', 100, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', '\\mbox{Neutralino Pseudorapidity } \\eta', 100, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', '\\mbox{Chargino Transverse Momentum, muon channel } p_t', 100, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', '\\mbox{Chargino Pseudorapidity, muon channel } \\eta', 100, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', '\\mbox{Chargino Phi, muon channel } \\phi', 40, -3.1415927, 3.1415927)
        self.h_chdeta = ROOT.TH1F('chdeta', '\\mbox{Chargino Delta Eta, muon channel } \\Delta \\eta', 100, 0, 2.5)
        self.h_chdphi = ROOT.TH1F('chdphi', '\\mbox{Chargino Delta Phi, muon channel } \\Delta \\phi', 100, 0, 3.1415927)
        self.h_chlenl = ROOT.TH1F('chlenl', '\\mbox{Chargino Decay Length (Lab Frame), muon channel } L', 100, 0, 5)
        self.h_chlenr = ROOT.TH1F('chlenr', '\\mbox{Chargino Decay Length (Rest Frame), muon channel } L_0', 100, 0, 6)
        self.h_chbeta = ROOT.TH1F('chbeta', '\\mbox{Chargino Beta, muon channel } \\beta', 100, 0, 1)
        self.h_chgamma = ROOT.TH1F('chgamma', '\\mbox{Chargino Gamma, muon channel } \\gamma', 100, 1, 35)
        self.h_chnrgl = ROOT.TH1F('chnrgl', '\\mbox{Chargino Energy, muon channel } E', 100, 0, 1400)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', '\\mbox{Chargino-Muon Delta Eta } \\Delta \\eta', 100, 0, 2.5)
        self.h_mix_chnmu_deta = ROOT.TH1F('mix_chnmu_deta', '\\mbox{Chargino-Muon Neutrino Delta Eta } \\Delta \\eta', 100, 0, 2.5)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', '\\mbox{Chargino-Neutralino Delta Eta } \\Delta \\eta', 100, 0, 1)
        # GRAPH CUSTOMIZATION
        gStyle.SetOptStat(1110) #see https://root.cern.ch/doc/master/classTStyle.html#a0ae6f6044b6d7a32756d7e98bb210d6c
        gStyle.SetStatColor(18)
        # GENERAL
        self.h_metptall.GetXaxis().SetTitle("MET (GeV)")
        self.h_metptall.GetYaxis().SetTitle("Counts")
        self.h_metpt.GetXaxis().SetTitle("MET (GeV)")
        self.h_metpt.GetYaxis().SetTitle("Counts")
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # JETS
        self.h_jetht1.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht1.GetYaxis().SetTitle("Counts")
        self.h_jetht2.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht2.GetYaxis().SetTitle("Counts")
        self.h_jetht3.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht3.GetYaxis().SetTitle("Counts")
        self.h_jetht4.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht4.GetYaxis().SetTitle("Counts")
        self.h_jetht5.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht5.GetYaxis().SetTitle("Counts")
        # 13 - MUON
        self.h_mupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_mupt.GetYaxis().SetTitle("Counts")
        self.h_mueta.GetXaxis().SetTitle("\\eta")
        self.h_mueta.GetYaxis().SetTitle("Counts")
        self.h_mupvdistancerestrest1.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistancerestrest1.GetYaxis().SetTitle("Counts")
        self.h_mupvdistancerestrest2.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistancerestrest2.GetYaxis().SetTitle("Counts")
        self.h_mupvdistancerestrest3.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistancerestrest3.GetYaxis().SetTitle("Counts")
        self.h_mupvdistancerestrest4.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistancerestrest4.GetYaxis().SetTitle("Counts")
        self.h_mupvdistancerestrest5.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistancerestrest5.GetYaxis().SetTitle("Counts")
        # 14 - MUON NETRINO
        self.h_nmupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_nmupt.GetYaxis().SetTitle("Counts")
        self.h_nmueta.GetXaxis().SetTitle("\\eta")
        self.h_nmueta.GetYaxis().SetTitle("Counts")
        # 1000022 - NEUTRALINO
        self.h_neupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_neupt.GetYaxis().SetTitle("Counts")
        self.h_neueta.GetXaxis().SetTitle("\\eta")
        self.h_neueta.GetYaxis().SetTitle("Counts")
        # 1000024 - CHARGINOS
        self.h_chpt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_chpt.GetYaxis().SetTitle("Counts")
        self.h_cheta.GetXaxis().SetTitle("\\eta")
        self.h_cheta.GetYaxis().SetTitle("Counts")
        self.h_chphi.GetXaxis().SetTitle("\\phi \\mbox{ (rad)}")
        self.h_chphi.GetYaxis().SetTitle("Counts")
        self.h_chdphi.GetXaxis().SetTitle("\\Delta \\phi \\mbox{ (rad)}")
        self.h_chdphi.GetYaxis().SetTitle("Counts")
        self.h_chdeta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_chdeta.GetYaxis().SetTitle("Counts")
        self.h_chlenl.GetXaxis().SetTitle("L \\mbox{ (cm)}")
        self.h_chlenl.GetYaxis().SetTitle("Counts")
        self.h_chlenr.GetXaxis().SetTitle("L \\mbox{ (cm)}")
        self.h_chlenr.GetYaxis().SetTitle("Counts")
        self.h_chbeta.GetXaxis().SetTitle("\\beta")
        self.h_chbeta.GetYaxis().SetTitle("Counts")
        self.h_chgamma.GetXaxis().SetTitle("\\gamma")
        self.h_chgamma.GetYaxis().SetTitle("Counts")
        self.h_chnrgl.GetXaxis().SetTitle("E \\mbox{ (GeV)}")
        self.h_chnrgl.GetYaxis().SetTitle("Counts")
        # MIXTURES
        self.h_mix_chmu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chnmu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chnmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chneu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chneu_deta.GetYaxis().SetTitle("Counts")
        # ADD HISTOGRAMS
        self.addObject(self.h_metptall)
        self.addObject(self.h_metpt)
        self.addObject(self.h_jetht1)
        self.addObject(self.h_jetht2)
        self.addObject(self.h_jetht3)
        self.addObject(self.h_jetht4)
        self.addObject(self.h_jetht5)
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)
        self.addObject(self.h_chphi)
        self.addObject(self.h_chdeta)
        self.addObject(self.h_chdphi)
        self.addObject(self.h_chlenl)
        self.addObject(self.h_chlenr)
        self.addObject(self.h_chbeta)
        self.addObject(self.h_chgamma)
        self.addObject(self.h_chnrgl)
        self.addObject(self.h_mupt)
        self.addObject(self.h_mueta)
        self.addObject(self.h_mupvdistancerestrest1)
        self.addObject(self.h_mupvdistancerestrest2)
        self.addObject(self.h_mupvdistancerestrest3)
        self.addObject(self.h_mupvdistancerestrest4)
        self.addObject(self.h_mupvdistancerestrest5)
        self.addObject(self.h_nmupt)
        self.addObject(self.h_nmueta)
        self.addObject(self.h_neupt)
        self.addObject(self.h_neueta)
        self.addObject(self.h_mix_chmu_deta)
        self.addObject(self.h_mix_chnmu_deta)
        self.addObject(self.h_mix_chneu_deta)
        print("beginJob function ended. Initializing analysis...")
        # TEMPORARY HISTOGRAMS
    def analyze(self, event):
        #Variables, Arrays
        genParts = Collection(event, "GenPart") #collection
        Jets = Collection(event, "Jet") #collection, given by NanoAODTools
        METpt = getattr(event, "MET_pt") #branch
        Muons = Collection(event, "Muon")
        PVx = getattr(event, "PV_x")
        PVy = getattr(event, "PV_y")
        PVz = getattr(event, "PV_z")
        chs_all = []
        chs = []
        mus = []
        mus2 = []
        Mus = []
        nmus = []
        neus = []
        jets = []
        global events_recorded
        global events_passed
        global events_selected
        eventRecorded = False
        #Function definitions
        def findAncestor(particle): #aims to find a mother particle. if it doesnt, it returns the original
            original = particle
            resonance = original
            while resonance.pdgId == original.pdgId:
                testResonance = genParts[resonance.genPartIdxMother] if resonance.genPartIdxMother in range(len(genParts)) else None
                try:
                    testResonance.pdgId
                except:
                    return original
                resonance = genParts[resonance.genPartIdxMother] if resonance.genPartIdxMother in range(len(genParts)) else None
            return resonance
        def addUniqueParticle(particle, list): #adds unique particle to list. on fail, it doesnt
            ids = []
            for item in list:
                ids.append(item.genPartIdxMother)
            if particle.genPartIdxMother not in ids:
                list.append(particle)
        def getStatusFlag(part, pos): #returns 0 or 1 of a bitwise, in position pos
            flag = str(part.statusFlags>>pos)
            return int(flag[:1])
        #scan all particles in the event by final state
        events_selected += 1
        self.h_metptall.Fill(METpt)
        genpartsids = []
        for particle in genParts:
            genpartsids.append(particle.pdgId)
            if abs(particle.pdgId) == 13:
                mother = findAncestor(particle) #mother must now be W. instill check.
                if abs(mother.pdgId) == 24: #must be W
                    gmother = findAncestor(mother) #chargino or irrelevant W
                    addUniqueParticle(particle, mus)
        init = ""
        for id in genpartsids:
            init = init + str(abs(id)) + ", "
        print(init)
        if len(mus) == 0:
            return False
        for Muon in Muons:
            if genParts[Muon.genPartIdx] in mus:
                d = math.sqrt(math.pow(Muon.dxy, 2) + math.pow(Muon.dz, 2))
                if Muon.pt >= 3 and abs(Muon.eta) <= 2.5 and METpt >= 100 and d >= 0.017:
                    Mus.append(Muon)
                    mus2.append(genParts[Muon.genPartIdx])
                    eventRecorded = True
                    events_passed += 1
        if len(Mus) == 0:
            return False
        #print("gen muons: " + str(len(mus)) + ", reco muons: " + str(len(Mus)) + ", gen mus2: "+ str(len(mus2)))
        for jet in Jets:
            if abs(jet.pt) >= 30:
                jets.append(jet)
        dists = []
        for Mu in Mus:
            d = math.sqrt(math.pow(Mu.dxy, 2) + math.pow(Mu.dz, 2))
            dists.append(d)
            self.h_mupt.Fill(Mu.pt)
            self.h_mueta.Fill(Mu.eta)
            if d >= d1:
                self.h_mupvdistancerest1.Fill(d)
            if d >= d2:
                self.h_mupvdistancerest2.Fill(d)
            if d >= d3:
                self.h_mupvdistancerest3.Fill(d)
            if d >= d4:
                self.h_mupvdistancerest4.Fill(d)
            if d >= d5:
                self.h_mupvdistancerest5.Fill(d)
        if eventRecorded == True:
            self.h_metpt.Fill(METpt)
            events_recorded += 1
            sum = 0
            for jet in jets:
                sum += jet.pt
            d = 0
            for di in dists:
                if di >= d:
                    d = di
            if d >= d1:
                self.h_jetht1.Fill(sum)
            if d >= d2:
                self.h_jetht2.Fill(sum)
            if d >= d3:
                self.h_jetht3.Fill(sum)
            if d >= d4:
                self.h_jetht4.Fill(sum)
            if d >= d5:
                self.h_jetht5.Fill(sum)
        #analysis ends here: return True
        return True

    def endJob(self):
        print("Initializing endJob function...")
        #CANVAS SETUP
        self.c = ROOT.TCanvas("canv", "The Canvas", 1000, 700)
        self.addObject(self.c)
        self.c.cd()
        #FITTING
        fit_mupvdistancerest = ROOT.TF1("fit_mupvdistancerest", "expo", 0, 10)
        fit_mupvdistancerest.SetParNames("mupvconst", "mupvslope")
        #fit_mupvdistancerest.SetParameter("mupvconst",)
        #self.mupvdistancerest1.Fit(fit_mupvdistancerest)
        #PRINTING
        print("Number of muon channel events: " + str(events_recorded))
        print("Number of passed entries: " + str(events_passed))
        print("Number of events selected: " + str(events_selected))
        print("Printing Histograms...")
        histList_all = ([self.h_metptall, self.h_jetht1, self.h_jetht2, self.h_jetht3, self.h_jetht4, self.h_jetht5, self.h_metpt, self.h_chpt, self.h_cheta,
                         self.h_chphi, self.h_chlenl, self.h_chlenr, self.h_chbeta, self.h_chgamma, self.h_chnrgl, self.h_chdeta, self.h_chdphi, self.h_mupt,
                         self.h_mueta, self.mupvdistancerest1, self.mupvdistancerest2, self.mupvdistancerest3, self.mupvdistancerest4, self.mupvdistancerest5, self.nmupt,
                         self.nmueta, self.neupt, self.neueta, self.mix_chmu_deta, self.mix_chnmu_deta, self.mix_chneu_deta])
        histList = ([self.h_metptall, self.h_metpt, self.h_mupt, self.h_mueta, self.mupvdistancerest1, self.mupvdistancerest2, self.mupvdistancerest3, self.mupvdistancerest4, self.mupvdistancerest5])
        XSECCH = 0.902569*1000
        L = 60
        scale = 1/events_all * XSECCH * L
        for hist in histList:
             hist.SetLineColor(38)
             hist.SetFillColor(38)
             hist.SetLineWidth(2)
             hist.GetXaxis().CenterTitle(True)
             hist.GetYaxis().CenterTitle(True)
             #hist.Scale(scale)
             hist.Draw()
             save = "y" + ver + "/" + "y" + ver + "_h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
             self.c.Update()
        #done here, remove stat box
        gStyle.SetOptStat(0)
        self.c.Update()
        #MET
        self.s_met = ROOT.THStack("s_met","\\mbox{Missing Energy Transverse (MET) Momentum } p_t");
        self.addObject(self.s_met)
        histList_met = [self.h_metpt, self.h_metptall]
        self.h_metptall.SetLineColor(30)
        self.h_metptall.SetFillColor(30)
        self.h_metpt.SetLineColor(8)
        self.h_metpt.SetFillColor(8)
        for hist in histList_met:
            self.s_met.Add(hist)
        self.leg_met = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_met.SetMargin(0.15)
        self.leg_met.AddEntry(self.h_metptall, "All W^{#pm} channels", "L")
        self.leg_met.AddEntry(self.h_metpt, "W^{#pm}#rightarrow #mu#nu_{#mu}", "L")
        self.s_met.Draw()
        gStyle.SetOptStat(0)
        self.leg_met.Draw()
        self.s_met.GetXaxis().SetTitle("\\mbox{MET (GeV)}")
        self.s_met.GetYaxis().SetTitle("Counts")
        self.s_met.GetXaxis().CenterTitle(True)
        self.s_met.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_met.GetName() + ".png")
        self.c.Update()
        #ETA
        Module.endJob(self)

preselection = "MET_pt >= 100 && Jet_pt >= 30"
#preselection = ""
#files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_2.root".format(os.environ['CMSSW_BASE'])]
files = (["{}/src/displacedSOS_mainbkg_260422_nanoV7/WJetsToLNu_HT100to200.root".format(os.environ['CMSSW_BASE'])])
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="y" + ver + ".root", histDirName="plots")
p.run()
