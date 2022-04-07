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

    # Runs ONLY ONCE before the event loop (define what you need for all the events, eg histograms)
    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        # --old & new histograms
        self.h_mupt = ROOT.TH1F('mupt', 'Muon Transverse Momentum (no filtering)', 40, 0, 40)
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 40, 0, 400)
        self.h_mueta = ROOT.TH1F('mueta', 'Muon Pseudorapidity (no filtering)', 30, 0, 5)
        self.h_vpt = ROOT.TH1F('vpt', 'Vector Sum of the Event (Muons, Electrons, Jets) (no filtering)', 40, 0, 400)
        self.h_vMinusMetpt = ROOT.TH1F('vMinusMetpt', 'Vector Sum of the Event Considering MET (no filtering)', 40, 0, 400)
        # --pass histograms, placed here for reference
        self.h_muptPass = ROOT.TH1F('muptPass', 'Muon Transverse Momentum (filtering)', 40, 0, 40)
        self.h_muetaPass = ROOT.TH1F('muetaPass', 'Muon Pseudorapidity (filtering)', 30, 0, 5)
        self.h_vptPass = ROOT.TH1F('vptPass', 'Vector Sum of the Event (Muons, Electrons, Jets) (filtering)', 40, 0, 400)
        self.h_vMinusMetptPass = ROOT.TH1F('vMinusMetptPass', 'Vector Sum of the Event Considering MET (filtering)', 40, 0, 400)
        # -- ratios
        self.h_muptRatio = ROOT.TH1F('muptRatio', 'Muon Transverse Momentum Ratio', 40, 0, 40)
        self.h_muetaRatio = ROOT.TH1F('muetaRatio', 'Muon Pseudorapidity Ratio', 30, 0, 5)
        self.h_vptRatio = ROOT.TH1F('vptRatio', 'Vector Sum of the Event (Muons, Electrons, Jets) Ratio', 40, 0 , 400)
        self.h_vMinusMetptRatio = ROOT.TH1F('vMinusMetptRatio', 'Vector Sum of the Event Considering MET Ratio)', 40, 0, 400)
        ## to add the histogram in the output RootFile ('histDisplacedAnalysisOut.root')
        self.addObject(self.h_muptPass)
        self.addObject(self.h_mupt)
        self.addObject(self.h_metpt)
        self.addObject(self.h_vpt)
        self.addObject(self.h_vptPass)
        self.addObject(self.h_vMinusMetpt)
        self.addObject(self.h_muetaPass)
        self.addObject(self.h_mueta)
        # -- ratios
        self.addObject(self.h_muptRatio)
        self.addObject(self.h_muetaRatio)
        self.addObject(self.h_vptRatio)
        self.addObject(self.h_vMinusMetptRatio)

    # Runs 1 time per event loop (the loop is handled by the PostProcessor)
    def analyze(self, event):
        #-- get collections:
        #-- muons is an array of all muons (= array entries with their measured properties: trivial ones like charge and mass, but also pt, eta and so on.
        muons = Collection(event, "Muon") 
        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron") #unused here but required (! check later why !)
        eventMET = getattr(event, "MET_pt") #the reconstructed MET is a special event obj that is not a full collection. it's ONLY 1 calculation per event
        # select events with at least 1 displaced muon (dxy>0.05 cm - minimum distance of muon track wrt the PV)
        if len( filter(lambda mu: abs(mu.dxy)>0.05, muons) ) < 1:
            return True # go to the next event:
                        # -- function ends here; no analysis will be done: nothing will be added in the histograms.

        #check the class https://root.cern.ch/doc/master/classTLorentzVector.html
        eventSum = ROOT.TLorentzVector()
        eventSumPass = ROOT.TLorentzVector()

        for mu in muons:  # loop on muons
            #-- add every property for all
            self.h_mupt.Fill(mu.pt) 
            self.h_mueta.Fill(abs(mu.eta))
            eventSum += mu.p4()
            #-- but now we need to make the 'Pass' histograms based on the criteria: "Muon_pt>5 && Muon_dz<0.5 && MET_pt>50."
            if (mu.pt > 5 and  mu.dz < 0.5):
                self.h_muptPass.Fill(mu.pt)
                self.h_muetaPass.Fill(abs(mu.eta))
                eventSumPass += mu.p4()
        for elec in electrons:  # loop on electrons
            eventSum += elec.p4()
        for jet in jets:  # loop on jets
            eventSum += jet.p4()

        self.h_vpt.Fill(eventSum.Pt()) 
        self.h_vptPass.Fill(eventSumPass.Pt()) 
        # now plot the MET
        self.h_metpt.Fill(eventMET)
        self.h_vMinusMetpt.Fill(abs(eventSum.Pt()-eventMET)) #there is resolution to all the quantities it's not an exact equality (welcome to Particle Physics)
        self.h_vMinusMetptPass.Fill(abs(eventSumPass.Pt()-eventMET)) #--resolution for passed muons
        
        ## MET (Missing Energy) is calculated by reverting the Reconstructed Transverse Event SUM 
        ## it's a vector in transverse plane equal to the sum but pointing backwards
        ## (so the Momentum is conserved in x-y), in z is the beams direction

        # --make the ratios
        self.h_muptRatio.Divide(self.h_muptPass, self.h_mupt)
        self.h_muetaRatio.Divide(self.h_muetaPass, self.h_mueta)
        self.h_vptRatio.Divide(self.h_vptPass, self.h_vpt) #--questionable existence?
        self.h_vMinusMetptRatio.Divide(self.h_vMinusMetptPass, self.h_vMinusMetpt) #--questionable existence?
        return True

preselection = "" ## no preselection
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_200_180_10_final.root".format(os.environ['CMSSW_BASE'])]
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="my_ex3Out.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## example root -l -b <file-to-open>.root
## Events->Print("Muon_*"), there will be a list of available TBranches (aka variables)
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta

