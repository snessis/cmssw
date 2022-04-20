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
        self.h_mupt = ROOT.TH1F('mupt', 'Muon Transverse Momentum', 200, 0, 100)
        self.h_mueta = ROOT.TH1F('mueta', 'Muon Pseudorapidity', 200, -6, 6)
        # 14 - MUON NETRINO
        self.h_nmupt = ROOT.TH1F('nmupt', 'Muon Neutrino Transverse Momentum', 200, 0, 100)
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
        self.addObject(self.h_nmueta)
        self.addObject(self.h_neupt)
        self.addObject(self.h_neueta)
        self.addObject(self.h_mix_chmu_deta)
        self.addObject(self.h_mix_chneu_deta)
        print("Initializing... beginJob function ended.")

    def analyze(self, event):
        genParts = Collection(event, "GenPart")
        eventMET = getattr(event, "MET_pt")
        self.h_metpt.Fill(eventMET)
        locateFinalStates = [13, 14, 1000022]
        leptonic = [13, 14]
        locatedCharginos = []
        locatedSpecificCharginos = []
        hadronic = [1,2,3,4,5,6,9,21]
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
            try:
                list.index(particle)
            except ValueError:
                list.append(particle)
        def checkUniqueParticle(particle, list):
            try:
                list.index(particle)
            except ValueError:
                return False
            return True

        #find chargino by making sure that it is the first ancestor, mass 200gev
        for particle in genParts:
            mother = findAncestor(particle)
            if abs(particle.pdgId) in locateFinalStates: #identify final state particle
                #mother must now be W or ch. instill check.
                #case for mu and nmu aka leptonic:
                if abs(particle.pdgId) in leptonic:
                    if abs(mother.pdgId) == 24: #is W
                        #loop until source is chargino
                        tmp = findAncestor(mother) #chargino or irrelevant W
                        if (tmp.pdgId == 1000024 and tmp.mass == 200.0):
                            addUniqueParticle(tmp, locatedSpecificCharginos)
                            deta = abs(particle.eta) - abs(tmp.eta)
                            if abs(particle.pdgId) == 13:
                                self.h_mupt.Fill(particle.pt)
                                self.h_mueta.Fill(particle.eta)
                                self.h_mix_chmu_deta.Fill(deta)
                            if abs(particle.pdgId) == 14:
                                self.h_nmupt.Fill(particle.pt)
                                self.h_nmueta.Fill(particle.eta)

        for particle in genParts: #need to repeat to verify
            mother = findAncestor(particle)
            #case for neu
            if abs(particle.pdgId) == 1000022 and abs(mother.pdgId) == 1000024 and mother.mass == 200.0:
                if checkUniqueParticle(mother, locatedSpecificCharginos) == True:
                    self.h_neupt.Fill(particle.pt)
                    self.h_neueta.Fill(particle.eta)
                    deta = abs(particle.eta) - abs(mother.eta)
                    self.h_mix_chneu_deta.Fill(deta)
            #now all first gen charginos, independant of reaction
            if (abs(particle.pdgId) == 1000024 and particle.mass == 200.0 and abs(mother.pdgId) != 1000024): # all charginos
                locatedCharginos.append(particle)
                self.h_chpt.Fill(particle.pt)
                self.h_cheta.Fill(particle.eta)
                self.h_chphi.Fill(particle.phi)
        #to calculate delta phi, delta eta, we need two charginos, or else there's no point
        print("Warning 3: locatedCharginos size:" + str(len(locatedCharginos)))
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
        impHist = [self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chdeta, self.h_chdphi, self.h_mupt, self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta, self.mix_chmu_deta, self.mix_chneu_deta]
        for hist in impHist:
             hist.Draw()
             save = "x11/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = ""
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_M150to200_DM5to20_ctau10.root".format(os.environ['CMSSW_BASE'])] ##new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x11.root", histDirName="plots")
p.run()
