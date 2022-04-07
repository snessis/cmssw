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

        self.h_mupt = ROOT.TH1F('mupt', 'Muon Transverse Momentum', 40, 0, 40)
        self.h_mudxy = ROOT.TH1F('mudxy', 'Muon Transverse Minimum Distance from PV', 30, 0, 30)
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 40, 0, 400)
        self.h_vpt = ROOT.TH1F('vpt', 'Vector Sum of the Event (Muons, Electrons, Jets)', 40, 0, 400)
        self.h_vMinusMetpt = ROOT.TH1F('vMinusMetpt', 'Vector Sum of the Event Considering MET', 40, 0, 400)
        self.h_nmuons = ROOT.TH1I('h_nmuons', 'Number of Muons Reconstructed per Event', 15, 0, 15)
        # My graphs start from here on out!
        self.h_mueta = ROOT.TH1F('mueta', 'Muon Pseudorapidity', 30, -5, 5)
        self.h_mudz = ROOT.TH1F('mudz', 'Muon z', 40, 0, 30)
        ## to add the histogram in the output RootFile ('histDisplacedAnalysisOut.root')
        self.addObject(self.h_mupt)
        self.addObject(self.h_mudxy)
        self.addObject(self.h_metpt)
        self.addObject(self.h_vpt)
        self.addObject(self.h_vMinusMetpt)
        self.addObject(self.h_nmuons)
        self.addObject(self.h_mueta)
        self.addObject(self.h_mudz)

    # Runs 1 time per event loop (the loop is handled by the PostProcessor)
    def analyze(self, event):
        muons = Collection(event, "Muon") #selected collection or reconstructed Muons
        jets = Collection(event, "Jet") #selected collection or reconstructed Jets
        ##
        ##
        electrons = Collection(event, "Electron") #selected collection or reconstructed Electrons (WE DONT INCLUDE THEM IN THIS STUDY, they are just needed for the event sum when we go low at Jet pt)
        ##
        eventMET = getattr(event, "MET_pt") #the reconstructed MET is a special event obj that is not a full collection. it's ONLY 1 calculation per event (against the muons for example that we have multiple in events)
        #eventMET = Collection(event, "MET",) #reconstructed MET of the event

        # select events with at least 1 displaced muon (dxy>0.05 cm - minimum distance of muon track wrt the PV)
        if len( filter(lambda mu: abs(mu.dxy)>0.05, muons) ) < 1:
            return True # go to the next event

        #check the class https://root.cern.ch/doc/master/classTLorentzVector.html
        eventSum = ROOT.TLorentzVector()

        for mu in muons:  # loop on muons
            self.h_mupt.Fill(mu.pt) ## for how to get variables see comment below
            self.h_mudxy.Fill(abs(mu.dxy))
            self.h_mueta.Fill(mu.eta)
            self.h_mudz.Fill(abs(mu.dz))
            eventSum += mu.p4()
        for elec in electrons:  # loop on electrons
            eventSum += elec.p4()
        for jet in jets:  # loop on jets
            eventSum += jet.p4()

        self.h_vpt.Fill(eventSum.Pt())  # fill histogram

        # now plot the MET
        self.h_metpt.Fill(eventMET)
        self.h_vMinusMetpt.Fill( abs(eventSum.Pt()-eventMET) ) #there is resolution to all the quantities it's not an exact equality (welcome to Particle Physics)
        ## MET (Missing Energy) is calculated by reverting the Reconstructed Transverse Event SUM 
        ## it's a vector in transverse plane equal to the sum but pointing backwards
        ## (so the Momentum is conserved in x-y), in z is the beams direction

        # fill also the #muons in the event
        self.h_nmuons.Fill(len(muons))

        return True


# this selects a subset of the events before running the events loop (the analyze code)
## preselection = "" ## no preselection
preselection = "Muon_pt>3.5 && MET_pt>50."

# the file to run
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_200_180_10_final.root".format(os.environ['CMSSW_BASE'])]

p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="my_ex2Out.root", histDirName="plots")
p.run()

## For help
##
## methods (functions like pt() for the collections can be found in the root files)
## example root -l -b <file-to-open>.root
## Events->Print("Muon_*"), there will be a list of available TBranches (aka variables)
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
