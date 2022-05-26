#!/usr/bin/env python
ver = "27_1"
#assignment: catch muons from Ws, cuts and same stuff from x26
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
ROOT.PyConfig.IgnoreCommandLineOptions = True
#define values here to print in endJob function call
N1 = 748300 #HT 100 to 200
N2 = 1248911 #HT 200 to 400
N3 = 411531 #HT 400 to 600
N4 = 1560343 #HT 600 to 800
N5 = 737750 #HT 800 to 1200
N6 = 775061 #HT 1200 to 2500
N7 = 429253 #HT 2500 to Inf
events_recorded = 0
events_all = N1
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
        self.h_jetht = ROOT.TH1F('jetht', '\\mbox{Jet HT}', 100, 0, 400) #component
        self.h_lhepartpt = ROOT.TH1F('lhepartpt', '\\mbox{LHE Particle } p_t', 100, 0, 1500) #component
        self.h_lheht = ROOT.TH1F('lheht', '\\mbox{LHE HT}', 100, 0, 3500) #component
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', '\\mbox{Muon Transverse Momentum } p_t', 80, 0, 150)
        self.h_mueta = ROOT.TH1F('mueta', '\\mbox{Muon Pseudorapidity } \\eta', 80, -6, 6)
        # 14 - MUON NEUTRINO
        self.h_nmupt = ROOT.TH1F('nmupt', '\\mbox{Muon Neutrino Transverse Momentum } p_t', 80, 0, 50)
        self.h_nmueta = ROOT.TH1F('nmueta', '\\mbox{Muon Neutrino Pseudorapidity } \\eta', 80, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', '\\mbox{Neutralino Transverse Momentum } p_t', 80, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', '\\mbox{Neutralino Pseudorapidity } \\eta', 80, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', '\\mbox{Chargino Transverse Momentum, muon channel } p_t', 80, 0, 1000)
        self.h_cheta = ROOT.TH1F('cheta', '\\mbox{Chargino Pseudorapidity, muon channel } \\eta', 80, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', '\\mbox{Chargino Phi, muon channel } \\phi', 40, -3.1415927, 3.1415927)
        self.h_chdeta = ROOT.TH1F('chdeta', '\\mbox{Chargino Delta Eta, muon channel } \\Delta \\eta', 80, 0, 5)
        self.h_chdphi = ROOT.TH1F('chdphi', '\\mbox{Chargino Delta Phi, muon channel } \\Delta \\phi', 80, 0, 3.1415927)
        self.h_chlenl = ROOT.TH1F('chlenl', '\\mbox{Chargino Decay Length (Lab Frame), muon channel } L', 80, 0, 5)
        self.h_chlenr = ROOT.TH1F('chlenr', '\\mbox{Chargino Decay Length (Rest Frame), muon channel } L_0', 80, 0, 6)
        self.h_chbeta = ROOT.TH1F('chbeta', '\\mbox{Chargino Beta, muon channel } \\beta', 80, 0, 1)
        self.h_chgamma = ROOT.TH1F('chgamma', '\\mbox{Chargino Gamma, muon channel } \\gamma', 80, 1, 35)
        self.h_chnrgl = ROOT.TH1F('chnrgl', '\\mbox{Chargino Energy, muon channel } E', 80, 0, 1400)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', '\\mbox{Chargino-Muon Delta Eta } \\Delta \\eta', 80, 0, 2)
        self.h_mix_chnmu_deta = ROOT.TH1F('mix_chnmu_deta', '\\mbox{Chargino-Muon Neutrino Delta Eta } \\Delta \\eta', 80, 0, 3.5)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', '\\mbox{Chargino-Neutralino Delta Eta } \\Delta \\eta', 80, 0, 0.6)
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
        self.h_jetht.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_jetht.GetYaxis().SetTitle("Counts")
        self.h_lhepartpt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_lhepartpt.GetYaxis().SetTitle("Counts")
        self.h_lheht.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_lheht.GetYaxis().SetTitle("Counts")
        # 13 - MUON
        self.h_mupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_mupt.GetYaxis().SetTitle("Counts")
        self.h_mueta.GetXaxis().SetTitle("\\eta")
        self.h_mueta.GetYaxis().SetTitle("Counts")
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
        self.addObject(self.h_jetht)
        self.addObject(self.h_lhepartpt)
        self.addObject(self.h_lheht)
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
        genParts = Collection(event, "GenPart") #collection, given by NanoAODTools
        genJets = Collection(event, "GenJet") #collection, given by NanoAODTools
        METpt = getattr(event, "MET_pt") #branch
        lheht = getattr(event, "LHE_HT")
        #N = event
        locateFinalStates = [13, 14, 1000022]
        leptonic = [13, 14]
        mus = []
        nmus = []
        jets = []
        global events_recorded
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
        self.h_metptall.Fill(METpt)
        for particle in genParts:
            if abs(particle.pdgId) in locateFinalStates: #identify final state particle
                mother = findAncestor(particle) #mother must now be W
                #case for mu and nmu aka leptonic:
                if abs(particle.pdgId) in leptonic:
                    if abs(mother.pdgId) == 24: #must be W
                        if abs(particle.pdgId) == 13 and getStatusFlag(particle, 13) == 1 and abs(particle.pt) >= 4 and abs(particle.eta) <= 2.5:
                            addUniqueParticle(particle, mus)
                        if abs(particle.pdgId) == 14 and getStatusFlag(particle, 13) == 1:
                            addUniqueParticle(particle, nmus)
        for jet in genJets:
            if abs(jet.pt) >= 25:
                jets.append(jet)
        if METpt >= 130 and len(jets) > 0 and len(mus) > 0:
            self.h_jetht.Fill(jet.pt)
            self.h_lheht.Fill(lheht)
            self.h_metpt.Fill(METpt)
            for mu in mus:
                self.h_mupt.Fill(mu.pt)
                self.h_mueta.Fill(mu.eta)
            events_recorded += 1
            return True
        else:
            return False

    def endJob(self):
        print("Initializing endJob function...")
        print("Number of retained events: " + str(events_recorded))
        print("Number of events: " + str(events_all))
        br = (events_recorded)/(2.*events_all)
        print("Channel branching ratio: " + str(br))
        #CANVAS SETUP
        self.c = ROOT.TCanvas("canv", "The Canvas", 1000, 700)
        self.addObject(self.c)
        self.c.cd()
        #PRINTING
        print("Printing Histograms...")
        histList_all = ([self.h_metptall, self.h_jetht, self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chlenl, self.h_chlenr, self.h_chbeta,
                         self.h_chgamma, self.h_chnrgl, self.h_chdeta, self.h_chdphi, self.h_mupt, self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta,
                         self.mix_chmu_deta, self.mix_chnmu_deta, self.mix_chneu_deta]) #outdated?
        histList = [self.h_jetht, self.h_lheht, self.h_metpt, self.h_mupt, self.h_mueta]
        fit_chlenr = self.h_chlenr.Fit("expo") #exp(p0+p1*x)
        for hist in histList:
             hist.SetLineColor(38)
             hist.GetXaxis().CenterTitle(True)
             hist.GetYaxis().CenterTitle(True)
             hist.Draw()
             savepng = "x" + ver + "/" + "x" + ver + "_h_" + hist.GetName() + ".png"
             self.c.SaveAs(savepng)
             self.c.Update()
        Module.endJob(self)

preselection = "GenJet_pt >= 30 && MET_pt >= 130"
#files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_2.root".format(os.environ['CMSSW_BASE'])]
files = (["{}/src/displacedSOS_mainbkg_260422_nanoV7/WJetsToLNu_HT100to200.root".format(os.environ['CMSSW_BASE'])])
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x" + ver + ".root", histDirName="plots")
p.run()
