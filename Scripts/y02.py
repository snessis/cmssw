#!/usr/bin/env python
ver = "02"
#cuts: met>=100, >=1 muons, muonpt >= 4, muoneta <=2.5, muondz < 1, muondxy > 0.1, RECO!!!!!!!!
#ctau 10 here
#incoprorate PV
import os, sys, math
if 'CMSSW_VERSION' not in os.environ:
    print("Run 'cmsenv' on ../src/")
    quit(1)
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import ROOT
from ROOT import gStyle, gROOT
from pprint import pprint
ROOT.PyConfig.IgnoreCommandLineOptions = True
#define values here to print in endJob function call
events_recorded = 0
events_passed = 0
events_selected = 0
events_all = 556249
locateFinalStates = [13, 14, 1000022]
leptonic = [13, 14]
hadronic = [1,2,3,4,5,6,21]
d1 = 1
d2 = 1.5
d3 = 2
d4 = 2.5
d5 = 3
class ExampleDisplacedAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        print("Creating ROOT objects...")
        # GENERAL
        self.h_metptall = ROOT.TH1F('metptall', '\\mbox{Missing Energy Transverse, all events (MET)}', 100, 0, 400)
        self.h_metpt = ROOT.TH1F('metpt', '\\mbox{Missing Energy Transverse, muon channel (MET)}', 100, 0, 400)
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # JETS
        self.h_jetht1 = ROOT.TH1F('jetht1', '\\mbox{Jet HT (for distance } d_1 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht2 = ROOT.TH1F('jetht2', '\\mbox{Jet HT (for distance } d_2 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht3 = ROOT.TH1F('jetht3', '\\mbox{Jet HT (for distance } d_3 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht4 = ROOT.TH1F('jetht4', '\\mbox{Jet HT (for distance } d_4 \\mbox{ cut)}', 100, 0, 3500) #component
        self.h_jetht5 = ROOT.TH1F('jetht5', '\\mbox{Jet HT (for distance } d_5 \\mbox{ cut)}', 100, 0, 3500) #component
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', '\\mbox{Muon Transverse Momentum } p_t', 80, 0, 50)
        self.h_mueta = ROOT.TH1F('mueta', '\\mbox{Muon Pseudorapidity } \\eta', 80, -6, 6)
        self.h_mupvdistance1 = ROOT.TH1F('mupvdistance1', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance2 = ROOT.TH1F('mupvdistance2', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance3 = ROOT.TH1F('mupvdistance3', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance4 = ROOT.TH1F('mupvdistance4', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance5 = ROOT.TH1F('mupvdistance5', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        # 14 - MUON NEUTRINO
        self.h_nmupt = ROOT.TH1F('nmupt', '\\mbox{Muon Neutrino Transverse Momentum } p_t', 80, 0, 50)
        self.h_nmueta = ROOT.TH1F('nmueta', '\\mbox{Muon Neutrino Pseudorapidity } \\eta', 80, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', '\\mbox{Neutralino Transverse Momentum } p_t', 80, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', '\\mbox{Neutralino Pseudorapidity } \\eta', 80, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', '\\mbox{Chargino Transverse Momentum, muon channel } p_t', 80, 0, 1000)
        self.h_cheta = ROOT.TH1F('cheta', '\\mbox{Chargino Pseudorapidity, muon channel } \\eta', 80, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', '\\mbox{Chargino Phi, muon channel } \\phi', 40, -3.1415927, 3.1415927)
        self.h_chdeta = ROOT.TH1F('chdeta', '\\mbox{Chargino Delta Eta, muon channel } \\Delta \\eta', 80, 0, 5)
        self.h_chdphi = ROOT.TH1F('chdphi', '\\mbox{Chargino Delta Phi, muon channel } \\Delta \\phi', 80, 0, 3.1415927)
        self.h_chlenl = ROOT.TH1F('chlenl', '\\mbox{Chargino Decay Length (Lab Frame), muon channel } L', 80, 0, 5)
        self.h_chlenr = ROOT.TH1F('chlenr', '\\mbox{Chargino Decay Length (Rest Frame), muon channel } L_0', 120, 0, 6)
        self.h_chbeta = ROOT.TH1F('chbeta', '\\mbox{Chargino Beta, muon channel } \\beta', 80, 0, 1)
        self.h_chgamma = ROOT.TH1F('chgamma', '\\mbox{Chargino Gamma, muon channel } \\gamma', 80, 1, 35)
        self.h_chnrgl = ROOT.TH1F('chnrgl', '\\mbox{Chargino Energy, muon channel } E', 80, 0, 1400)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', '\\mbox{Chargino-Muon Delta Eta } \\Delta \\eta', 80, 0, 2)
        self.h_mix_chnmu_deta = ROOT.TH1F('mix_chnmu_deta', '\\mbox{Chargino-Muon Neutrino Delta Eta } \\Delta \\eta', 80, 0, 3.5)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', '\\mbox{Chargino-Neutralino Delta Eta } \\Delta \\eta', 80, 0, 0.6)
        # GRAPH CUSTOMIZATION
        gStyle.SetOptStat(1110) #see https://root.cern.ch/doc/master/classTStyle.html#a0ae6f6044b6d7a32756d7e98bb210d6c
        gStyle.SetStatColor(18)
        # GENERAL
        self.h_metptall.GetXaxis().SetTitle("MET (GeV)")
        self.h_metptall.GetYaxis().SetTitle("Counts")
        self.h_metpt.GetXaxis().SetTitle("MET (GeV)")
        self.h_metpt.GetYaxis().SetTitle("Counts")
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # JETS
        self.h_jetht1.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht1.GetYaxis().SetTitle("Counts")
        self.h_jetht2.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht2.GetYaxis().SetTitle("Counts")
        self.h_jetht3.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht3.GetYaxis().SetTitle("Counts")
        self.h_jetht4.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht4.GetYaxis().SetTitle("Counts")
        self.h_jetht5.GetXaxis().SetTitle("\\mbox{HT (GeV)}")
        self.h_jetht5.GetYaxis().SetTitle("Counts")
        # 13 - MUON
        self.h_mupt.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.h_mupt.GetYaxis().SetTitle("Counts")
        self.h_mueta.GetXaxis().SetTitle("\\eta")
        self.h_mueta.GetYaxis().SetTitle("Counts")
        self.h_mupvdistance1.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistance1.GetYaxis().SetTitle("Counts")
        self.h_mupvdistance2.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistance2.GetYaxis().SetTitle("Counts")
        self.h_mupvdistance3.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistance3.GetYaxis().SetTitle("Counts")
        self.h_mupvdistance4.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistance4.GetYaxis().SetTitle("Counts")
        self.h_mupvdistance5.GetXaxis().SetTitle("l (dm)")
        self.h_mupvdistance5.GetYaxis().SetTitle("Counts")
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
        self.h_chphi.GetXaxis().SetTitle("\\phi \\mbox{ (rad)}")
        self.h_chphi.GetYaxis().SetTitle("Counts")
        self.h_chdphi.GetXaxis().SetTitle("\\Delta \\phi \\mbox{ (rad)}")
        self.h_chdphi.GetYaxis().SetTitle("Counts")
        self.h_chdeta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_chdeta.GetYaxis().SetTitle("Counts")
        self.h_chlenl.GetXaxis().SetTitle("L \\mbox{ (cm)}")
        self.h_chlenl.GetYaxis().SetTitle("Counts")
        self.h_chlenr.GetXaxis().SetTitle("L \\mbox{ (cm)}")
        self.h_chlenr.GetYaxis().SetTitle("Counts")
        self.h_chbeta.GetXaxis().SetTitle("\\beta")
        self.h_chbeta.GetYaxis().SetTitle("Counts")
        self.h_chgamma.GetXaxis().SetTitle("\\gamma")
        self.h_chgamma.GetYaxis().SetTitle("Counts")
        self.h_chnrgl.GetXaxis().SetTitle("E \\mbox{ (GeV)}")
        self.h_chnrgl.GetYaxis().SetTitle("Counts")
        # MIXTURES
        self.h_mix_chmu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chnmu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chnmu_deta.GetYaxis().SetTitle("Counts")
        self.h_mix_chneu_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.h_mix_chneu_deta.GetYaxis().SetTitle("Counts")
        # ADD HISTOGRAMS
        self.addObject(self.h_metptall)
        self.addObject(self.h_metpt)
        self.addObject(self.h_jetht1)
        self.addObject(self.h_jetht2)
        self.addObject(self.h_jetht3)
        self.addObject(self.h_jetht4)
        self.addObject(self.h_jetht5)
        self.addObject(self.h_chpt)
        self.addObject(self.h_cheta)
        self.addObject(self.h_chphi)
        self.addObject(self.h_chdeta)
        self.addObject(self.h_chdphi)
        self.addObject(self.h_chlenl)
        self.addObject(self.h_chlenr)
        self.addObject(self.h_chbeta)
        self.addObject(self.h_chgamma)
        self.addObject(self.h_chnrgl)
        self.addObject(self.h_mupt)
        self.addObject(self.h_mueta)
        self.addObject(self.h_mupvdistance1)
        self.addObject(self.h_mupvdistance2)
        self.addObject(self.h_mupvdistance3)
        self.addObject(self.h_mupvdistance4)
        self.addObject(self.h_mupvdistance5)
        self.addObject(self.h_nmupt)
        self.addObject(self.h_nmueta)
        self.addObject(self.h_neupt)
        self.addObject(self.h_neueta)
        self.addObject(self.h_mix_chmu_deta)
        self.addObject(self.h_mix_chnmu_deta)
        self.addObject(self.h_mix_chneu_deta)
        print("beginJob function ended. Initializing analysis...")
        # TEMPORARY HISTOGRAMS
    def analyze(self, event):
        #Variables, Arrays
        genParts = Collection(event, "GenPart") #collection
        Jets = Collection(event, "Jet") #collection, given by NanoAODTools
        METpt = getattr(event, "MET_pt") #branch
        Muons = Collection(event, "Muon")
        PVx = getattr(event, "PV_x")
        PVy = getattr(event, "PV_y")
        PVz = getattr(event, "PV_z")
        #N = event
        chs_all = []
        chs = []
        mus = []
        mus2 = []
        Mus = []
        nmus = []
        neus = []
        jets = []
        global events_recorded
        global events_passed
        global events_selected
        eventRecorded = False
        #Function definitions
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
            ids = []
            for item in list:
                ids.append(item.genPartIdxMother)
            if particle.genPartIdxMother not in ids:
                list.append(particle)
        def getStatusFlag(part, pos): #returns 0 or 1 of a bitwise, in position pos
            flag = str(part.statusFlags>>pos)
            return int(flag[:1])
        #scan all particles in the event by final state
        events_selected += 1
        self.h_metptall.Fill(METpt)
        for particle in genParts:
            if abs(particle.pdgId) in locateFinalStates: #identify final state particle
                mother = findAncestor(particle) #mother must now be W or ch. instill check.
                #case for mu and nmu aka leptonic:
                if abs(particle.pdgId) in leptonic:
                    if abs(mother.pdgId) == 24: #must be W
                        gmother = findAncestor(mother) #chargino or irrelevant W
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
        if len(mus) == 0:
            return False
        for jet in Jets:
            if abs(jet.pt) >= 30:
                jets.append(jet)
        for Muon in Muons:
            if genParts[Muon.genPartIdx] in mus: # and Muon.pt >= 3.5 and Muon.eta <= 3 and METpt >= 100 and Muon.dz <= 2:
                Mus.append(Muon)
                mus2.append(genParts[Muon.genPartIdx])
                eventRecorded = True
                events_passed += 1
        print("gen muons: " + str(len(mus)) + ", reco muons: " + str(len(Mus)) + ", gen mus2: "+ str(len(mus2)))
        if len(Mus) == 0:
            return False
        dists = []
        for Mu in Mus:
            d = math.sqrt(math.pow(Mu.dxy, 2) + math.pow(Mu.dz, 2))
            dists.append(d)
            self.h_mupt.Fill(Mu.pt)
            self.h_mueta.Fill(Mu.eta)
            if d >= d1:
                self.h_mupvdistance1.Fill(d)
            if d >= d2:
                self.h_mupvdistance2.Fill(d)
            if d >= d3:
                self.h_mupvdistance3.Fill(d)
            if d >= d4:
                self.h_mupvdistance4.Fill(d)
            if d >= d5:
                self.h_mupvdistance5.Fill(d)
        if eventRecorded == True:
            self.h_metpt.Fill(METpt)
            events_recorded += 1
            sum = 0
            for jet in jets:
                sum += jet.pt
            d = 0
            for di in dists:
                if di >= d:
                    d = di
            if d >= d1:
                self.h_jetht1.Fill(sum)
            if d >= d2:
                self.h_jetht2.Fill(sum)
            if d >= d3:
                self.h_jetht3.Fill(sum)
            if d >= d4:
                self.h_jetht4.Fill(sum)
            if d >= d5:
                self.h_jetht5.Fill(sum)
        #analysis ends here: return True
        return True

    def endJob(self):
        print("Initializing endJob function...")
        #CANVAS SETUP
        self.c = ROOT.TCanvas("canv", "The Canvas", 1000, 700)
        self.addObject(self.c)
        self.c.cd()
        #FITTING
        fit_chlenr = ROOT.TF1("fit_chlenr", "expo", 0, 10)
        fit_chlenr.SetParNames("chdecayconst", "chdecayslope")
        fit_mupvdistance = ROOT.TF1("fit_mupvdistance", "expo", 0, 10)
        fit_mupvdistance.SetParNames("mupvconst", "mupvslope")
        #fit_mupvdistance.SetParameter("mupvconst",)
        #self.chlenr.Fit(fit_chlenr)
        #self.mupvdistance1.Fit(fit_mupvdistance)
        #PRINTING
        print("Number of muon channel events: " + str(events_recorded))
        print("Number of passed entries: " + str(events_passed))
        print("Number of events selected: " + str(events_selected))
        br = (events_recorded)/(2.*events_all)
        print("Channel branching ratio: " + str(br))
        print("Printing Histograms...")
        histList_all = ([self.h_metptall, self.h_jetht1, self.h_jetht2, self.h_jetht3, self.h_jetht4, self.h_jetht5, self.h_metpt, self.h_chpt, self.h_cheta,
                         self.h_chphi, self.h_chlenl, self.h_chlenr, self.h_chbeta, self.h_chgamma, self.h_chnrgl, self.h_chdeta, self.h_chdphi, self.h_mupt,
                         self.h_mueta, self.mupvdistance1, self.mupvdistance2, self.mupvdistance3, self.mupvdistance4, self.mupvdistance5, self.nmupt,
                         self.nmueta, self.neupt, self.neueta, self.mix_chmu_deta, self.mix_chnmu_deta, self.mix_chneu_deta])
        histList = []
        for hist in histList:
             hist.SetLineColor(38)
             hist.GetXaxis().CenterTitle(True)
             hist.GetYaxis().CenterTitle(True)
             hist.Draw()
             save = "y" + ver + "/" + "y" + ver + "_h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
             self.c.Update()
        Module.endJob(self)

preselection = "MET_pt >= 100 && Jet_pt >= 30"
#files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_2.root".format(os.environ['CMSSW_BASE'])]
files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_10.root".format(os.environ['CMSSW_BASE'])] #new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="y" + ver + ".root", histDirName="plots")
p.run()
