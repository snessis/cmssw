#!/usr/bin/env python
ver = "26_2"
#x26 - code beautification &
#assignment: HT thing
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
events_all = 0
N1 = 748300 #HT 100 to 200
N2 = 1248911 #HT 200 to 400
N3 = 411531 #HT 400 to 600
N4 = 1560343 #HT 600 to 800
N5 = 737750 #HT 800 to 1200
N6 = 775061 #HT 1200 to 2500
N7 = 429253 #HT 2500 to Inf
XSection = 1
Lum = 1
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
        self.h_jetht = ROOT.TH1F('jetht', '\\mbox{Jet } HT', 100, 0, 1500)
        # 13 - MUON
        self.h_mupt = ROOT.TH1F('mupt', '\\mbox{Muon Transverse Momentum } p_t', 80, 0, 50)
        self.h_mueta = ROOT.TH1F('mueta', '\\mbox{Muon Pseudorapidity } \\eta', 80, -6, 6)
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
        self.h_chlenr = ROOT.TH1F('chlenr', '\\mbox{Chargino Decay Length (Rest Frame), muon channel } L_0', 80, 0, 6)
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
        self.h_jetht.GetXaxis().SetTitle("E_t \\mbox{ (GeV)}")
        self.h_jetht.GetYaxis().SetTitle("Counts")
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
        genJets = Collection(event, "GenJet")
        METpt = getattr(event, "MET_pt") #branch
        #N = event
        locateFinalStates = [13, 14, 1000022]
        leptonic = [13, 14]
        chs_all = []
        chs = []
        mus = []
        nmus = []
        neus = []
        global events_recorded
        global events_all
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
        events_all += 1
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
        for jet in genJets:
            if abs(jet.pt) >= 25:
                self.h_jetht.Fill(jet.p4().E())
        #x12 algorithm for faster handling & incoporates same parent generation for mu, nmu, neu. incoprorate cuts here
        for mu in mus:
            #enter cuts here
            if mu.pt >= 4 and mu.eta <= 2.5 and len(mus) == 2 and METpt >= 130:
                mu_mother = findAncestor(mu) #W
                for nmu in nmus:
                    nmu_mother = findAncestor(nmu) #W
                    if nmu_mother.genPartIdxMother == mu_mother.genPartIdxMother:
                        mu_gmother = findAncestor(mu_mother) #ch
                        nmu_gmother = findAncestor(nmu_mother) #ch
                        if mu_gmother.genPartIdxMother == nmu_gmother.genPartIdxMother: #chargino must be the same
                            for neu in neus:
                                neu_mother = findAncestor(neu) #chargino
                                if mu_gmother.genPartIdxMother == neu_mother.genPartIdxMother: #end point
                                    ch = mu_gmother
                                    w = mu_mother
                                    events_recorded += 1
                                    self.h_metpt.Fill(METpt)
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
        print("Number of muon channel events: " + str(events_recorded))
        print("Number of events: " + str(events_all))
        br = (events_recorded)/(2.*events_all)
        print("Channel branching ratio: " + str(br))
        #CANVAS SETUP
        self.c = ROOT.TCanvas("canv", "The Canvas", 1000, 700)
        self.addObject(self.c)
        self.c.cd()
        #PRINTING
        print("Printing Histograms...")
        histList_all = ([self.h_metptall, self.h_jetht, self.h_metpt, self.h_chpt, self.h_cheta, self.h_chphi, self.h_chlenl, self.h_chlenr, self.h_chbeta,
                         self.h_chgamma, self.h_chnrgl, self.h_chdeta, self.h_chdphi, self.h_mupt, self.h_mueta, self.nmupt, self.nmueta, self.neupt, self.neueta,
                         self.mix_chmu_deta, self.mix_chnmu_deta, self.mix_chneu_deta])
        histList = [self.h_jetht]
        fit_chlenr = self.h_chlenr.Fit("expo") #exp(p0+p1*x)
        for hist in histList:
             hist.SetLineColor(38)
             hist.GetXaxis().CenterTitle(True)
             hist.GetYaxis().CenterTitle(True)
             hist.Draw()
             savepng = "x" + ver + "/" + "x" + ver + "_h_" + hist.GetName() + ".png"
             saveroot = "x" + ver + "/" + "x" + ver + "_h_" + hist.GetName() + ".root"
             self.c.SaveAs(savepng)
             self.c.SaveAs(saveroot)
             self.c.Update()
             hist.Write()
        Module.endJob(self)

preselection = "GenJet_pt >= 25"
#files = ["{}/src/DisplacedCharginos_May4_unskimmed/SMS_TChiWW_Disp_200_195_2.root".format(os.environ['CMSSW_BASE'])]
files = (["{}/src/displacedSOS_mainbkg_260422_nanoV7/WJetsToLNu_HT200to400.root".format(os.environ['CMSSW_BASE'])])
p = PostProcessor(".", files, cut=preselection, branchsel=None, modules=[ExampleDisplacedAnalysis()], noOut=True, histFileName="x" + ver + ".root", histDirName="plots")
p.run()
