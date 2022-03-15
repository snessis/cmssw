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
        self.h_chphi = ROOT.TH1F('chphi', 'Chargino Phi', 250, -3.2, 3.2)
        # HISTOGRAMS
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)
        self.addObject(self.h_chphi)

    def analyze(self, event):
        genParts = Collection(event, "GenPart")
        finalReq = [13] #13, 24, 1000022, 1000024 -> muon, W, neutralino, chargino
        finalSampleEvent = []
        feventSum = ROOT.TLorentzVector()
        i = 1 #for logging

        for particle in genParts:
            if abs(particle.pdgId) in finalReq: #particle is muon
                mother = genParts[particle.genPartIdxMother] if particle.genPartIdxMother in range(len(genParts)) else None # to be W
                if mother is not None:
                    grandmother = genParts[mother.genPartIdxMother] if mother.genPartIdxMother in range(len(genParts)) else None # to be chargino
                    if grandmother is not None:
                        grandgrandmother = genParts[grandmother.genPartIdxMother] if grandmother.genPartIdxMother in range(len(genParts)) else None # to be None, popped from protons
                        gg3 = genParts[grandgrandmother.genPartIdxMother] if grandgrandmother.genPartIdxMother in range(len(genParts)) else None # to be None, popped from protons
                        #if gg3 is None:
                        #    print("gg3 is None!)"
                        #if gg3 is not None:
                        #    print("gg3 id: " + str(gg3.pdgId))
                        if 3==3: #adj
                            if abs(particle.pdgId) ==  13 and abs(mother.pdgId) == 24 and abs(grandmother.pdgId) == 1000024:
                                finalSampleEvent.append(grandgrandmother)
                                self.h_chpt.Fill(grandgrandmother.pt)
                                self.h_cheta.Fill(grandgrandmother.eta)
                                self.h_chphi.Fill(grandgrandmother.phi)
		               #tedious logging to see if things are ok
		                        print("id: " + str(particle.pdgId) + ", mid: " + str(mother.pdgId) + ", gmid: " + str(grandmother.pdgId) + ", ggmid: " + str(grandgrandmother.pdgId) + ", loopnum: " + str(i))
                                print("gg3id: " + str(gg3.pdgId))
		                        i += 1
	print("finalSampleEvent size: " + str(len(finalSampleEvent)))
	#if len(finalSampleEvent) == 2:
	#    i = 1
	#    if finalSampleEvent[0].pdgId == -finalSampleEvent[1].pdgId:
	#    	for particle in finalSampleEvent:
	#     	    self.h_chpt.Fill(particle.pt)
	#    	    self.h_cheta.Fill(particle.eta)
	#    	    self.h_chphi.Fill(particle.phi)
	#    	    finalSample.append(particle)
	#    	    print("We got one! particle sample num: " + str(i) + " out of 2")
	#    	    feventSum += particle.p4()
	#    	    i += 1

        return True

    def endJob(self):
        self.c = ROOT.TCanvas("x7c", "Canvas", 900, 660)
        self.addObject(self.c)
        self.c.cd()
        impHist = [self.h_chpt, self.h_cheta, self.h_chphi]
        for hist in impHist:
             hist.Draw()
             save = "x7/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = "" ## no preselection
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_200_180_10_final.root".format(os.environ['CMSSW_BASE'])]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x6.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## example root -l -b <file-to-open>.root
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
