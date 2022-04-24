#!/usr/bin/env python
#x13 - pt for x12, graph beautifying
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
        self.h_metpt = ROOT.TH1F('metpt', 'Missing Transverse Momentum', 175, 0, 400)
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', 'Muon Transverse Momentum', 175, 0, 100)
        self.h_mueta = ROOT.TH1F('mueta', 'Muon Pseudorapidity', 175, -6, 6)
        # 14 - MUON NETRINO
        self.h_nmupt = ROOT.TH1F('nmupt', 'Muon Neutrino Transverse Momentum', 175, 0, 100)
        self.h_nmueta = ROOT.TH1F('nmueta', 'Muon Neutrino Pseudorapidity', 175, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', 'Neutralino Transverse Momentum', 175, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', 'Neutralino Pseudorapidity', 175, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', 'All Chargino Transverse Momentum', 175, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', 'All Chargino Pseudorapidity', 175, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', 'All Chargino Phi', 175, -3.2, 3.2)
        self.h_chdeta = ROOT.TH1F('chdeta', 'All Chargino Delta Eta', 175, 0, 6)
        self.h_chdphi = ROOT.TH1F('chdphi', 'All Chargino Delta Phi', 175, 0, 3.2)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', 'Chargino-Muon Delta Eta', 175, 0, 4)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', 'Chargino-Neutralino Delta Eta', 175, 0, 1)
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
        hadronic = [1,2,3,4,5,6,9,21]
        locatedCharginos = []
        locatedSpecificCharginos = []
        mus = []
        nmus = []
        neus = []
        def findAncestor(particle, log): #aims to find a mother particle. if it doesnt, it returns the original
            original = particle
            resonance = original
            if log == True:
                print("Warning pre-4: Starting process")
            while resonance.pdgId == original.pdgId:
                testResonance = genParts[resonance.genPartIdxMother] if resonance.genPartIdxMother in range(len(genParts)) else None
                try:
                    testResonance.pdgId
                except:
                    if log == True:
                        print("Warning 4.5: Exception. Returning original")
                    return original
                resonance = genParts[resonance.genPartIdxMother] if resonance.genPartIdxMother in range(len(genParts)) else None
            if log == True:
                print("Warning 4: Original id: " + str(original.pdgId) + ", Mother id: " + str(resonance.pdgId))
            return resonance
        def addUniqueParticle(particle, list): #adds unique particle to list. on fail, it doesnt
            ids = []
            for item in list:
                ids.append(item.genPartIdxMother)
            if particle.genPartIdxMother not in ids:
                list.append(particle)
        def particleInList(particle, list):
            ids = []
            for item in list:
                ids.append(item.genPartIdxMother)
            if particle.genPartIdxMother in ids:
                return True
            else:
                return False
        #find chargino by making sure that it is the first ancestor, mass 200gev
        for particle in genParts:
            if abs(particle.pdgId) in locateFinalStates: #identify final state particle
                mother = findAncestor(particle, False)
                #mother must now be W or ch. instill check.
                #case for mu and nmu aka leptonic:
                if abs(particle.pdgId) in leptonic:
                    if abs(mother.pdgId) == 24: #must be W
                        gmother = findAncestor(mother, False) #chargino or irrelevant W
                        if (gmother.pdgId == 1000024 and gmother.mass == 200.0):
                            addUniqueParticle(gmother, locatedSpecificCharginos)
                            if abs(particle.pdgId) == 13 and abs(particle.pt) >= 5:
                                addUniqueParticle(particle, mus)
                            if abs(particle.pdgId) == 14:
                                addUniqueParticle(particle, nmus)
                if abs(particle.pdgId) == 1000022 and abs(mother.pdgId) == 1000024 and mother.mass == 200.0:
                    addUniqueParticle(mother, locatedSpecificCharginos)
                    addUniqueParticle(particle, neus)
            else:
                return True
        #x12 algorithm for faster handling & incoporates same parent generation for mu, nmu, neu
        mn_moms = 0
        ch_moms = 0
        for mu in mus:
            mu_mother = findAncestor(mu, False) #W
            for nmu in nmus:
                nmu_mother = findAncestor(nmu, False) #W
                if nmu_mother.genPartIdxMother == mu_mother.genPartIdxMother:
                    mn_moms += 1
                    mu_gmother = findAncestor(mu_mother, False) #chargino
                    nmu_gmother = findAncestor(nmu_mother, False) #chargino must be the same
                    if mu_gmother.genPartIdxMother == nmu_gmother.genPartIdxMother:
                        #nmu_gmother = findAncestor(nmu_mother)
                        for neu in neus:
                            neu_mother = findAncestor(neu, False) #chargino
                            if mu_gmother.genPartIdxMother == neu_mother.genPartIdxMother:
                                ch_moms += 1
                                deta_mu = abs(mu.eta) - abs(mu_gmother.eta)
                                self.h_mupt.Fill(mu.pt)
                                self.h_mueta.Fill(mu.eta)
                                self.h_mix_chmu_deta.Fill(deta_mu)
                                self.h_nmupt.Fill(nmu.pt)
                                self.h_nmueta.Fill(nmu.eta)
                                self.h_neupt.Fill(neu.pt)
                                self.h_neueta.Fill(neu.eta)
                                deta_neu = abs(neu.eta) - abs(neu_mother.eta)
                                self.h_mix_chneu_deta.Fill(deta_neu)
        #to calculate delta phi, delta eta, we need two charginos, or else there's no point
        if len(locatedSpecificCharginos) == 2:
            for particle in locatedSpecificCharginos:
                self.h_chpt.Fill(particle.pt)
                self.h_cheta.Fill(particle.eta)
                self.h_chphi.Fill(particle.phi)
            part1 = locatedSpecificCharginos[0]
            part2 = locatedSpecificCharginos[1]
            deta = abs(part1.eta) - abs(part2.eta)
            dphi = part1.phi - part2.phi
            self.h_chdeta.Fill(deta)
            self.h_chdphi.Fill(dphi)
        return True

    def endJob(self):
        #CANVAS
        self.c = ROOT.TCanvas("x13c", "The Canvas", 900, 660)
        self.addObject(self.c)
        self.c.cd()
        # GRAPHS
        # GENERAL

        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # 13 - MUON
        self.h_mupt.GetXaxis().SetTitle("pt (GeV)")
        self.h_mupt.GetYaxis().SetTitle("Counts")
        self.h_mueta.GetXaxis().SetTitle("eta")
        self.h_mueta.GetYaxis().SetTitle("Counts")
        # 14 - MUON NETRINO
        self.h_nmupt.GetXaxis().SetTitle("pt (GeV)")
        self.h_nmupt.GetYaxis().SetTitle("Counts")
        self.h_nmueta.GetXaxis().SetTitle("eta")
        self.h_nmueta.GetYaxis().SetTitle("Counts")
        # 1000022 - NEUTRALINO
        self.h_neupt.GetXaxis().SetTitle("pt (GeV)")
        self.h_neupt.GetYaxis().SetTitle("Counts")
        self.h_neuta.GetXaxis().SetTitle("eta")
        self.h_neuta.GetYaxis().SetTitle("Counts")
        # 1000024 - CHARGINOS
        self.h_chpt.GetXaxis().SetTitle("pt (GeV)")
        self.h_chpt.GetYaxis().SetTitle("Counts")
        self.h_cheta.GetXaxis().SetTitle("eta")
        self.h_cheta.GetYaxis().SetTitle("Counts")
        self.h_chphi.GetXaxis().SetTitle("phi (rad)")
        self.h_chphi.GetYaxis().SetTitle("Counts")
        self.h_chdphi.GetXaxis().SetTitle("delta phi (rad)")
        self.h_chdphi.GetYaxis().SetTitle("Counts")
        self.h_chdeta.GetXaxis().SetTitle("delta eta")
        self.h_chdeta.GetYaxis().SetTitle("Counts")
        # MIXTURES
        self.h_mix_chmu_deta.GetXaxis().SetTitle("delta eta")
        self.h_mix_chmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chneu_deta.GetXaxis().SetTitle("delta eta")
        self.h_mix_chneu_deta.GetYaxis().SetTitle("Counts")
        #PRINTING
        histList = [self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chdeta, self.h_chdphi, self.h_mupt, self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta, self.mix_chmu_deta, self.mix_chneu_deta]
        for hist in histList:
             hist.Draw()
             save = "x13/h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
        Module.endJob(self)

preselection = ""
files = ["{}/src/DisplacedCharginos_Dec8_2DispMuonsSkim/SMS_TChiWW_Disp_M150to200_DM5to20_ctau10.root".format(os.environ['CMSSW_BASE'])] ##new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x13.root", histDirName="plots")
p.run()
