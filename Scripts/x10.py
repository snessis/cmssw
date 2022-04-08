#!/usr/bin/env python
import os, sys
if 'CMSSW_VERSION' not in os.environ:
    print("Run 'cmsenv' please")
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
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 40, 0, 400)
        # CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', 'Chargino Transverse Momentum', 250, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', 'Chargino Pseudorapidity', 250, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', 'Chargino Phi', 250, -3.2, 3.2)
        self.h_chdeta = ROOT.TH1F('chdeta', 'Chargino Delta Eta', 250, 0, 6)
        self.h_chdphi = ROOT.TH1F('chdphi', 'Chargino Delta Phi', 250, 0, 3.2)
        # ADD HISTOGRAMS
        self.addObject(self.h_metpt)
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)
        self.addObject(self.h_chphi)
        self.addObject(self.h_chdeta)
        self.addObject(self.h_chdphi)

    def analyze(self, event):
        genParts = Collection(event, "GenPart")
        eventMET = getattr(event, "MET_pt")
        finalReq = [1000024] #13, 24, 1000022, 1000024 -> muon, W, neutralino, chargino. see https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        finalSampleEvent = []
        counter = 0;
        #find chargino by making sure that it is the first ancestor, mass 200gev
        for particle in genParts:
            if (abs(particle.pdgId) in finalReq):
                 mother = genParts[particle.genPartIdxMother] if particle.genPartIdxMother in range(len(genParts)) else None # to be W
                 counter += 1;
                 if (abs(mother.pdgId) not in [1000024] and particle.mass == 200.0):
                     finalSampleEvent.append(particle)
                     self.h_chpt.Fill(particle.pt)
                     self.h_cheta.Fill(particle.eta)
                     self.h_chphi.Fill(particle.phi)
                     self.h_chmass.Fill(particle.mass)
        #if len(finalSampleEvent) > 0:
        #    print("genPart particles: " + str(len(genParts)) + ", charginos: " + str(counter) + ", first ancestors: " + str(len(finalSampleEvent)))
        #to calculate delta phi, delta eta, we need two charginos, or else there's no point
	    if len(finalSampleEvent) == 2:
	        part1 = finalSampleEvent[0]
            part2 = finalSampleEvent[1]
            if part1.pdgId == -part2.pdgId:
                for particle in finalSampleEvent:
                    deta = abs(part1.eta) - abs(part2.eta)
                    dphi = part1.phi - part2.phi
                    self.h_chdeta.Fill(deta)
                    self.h_chdphi.Fill(dphi)
            else:
                print("Spotted like charge pair")
                print("p1: " + str(part1.pdgId) + ", p2: " + str(part2.pdgId))
	    self.h_metpt.Fill(eventMET)
        return True

    def endJob(self):
        self.c = ROOT.TCanvas("x10c", "The Canvas", 900, 660)
        self.addObject(self.c)
        self.c.cd()
        impHist = [self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chdeta, self.h_chdphi]
        for hist in impHist:
             hist.Draw()
             save = "x10/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = ""
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_M150to200_DM5to20_ctau10.root".format(os.environ['CMSSW_BASE'])] ##new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x8.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
