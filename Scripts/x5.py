#!/usr/bin/env python
import os, sys
if 'CMSSW_VERSION' not in os.environ:
    print("Run 'cmsenv'")
    quit(1)

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

class ExampleDisplacedAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        # GENERAL 
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 150, 0, 800)
        self.h_vpt = ROOT.TH1F('vpt', 'Vector Sum of the Event', 150, 0, 800)
        self.h_vMinusMetpt = ROOT.TH1F('vMinusMetpt', 'Vector Sum of the Event Minus MET', 150, 0, 800)
        # MUONS
        self.h_mupt = ROOT.TH1F('mupt', 'Muon Transverse Momentum', 150, 0, 40)
        self.h_mueta = ROOT.TH1F('mueta', 'Muon Pseudorapidity', 150, -4, 4)
        # WS
        self.h_wpt = ROOT.TH1F('wpt', 'W Transverse Momentum', 150, 0, 100)
        self.h_weta = ROOT.TH1F('weta', 'W Pseudorapidity', 150, -6, 6)
        # CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', 'Chargino Transverse Momentum', 150, 0, 1000)
        self.h_chpt2 = ROOT.TH1F('chpt2', 'Chargino Transverse Momentum High Res', 150, 0, 1000)
        self.h_cheta = ROOT.TH1F('cheta', 'Chargino Pseudorapidity', 150, -6, 6)
        # HISTOGRAMS
        self.addObject(self.h_metpt)
        self.addObject(self.h_vpt)
        self.addObject(self.h_vMinusMetpt)
        self.addObject(self.h_mupt)
        self.addObject(self.h_mueta)
        self.addObject(self.h_wpt)
        self.addObject(self.h_weta)
        self.addObject(self.h_chpt)
        self.addObject(self.h_chpt2)
        self.addObject(self.h_cheta)

    def analyze(self, event):
        #get collections and define lists
        muons = Collection(event, "Muon") 
        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron") #unused here but required (! check later why !)
        genparts = Collection(event, "GenPart")
        eventMET = getattr(event, "MET_pt") #it's ONLY 1 calculation per event
        eventSum = ROOT.TLorentzVector()
        interestingParts = []
        reqParts = [13, 24, 1000024]
        ws = []
        charginos = []
        
        for mu in muons:
            self.h_mupt.Fill(mu.pt) 
            self.h_mueta.Fill(mu.eta)
            eventSum += mu.p4()
        for elec in electrons:
            eventSum += elec.p4()
        for jet in jets:
            eventSum += jet.p4() 
        for particle in genparts:
            eventSum += particle.p4()
            if abs(particle.pdgId) in reqParts:
                 interestingParts.append(particle)
                 if abs(particle.pdgId) == 24:
                     ws.append(particle)
                     self.h_wpt.Fill(particle.pt)
                     self.h_weta.Fill(particle.eta)
                 if abs(particle.pdgId) == 1000024:
                     charginos.append(particle)
                     self.h_chpt.Fill(particle.pt)
                     self.h_chpt2.Fill(particle.pt)
                     self.h_cheta.Fill(particle.eta) 
        self.h_metpt.Fill(eventMET)
        self.h_vpt.Fill(eventSum.Pt()) 
        self.h_vMinusMetpt.Fill(abs(eventSum.Pt()-eventMET)) 
        return True

    def endJob(self):
        self.c = ROOT.TCanvas("x5c", "Canvas")
        self.addObject(self.c)
        self.c.cd()
        impHist = [self.h_chpt, self.h_chpt2, self.h_cheta, self.h_wpt, self.h_weta, self.h_mupt, self.h_mueta, self.h_metpt, self.h_vpt, self.h_vMinusMetpt]
        for hist in impHist:
             hist.Draw()
             save = "x5/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = "" ## no preselection
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_200_180_10_final.root".format(os.environ['CMSSW_BASE'])]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x5.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## example root -l -b <file-to-open>.root
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
