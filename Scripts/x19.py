#!/usr/bin/env python
#x19 - ONLY muon decay channel, solid structure of x14: CUT: muon eta <= 3
#notable scripts: x18 muon pt 15, x17 muon pt 10, x16 muon pt 5, x14 no cut
ver = "19"
import os, sys
if 'CMSSW_VERSION' not in os.environ:
    print("Run 'cmsenv' on ../src/")
    quit(1)
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import ROOT
from ROOT import gStyle, gROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
#define values here to print in endJob function call
val1 = 0

class ExampleDisplacedAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        print("Creating ROOT objects...")
        # GENERAL
        self.h_metptall = ROOT.TH1F('metptall', '\\mbox{Missing Transverse Momentum, all events (MET)}', 100, 0, 400)
        self.h_metpt = ROOT.TH1F('metpt', '\\mbox{Missing Transverse Momentum, muon channel (MET)}', 100, 0, 400)
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', '\\mbox{Muon Transverse Momentum } p_t', 100, 0, 50)
        self.h_mueta = ROOT.TH1F('mueta', '\\mbox{Muon Pseudorapidity } \\eta', 100, -6, 6)
        # 14 - MUON NETRINO
        self.h_nmupt = ROOT.TH1F('nmupt', '\\mbox{Muon Neutrino Transverse Momentum } p_t', 100, 0, 50)
        self.h_nmueta = ROOT.TH1F('nmueta', '\\mbox{Muon Neutrino Pseudorapidity } \\eta', 100, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', '\\mbox{Neutralino Transverse Momentum } p_t', 100, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', '\\mbox{Neutralino Pseudorapidity } \\eta', 100, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', '\\mbox{Muon Channel Transverse Momentum } p_t', 100, 0, 1000)
        self.h_cheta = ROOT.TH1F('cheta', '\\mbox{Muon Channel Chargino Pseudorapidity } \\eta', 100, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', '\\mbox{Muon Channel Chargino Phi } \\phi', 50, -3.1415927, 3.1415927)
        self.h_chdeta = ROOT.TH1F('chdeta', '\\mbox{Muon Channel Chargino Delta Eta } \\Delta \\eta', 100, 0, 5)
        self.h_chdphi = ROOT.TH1F('chdphi', '\\mbox{Muon Channel Chargino Delta Phi } \\Delta \\phi', 100, 0, 3.1415927)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', '\\mbox{Chargino-Muon Delta Eta } \\Delta \\eta', 100, 0, 2)
        self.h_mix_chnmu_deta = ROOT.TH1F('mix_chnmu_deta', '\\mbox{Chargino-Muon Neutrino Delta Eta } \\Delta \\eta', 100, 0, 3.5)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', '\\mbox{Chargino-Neutralino Delta Eta } \\Delta \\eta', 100, 0, 0.6)
        # ADD HISTOGRAMS
        self.addObject(self.h_metptall)
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
        self.addObject(self.h_mix_chnmu_deta)
        self.addObject(self.h_mix_chneu_deta)
        print("Initializing analysis... beginJob function ended.")

    def analyze(self, event):
        #Variables, Arrays
        genParts = Collection(event, "GenPart")
        locateFinalStates = [13, 14, 1000022]
        leptonic = [13, 14]
        chs_all = []
        chs = []
        mus = []
        nmus = []
        neus = []
        #Function definitions
        def findAncestor(particle, log): #aims to find a mother particle. if it doesnt, it returns the original
            original = particle
            resonance = original
            while resonance.pdgId == original.pdgId:
                testResonance = genParts[resonance.genPartIdxMother] if resonance.genPartIdxMother in range(len(genParts)) else None
                try:
                    testResonance.pdgId
                except:
                    if log == True:
                        print("Warning 5: Exception. Returning original")
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
        def particleInList(particle, list): #checks if a particle is in a list
            ids = []
            for item in list:
                ids.append(item.genPartIdxMother)
            if particle.genPartIdxMother in ids:
                return True
            else:
                return False
        def getStatusFlag(part, pos): #returns 0 or 1 of a bitwise, in position pos
            flag = str(part.statusFlags>>pos)
            return int(flag[:1])

        #scan all particles in the event by final state
        for particle in genParts:
            if abs(particle.pdgId) in locateFinalStates: #identify final state particle
                mother = findAncestor(particle, False) #mother must now be W or ch. instill check.
                #case for mu and nmu aka leptonic:
                if abs(particle.pdgId) in leptonic:
                    if abs(mother.pdgId) == 24: #must be W
                        gmother = findAncestor(mother, False) #chargino or irrelevant W
                        if abs(gmother.pdgId) == 1000024: #must be ch
                        addUniqueParticle(gmother, chs)
                            if abs(particle.pdgId) == 13 and getStatusFlag(particle, 13) == 1:
                                addUniqueParticle(particle, mus)
                            if abs(particle.pdgId) == 14 and getStatusFlag(particle, 13) == 1:
                                addUniqueParticle(particle, nmus)
                #case for neu
                if abs(particle.pdgId) == 1000022 and abs(mother.pdgId) == 1000024 and particle.status == 1:
                    addUniqueParticle(mother, chs_all) #since a neu is always produced, any ch added here is from any W decay channel
                    addUniqueParticle(particle, neus)
        if len(mus) > 2 or len(nmus) > 2:
            print("Warning 8: length of mus, nmus: " + str(len(mus)) + ", " + str(len(nmus)))
        #x12 algorithm for faster handling & incoporates same parent generation for mu, nmu, neu. incoprorate cuts here
        for mu in mus:
            mu_mother = findAncestor(mu, False) #W
            for nmu in nmus:
                nmu_mother = findAncestor(nmu, False) #W
                if nmu_mother.genPartIdxMother == mu_mother.genPartIdxMother:
                    mu_gmother = findAncestor(mu_mother, False) #ch
                    nmu_gmother = findAncestor(nmu_mother, False) #ch
                    if mu_gmother.genPartIdxMother == nmu_gmother.genPartIdxMother: #chargino must be the same
                        for neu in neus:
                            neu_mother = findAncestor(neu, False) #chargino
                            if mu_gmother.genPartIdxMother == neu_mother.genPartIdxMother:
                                eventMET_muonchannel = getattr(event, "MET_pt")
                                self.h_metpt.Fill(eventMET_muonchannel)
                                deta_mu = abs(mu.eta) - abs(mu_gmother.eta)
                                self.h_mupt.Fill(mu.pt)
                                self.h_mueta.Fill(mu.eta)
                                self.h_mix_chmu_deta.Fill(deta_mu)
                                deta_nmu = abs(nmu.eta) - abs(mu_gmother.eta)
                                self.h_nmupt.Fill(nmu.pt)
                                self.h_nmueta.Fill(nmu.eta)
                                self.h_mix_chnmu_deta.Fill(deta_nmu)
                                self.h_neupt.Fill(neu.pt)
                                self.h_neueta.Fill(neu.eta)
                                deta_neu = abs(neu.eta) - abs(neu_mother.eta)
                                self.h_mix_chneu_deta.Fill(deta_neu)
        #to calculate delta phi, delta eta, we need two charginos, or else there's no point
        for particle in chs:
            self.h_chpt.Fill(particle.pt)
            self.h_cheta.Fill(particle.eta)
            self.h_chphi.Fill(particle.phi)
        if len(chs) == 2:
            part1 = chs[0]
            part2 = chs[1]
            deta = abs(part1.eta) - abs(part2.eta)
            dphi = part1.phi - part2.phi
            self.h_chdeta.Fill(deta)
            self.h_chdphi.Fill(dphi)
        eventMET = getattr(event, "MET_pt")
        self.h_metptall.Fill(eventMET)
        if len(nmus) > 0:
            val1 = nmus[0].mass
        #analysis ends here: return True
        return True

    def endJob(self):
        print("Initializing endJob function...")
        #CANVAS
        self.c = ROOT.TCanvas("canv", "The Canvas", 1000, 700)
        self.addObject(self.c)
        self.c.cd()
        # GRAPHS
        # GENERAL
        gStyle.SetOptStat(1110) #see https://root.cern.ch/doc/master/classTStyle.html#a0ae6f6044b6d7a32756d7e98bb210d6c
        gStyle.SetStatColor(18)
        self.h_metptall.GetXaxis().SetTitle("MET (GeV)")
        self.h_metptall.GetYaxis().SetTitle("Counts")
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # 13 - MUON
        self.h_mupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_mupt.GetYaxis().SetTitle("Counts")
        self.h_mueta.GetXaxis().SetTitle("\\eta")
        self.h_mueta.GetYaxis().SetTitle("Counts")
        # 14 - MUON NETRINO
        self.h_nmupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_nmupt.GetYaxis().SetTitle("Counts")
        self.h_nmueta.GetXaxis().SetTitle("\\eta")
        self.h_nmueta.GetYaxis().SetTitle("Counts")
        # 1000022 - NEUTRALINO
        self.h_neupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_neupt.GetYaxis().SetTitle("Counts")
        self.h_neueta.GetXaxis().SetTitle("\\eta")
        self.h_neueta.GetYaxis().SetTitle("Counts")
        # 1000024 - CHARGINOS
        self.h_chpt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_chpt.GetYaxis().SetTitle("Counts")
        self.h_cheta.GetXaxis().SetTitle("\\eta")
        self.h_cheta.GetYaxis().SetTitle("Counts")
        self.h_chphi.GetXaxis().SetTitle("\\phi$ \\mbox{ (rad)}")
        self.h_chphi.GetYaxis().SetTitle("Counts")
        self.h_chdphi.GetXaxis().SetTitle("\\Delta \\phi \\mbox{ (rad)}")
        self.h_chdphi.GetYaxis().SetTitle("Counts")
        self.h_chdeta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_chdeta.GetYaxis().SetTitle("Counts")
        # MIXTURES
        self.h_mix_chmu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chnmu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chnmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chneu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chneu_deta.GetYaxis().SetTitle("Counts")
        #PRINTING
        print("Printing Histograms...")
        print("Muon Neutrino mass: " + str(val1))
        histList = [self.h_metptall, self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chdeta, self.h_chdphi, self.h_mupt, self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta, self.mix_chmu_deta, self.mix_chnmu_deta, self.mix_chneu_deta]
        for hist in histList:
             hist.SetLineColor(38)
             hist.GetXaxis().CenterTitle(True)
             hist.GetYaxis().CenterTitle(True)
             hist.Draw()
             save = "x" + ver + "/" + "x" + ver + "h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
             self.c.Update()
        Module.endJob(self)

preselection = ""
files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_190_10.root".format(os.environ['CMSSW_BASE'])] ##new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x" + ver + ".root", histDirName="plots")
p.run()
