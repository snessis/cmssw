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
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 170, 0, 1300)
        self.h_vpt = ROOT.TH1F('vpt', 'Vector Sum of the Event', 170, 0, 1300)
        self.h_vMinusMetpt = ROOT.TH1F('vMinusMetpt', 'Vector Sum of the Event Minus MET', 170, 0, 1300)
        # CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', 'Chargino Transverse Momentum', 170, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', 'Chargino Pseudorapidity', 170, -6, 6)
        # HISTOGRAMS
        self.addObject(self.h_metpt)
        self.addObject(self.h_vpt)
        self.addObject(self.h_vMinusMetpt)
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)

    def analyze(self, event):
        #get collections and define lists
        muons = Collection(event, "Muon") 
        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron") #unused here but required (! check later why !)
        genParts = Collection(event, "GenPart")
        eventMET = getattr(event, "MET_pt")
        eventSum = ROOT.TLorentzVector()
        finalReq = [1000022, 13]
        finalSample = []
        omegaSample = []
        omegaReq = [13, 24, 1000022, 1000024] #muon, W, neutralino, chargino
        i = 1
        
        for mu in muons:
            eventSum += mu.p4()
        for elec in electrons:
            eventSum += elec.p4()
        for jet in jets:
            eventSum += jet.p4()   
        for particle in genParts:
            eventSum += particle.p4()
            if abs(particle.pdgId) in finalReq:
                mother = genParts[particle.genPartIdxMother] if particle.genPartIdxMother in range(len(genParts)) else None
                grandmother = genParts[mother.genPartIdxMother] if mother.genPartIdxMother in range(len(genParts)) else None # to be chargino
                if abs(particle.pdgId) ==  13 and abs(mother.pdgId) == 24 and abs(grandmother.pdgId) == 1000024: 
		    finalSample.append(particle)
		    self.h_chpt.Fill(grandmother.pt)
		    self.h_cheta.Fill(grandmother.eta)
		    print("genParts size: " + str(len(genParts)) + ", particle id: "+ str(particle.pdgId) + ", mother id: " + str(mother.pdgId) + ", particle in array: " + str(i))
		    i += 1
                
        self.h_metpt.Fill(eventMET)
        self.h_vpt.Fill(eventSum.Pt()) 
        self.h_vMinusMetpt.Fill(abs(eventSum.Pt()-eventMET)) 
        return True

    def endJob(self):
        self.c = ROOT.TCanvas("x6c", "Canvas", 900, 660)
        self.addObject(self.c)
        self.c.cd()
        impHist = [self.h_chpt, self.h_cheta, self.h_metpt, self.h_vpt, self.h_vMinusMetpt]
        for hist in impHist:
             hist.Draw()
             save = "x6/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)
        

preselection = "" ## no preselection
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_200_180_10_final.root".format(os.environ['CMSSW_BASE'])]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x6.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## example root -l -b <file-to-open>.root
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
