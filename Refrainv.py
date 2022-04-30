##Refrapy - Seismic Refraction Data Analysis
##Refrainv - Data inversion
##Author: Victor Guedes, MSc
##E-mail: vjs279@hotmail.com

from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
from matplotlib.colors import is_color_like
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Toplevel, Frame, Button, Label, filedialog, messagebox, PhotoImage, simpledialog, Entry
from os import path, makedirs, getcwd
from obspy import read
from obspy.signal.filter import lowpass, highpass
from scipy.signal import resample
from scipy.interpolate import interp1d,griddata
from numpy import array, where, polyfit, linspace, meshgrid, column_stack, c_, savetxt, shape,reshape,concatenate, hstack, linalg, mean, sqrt, zeros, arange, linspace, square, sort, unique
from numpy import all as np_all
from Pmw import initialise, Balloon
import pygimli as pg
from pygimli.physics import TravelTimeManager

class Refrainv(Tk):
    
    def __init__(self):
        
        super().__init__()
        self.geometry("1600x900")
        self.title('Refrapy - Refrainv v2.0.0')
        self.configure(bg = "#F0F0F0")
        self.resizable(0,0)
        self.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

        frame_toolbar = Frame(self)
        frame_toolbar.grid(row=0,column=0,sticky="EW")
        
        photo = PhotoImage(file="%s/images/ico_refrapy.gif"%getcwd())
        labelPhoto = Label(frame_toolbar, image = photo, width = 151)
        labelPhoto.image = photo
        labelPhoto.grid(row=0, column =0, sticky="W")
        self.statusLabel = Label(frame_toolbar, text = "Create or load a project to start", font=("Arial", 11))
        self.statusLabel.grid(row = 0, column = 18, sticky = "W")

        initialise(self)

        self.ico_newProject = PhotoImage(file="%s/images/ico_newProject.gif"%getcwd())
        self.ico_loadProject = PhotoImage(file="%s/images/ico_loadProject.gif"%getcwd())
        self.ico_openPick = PhotoImage(file="%s/images/ico_loadPicks.gif"%getcwd())
        self.ico_invTimeterms = PhotoImage(file="%s/images/vm.gif"%getcwd())
        self.ico_invTomo = PhotoImage(file="%s/images/tomogram.gif"%getcwd())
        self.ico_layerMode = PhotoImage(file="%s/images/camadas.gif"%getcwd())
        self.ico_clearLayers = PhotoImage(file="%s/images/limpar.gif"%getcwd())
        self.ico_layer1 = PhotoImage(file="%s/images/layer1.gif"%getcwd())
        self.ico_layer2 = PhotoImage(file="%s/images/layer2.gif"%getcwd())
        self.ico_layer3 = PhotoImage(file="%s/images/layer3.gif"%getcwd())
        self.ico_reset = PhotoImage(file="%s/images/fechar.gif"%getcwd())
        self.ico_plotOptions = PhotoImage(file="%s/images/ico_plotOptions.gif"%getcwd())
        self.ico_save = PhotoImage(file="%s/images/salvar.gif"%getcwd())
        self.ico_fit = PhotoImage(file="%s/images/ico_fit.gif"%getcwd())
        self.ico_invOptions = PhotoImage(file="%s/images/opt.gif"%getcwd())
        self.ico_velmesh = PhotoImage(file="%s/images/ico_velmesh.gif"%getcwd())
        self.ico_3d = PhotoImage(file="%s/images/ico_3d.gif"%getcwd())

        bt = Button(frame_toolbar,image = self.ico_newProject,command = self.createProject,width=25)
        bt.grid(row = 0, column = 1, sticky="W")
        bl = Balloon(self)
        bl.bind(bt,"Create new project path")
        
        bt = Button(frame_toolbar,image = self.ico_loadProject,command = self.loadProject,width=25)
        bt.grid(row = 0, column = 2, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Load project path")
        
        bt = Button(frame_toolbar, image = self.ico_openPick,command = self.loadPick)
        bt.grid(row = 0, column = 3, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Load pick file")

        bt = Button(frame_toolbar, image = self.ico_layerMode,command = self.layersInterpretation)
        bt.grid(row = 0, column = 4, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Enable/disable layer assignmet mode (time-terms inversion)")

        bt = Button(frame_toolbar, image = self.ico_layer1,command = self.assignLayer1)
        bt.grid(row = 0, column = 5, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Assign layer 1 (direct wave)")

        bt = Button(frame_toolbar, image = self.ico_layer2,command = self.assignLayer2)
        bt.grid(row = 0, column = 6, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Assign layer 2 (refracted wave)")

        bt = Button(frame_toolbar, image = self.ico_layer3,command = self.assignLayer3)
        bt.grid(row = 0, column = 7, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Assign layer 3 (refracted wave)")

        bt = Button(frame_toolbar, image = self.ico_clearLayers,command = self.clearLayerAssignment)
        bt.grid(row = 0, column = 8, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Clear layer assignment")

        bt = Button(frame_toolbar, image = self.ico_invTimeterms,command = self.runTimeTerms)
        bt.grid(row = 0, column = 9, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Run time-terms inversion")

        bt = Button(frame_toolbar, image = self.ico_invTomo,command = self.runTomography)
        bt.grid(row = 0, column = 10, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Run tomography inversion")

        bt = Button(frame_toolbar, image = self.ico_fit,command = self.showFit)
        bt.grid(row = 0, column = 11, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Show model response (fit)")

        bt = Button(frame_toolbar, image = self.ico_velmesh,command = self.showPgResult)
        bt.grid(row = 0, column = 12, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Show tomography velocity model with mesh")

        bt = Button(frame_toolbar, image = self.ico_3d,command = self.build3d)
        bt.grid(row = 0, column = 13, sticky="W")
        b = Balloon(self)
        b.bind(bt,"3D view of velocity model")

        bt = Button(frame_toolbar, image = self.ico_save,command = self.saveResults)
        bt.grid(row = 0, column = 14, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Save results")

        bt = Button(frame_toolbar, image = self.ico_invOptions,command = self.loadPick)
        bt.grid(row = 0, column = 15, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Inversion options")

        bt = Button(frame_toolbar, image = self.ico_plotOptions,command = self.plotOptions)
        bt.grid(row = 0, column = 16, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Plot options")

        bt = Button(frame_toolbar, image = self.ico_reset,command = self.loadPick)
        bt.grid(row = 0, column = 17, sticky="W")
        b = Balloon(self)
        b.bind(bt,"Reset all")

        self.protocol("WM_DELETE_WINDOW", self.kill)
        self.initiateVariables()

    def initiateVariables(self):

        self.projReady = False
        self.xdata = []
        self.tdata = []
        self.sources = []
        self.dataArts = []
        self.data_sourcesArts = []
        self.data_pg = False
        self.tomoPlot = False
        self.timetermsPlot = False
        self.timetermsInv = False
        self.tomoMesh = False
        self.showRayPath = False
        self.rayPathColor = 'k'
        self.colormap = "jet_r"
        self.cmPlot = None
        self.coords_3d = []
        self.layerInterpretationMode = False
        self.layer2interpretate = 1
        self.layer1, self.layer2, self.layer3 = [],[],[]
    
    def kill(self):

        out = messagebox.askyesno("Refrainv", "Do you want to close the software?")

        if out: self.destroy(); self.quit()

    def assignLayer1(self):

        if self.layerInterpretationMode:
            
            self.layer2interpretate = 1    
            self.statusLabel.configure(text = 'Layer %d interpratation enabled!'%self.layer2interpretate)

    def assignLayer2(self):

        if self.layerInterpretationMode:
            
            self.layer2interpretate = 2 
            self.statusLabel.configure(text = 'Layer %d interpratation enabled!'%self.layer2interpretate)

    def assignLayer3(self):

        if self.layerInterpretationMode:
            
            self.layer2interpretate = 3   
            self.statusLabel.configure(text = 'Layer %d interpratation enabled!'%self.layer2interpretate)

    def clearLayerAssignment(self):

        if messagebox.askyesno("Refrainv", "Clear layer interpretation?"):
                            
            del self.layer1[:]
            del self.layer2[:]
            del self.layer3[:]
            
            for i in range(len(self.sources)):
                
                for b in self.dataArts[i][self.sources[i]]:
                    
                    b.set_color("white")
                    b.set_edgecolor("k")

            self.fig_data.canvas.draw()
            messagebox.showinfo(title="Refrapick", message="Layer assignment was cleared!")
        
    def createPanels(self):

        self.frame_plots = Frame(self, bg = "white")
        self.frame_plots.grid(row = 1, column = 0, sticky = "NSWE")

        self.frame_data = Frame(self.frame_plots)
        self.frame_data.grid(row = 0, column = 0, sticky = "W", rowspan = 2)
        self.fig_data = plt.figure(figsize = (6,8.1))
        canvas_data = FigureCanvasTkAgg(self.fig_data, self.frame_data)
        canvas_data.draw()
        toolbar_data = NavigationToolbar2Tk(canvas_data, self.frame_data)
        toolbar_data.update()
        canvas_data._tkcanvas.pack()
        self.ax_data = self.fig_data.add_subplot(111)
        self.fig_data.patch.set_facecolor('#F0F0F0')
        self.ax_data.set_title("Observed data")
        self.ax_data.set_xlabel("POSITION [m]")
        self.ax_data.set_ylabel("TIME [s]")
        self.ax_data.grid(lw = .5, alpha = .5)
        self.ax_data.spines['right'].set_visible(False)
        self.ax_data.spines['top'].set_visible(False)
        self.ax_data.yaxis.set_ticks_position('left')
        self.ax_data.xaxis.set_ticks_position('bottom')
        
        
        self.frame_timeterms = Frame(self.frame_plots)
        self.frame_timeterms.grid(row = 0, column = 1, sticky = "NSWE")
        self.fig_timeterms = plt.figure(figsize = (9.5,3.7))
        canvas_timeterms = FigureCanvasTkAgg(self.fig_timeterms, self.frame_timeterms)
        canvas_timeterms.draw()
        toolbar_timeterms = NavigationToolbar2Tk(canvas_timeterms, self.frame_timeterms)
        toolbar_timeterms.update()
        canvas_timeterms._tkcanvas.pack()
        self.ax_timeterms = self.fig_timeterms.add_subplot(111)
        self.fig_timeterms.patch.set_facecolor('#F0F0F0')
        self.ax_timeterms.set_title("Time-terms velocity model")
        self.ax_timeterms.set_xlabel("POSITION [m]")
        self.ax_timeterms.set_ylabel("DEPTH [m]")
        self.ax_timeterms.grid(lw = .5, alpha = .5)
        self.ax_timeterms.set_aspect("equal")
        self.ax_timeterms.spines['right'].set_visible(False)
        self.ax_timeterms.spines['top'].set_visible(False)
        self.ax_timeterms.yaxis.set_ticks_position('left')
        self.ax_timeterms.xaxis.set_ticks_position('bottom')

        self.frame_tomography = Frame(self.frame_plots)
        self.frame_tomography.grid(row = 1, column = 1, sticky = "NSWE")
        self.fig_tomography = plt.figure(figsize = (9.5,3.7))
        canvas_tomography = FigureCanvasTkAgg(self.fig_tomography, self.frame_tomography)
        canvas_tomography.draw()
        toolbar_tomography = NavigationToolbar2Tk(canvas_tomography, self.frame_tomography)
        toolbar_tomography.update()
        canvas_tomography._tkcanvas.pack()
        self.ax_tomography = self.fig_tomography.add_subplot(111)
        self.fig_tomography.patch.set_facecolor('#F0F0F0')
        self.ax_tomography.set_title("Tomography velocity model")
        self.ax_tomography.set_xlabel("POSITION [m]")
        self.ax_tomography.set_ylabel("DEPTH [m]")
        self.ax_tomography.grid(lw = .5, alpha = .5)
        self.ax_tomography.set_aspect("equal")
        self.ax_tomography.spines['right'].set_visible(False)
        self.ax_tomography.spines['top'].set_visible(False)
        self.ax_tomography.yaxis.set_ticks_position('left')
        self.ax_tomography.xaxis.set_ticks_position('bottom')

        self.frame_plots.tkraise()
      
    def createProject(self):

        self.projPath = filedialog.askdirectory()
        
        if self.projPath:
            
            projName = simpledialog.askstring("Refrapick","Enter the name of the project to be created:")
            
            if not path.exists(self.projPath+"/"+projName):
                
                makedirs(self.projPath+"/"+projName)
                local = self.projPath+"/"+projName+"/"
                makedirs(local+"data")
                self.p_data = local+"data/"
                makedirs(local+"picks")
                self.p_picks = local+"picks/"
                makedirs(local+"models")
                self.p_models = local+"models/"
                makedirs(local+"gps")
                self.p_gps = local+"gps/"
                self.projPath = local
                self.projReady = True
                self.createPanels()
                messagebox.showinfo(title="Refrapick", message="Successfully created the project!")
                self.statusLabel.configure(text="Project path ready!",font=("Arial", 11))
                
            else:
                
                messagebox.showinfo(title="Refrapick", message="A project was detected, please choose another name or directory!")

    def loadProject(self):

        self.projPath = filedialog.askdirectory()
        
        if self.projPath:
            
            if path.exists(self.projPath+"/"+"data") and \
            path.exists(self.projPath+"/"+"picks") and \
            path.exists(self.projPath+"/"+"models") and \
            path.exists(self.projPath+"/"+"gps"):

                self.p_data = self.projPath+"/"+"data/"
                self.p_picks = self.projPath+"/"+"picks/"
                self.p_models = self.projPath+"/"+"models/"
                self.p_gps = self.projPath+"/"+"gps/"
                self.projReady = True
                self.createPanels()
                messagebox.showinfo(title="Refrapick", message="Successfully loaded the project path!")
                self.statusLabel.configure(text="Project path ready!",font=("Arial", 11))
                
            else: messagebox.showerror(title="Refrapick", message="Not all folders were detected!\nPlease, check the structure of the selected project.")

    def loadPick(self):
        
        if self.projReady:

            pickFile = filedialog.askopenfilename(title='Open', initialdir = self.projPath+"/picks/", filetypes=[('Pick file', '*.sgt')])
            self.lineName = path.basename(pickFile)[:-4]

            if pickFile:

                self.data_pg = pg.DataContainer(pickFile, 's g')

                with open(pickFile, "r") as file:

                    lines = file.readlines()
                    npoints = int(lines[0].split()[0])
                    sgx = [float(i.split()[0]) for i in lines[2:2+npoints]]
                    sgz = [float(i.split()[1]) for i in lines[2:2+npoints]]
                    sgtindx = lines.index("#s g t\n")
                    s = [int(i.split()[0]) for i in lines[sgtindx+1:]]
                    g = [int(i.split()[1]) for i in lines[sgtindx+1:]]
                    t = [float(i.split()[2]) for i in lines[sgtindx+1:]]
                    sx = [sgx[i-1] for i in s]
                    gx = [sgx[i-1] for i in g]
                    gz = [sgz[i-1] for i in g]
                    self.gx = gx
                    self.gz = gz
                    print(gz)
                    self.sgx = sgx
                    self.sgz = sgz
                    self.dx = self.gx[1]-self.gx[0]

                    for i,src in enumerate(list(set(sx))):
    
                        self.sources.append(src)
                        #self.xdata.append([])
                        #self.tdata.append([])
                        #self.dataArts.append([])
                        self.xdata.append({src:[]})
                        self.tdata.append({src:[]})
                        self.dataArts.append({src:[]})
                        sourcePlot = self.ax_data.scatter(src,0,c="y",edgecolor="k",s=100,marker="*",zorder=99)
                        self.data_sourcesArts.append(sourcePlot)

                        for j,x in enumerate(gx):

                            if sx[j] == src:

                                self.xdata[i][src].append(x)
                                self.tdata[i][src].append(t[j])
                                dataPlot = self.ax_data.scatter(x,t[j],facecolors='w',s=self.dx*4,edgecolor="k",picker=5,zorder=99)
                                self.dataArts[i][src].append(dataPlot)
                            
                        self.ax_data.plot(self.xdata[i][src], self.tdata[i][src], c = "k")

                    self.fig_data.canvas.draw()

    def runTimeTerms(self):

        if self.data_pg:
                    
            self.clearTimeTermsPlot()

            regw = simpledialog.askfloat("Refrainv", "Enter the regularization weight to be used for data inversion or cancel for default (lambda = 0.1)")
            
            if regw == None: regw = 0.1

            gx = list(set(self.gx))
            gz = self.gz[:len(gx)]
            
            def solve(layer, G, d, w):
                
                rMs = zeros((int(len(layer)), int(len(self.sources)+len(gx)+1)))
                r = 0
                
                for i in range(len(gx)):
                    
                    for j in range(len(self.sources)):
                        
                        if  self.sources[j] > min(gx) and self.sources[j] < max(gx): #se for fonte intermediaria
                            
                            if gx[i]+self.dx >= self.sources[j] and gx[i]-self.dx <= self.sources[j]:
                                
                                rMs[r][j] = w
                                rMs[r][len(self.sources)+i] = -w
                                r += 1
                                
                        elif self.sources[j] <= min(gx):
                            
                            if gx[i]-self.dx <= self.sources[j]:
                                
                                rMs[r][j] = w
                                rMs[r][len(self.sources)+i] = -w
                                r += 1
                                
                        elif self.sources[j] >= max(gx):
                            
                            if gx[i]+self.dx >= self.sources[j]:
                                
                                rMs[r][j] = w
                                rMs[r][len(self.sources)+i] = -w
                                r += 1
                                
                rMs = rMs[~np_all(rMs == 0, axis=1)] #regularization matrix of time-terms from sources
                rMg = zeros((int(len(layer)), int(len(self.sources)+len(gx)+1)))
                
                for i,j in zip(range(shape(rMg)[0]), range(shape(rMg)[1])):
                    
                    try:
                        
                        rMg[i][len(self.sources)+j] = w
                        rMg[i][len(self.sources)+j+1] = -w
                        
                    except: pass
                   
                rMg = rMg[~np_all(rMg == 0, axis=1)][:-2] #regularization matrix of time-terms from geophones
                rM = concatenate((rMs, rMg))
                rd = hstack((d, [i*0 for i in range(shape(rM)[0])]))
                rG = concatenate((G, rM))
                sol, sse, rank, sv = linalg.lstsq(rG, rd)
                
                return sol

            if self.layer1:
                
                d1 = array([self.layer1[i][1] for i in range(len(self.layer1))])
                G1 = array([self.layer1[i][3] for i in range(len(self.layer1))])
                G1 = reshape(G1, (len(G1),1))
                v1 = []
                
                for time,delta in zip(d1,G1):
                    
                    if delta == 0: pass
                    else: v1.append(time/delta)

                s1 = mean(v1)
                v1 = 1/s1
                self.velocity1 = v1
                list_ot1, list_pt1 = [],[]
                    
                for p in self.layer1:
                    
                    s = p[-2]
                    g = p[-1]
                    x = p[-3]
                    ot = p[1] #observed traveltime
                    pt = x/v1 #predicted traveltime
                    geop = p[0]
                    list_ot1.append(ot)
                    list_pt1.append(pt)

                self.timeterms_respLayer1 = list_pt1

                if self.layer2:
                    
                    d2 = array([self.layer2[i][1] for i in range(len(self.layer2))])
                    G2 = zeros((int(len(self.layer2)),
                                   int(len(self.sources)+len(gx)+1)))

                    for i in range(len(self.layer2)):
                        
                        G2[i][self.layer2[i][-2]] = 1
                        G2[i][self.layer2[i][-1]+len(self.sources)] = 1
                        G2[i][-1] = self.layer2[i][-3]

                    sol_layer2 = solve(self.layer2, G2, d2, regw)
                    v2 = 1/sol_layer2[-1] #m/s
                    self.velocity2 = v2

                if self.layer3:
                    
                    d3 = array([self.layer3[i][1] for i in range(len(self.layer3))])
                    G3 = zeros((int(len(self.layer3)),
                                   int(len(self.sources)+len(gx)+1)))

                    for i in range(len(self.layer3)):
                        
                        G3[i][self.layer3[i][-2]] = 1
                        G3[i][self.layer3[i][-1]+len(self.sources)] = 1
                        G3[i][-1] = self.layer3[i][-3]

                    sol_layer3 = solve(self.layer3, G3, d3, regw)
                    v3 = 1/sol_layer3[-1] #m/s
                    self.velocity3 = v3
                 
                #self.sgp = sort(concatenate((arange(gx[0],gx[0]+len(gx)*self.dx,self.dx),array(self.sources))))
            
                if self.layer1 and self.layer2 and not self.layer3:
                    
                    dtg = array([i for i in sol_layer2[len(self.sources):-1]]) #delay-time of all geophones
                    dts = array([i for i in sol_layer2[:len(self.sources)]]) #delay-time of all sources

                    list_ot2, list_pt2 = [],[]
                    
                    for p in self.layer2:
                        
                        s = p[-2]
                        g = p[-1]
                        x = p[-3]
                        ot = p[1] #observed traveltime
                        geop = p[0]
                        pt = dts[s]+dtg[g]+sol_layer2[-1]*x #predicted traveltime
                        list_ot2.append(ot)
                        list_pt2.append(pt)
                        
                    self.timeterms_respLayer2 = list_pt2
                        
                    dlayer2 = gz-((dtg*v1*v2)/(sqrt((v2**2)-(v1**2))))
                    self.depthLayer2 = dlayer2
                    
                    try:
                        
                        #self.ax_timeterms.plot(gx,gz,c="r")
                        #self.ax_timeterms.plot(gx,dlayer2,c="b")
                        f = interp1d(gx, dlayer2, kind = 'linear', fill_value='extrapolate')
                        sdlayer2 = f(linspace(gx[0], gx[-1], 1000))
                        f = interp1d(gx, gz, kind = 'linear', fill_value='extrapolate')
                        s_surf = f(linspace(gx[0], gx[-1], 1000))
                        self.tt_layer1 = self.ax_timeterms.fill_between(linspace(gx[0], gx[-1], 1000),sdlayer2,s_surf, color = "red",
                                          alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                        self.tt_layer2 = self.ax_timeterms.fill_between(linspace(gx[0], gx[-1], 1000),sdlayer2, min(sdlayer2)*0.99,
                                          alpha = .5,edgecolor = "k", color = "green",
                                          label = "%.0f m/s"%v2)
                        
                    except:
                        
                        self.tt_layer1 = self.ax_timeterms.fill_between(gx,dlayer2, gz, color = "red", alpha = .5,edgecolor = "k",
                                          label = "%.0f m/s"%v1)
                        self.tt_layer2 = self.ax_timeterms.fill_between(gx,dlayer2, min(dlayer2)*0.99, alpha = .5,edgecolor = "k",
                                          color = "green", label = "%.0f m/s"%v2)
        
                elif self.layer1 and self.layer2 and self.layer3:
                                      
                    dtg2 = array([i for i in sol_layer2[len(self.sources):-1]]) #delay-time of all geophones2
                    dtg3 = array([i for i in sol_layer3[len(self.sources):-1]]) #delay-time of all geophones3
                    dts2 = array([i for i in sol_layer2[:len(self.sources)]]) #delay-time of all sources2
                    dts3 = array([i for i in sol_layer3[:len(self.sources)]]) #delay-time of all sources3

                    list_ot2, list_pt2 = [],[]
                    
                    for p in self.layer2:
                        
                        s = p[-2]
                        g = p[-1]
                        x = p[-3]
                        ot = p[1] #observed traveltime
                        geop = p[0]
                        pt = dts2[s]+dtg2[g]+sol_layer2[-1]*x #predicted traveltime
                        list_ot2.append(ot)
                        list_pt2.append(pt)

                    list_ot3, list_pt3 = [],[]
                    
                    for p in self.layer3:
                        
                        s = p[-2]
                        g = p[-1]
                        x = p[-3]
                        ot = p[1] #observed traveltime
                        geop = p[0]
                        pt = dts3[s]+dtg3[g]+sol_layer3[-1]*x #predicted traveltime
                        list_ot3.append(ot)
                        list_pt3.append(pt)

                    self.timeterms_respLayer2 = list_pt2
                    self.timeterms_respLayer3 = list_pt3
                    upvmed = (v1+v2)/2
                        
                    #dlayer2 = gz-((dtg2*v1*v2)/(sqrt((v2**2)-(v1**2)))/1000)
                    dlayer2 = gz-((dtg2*v1*v2)/(sqrt((v2**2)-(v1**2))))
                    self.depthLayer2 = dlayer2
                    #dlayer3 = gz-((dtg3*upvmed*v3)/(sqrt((v3**2)-(upvmed**2)))/1000)
                    dlayer3 = gz-((dtg3*upvmed*v3)/(sqrt((v3**2)-(upvmed**2))))
                    self.depthLayer3 = dlayer3
                        
                    try:
                        
                        s_surf = f(linspace(gx[0], gx[-1], 1000))
                        f2 = interp1d(arange(gx[0], (len(gx)*self.dx)+gx[0], self.dx), dlayer2, kind = 'cubic', fill_value='extrapolate')
                        sdlayer2 = f2(linspace(gx[0], gx[0]+(len(gx)*self.dx)-self.dx, 1000))
                        f3 = interp1d(arange(gx[0], (len(gx)*self.dx)+gx[0], self.dx), dlayer3, kind = 'cubic', fill_value='extrapolate')
                        sdlayer3 = f3(linspace(gx[0], gx[0]+(len(gx)*self.dx)-self.dx, 1000))
                        self.tt_layer1 = self.tt_ax3.fill_between(linspace(gx[0], gx[-1], 1000),sdlayer2,s_surf, color = "red",
                                          alpha = .5,edgecolor = "k", label = "%.0f m/s"%v1)
                        self.tt_layer2 = self.ax_timeterms.fill_between(linspace(gx[0], gx[-1], 1000),sdlayer2, sdlayer3, alpha = .5,
                                          edgecolor = "k", color = "green", label = "%.0f m/s"%v2)
                        self.tt_layer3 = self.ax_timeterms.fill_between(linspace(gx[0], gx[-1], 1000),sdlayer3, min(sdlayer3)*1.1,
                                          alpha = .5,edgecolor = "k", color = "blue",
                                          label = "%.0f m/s"%v3)
                        
                    except:
                        
                        self.tt_layer1 = self.ax_timeterms.fill_between(gx,dlayer2,gz, color = "red", alpha = .5,edgecolor = "k",
                                          label = "%.0f m/s"%v1)
                        self.tt_layer2 = self.ax_timeterms.fill_between(gx,dlayer2, dlayer3, alpha = .5,edgecolor = "k", color = "green",
                                          label = "%.0f m/s"%v2)
                        self.tt_layer3 = self.ax_timeterms.fill_between(gx,dlayer3, min(dlayer3)*1.1, alpha = .5,edgecolor = "k",
                                          color = "blue", label = "%.0f m/s"%v3)

     
                self.ax_timeterms.legend(loc="best")
                self.timetermsPlot = True
                self.fig_timeterms.canvas.draw()

                if self.layer1 and self.layer2 and not self.layer3:

                    self.timeterms_response = self.timeterms_respLayer1+self.timeterms_respLayer2
                    obs_tt = list_ot1+list_ot2
                    rmse = sqrt(mean((array(self.timeterms_response)-array(obs_tt))**2))
                    relrmse = (sqrt(mean(square((array(obs_tt) - array(self.timeterms_response)) / array(obs_tt))))) * 100
                    messagebox.showinfo('Refrainv','Absolute RMSE = %.2f ms\nRelative RMSE = %.2f%%'%(rmse,relrmse))

                elif self.layer1 and self.layer2 and self.layer3:

                    self.timeterms_response = self.timeterms_respLayer1+self.timeterms_respLayer2+self.timeterms_respLayer3
                    obs_tt = list_ot1+list_ot2+list_ot3
                    rmse = sqrt(mean((array(self.timeterms_response)-array(obs_tt))**2))
                    relrmse = (sqrt(mean(square((array(obs_tt) - array(self.timeterms_response)) / array(obs_tt))))) * 100
                    messagebox.showinfo('Refrainv','The velocity model was created!\nAbsolute RMSE = %.2f ms\nRelative RMSE = %.2f%%'%(rmse,relrmse))
    
    def layersInterpretation(self):

        if self.data_pg:

            if self.layerInterpretationMode == False:
                
                self.layerInterpretationMode = True
                self.statusLabel.configure(text = 'Layer %d interpratation enabled!'%self.layer2interpretate)
                    
                def onpick(event):
                    
                    art = event.artist
                    artx = art.get_offsets()[0][0]
                    artt = art.get_offsets()[0][1]

                    for i in range(len(self.sources)):
                        
                        if art in self.dataArts[i][self.sources[i]]:
                            
                            arts = self.sources[i]
                            iS = i 
                            
                    if artx >= arts:
                        
                        for b in self.dataArts[iS][arts]:
                            
                            bx = b.get_offsets()[0][0]
                            iG = where(array(self.dataArts[iS][arts]) == b)[0][0]
                            
                            if arts <= bx <= artx:
                                
                                bt = b.get_offsets()[0][1]
                                
                                if self.layer2interpretate == 1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1:
                                    
                                    b.set_color("red")
                                    self.layer1.append((bx,bt,arts,abs(arts-bx),iS, iG))#geophone_position , arrival_time , source_poisition , offset , index_source , index_geophone

                                    if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer2:
                                        
                                        self.layer2.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                                        
                                elif self.layer2interpretate == 2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2:
                                    
                                    b.set_color("lightgreen")
                                    self.layer2.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                    
                                    if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer3:
                                        
                                        self.layer3.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                                        
                                elif self.layer2interpretate == 3 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer3:

                                    b.set_color("blue")
                                    self.layer3.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                    
                    elif artx <= arts:
                        
                        for b in self.dataArts[iS][arts]:
                            
                            bx = b.get_offsets()[0][0]
                            iG = where(array(self.dataArts[iS][arts]) == b)[0][0]
                            
                            if arts >= bx >= artx:
                                
                                bt = b.get_offsets()[0][1]
                                
                                if self.layer2interpretate == 1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1:
                                    
                                    b.set_color("red")
                                    self.layer1.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                    
                                    if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer2:
                                        
                                        self.layer2.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                                        
                                elif self.layer2interpretate == 2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2:
                                    
                                    b.set_color("lightgreen")
                                    self.layer2.append((bx,bt,arts,abs(arts-bx),iS, iG))
                                    
                                    if (bx,bt,arts,abs(arts-bx),iS, iG) in self.layer3:
                                        
                                        self.layer3.remove((bx,bt,arts,abs(arts-bx),iS, iG))
                                        
                                elif self.layer2interpretate == 3 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer2 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer1 and (bx,bt,arts,abs(arts-bx),iS, iG) not in self.layer3:

                                    b.set_color("blue")
                                    self.layer3.append((bx,bt,arts,abs(arts-bx),iS, iG))
                    
                    self.fig_data.canvas.draw()

                def onkey(event):
                    
                    if event.key == "1": self.layer2interpretate = 1
                    elif event.key == "2": self.layer2interpretate = 2
                    elif event.key == "3": self.layer2interpretate = 3
                    
                    self.statusLabel.configure(text = 'Layer %d interpratation enabled!'%self.layer2interpretate)
                    
                    if event.key == "C" or event.key == "c":
                        
                        if messagebox.askyesno("Refrainv", "Clear layer interpretation?"):
                            
                            del self.layer1[:]
                            del self.layer2[:]
                            del self.layer3[:]
                            
                            for i in range(len(self.sources)):
                                
                                for b in self.dataArts[i][self.sources[i]]:
                                    
                                    b.set_color("white")
                                    b.set_edgecolor("k")

                            self.fig_data.canvas.draw()

                self.timeterms_pickEvent = self.fig_data.canvas.mpl_connect('pick_event', onpick)
                self.timeterms_keyEvent = self.fig_data.canvas.mpl_connect('key_press_event', onkey)
                messagebox.showinfo('Refrapy','Layer interpretation enabled!')

            else:
                
                self.fig_data.canvas.mpl_disconnect(self.timeterms_pickEvent)
                self.fig_data.canvas.mpl_disconnect(self.timeterms_keyEvent)
                self.statusLabel.configure(text = 'Layer interpratation disabled')
                messagebox.showinfo('Refrainv','Layer interpretation disabled!')
                self.layerInterpretationMode = False
    
    def clearTomoPlot(self):

        self.fig_tomography.clf()
        self.ax_tomography = self.fig_tomography.add_subplot(111)
        self.fig_tomography.patch.set_facecolor('#F0F0F0')
        self.ax_tomography.set_title("Tomography velocity model")
        self.ax_tomography.set_xlabel("POSITION [m]")
        self.ax_tomography.set_ylabel("DEPTH [m]")
        self.ax_tomography.grid(lw = .5, alpha = .5)
        self.ax_tomography.set_aspect("equal")
        self.ax_tomography.spines['right'].set_visible(False)
        self.ax_tomography.spines['top'].set_visible(False)
        self.ax_tomography.yaxis.set_ticks_position('left')
        self.ax_tomography.xaxis.set_ticks_position('bottom')
        self.tomoPlot = False
        self.fig_tomography.canvas.draw()

    def clearTimeTermsPlot(self):

        self.fig_timeterms.clf()
        self.ax_timeterms = self.fig_timeterms.add_subplot(111)
        self.fig_timeterms.patch.set_facecolor('#F0F0F0')
        self.ax_timeterms.set_title("Time-terms velocity model")
        self.ax_timeterms.set_xlabel("POSITION [m]")
        self.ax_timeterms.set_ylabel("DEPTH [m]")
        self.ax_timeterms.grid(lw = .5, alpha = .5)
        self.ax_timeterms.set_aspect("equal")
        self.ax_timeterms.spines['right'].set_visible(False)
        self.ax_timeterms.spines['top'].set_visible(False)
        self.ax_timeterms.yaxis.set_ticks_position('left')
        self.ax_timeterms.xaxis.set_ticks_position('bottom')
        self.timetermsPlot = False
        self.fig_timeterms.canvas.draw()
                
    def runTomography(self):

        if self.data_pg:

            self.mgr = TravelTimeManager()

            tomoWindow = Toplevel(self)
            tomoWindow.title('Refrainv - Tomography')
            tomoWindow.configure(bg = "#F0F0F0")
            tomoWindow.geometry("300x640")
            tomoWindow.resizable(0,0)
            tomoWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

            def viewMesh():

                maxDepth = float(maxDepth_entry.get())
                paraDX = float(paraDX_entry.get())
                paraMaxCellSize = float(paraMaxCellSize_entry.get())
                self.tomoMesh = self.mgr.createMesh(data=self.data_pg,paraDepth=maxDepth,paraDX=paraDX,paraMaxCellSize=paraMaxCellSize)

                meshWindow = Toplevel(self)
                meshWindow.title('Refrainv - Mesh')
                meshWindow.configure(bg = "#F0F0F0")
                #meshWindow.geometry("1024x768")
                meshWindow.resizable(0,0)
                meshWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

                frame = Frame(meshWindow)
                frame.grid(row = 0, column = 0)
                fig = plt.figure(figsize = (12,6))#.2,8.62))
                fig.patch.set_facecolor('#F0F0F0')
                canvas = FigureCanvasTkAgg(fig, frame)
                canvas.draw()
                toolbar = NavigationToolbar2Tk(canvas, frame)
                toolbar.update()
                canvas._tkcanvas.pack()
                
                ax = fig.add_subplot(111)
                ax.set_ylabel("POSITION [m]")
                ax.set_xlabel("DEPTH [m]")
                ax.grid(lw = .5, alpha = .5)

                #vel = ra.paraModel()
                pg.show(self.tomoMesh, ax = ax)
                #pg.viewer.mpl.drawSensors(ax, data.sensorPositions(), diam=0.5, color="k")
                ax.set_xlabel('Distance (m)')
                ax.set_ylabel('Elevation (m)')
                ax.set_title('Mesh for traveltimes tomography')

                ax.set_aspect("equal")
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')

                fig.canvas.draw()
                meshWindow.tkraise()
                #print(m.dimension)
                #print(m.yMin())
                #print(m.yMax())

            def runInversion():

                if self.tomoPlot:

                    self.clearTomoPlot()
                    
                #if self.tomoMesh == False:

                maxDepth = float(maxDepth_entry.get())
                paraDX = float(paraDX_entry.get())
                paraMaxCellSize = float(paraMaxCellSize_entry.get())
                self.tomoMesh = self.mgr.createMesh(data=self.data_pg,paraDepth=maxDepth,paraDX=paraDX,paraMaxCellSize=paraMaxCellSize)

                lam = float(lam_entry.get())
                zWeigh = float(zWeigh_entry.get())
                vTop = float(vTop_entry.get())
                vBottom = float(vBottom_entry.get())
                minVelLimit = float(minVelLimit_entry.get())
                maxVelLimit = float(maxVelLimit_entry.get())
                self.minVelLimit = minVelLimit
                self.maxVelLimit = maxVelLimit
                secNodes = int(secNodes_entry.get())
                maxIter = int(maxIter_entry.get())
   
                vest = self.mgr.invert(data=self.data_pg,mesh=self.tomoMesh,verbose=False,lam=lam,zWeight=zWeigh,useGradient=True,
                               vTop=vTop,vBottom=vBottom,maxIter=maxIter,limits=[minVelLimit,maxVelLimit],secNodes=secNodes)
                
                self.parameters_tomo = [maxDepth,paraDX,paraMaxCellSize,lam,zWeigh,vTop,vBottom,minVelLimit,maxVelLimit,secNodes,maxIter,
                                        int(xngrid_entry.get()),int(yngrid_entry.get()),int(nlevels_entry.get()),
                                        self.mgr.inv.maxIter,self.mgr.inv.relrms(),self.mgr.inv.chi2()]
                plotContourModel()

            def plotContourModel():
   
                xzv = column_stack((self.mgr.paraDomain.cellCenters(), self.mgr.model))
                x = (xzv[:,0])
                z = (xzv[:,1])
                v = (xzv[:,3])

                self.tomoModel_x = x
                self.tomoModel_z = z
                self.tomoModel_v = v
                
                nx = int(xngrid_entry.get())
                ny = int(yngrid_entry.get())
                x_grid = linspace(min(x), max(x), nx)
                y_grid = linspace(min(z), max(z), ny)
                xi,zi = meshgrid(x_grid,y_grid)
                vi = griddata((x, z), v,(xi,zi), method = 'linear')

                nlevels = int(nlevels_entry.get())
                
                cm = self.ax_tomography.contourf(xi, zi, vi, levels=nlevels,
                                    cmap=self.colormap, extend="both")

                self.cmPlot = cm

                divider = make_axes_locatable(self.ax_tomography)
                cax = divider.append_axes("right", size="2%", pad=0.05)

                cbar = self.fig_tomography.colorbar(cm,orientation="vertical", label = "[m/s]",
                             format='%d',cax=cax)

                x2max = [max(self.sources)]
                x2min = [min(self.sources)]
                
                for i in range(len(self.sources)): x2max.append(max(self.xdata[i])); x2min.append(min(self.xdata[i]))
                
                xlim = self.sgx+[max(x2max),min(x2min)]
                zlim = self.sgz+[self.tomoMesh.yMin(),self.tomoMesh.yMin()]

                self.topographyx, self.topographyz = [], []

                for i in range(len(self.sgx)):

                    if self.sgx[i] <= max(x2max) and self.sgx[i] >= min(x2min): self.topographyx.append(self.sgx[i]); self.topographyz.append(self.sgz[i])

                xblank, zblank = [], []

                for i in range(len(xlim)):

                    if xlim[i] <= max(x2max) and xlim[i] >= min(x2min): xblank.append(xlim[i]); zblank.append(zlim[i])
                
                self.xbln = xblank
                self.zbln = zblank

                self.ax_tomography.plot(self.topographyx, self.topographyz, c= "k", lw = 1.5)
                
                limits = [(i,j) for i,j in zip(xblank,zblank)]
                
                clippath = Path(limits)
                patch = PathPatch(clippath, facecolor='none', alpha = 0)
                self.ax_tomography.add_patch(patch)

                patch = PathPatch(clippath, facecolor='none', alpha = 0)
                self.ax_tomography.add_patch(patch)

                for c in cm.collections: c.set_clip_path(patch)

                if self.showRayPath: self.mgr.drawRayPaths(self.ax_tomography,color=self.rayPathColor)
                    
                self.ax_tomography.set_xlim(min(x2min),max(x2max))
                self.fig_tomography.canvas.draw()
                self.tomoPlot = True
                self.showFit()
                tomoWindow.destroy()

            offsets = []
            
            for i in range(len(self.sources)):

                for x in self.xdata[i][self.sources[i]]:

                    offsets.append(abs(self.sources[i]-x))
            
            Label(tomoWindow, text="Mesh options", font=("Arial", 11)).grid(row=0,column=0,columnspan=2,pady=10,sticky="E")
            
            Label(tomoWindow, text = "Maximum depth (max offset = %.2f m)"%max(offsets)).grid(row=1,column=0,pady=5,sticky="E")
            maxDepth_entry = Entry(tomoWindow,width=6)
            maxDepth_entry.grid(row=1,column=1,pady=5)
            maxDepth_entry.insert(0, str(max(offsets)*0.4))#str(int((self.gx[-1]-self.gx[0])*0.4)))

            Label(tomoWindow, text = "# of nodes between receivers").grid(row=2,column=0,pady=5,sticky="E")
            paraDX_entry = Entry(tomoWindow,width=6)
            paraDX_entry.grid(row=2,column=1,pady=5)
            paraDX_entry.insert(0,"0.33")

            Label(tomoWindow, text = "Maximum cell size").grid(row=3,column=0,pady=5,sticky="E")
            paraMaxCellSize_entry = Entry(tomoWindow,width=6)
            paraMaxCellSize_entry.grid(row=3,column=1,pady=5)
            paraMaxCellSize_entry.insert(0,str((self.gx[1]-self.gx[0])))
            
            button = Button(tomoWindow, text="View mesh", command=viewMesh).grid(row=4,column=0,columnspan=2,pady=5,sticky="E")

            Label(tomoWindow, text="Inversion options", font=("Arial", 11)).grid(row=5,column=0,columnspan=2,pady=10,sticky="E")
            
            Label(tomoWindow, text = "Smoothing (lam)").grid(row=6,column=0,pady=5,sticky="E")
            lam_entry = Entry(tomoWindow,width=6)
            lam_entry.grid(row=6,column=1,pady=5)
            lam_entry.insert(0,"50")

            Label(tomoWindow, text = "Vertical to horizontal smoothing (zweigh)").grid(row=7,column=0,pady=5,sticky="E")
            zWeigh_entry = Entry(tomoWindow,width=6)
            zWeigh_entry.grid(row=7,column=1,pady=5)
            zWeigh_entry.insert(0,"0.2")

            Label(tomoWindow, text = "Velocity at the top of the model").grid(row=8,column=0,pady=5,sticky="E")
            vTop_entry = Entry(tomoWindow,width=6)
            vTop_entry.grid(row=8,column=1,pady=5)
            vTop_entry.insert(0,"300")
            
            Label(tomoWindow, text = "Velocity at the bottom of the model").grid(row=9,column=0,pady=5,sticky="E")
            vBottom_entry = Entry(tomoWindow,width=6)
            vBottom_entry.grid(row=9,column=1,pady=5)
            vBottom_entry.insert(0,"3000")

            Label(tomoWindow, text = "Minimum velocity limit").grid(row=10,column=0,pady=5,sticky="E")
            minVelLimit_entry = Entry(tomoWindow,width=6)
            minVelLimit_entry.grid(row=10,column=1,pady=5)
            minVelLimit_entry.insert(0,"100")

            Label(tomoWindow, text = "Maximum velocity limit").grid(row=11,column=0,pady=5,sticky="E")
            maxVelLimit_entry = Entry(tomoWindow,width=6)
            maxVelLimit_entry.grid(row=11,column=1,pady=5)
            maxVelLimit_entry.insert(0,"4000")

            Label(tomoWindow, text = "# of secondary nodes").grid(row=12,column=0,pady=5,sticky="E")
            secNodes_entry = Entry(tomoWindow,width=6)
            secNodes_entry.grid(row=12,column=1,pady=5)
            secNodes_entry.insert(0,"3")

            Label(tomoWindow, text = "Maximum # of iterations").grid(row=13,column=0,pady=5,sticky="E")
            maxIter_entry = Entry(tomoWindow,width=6)
            maxIter_entry.grid(row=13,column=1,pady=5)
            maxIter_entry.insert(0,"20")

            Label(tomoWindow, text="Contour plot options", font=("Arial", 11)).grid(row=14,column=0,columnspan=2,pady=10,sticky="E")
            
            Label(tomoWindow, text = "# of nodes for gridding (x)").grid(row=15,column=0,pady=5,sticky="E")
            xngrid_entry = Entry(tomoWindow,width=6)
            xngrid_entry.grid(row=15,column=1,pady=5)
            xngrid_entry.insert(0,"1000")

            Label(tomoWindow, text = "# of nodes for gridding (y)").grid(row=16,column=0,pady=5,sticky="E")
            yngrid_entry = Entry(tomoWindow,width=6)
            yngrid_entry.grid(row=16,column=1,pady=5)
            yngrid_entry.insert(0,"1000")

            Label(tomoWindow, text = "# of contour levels").grid(row=17,column=0,pady=5,sticky="E")
            nlevels_entry = Entry(tomoWindow,width=6)
            nlevels_entry.grid(row=17,column=1,pady=5)
            nlevels_entry.insert(0,"20")
            
            button = Button(tomoWindow, text="Run inversion", command=runInversion).grid(row=18,column=0,columnspan=2,pady=5,sticky="E")

            tomoWindow.tkraise()

    def saveResults(self):

        if self.tomoPlot:

            savetxt(self.projPath+"/models/%s_xzv.txt"%(self.lineName),c_[self.tomoModel_x,self.tomoModel_z,self.tomoModel_v], fmt = "%.2f", header = "x z velocity",comments="")
            self.fig_tomoFit.savefig(self.projPath+"/models/%s_tomography_response.jpeg"%(self.lineName), format="jpeg",dpi = 300,transparent=True)
            self.fig_tomography.savefig(self.projPath+"/models/%s_tomography_model.jpeg"%(self.lineName), format="jpeg",dpi = 300,transparent=True)
            savetxt(self.projPath+"/models/%s_topography.txt"%(self.lineName),c_[self.topographyx,self.topographyz], fmt = "%.2f", header = "x z",comments="")
            savetxt(self.projPath+"/models/%s_tomography_limits.bln"%(self.lineName),c_[self.xbln,self.zbln], fmt = "%.2f", header = "%d,1"%len(self.xbln),comments="")

            if self.coords_3d: savetxt(self.projPath+"/models/%s_tomography_xyzv.txt"%(self.lineName),c_[self.new_x,self.new_y,self.tomoModel_z,self.tomoModel_v], fmt = "%.2f", header = "x y z velocity",comments="")

            with open(self.projPath+"/models/%s_tomography_parameters.txt"%(self.lineName),"w") as outFile:

                outFile.write("%s - Traveltimes tomography parameters\n\n"%self.lineName)
                outFile.write("Mesh options\n")
                outFile.write("Maximum depth %.2f\n"%(self.parameters_tomo[0]))
                outFile.write("# of nodes between receivers %.2f\n"%(self.parameters_tomo[1]))
                outFile.write("Maximum cell size %.2f\n\n"%(self.parameters_tomo[2]))
                outFile.write("Inversion options\n")
                outFile.write("Smoothing (lam) %.2f\n"%(self.parameters_tomo[3]))
                outFile.write("Vertical to horizontal smoothing (zweigh) %.2f\n"%(self.parameters_tomo[4]))
                outFile.write("Velocity at the top of the model %.2f\n"%(self.parameters_tomo[5]))
                outFile.write("Velocity at the bottom of the model %.2f\n"%(self.parameters_tomo[6]))
                outFile.write("Minimum velocity limit %.2f\n"%(self.parameters_tomo[7]))
                outFile.write("Maximum velocity limit %.2f\n"%(self.parameters_tomo[8]))
                outFile.write("# of secondary nodes %d\n"%(self.parameters_tomo[9]))
                outFile.write("Maximum # of iterations %d\n\n"%(self.parameters_tomo[10]))
                outFile.write("Contour plot options\n")
                outFile.write("# of nodes for gridding (x) %d\n"%(self.parameters_tomo[11]))
                outFile.write("# of nodes for gridding (y) %d\n"%(self.parameters_tomo[12]))
                outFile.write("# of contour levels %d\n\n"%(self.parameters_tomo[13]))
                outFile.write("Model response\n")
                outFile.write("Final iteration %d\n"%(self.parameters_tomo[14]))
                outFile.write("Relative RMSE %.2f\n"%(self.parameters_tomo[15]))
                outFile.write("Chi² %.2f\n"%(self.parameters_tomo[16]))

        if self.timetermsPlot:

            self.fig_data.savefig(self.projPath+"/models/%s_layers_assignment.jpeg"%(self.lineName), format="jpeg",dpi = 300,transparent=True)
            self.fig_timetermsFit.savefig(self.projPath+"/models/%s_timeterms_response.jpeg"%(self.lineName), format="jpeg",dpi = 300,transparent=True)
            self.fig_timeterms.savefig(self.projPath+"/models/%s_timeterms_model.jpeg"%(self.lineName), format="jpeg",dpi = 300,transparent=True)

        if self.timetermsPlot or self.tomoPlot: messagebox.showinfo(title="Refrainv", message="All results saved in %s"%(self.projPath+"/models/"))
    
    def showFit(self):

        if self.data_pg:

            fitWindow = Toplevel(self)
            fitWindow.title('Refrainv - Fit')
            fitWindow.configure(bg = "#F0F0F0")
            fitWindow.resizable(0,0)
            fitWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

            frame1 = Frame(fitWindow)
            frame1.grid(row = 0, column = 0)
            fig1 = plt.figure(figsize = (7.1,8.62))
            fig1.patch.set_facecolor('#F0F0F0')
            canvas1 = FigureCanvasTkAgg(fig1, frame1)
            canvas1.draw()
            toolbar1 = NavigationToolbar2Tk(canvas1, frame1)
            toolbar1.update()
            canvas1._tkcanvas.pack()

            frame2 = Frame(fitWindow)
            frame2.grid(row = 0, column = 1)
            fig2 = plt.figure(figsize = (7.1,8.62))
            fig2.patch.set_facecolor('#F0F0F0')
            canvas2 = FigureCanvasTkAgg(fig2, frame2)
            canvas2.draw()
            toolbar2 = NavigationToolbar2Tk(canvas2, frame2)
            toolbar2.update()
            canvas2._tkcanvas.pack()
            
            ax_fitTimeterms = fig1.add_subplot(111)
            ax_fitTimeterms.set_ylabel("TRAVELTIME [s]")
            ax_fitTimeterms.set_xlabel("POSITION [m]")
            ax_fitTimeterms.grid(lw = .5, alpha = .5)
            ax_fitTimeterms.set_title("Time-terms inversion fit")

            ax_fitTomography = fig2.add_subplot(111)
            
            if self.tomoPlot:

                pg.physics.traveltime.drawFirstPicks(ax_fitTomography, self.data_pg, marker="o", lw = 0)
                pg.physics.traveltime.drawFirstPicks(ax_fitTomography, self.data_pg, tt= self.mgr.inv.response, marker="", linestyle = "--")
                legend_elements = [Line2D([0], [0], marker='o', color='k', label='Observed data', markerfacecolor='k', markersize=7),
                                   Line2D([0], [0], color='k', lw=1, ls = "--", label='Model response')]
                ax_fitTomography.legend(handles=legend_elements, loc='best')
                
            else:

                pg.physics.traveltime.drawFirstPicks(ax_fitTomography, self.data_pg, marker="o", lw = 1)

            for art in ax_fitTomography.get_lines(): art.set_color("k")    
            
            ax_fitTomography.set_ylabel("TRAVELTIME [s]")
            ax_fitTomography.set_xlabel("POSITION [m]")
            ax_fitTomography.grid(lw = .5, alpha = .5)

            if self.tomoPlot: ax_fitTomography.set_title("Tomography inversion fit\n%d iterations | RRMSE = %.2f%%"%(self.mgr.inv.maxIter,self.mgr.inv.relrms())) #mgr.absrms() mgr.chi2()
            else: ax_fitTomography.set_title("Observed traveltimes")
       
            fig1.canvas.draw()
            fig2.canvas.draw()
            self.fig_tomoFit = fig2
            self.fig_timetermsFit = fig1
            fitWindow.tkraise()

    def showPgResult(self):

        if self.tomoPlot:

            pgWindow = Toplevel(self)
            pgWindow.title('Refrainv - Velocity model with mesh')
            pgWindow.configure(bg = "#F0F0F0")
            pgWindow.resizable(0,0)
            pgWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

            frame = Frame(pgWindow)
            frame.grid(row = 0, column = 0)
            fig = plt.figure(figsize = (14.2,8.62))
            fig.patch.set_facecolor('#F0F0F0')
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, frame)
            toolbar.update()
            canvas._tkcanvas.pack()
            ax_pg = fig.add_subplot(111)
            
            pg.show(self.tomoMesh, self.mgr.model, label = "[m/s]",
                    cMin=self.minVelLimit,cMax=self.maxVelLimit,cMap=self.colormap,ax = ax_pg)

            if self.showRayPath: self.mgr.drawRayPaths(ax = ax_pg,color=self.rayPathColor)

            ax_pg.set_ylabel("DEPTH [m]")
            ax_pg.set_xlabel("DISTANCE [m]")
            ax_pg.grid(lw = .5, alpha = .5)
            ax_pg.set_title("Tomography velocity model")
            
            fig.canvas.draw()
            pgWindow.tkraise()

    def build3d(self):
            
        if self.tomoPlot:

            if not self.coords_3d:

                messagebox.showinfo(title="Refrainv", message="Select now the file containing the survey line coordinates (4-column file: distance,x,y,elevation)")

                file_3d = filedialog.askopenfilename(title='Open', initialdir = self.projPath+"/gps/", filetypes=[('Text file', '*.txt'),('CSV file', '*.csv')])
                d,x,y,z = [],[],[],[]
                
                with open(file_3d, "r") as file:

                    lines = file.readlines()

                    for l in lines:

                        dist = l.replace(' ', ',').replace('	',',').replace(';',',').replace('\n','').split(',')[0]
                        xcoord = l.replace(' ', ',').replace('	',',').replace(';',',').replace('\n','').split(',')[1]
                        ycoord = l.replace(' ', ',').replace('	',',').replace(';',',').replace('\n','').split(',')[2]
                        elev = l.replace(' ', ',').replace('	',',').replace(';',',').replace('\n','').split(',')[3]
                        d.append(float(dist))
                        x.append(float(xcoord))
                        y.append(float(ycoord))
                        z.append(float(elev))

                self.coords_3d.append(d)
                self.coords_3d.append(x)
                self.coords_3d.append(y)
                self.coords_3d.append(z)

            if self.coords_3d:

                def save3dtomo():

                    tomo3dfile_out = filedialog.asksaveasfilename(title='Save',initialdir = self.projPath+"/models/",filetypes=[('Text file', '*.txt')])

                    if tomo3dfile_out:

                        savetxt(tomo3dfile_out+".txt",c_[self.new_x,self.new_y,self.tomoModel_z,self.tomoModel_v], fmt = "%.2f", header = "x y z velocity",comments="")
                        messagebox.showinfo(title="Refrainv", message="File saved!")
                        plot3dwindow.tkraise()

                plot3dwindow = Toplevel(self)
                plot3dwindow.title('Refrainv - 3D view')
                plot3dwindow.configure(bg = "#F0F0F0")
                plot3dwindow.geometry("1600x900")
                plot3dwindow.resizable(0,0)
                plot3dwindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())

                frame_buttons = Frame(plot3dwindow)
                frame_buttons.grid(row = 0, column = 0, columnspan=100,sticky="W")

                Button(frame_buttons,text="Save time-terms model 3D file",command=save3dtomo).grid(row=0,column=0,sticky="W")
                Button(frame_buttons,text="Save tomography model 3D file",command=save3dtomo).grid(row=0,column=1,sticky="W")
                
                frame1 = Frame(plot3dwindow)
                frame1.grid(row = 1, column = 0, rowspan=2)
                frame2 = Frame(plot3dwindow)
                frame2.grid(row = 1, column = 1)
                frame3 = Frame(plot3dwindow)
                frame3.grid(row = 2, column = 1)
                
                fig1 = plt.figure(figsize = (5,5))
                fig1.patch.set_facecolor('#F0F0F0')
                canvas1 = FigureCanvasTkAgg(fig1, frame1)
                canvas1.draw()
                toolbar1 = NavigationToolbar2Tk(canvas1, frame1)
                toolbar1.update()
                canvas1._tkcanvas.pack()

                fig2 = plt.figure(figsize = (11.1,3.95))
                fig2.patch.set_facecolor('#F0F0F0')
                canvas2 = FigureCanvasTkAgg(fig2, frame2)
                canvas2.draw()
                toolbar2 = NavigationToolbar2Tk(canvas2, frame2)
                toolbar2.update()
                canvas2._tkcanvas.pack()

                fig3 = plt.figure(figsize = (11.1,3.95))
                fig3.patch.set_facecolor('#F0F0F0')
                canvas3 = FigureCanvasTkAgg(fig3, frame3)
                canvas3.draw()
                toolbar3 = NavigationToolbar2Tk(canvas3, frame3)
                toolbar3.update()
                canvas3._tkcanvas.pack()

                ax_coords = fig1.add_subplot(111, aspect = "equal")
                ax_coords.set_ylabel("Y [m]")
                ax_coords.set_xlabel("X [m]")
                ax_coords.grid(lw = .5, alpha = .5)
                ax_coords.set_title("Survey coordinates")
                ax_coords.set_facecolor('#F0F0F0')
                
                ax_3d_timeterms = fig2.add_subplot(111, projection = "3d")
                ax_3d_timeterms.set_box_aspect((1, 1, 1))

                ax_3d_tomo = fig3.add_subplot(111, projection = "3d")
                ax_3d_tomo.set_box_aspect((1, 1, 1))

                ax_3d_timeterms.set_ylabel("Y [m]")
                ax_3d_timeterms.set_xlabel("X [m]")
                ax_3d_timeterms.set_zlabel("ELEVATION [m]")
                ax_3d_timeterms.grid(lw = .5, alpha = .5)
                ax_3d_timeterms.set_title("Time-terms velocity model")
                ax_3d_timeterms.set_facecolor('#F0F0F0')
                
                ax_3d_tomo.set_ylabel("Y [m]")
                ax_3d_tomo.set_xlabel("X [m]")
                ax_3d_tomo.set_zlabel("ELEVATION [m]")
                ax_3d_tomo.grid(lw = .5, alpha = .5)
                ax_3d_tomo.set_title("Tomography velocity model")
                ax_3d_tomo.set_facecolor('#F0F0F0')

                ax_coords.ticklabel_format(useOffset=False, style='plain')
                ax_3d_timeterms.ticklabel_format(useOffset=False, style='plain')
                ax_3d_tomo.ticklabel_format(useOffset=False, style='plain')
                
                fig1.canvas.draw()
                fig2.canvas.draw()
                fig3.canvas.draw()

                fx = interp1d(self.coords_3d[0],self.coords_3d[1], kind = "linear", fill_value = "extrapolate")
                fy = interp1d(self.coords_3d[0],self.coords_3d[2], kind = "linear", fill_value = "extrapolate")
                self.new_x = fx(self.tomoModel_x)
                self.new_y = fy(self.tomoModel_x)
                ax_coords.plot(self.coords_3d[1],self.coords_3d[2],c="k")
                cm = ax_3d_tomo.scatter(self.new_x,self.new_y,self.tomoModel_z,c = self.tomoModel_v, cmap = self.colormap, s = self.dx)
                
                fig1.canvas.draw()
                fig2.canvas.draw()
                fig3.canvas.draw()
                plot3dwindow.tkraise()
    
    def plotOptions(self):

        def rayPath():
            
            if self.showRayPath == False:

                show = messagebox.askyesno("Refrainv", "Do you want to show the ray path?")

                if show:

                    self.showRayPath = True

                    if self.tomoPlot:

                        self.mgr.drawRayPaths(self.ax_tomography,color=self.rayPathColor)
                        self.fig_tomography.canvas.draw()

                    messagebox.showinfo(title="Refrainv", message="The ray path view has been enabled!")
                    plotOptionsWindow.tkraise()

            else:

                hide = messagebox.askyesno("Refrainv", "Do you want to hide the ray path?")

                if hide:

                    self.showRayPath = False

                    if self.tomoPlot:
                        
                        for art in self.ax_tomography.collections:

                            if str(type(art)) == "<class 'matplotlib.collections.LineCollection'>": art.remove()

                        self.fig_tomography.canvas.draw()

                    messagebox.showinfo(title="Refrainv", message="The ray path view has be disabled!")
                    plotOptionsWindow.tkraise()

        def rayPathLineColor():

            new_color = simpledialog.askstring("Refrainv","Enter the new ray path line color (must be accepted by matplotlib):")

            if is_color_like(new_color):

                self.rayPathColor = new_color
                
                if self.tomoPlot:

                    messagebox.showinfo(title="Refrainv", message="To update the ray path color you must now hide and show the ray path!")
                    self.showRayPath = True
                    rayPath() #force removal of ray paths
                    rayPath() #plot it
                    
                messagebox.showinfo(title="Refrainv", message="The ray path line color has been changed")
                plotOptionsWindow.tkraise()

            else: messagebox.showerror(title="Refrainv", message="Invalid color!"); plotOptionsWindow.tkraise()
            
        def colormap():

            new_cmap = simpledialog.askstring("Refrainv","Enter the new color map to be used (must be accepted by matplotlib):")

            if new_cmap in plt.colormaps():

                self.colormap = new_cmap

                if self.tomoPlot:

                    self.cmPlot.set_cmap(self.colormap)
                    self.fig_tomography.canvas.draw()

                messagebox.showinfo(title="Refrainv", message="The color map has been changed!")
                plotOptionsWindow.tkraise()

            else: messagebox.showerror(title="Refrainv", message="Invalid color map!"); plotOptionsWindow.tkraise()
        
        plotOptionsWindow = Toplevel(self)
        plotOptionsWindow.title('Refrainv - Plot options')
        plotOptionsWindow.configure(bg = "#F0F0F0")
        plotOptionsWindow.geometry("350x520")
        plotOptionsWindow.resizable(0,0)
        plotOptionsWindow.iconbitmap("%s/images/ico_refrapy.ico"%getcwd())
        Label(plotOptionsWindow, text = "Plot options",font=("Arial", 11)).grid(row=0,column=0,sticky="EW",pady=5,padx=65)
        Label(plotOptionsWindow, text = "Tomography velocity model",bg="white",font=("Arial", 11)).grid(row=1,column=0,sticky="EW",pady=5,padx=65)
        Button(plotOptionsWindow,text="Show/hide ray path", command = rayPath, width = 30).grid(row = 2, column = 0,pady=5,padx=65)
        Button(plotOptionsWindow,text="Change ray path line color", command = rayPathLineColor, width = 30).grid(row = 3, column = 0,pady=5,padx=65)
        Button(plotOptionsWindow,text="Change colormap", command = colormap, width = 30).grid(row = 4, column = 0,pady=5,padx=65)
        
        plotOptionsWindow.tkraise()
        
app = Refrainv()
app.mainloop()




