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

class ExampleDisplacedAnalysis(Module): #this just turned out to be a better optimized x6.
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        # GENERAL
        # CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', 'Chargino Transverse Momentum', 250, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', 'Chargino Pseudorapidity', 250, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', 'Chargino Phi', 250, -6.4, 6.4)
        self.h_chdeta = ROOT.TH1F('chdeta', 'Chargino Delta Eta', 250, 0, 6)
        self.h_chdphi = ROOT.TH1F('chdphi', 'Chargino Delta Phi', 250, 0, 6.4)
        # ADD HISTOGRAMS
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)
        self.addObject(self.h_chphi)
        self.addObject(self.h_chdeta)
        self.addObject(self.h_chdphi)

    def analyze(self, event):
        genParts = Collection(event, "GenPart")
        finalReq = [13] #13, 24, 1000022, 1000024 -> muon, W, neutralino, chargino
        finalSampleEvent = []
        feventSum = ROOT.TLorentzVector() #unused
        #find the particles we need via searhing their family history
        for particle in genParts:
            if abs(particle.pdgId) in finalReq: #particle is muon
                mother = genParts[particle.genPartIdxMother] if particle.genPartIdxMother in range(len(genParts)) else None # to be W
                if mother is not None:
                    grandmother = genParts[mother.genPartIdxMother] if mother.genPartIdxMother in range(len(genParts)) else None # to be chargino
                    if grandmother is not None:
                        if abs(particle.pdgId) ==  13 and abs(mother.pdgId) == 24 and abs(grandmother.pdgId) == 1000024:
                            finalSampleEvent.append(grandmother)
                            self.h_chpt.Fill(grandmother.pt)
                            self.h_cheta.Fill(grandmother.eta)
                            self.h_chphi.Fill(grandmother.phi)                       
        #to calculate delta phi, delta eta, we need two charginos, or else there's no point
	if len(finalSampleEvent) == 2:
	    part1 = finalSampleEvent[0]
	    part2 = finalSampleEvent[1]
	    if part1.pdgId == -part2.pdgId: #uneccesary? testing now.
	    	for particle in finalSampleEvent:
	    	    deta = abs(part1.eta) - abs(part2.eta)
	    	    dphi = abs(part1.phi) - abs(part2.phi)
	    	    self.h_chdeta.Fill(deta)
	    	    self.h_chdphi.Fill(dphi)
	    else:
	        print("We have a whoopsie?")
	        print("p1: " + str(part1.pdgId) + ", p2: " + str(part2.pdgId))
        return True

    def endJob(self):
        self.c = ROOT.TCanvas("x8c", "The Canvas", 900, 660)
        self.addObject(self.c)
        self.c.cd()
        impHist = [self.h_chpt, self.h_cheta, self.h_chphi, self.h_chdeta, self.h_chdphi]
        for hist in impHist:
             hist.Draw()
             save = "x8/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = "" ## no preselection
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_200_180_10_final.root".format(os.environ['CMSSW_BASE'])]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x8.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## example root -l -b <file-to-open>.root
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
