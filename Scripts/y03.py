#!/usr/bin/env python
ver = "03"
#no cuts
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
d1 = 0.75
d2 = 1
d3 = 1.25
d4 = 1.5
d5 = 1.75
class ExampleDisplacedAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        print("Creating ROOT objects...")
        # GENERAL
        self.h_metptall = ROOT.TH1F('metptall', '\\mbox{Missing Energy Transverse, all events (MET)}', 120, 0, 400)
        self.h_metpt = ROOT.TH1F('metpt', '\\mbox{Missing Energy Transverse, muon channel (MET)}', 120, 0, 400)
        # PARTICLE SPECIFIC - SEE https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf
        # JETS
        self.h_jetht1 = ROOT.TH1F('jetht1', '\\mbox{Jet HT (for distance } d_1 \\mbox{ cut)}', 120, 0, 3500) #component
        self.h_jetht2 = ROOT.TH1F('jetht2', '\\mbox{Jet HT (for distance } d_2 \\mbox{ cut)}', 120, 0, 3500) #component
        self.h_jetht3 = ROOT.TH1F('jetht3', '\\mbox{Jet HT (for distance } d_3 \\mbox{ cut)}', 120, 0, 3500) #component
        self.h_jetht4 = ROOT.TH1F('jetht4', '\\mbox{Jet HT (for distance } d_4 \\mbox{ cut)}', 120, 0, 3500) #component
        self.h_jetht5 = ROOT.TH1F('jetht5', '\\mbox{Jet HT (for distance } d_5 \\mbox{ cut)}', 120, 0, 3500) #component
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', '\\mbox{Muon Transverse Momentum } p_t', 120, 0, 25)
        self.h_mueta = ROOT.TH1F('mueta', '\\mbox{Muon Pseudorapidity } \\eta', 120, -6, 6)
        self.h_mupvdistance1 = ROOT.TH1F('mupvdistance1', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance2 = ROOT.TH1F('mupvdistance2', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance3 = ROOT.TH1F('mupvdistance3', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance4 = ROOT.TH1F('mupvdistance4', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        self.h_mupvdistance5 = ROOT.TH1F('mupvdistance5', '\\mbox{Muon-PV Distance (Lab Frame) } l', 120, 0, 15)
        # 14 - MUON NEUTRINO
        self.h_nmupt = ROOT.TH1F('nmupt', '\\mbox{Muon Neutrino Transverse Momentum } p_t', 120, 0, 25)
        self.h_nmueta = ROOT.TH1F('nmueta', '\\mbox{Muon Neutrino Pseudorapidity } \\eta', 120, -6, 6)
        # 1000022 - NEUTRALINO
        self.h_neupt = ROOT.TH1F('neupt', '\\mbox{Neutralino Transverse Momentum } p_t', 120, 0, 1100)
        self.h_neueta = ROOT.TH1F('neueta', '\\mbox{Neutralino Pseudorapidity } \\eta', 120, -6, 6)
        # 1000024 - CHARGINOS
        self.h_chpt = ROOT.TH1F('chpt', '\\mbox{Chargino Transverse Momentum, muon channel } p_t', 120, 0, 1100)
        self.h_cheta = ROOT.TH1F('cheta', '\\mbox{Chargino Pseudorapidity, muon channel } \\eta', 120, -6, 6)
        self.h_chphi = ROOT.TH1F('chphi', '\\mbox{Chargino Phi, muon channel } \\phi', 40, -3.1415927, 3.1415927)
        self.h_chdeta = ROOT.TH1F('chdeta', '\\mbox{Chargino Delta Eta, muon channel } \\Delta \\eta', 120, 0, 2.5)
        self.h_chdphi = ROOT.TH1F('chdphi', '\\mbox{Chargino Delta Phi, muon channel } \\Delta \\phi', 120, 0, 3.1415927)
        self.h_chlenl = ROOT.TH1F('chlenl', '\\mbox{Chargino Decay Length (Lab Frame), muon channel } L', 120, 0, 5)
        self.h_chlenr = ROOT.TH1F('chlenr', '\\mbox{Chargino Decay Length (Rest Frame), muon channel } L_0', 120, 0, 6)
        self.h_chbeta = ROOT.TH1F('chbeta', '\\mbox{Chargino Beta, muon channel } \\beta', 120, 0, 1)
        self.h_chgamma = ROOT.TH1F('chgamma', '\\mbox{Chargino Gamma, muon channel } \\gamma', 120, 1, 35)
        self.h_chnrgl = ROOT.TH1F('chnrgl', '\\mbox{Chargino Energy, muon channel } E', 120, 0, 1400)
        # MIXTURES
        self.h_mix_chmu_deta = ROOT.TH1F('mix_chmu_deta', '\\mbox{Chargino-Muon Delta Eta } \\Delta \\eta', 120, 0, 2.5)
        self.h_mix_chnmu_deta = ROOT.TH1F('mix_chnmu_deta', '\\mbox{Chargino-Muon Neutrino Delta Eta } \\Delta \\eta', 120, 0, 2.5)
        self.h_mix_chneu_deta = ROOT.TH1F('mix_chneu_deta', '\\mbox{Chargino-Neutralino Delta Eta } \\Delta \\eta', 120, 0, 0.6)
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
            if genParts[Muon.genPartIdx] in mus and Muon.pt >= 4 and Muon.eta <= 2.5 and METpt >= 100 and Muon.dz <= 4:
                Mus.append(Muon)
                mus2.append(genParts[Muon.genPartIdx])
        #x12 algorithm for faster handling & incoporates same parent generation for mu, nmu, neu. incoprorate cuts here
        if len(mus) >= 1:
            dists = []
            self.h_metpt.Fill(METpt)
            for mu in mus:
                #enter cuts here
                #if mu.pt >= 4 and mu.eta <= 2.5 and len(mus) == 2 and METpt >= 130:
                mu_mother = findAncestor(mu) #W
                for nmu in nmus:
                    nmu_mother = findAncestor(nmu) #W
                    if nmu_mother.genPartIdxMother == mu_mother.genPartIdxMother:
                        mu_gmother = findAncestor(mu_mother) #ch
                        nmu_gmother = findAncestor(nmu_mother) #ch
                        if mu_gmother.genPartIdxMother == nmu_gmother.genPartIdxMother: #chargino must be the same
                            for neu in neus:
                                neu_mother = findAncestor(neu) #chargino
                                ch = mu_gmother
                                w = mu_mother
                                #tail = ROOT.TVector3(ch.vtx_x, ch.vtx_y, ch.vtx_z)
                                tail = ROOT.TVector3(PVx, PVy, PVz)
                                head = ROOT.TVector3(mu.vtx_x, mu.vtx_y, mu.vtx_z)
                                d = (head - tail).Mag()
                                dists.append(d)
                                if mu_gmother.genPartIdxMother == neu_mother.genPartIdxMother: #end point
                                    eventRecorded = True
                                    events_recorded += 1
                                    deta_mu = abs(mu.eta) - abs(ch.eta)
                                    self.h_mupt.Fill(mu.pt)
                                    self.h_mueta.Fill(mu.eta)
                                    self.h_mix_chmu_deta.Fill(deta_mu)
                                    deta_nmu = abs(nmu.eta) - abs(ch.eta)
                                    self.h_nmupt.Fill(nmu.pt)
                                    self.h_nmueta.Fill(nmu.eta)
                                    self.h_mix_chnmu_deta.Fill(deta_nmu)
                                    self.h_neupt.Fill(neu.pt)
                                    self.h_neueta.Fill(neu.eta)
                                    deta_neu = abs(neu.eta) - abs(ch.eta)
                                    self.h_mix_chneu_deta.Fill(deta_neu)
                                    self.h_chpt.Fill(ch.pt)
                                    self.h_cheta.Fill(ch.eta)
                                    self.h_chphi.Fill(ch.phi)
                                    g = ch.p4().Gamma()
                                    b = ch.p4().Beta()
                                    self.h_chbeta.Fill(b)
                                    self.h_chgamma.Fill(g)
                                    self.h_chnrgl.Fill(ch.p4().E())
                                    if len(chs) == 2: #event with two muonic channels
                                        part1 = chs[0]
                                        part2 = chs[1]
                                        deta = abs(part1.eta) - abs(part2.eta)
                                        dphi = part1.phi - part2.phi
                                        self.h_chdeta.Fill(deta)
                                        self.h_chdphi.Fill(dphi)
                                    #chx4 = ROOT.TLorentzVector(L, -L.Mag()/b)
                                    #boost = chp4.BoostVector()
                                    #chx4.Boost(-boost)
                                    #lr = math.sqrt(chx4.X()*chx4.X() + chx4.Y()*chx4.Y() + chx4.Z()*chx4.Z())
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
        if eventRecorded == True:
            events_passed += 1
        #self.h_lheht.Fill(lheht)
        for neu in neus:
            ch = findAncestor(neu)
            tail = ROOT.TVector3(ch.vtx_x, ch.vtx_y, ch.vtx_z)
            head = ROOT.TVector3(neu.vtx_x, neu.vtx_y, neu.vtx_z)
            L = head - tail
            chp4 = ch.p4()
            g = chp4.Gamma()
            b = chp4.Beta()
            self.h_chlenl.Fill(L.Mag())
            self.h_chlenr.Fill(L.Mag()/(b*g))
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
        #fit_mupvdistance = ROOT.TF1("fit_mupvdistance", "expo", 0, 10)
        #fit_mupvdistance.SetParNames("mupvconst", "mupvslope")
        #fit_mupvdistance.SetParameter("mupvconst",)
        self.chlenr.Fit(fit_chlenr)
        #self.mupvdistance1.Fit(fit_mupvdistance)
        #MORE HISTOGRAMS
        #PRINTING
        print("Number of muon channel events: " + str(events_recorded))
        print("Number of passed entries: " + str(events_passed))
        print("Number of events selected: " + str(events_selected))
        br = (events_passed)/(2.*events_all)
        print("Channel branching ratio: " + str(br))
        print("Printing Histograms...")
        histList_all = ([self.h_metptall, self.h_jetht1, self.h_jetht2, self.h_jetht3, self.h_jetht4, self.h_jetht5, self.h_metpt, self.h_chpt, self.h_cheta,
                         self.h_chphi, self.h_chlenl, self.h_chlenr, self.h_chbeta, self.h_chgamma, self.h_chnrgl, self.h_chdeta, self.h_chdphi, self.h_mupt,
                         self.h_mueta, self.mupvdistance1, self.mupvdistance2, self.mupvdistance3, self.mupvdistance4, self.mupvdistance5, self.nmupt,
                         self.nmueta, self.neupt, self.neueta, self.h_mix_chmu_deta, self.h_mix_chnmu_deta, self.h_mix_chneu_deta])
        histList = ([self.h_metptall, self.h_metpt, self.h_chpt, self.h_cheta,
                    self.h_chphi, self.h_chlenl, self.h_chlenr, self.h_chbeta, self.h_chgamma, self.h_chdeta, self.h_chdphi, self.h_mupt,
                    self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta, self.h_mix_chmu_deta, self.h_mix_chnmu_deta, self.h_mix_chneu_deta])
        XSECCH = 0.902569*1000
        L = 60
        scale = 1/events_all * XSECCH * L
        for hist in histList:
             hist.SetLineColor(38)
             hist.SetFillColor(38)
             hist.SetLineWidth(2)
             hist.GetXaxis().CenterTitle(True)
             hist.GetYaxis().CenterTitle(True)
             #hist.Scale(scale)
             hist.Draw()
             save = "y" + ver + "/" + "y" + ver + "_h_" + hist.GetName() + ".png"
             self.c.SaveAs(save)
             self.c.Update()
        #done here, remove stat box
        gStyle.SetOptStat(0);
        #DETA
        self.s_deta = ROOT.THStack("s_deta","\\mbox{Total Particle Delta Eta } \\Delta \\eta");
        self.addObject(self.s_deta)
        histList_deta = [self.h_chdeta, self.h_mix_chmu_deta, self.h_mix_chnmu_deta]#, self.h_mix_chneu_deta]
        self.h_chdeta.SetLineColor(2)
        self.h_chdeta.SetFillColor(2)
        self.h_mix_chmu_deta.SetLineColor(3)
        self.h_mix_chmu_deta.SetFillColor(3)
        self.h_mix_chnmu_deta.SetLineColor(4)
        self.h_mix_chnmu_deta.SetFillColor(4)
        self.h_mix_chneu_deta.SetLineColor(6)
        self.h_mix_chneu_deta.SetFillColor(6)
        for hist in histList_deta:
            self.s_deta.Add(hist)
        self.leg_deta = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_deta.SetMargin(0.15)
        self.leg_deta.AddEntry(self.h_chdeta, "#tilde{#chi}_{1}^{#pm} - #tilde{#chi}_{1}^{#pm}", "L")
        self.leg_deta.AddEntry(self.h_mix_chmu_deta, "#tilde{#chi}_{1}^{#pm} - #mu", "L")
        self.leg_deta.AddEntry(self.h_mix_chnmu_deta, "#tilde{#chi}_{1}^{#pm} - #nu", "L")
        #self.leg_deta.AddEntry(self.h_mix_chneu_deta, "#tilde{#chi}_{1}^{#pm}- #tilde{#chi}_{1}^{0}", "L")
        self.s_deta.Draw()
        self.leg_deta.Draw()
        self.s_deta.GetXaxis().SetTitle("\\Delta \\eta")
        self.s_deta.GetYaxis().SetTitle("Counts")
        self.s_deta.GetXaxis().CenterTitle(True)
        self.s_deta.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_deta.GetName() + ".png")
        self.c.Update()
        self.h_mix_chneu_deta.Draw()
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.h_mix_chneu_deta.GetName() + "_fancy.png")
        self.c.Update()
        #PT
        self.s_pt_sus = ROOT.THStack("s_pt_sus","\\tilde{\\chi}_1^\\pm, \\tilde{\\chi}_1^0 \\mbox{ Transverse Momentum } p_t");
        self.s_pt_sm = ROOT.THStack("s_pt_sm","\\mu, \\nu \\mbox{ Transverse Momentum } p_t");
        self.addObject(self.s_pt_sus)
        self.addObject(self.s_pt_sm)
        histList_pt_sus = [self.h_chpt, self.h_neupt]
        histList_pt_sm = [self.h_mupt, self.h_nmupt]
        self.h_chpt.SetLineColor(2)
        self.h_chpt.SetFillColor(2)
        self.h_mupt.SetLineColor(3)
        self.h_mupt.SetFillColor(3)
        self.h_nmupt.SetLineColor(4)
        self.h_nmupt.SetFillColor(4)
        self.h_neupt.SetLineColor(6)
        self.h_neupt.SetFillColor(6)
        self.s_pt_sus.Add(self.h_chpt)
        self.s_pt_sus.Add(self.h_neupt)
        self.s_pt_sm.Add(self.h_mupt)
        self.s_pt_sm.Add(self.h_nmupt)
        self.leg_pt_sus = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_pt_sus.SetMargin(0.15)
        self.leg_pt_sus.AddEntry(self.h_chpt, "#tilde{#chi}_{1}^{#pm}", "L" )
        self.leg_pt_sus.AddEntry(self.h_neupt, "#tilde{#chi}_{1}^{0}", "L")
        self.s_pt_sus.Draw()
        self.leg_pt_sus.Draw()
        self.s_pt_sus.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.s_pt_sus.GetYaxis().SetTitle("Counts")
        self.s_pt_sus.GetXaxis().CenterTitle(True)
        self.s_pt_sus.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_pt_sus.GetName() + ".png")
        self.c.Update()
        self.leg_pt_sm = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_pt_sm.SetMargin(0.15)
        self.leg_pt_sm.AddEntry(self.h_mupt, "#mu", "L")
        self.leg_pt_sm.AddEntry(self.h_nmupt, "#nu", "L")
        self.s_pt_sm.Draw()
        self.leg_pt_sm.Draw()
        self.s_pt_sm.GetXaxis().SetTitle("p_t \\mbox{ (GeV)}")
        self.s_pt_sm.GetYaxis().SetTitle("Counts")
        self.s_pt_sm.GetXaxis().CenterTitle(True)
        self.s_pt_sm.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_pt_sm.GetName() + ".png")
        self.c.Update()
        #MET
        self.s_met = ROOT.THStack("s_met","\\mbox{Missing Energy Transverse (MET) Momentum } p_t");
        self.addObject(self.s_met)
        histList_met = [self.h_metpt, self.h_metptall]
        self.h_metptall.SetLineColor(30)
        self.h_metptall.SetFillColor(30)
        self.h_metpt.SetLineColor(8)
        self.h_metpt.SetFillColor(8)
        for hist in histList_met:
            self.s_met.Add(hist)
        self.leg_met = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_met.SetMargin(0.15)
        self.leg_met.AddEntry(self.h_metptall, "All W^{#pm} channels", "L")
        self.leg_met.AddEntry(self.h_metpt, "W^{#pm}#rightarrow #mu#nu_{#mu}", "L")
        self.s_met.Draw()
        self.leg_met.Draw()
        self.s_met.GetXaxis().SetTitle("\\mbox{MET (GeV)}")
        self.s_met.GetYaxis().SetTitle("Counts")
        self.s_met.GetXaxis().CenterTitle(True)
        self.s_met.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_met.GetName() + ".png")
        self.c.Update()
        #ETA
        self.s_eta_sus = ROOT.THStack("s_eta_sus","\\tilde{\\chi}_1^\\pm, \\tilde{\\chi}_1^0 \\mbox{ Pseudorapidity } \\eta");
        self.s_eta_sm = ROOT.THStack("s_eta_sm","\\mu,\\nu \\mbox{ Pseudorapidity } \\eta");
        self.addObject(self.s_eta_sus)
        self.addObject(self.s_eta_sm)
        histList_eta_sus = [self.h_cheta, self.h_neueta]
        histList_eta_sm = [self.h_mueta, self.h_nmueta]
        self.h_cheta.SetLineColor(2)
        self.h_cheta.SetFillColor(2)
        self.h_mueta.SetLineColor(3)
        self.h_mueta.SetFillColor(3)
        self.h_nmueta.SetLineColor(4)
        self.h_nmueta.SetFillColor(4)
        self.h_neueta.SetLineColor(6)
        self.h_neueta.SetFillColor(6)
        self.s_eta_sus.Add(self.h_cheta)
        self.s_eta_sus.Add(self.h_neueta)
        self.s_eta_sm.Add(self.h_mueta)
        self.s_eta_sm.Add(self.h_nmueta)
        self.leg_eta_sus = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_eta_sus.SetMargin(0.15)
        self.leg_eta_sus.AddEntry(self.h_cheta, "#tilde{#chi}_{1}^{#pm}", "L" )
        self.leg_eta_sus.AddEntry(self.h_neueta, "#tilde{#chi}_{1}^{0}", "L")
        self.s_eta_sus.Draw()
        self.leg_eta_sus.Draw()
        self.s_eta_sus.GetXaxis().SetTitle("\\eta \\mbox{ (GeV)}")
        self.s_eta_sus.GetYaxis().SetTitle("Counts")
        self.s_eta_sus.GetXaxis().CenterTitle(True)
        self.s_eta_sus.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_eta_sus.GetName() + ".png")
        self.c.Update()
        self.leg_eta_sm = ROOT.TLegend(0.70,0.75,0.90,0.90)
        self.leg_eta_sm.SetMargin(0.15)
        self.leg_eta_sm.AddEntry(self.h_mueta, "#mu", "L")
        self.leg_eta_sm.AddEntry(self.h_nmueta, "#nu_{#mu}", "L")
        self.s_eta_sm.Draw()
        self.leg_eta_sm.Draw()
        self.s_eta_sm.GetXaxis().SetTitle("\\eta \\mbox{ (GeV)}")
        self.s_eta_sm.GetYaxis().SetTitle("Counts")
        self.s_eta_sm.GetXaxis().CenterTitle(True)
        self.s_eta_sm.GetYaxis().CenterTitle(True)
        self.c.SaveAs("y" + ver + "/" + "y" + ver + "_h_" + self.s_eta_sm.GetName() + ".png")
        self.c.Update()
        Module.endJob(self)

#preselection = "MET_pt >= 100 && Jet_pt >= 30"
preselection = ""
#files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_2.root".format(os.environ['CMSSW_BASE'])]
files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_10.root".format(os.environ['CMSSW_BASE'])] #new file!
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="y" + ver + ".root", histDirName="plots")
p.run()
