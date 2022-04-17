#!/usr/bin/env python
#x11 - Quantities for new daughters, advance!
import os, sys
if 'CMSSW_VERSION' not in os.environ:
    print("Run 'cmsenv' on ../src/ please")
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
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 200, 0, 400)
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', 'Muon Transverse Momentum', 200, 0, 1100)
        self.h_mueta = ROOT.TH1F('mueta', 'Muon Pseudorapidity', 200, -6, 6)
        # 14 - MUON NETRINO
        self.h_nmupt = ROOT.TH1F('nmupt', 'Muon Neutrino Transverse Momentum', 200, 0, 1100)
        self.h_nmueta = ROOT.TH1F('nmueta', 'Muon Neutrino Pseudorapidity', 200, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', 'Neutralino Transverse Momentum', 200, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', 'Neutralino Pseudorapidity', 200, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', 'All Chargino Transverse Momentum', 200, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', 'All Chargino Pseudorapidity', 200, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', 'All Chargino Phi', 200, -3.2, 3.2)
        self.h_chdeta = ROOT.TH1F('chdeta', 'All Chargino Delta Eta', 200, 0, 6)
        self.h_chdphi = ROOT.TH1F('chdphi', 'All Chargino Delta Phi', 200, 0, 3.2)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', 'Chargino-Muon Delta Eta', 200, 0, 6)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', 'Chargino-Neutralino Delta Eta', 200, 0, 6)
        # ADD HISTOGRAMS
        self.addObject(self.h_metpt)
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)
        self.addObject(self.h_chphi)
        self.addObject(self.h_chdeta)
        self.addObject(self.h_chdphi)
        self.addObject(self.h_mupt)
        self.addObject(self.h_mueta)
        self.addObject(self.h_nmupt)
        self.addObject(self.h_nmupt)
        self.addObject(self.h_neupt)
        self.addObject(self.h_neueta)
        self.addObject(self.h_mix_chmu_deta)
        self.addObject(self.h_mix_chneu_deta)
        print("Initializing... beginJob function ended.")

    def analyze(self, event):
        genParts = Collection(event, "GenPart")
        eventMET = getattr(event, "MET_pt")
        self.h_metpt.Fill(eventMET)
        locateCharginos = [1000024]
        locateFinalStates = [13, 14, 1000022]
        leptonic = [13, 14]
        locatedCharginos = []
        locatedSpecificCharginos = []
        #def cycleResonance(particle, id):
        #    while abs(particle.pdgId) == id:
        #        if abs(particle.pdgId) != id:
        #            break
        #        particle =
        #def addUniqueChargino(particle):
        counter = 0
        #find chargino by making sure that it is the first ancestor, mass 200gev
        for particle in genParts:
            mother = genParts[particle.genPartIdxMother] if particle.genPartIdxMother in range(len(genParts)) else None
            if abs(particle.pdgId) in locateFinalStates: #identify final state particle:
                #mother must now be W or ch.
                #case for mu and nmu:
                if abs(particle.pdgId) in leptonic:
                    if abs(mother.pdgId) == 24:
                        #loop until source is chargino
                        tmp = mother #temp variable set, not actually mother... unless?
                        while abs(tmp.pdgId) == 24:
                            if abs(tmp.pdgId) != 24:
                                break
                            tmp = genParts[tmp.genPartIdxMother] if tmp.genPartIdxMother in range(len(genParts)) else None
                        if (tmp.pdgId == 1000024 and tmp.mass == 200.0) and not locatedSpecificCharginos.index(tmp):
                            locatedSpecificCharginos.append(tmp)
                        if abs(particle.pdgId) == 13:
                            self.h_mupt.Fill(particle.pt)
                            self.h_mueta.Fill(particle.eta)
                        if abs(particle.pdgId) == 14:
                            self.h_nmupt.Fill(particle.pt)
                            self.h_nmueta.Fill(particle.eta)
                #now for neu
                if abs(particle.pdgId) == 1000022:
                    if (mother.pdgId == 1000024 and mother.mass == 200.0) and not locatedSpecificCharginos.index(mother):
                        locatedSpecificCharginos.append(mother) #to improve here
                        self.h_neupt.Fill(particle.pt)
                        self.h_neueta.Fill(particle.eta)
                #now all first gen charginos, independant of reaction
                if (abs(particle.pdgId) == 1000024 and particle.mass == 200.0): # all charginos
                     counter += 1;
                     if (abs(mother.pdgId) == 1000024 and particle.mass == 200.0): #mother not same particle id, source is q,g: can improve
                         locatedCharginos.append(particle)
                         self.h_chpt.Fill(particle.pt)
                         self.h_cheta.Fill(particle.eta)
                         self.h_chphi.Fill(particle.phi)
        #to calculate delta phi, delta eta, we need two charginos, or else there's no point
        if len(locatedCharginos) == 2:
            part1 = locatedCharginos[0]
            part2 = locatedCharginos[1]
            if part1.pdgId == -part2.pdgId:
                for particle in locatedCharginos:
                    deta = abs(part1.eta) - abs(part2.eta)
                    dphi = part1.phi - part2.phi
                    self.h_chdeta.Fill(deta)
                    self.h_chdphi.Fill(dphi)
            else:
                print("Warning 1: Spotted like charge pair") #this doesnt show anymore, phew
                print("p1: " + str(part1.pdgId) + ", p2: " + str(part2.pdgId))
        return True

    def endJob(self):
        self.c = ROOT.TCanvas("x11c", "The Canvas", 900, 660)
        self.addObject(self.c)
        self.c.cd()
        impHist = [self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chdeta, self.h_chdphi, self.h_mupt, self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta]
        for hist in impHist:
             hist.Draw()
             save = "x11/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = ""
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_M150to200_DM5to20_ctau10.root".format(os.environ['CMSSW_BASE'])] ##new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x11.root", histDirName="plots")
p.run()

## methods (functions like pt() for the collections can be found in the root files)
## Just ignore the underscore '_' after the collection name, eg Muon_pt -> mu.pt, Muon_eta -> mu.eta
