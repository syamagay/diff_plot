import ROOT
# import TFile,TTree,TH1D,TH2D
import sys,glob,json

TMP_DIR="/home/yamagaya/Desktop/Yarr-sw/LatestYarr2/src/data"

ROOT.gStyle.SetOptStat("eMinoru")
    # set line color  
    # 1: black  (default)  
    # 2: red  
    # 3: green  
    # 4: blue  
    # 5: yellow  
    # 6: magenda  
    # 7: cyan  
    # 8: yellowgreen  
    # 9: purple  
    # 10: white  

def range_diffplot(plotType):
    a=["100","-500","500"]
    if plotType == "ThresholdMap-0":
        a=["100","-500","500"]
    elif plotType == "NoiseMap-0" :
        a=["100","-150","150"]
    elif plotType == "StatusMap-0" :
        a=["10","-10","10"]
    elif plotType == "Chi2Map-0" :
        a=["10","-5","5"]
    elif plotType == "OccupancyMap" :
        a=["10","-10","10"]
    elif plotType == "EnMask" :
        a=["4","-2","2"]
    elif plotType == "MeanTotMap0" :
        a=["32","-16","16"]
    elif plotType == "SigmaTotMap0" :
        a=["32","-16","16"]
    elif plotType == "NoiseOccupancy" :
        a=["20","-10","10"]
    elif plotType == "NoiseMask" :
        a=["4","-2","2"]
    elif "OccupancyMap-" in plotType :
        a=["100","-100","100"]
    else :
        print 'MapType = {} is not registed. Set default range = [100,-500,500]...... '.format(plotType)
    
    return a

def check(a,b):
    if a != b:
        print "selected run are not same scan."
        sys.exit()
def diff_pixelconfig(a,b,par1,par2,h3_0,h3_1,h3_m1,h3_2,h3_m2):
    if par1 == par2 :
        h3_0.Fill(a-b)
    elif par1-par2==1 :
        h3_1.Fill(a-b)
    elif par1-par2==-1 :
        h3_m1.Fill(a-b)
    elif par1-par2==2 :
        h3_2.Fill(a-b)
    elif par1-par2==-2 :
        h3_m2.Fill(a-b)
    
def main(run_1,run_2,parName):
    #parName='TDAC'
    #args=sys.argv

    #run_1=args[1]
    #run_2=args[2]

    #temporary
    zrange=["100","-500","500"]
    #TMP_DIR="~/Desktop/Yarr-sw/LatestYarr2/src/data"

    DAT_file_1='{0}/*{1}_*/*.dat'.format(TMP_DIR,run_1) #list
    DAT_file_2='{0}/*{1}_*/*.dat'.format(TMP_DIR,run_2) #list
    Config_file_1='{0}/*{1}_*/*.before'.format(TMP_DIR,run_1)
    Config_file_2='{0}/*{1}_*/*.before'.format(TMP_DIR,run_2)

    #print Config_file_1

    __cf_1=glob.glob(Config_file_1)
    __cf_2=glob.glob(Config_file_2)

    _cf_json_1=open(__cf_1[0])
    _cf_json_2=open(__cf_2[0])

    cf_json_1=json.load(_cf_json_1)
    cf_json_2=json.load(_cf_json_2)

    #print '{}'.format(cf_json_1['FE-I4B']['PixelConfig'][0])

    print DAT_file_1,DAT_file_2

    files_1 = glob.glob(DAT_file_1)
    files_2 = glob.glob(DAT_file_2)

    information_num=8
   # print files_1
    datafile=ROOT.TFile('../root/Diff_{0}_{1}.root'.format(run_1,run_2),"recreate");
    #datafile=ROOT.TFile('../root/Diff_Plot.root',"recreate");
    #PIXEL_TREE=ROOT.TTREE("PIXEL_TREE","")

    file_count=0
    PRECANVAS=ROOT.TCanvas("PRECANVAS","")
    output_pdf='../temp/{0}_{1}.pdf'.format(run_1,run_2)
    #output_pdf='../temp/Diff_plot.pdf'
    PRECANVAS.Print('{0}['.format(output_pdf))
    for dat_file in files_1:
        information_num=8
        dat_file2 = files_2[file_count]
  #      print dat_file2
        file_count+=1
 #       print dat_file
        with open(dat_file) as f:
            with open(dat_file2) as f2:
                count = 0
                row=0
                column=0
                for f_line in f:
                    f_line2=f2.readline()
                    if count == 0:
                        Hist_Type=f_line
                        Hist_Type2=f_line2
                        check(Hist_Type,Hist_Type2)
                        if "Histo1d" in Hist_Type:
                            information_num=7
                    elif count == 1: 
                        mapType=f_line.split()
                        mapType2=f_line2.split()
                        check(mapType,mapType2)
                    elif count == 2:
                        xaxis = f_line
                        xaxis2 = f_line2
                        check(xaxis,xaxis2)
                    elif count == 3:
                        yaxis = f_line
                        yaxis2= f_line2
                        check(yaxis,yaxis2)
                    elif count == 4:
                        zaxis = f_line
                        zaxis2= f_line2
                        check(zaxis,zaxis2)
                    elif count == 5:
                        xrange = f_line.split()
                        xrange2 = f_line2.split()
                        if "Histo2d" in Hist_Type :
                            check(xrange,xrange2)
                    elif count == 6 and ("Histo2d" in Hist_Type):
                        yrange = f_line.split()
                        yrange2 = f_line2.split()
                        check(yrange,yrange2)
                    if count >= information_num:
                        par_pixels = f_line
                        par_pixels2= f_line2
                        if count == information_num : 
                            if "Histo1d" in Hist_Type:
                                h=ROOT.TH1F(mapType[0],mapType[0]+";"+"  "+xaxis+";   "+yaxis,int(xrange[0]),float(xrange[1]),float(xrange[2]))
                                h2=ROOT.TH1F(mapType[0]+"2",mapType[0]+";"+"  "+xaxis+";   "+yaxis,int(xrange[0]),float(xrange[1]),float(xrange[2]))
                                binsize=(float(xrange[2])-float(xrange[1]))/int(xrange[0])
                                if ".5" in xrange[1] :
                                    x_start=float(xrange[1])+0.5
                                else :
                                    x_start=float(xrange[1])
                            else:
                                c1=ROOT.TCanvas(mapType[0],mapType[0])
                                c2=ROOT.TCanvas(mapType[0]+"2",mapType[0]+"2")
                                c3=ROOT.TCanvas("Diff_"+mapType[0],"Diff_"+mapType[0])

                                h=ROOT.TH2F(mapType[0],mapType[0]+";"+"  "+xaxis+";   "+yaxis+";  "+zaxis,int(xrange[0]),float(xrange[1]),float(xrange[2]),int(yrange[0]),float(yrange[1]),float(yrange[2]))
                                h2=ROOT.TH2F(mapType[0]+"2",mapType[0]+";"+"  "+xaxis+";   "+yaxis+";  "+zaxis,int(xrange[0]),float(xrange[1]),float(xrange[2]),int(yrange[0]),float(yrange[1]),float(yrange[2]))
                                if int(xrange[0]) == int(xrange2[0]):
                                    c4=ROOT.TCanvas("Diff_"+mapType[0]+"_"+parName,"Diff_"+mapType[0])
                                    zrange=range_diffplot(mapType[0])
                                    h3=ROOT.TH1F("Diff_"+mapType[0],"Diff_"+mapType[0]+";"+"  "+zaxis+"; # pixels",int(zrange[0]),float(zrange[1]),float(zrange[2]))
                                    h4=ROOT.THStack("Diff_"+parName+"_"+mapType[0],"Diff_"+mapType[0])
                                    h3_0=ROOT.TH1F("Diff_"+mapType[0]+"_Diff_"+parName+"=0","Diff_"+mapType[0]+";"+"  "+zaxis+"; # pixels",int(zrange[0]),float(zrange[1]),float(zrange[2]))
                                    h3_1=ROOT.TH1F("Diff_"+mapType[0]+"_Diff_"+parName+"=1","Diff_"+mapType[0]+";"+"  "+zaxis+"; # pixels",int(zrange[0]),float(zrange[1]),float(zrange[2]))
                                    h3_m1=ROOT.TH1F("Diff_"+mapType[0]+"_Diff_"+parName+"=-1","Diff_"+mapType[0]+";"+"  "+zaxis+"; # pixels",int(zrange[0]),float(zrange[1]),float(zrange[2]))
                                    h3_2=ROOT.TH1F("Diff_"+mapType[0]+"_Diff_"+parName+"=2","Diff_"+mapType[0]+";"+"  "+zaxis+"; # pixels",int(zrange[0]),float(zrange[1]),float(zrange[2]))
                                    h3_m2=ROOT.TH1F("Diff_"+mapType[0]+"_Diff_"+parName+"=-2","Diff_"+mapType[0]+";"+"  "+zaxis+"; # pixels",int(zrange[0]),float(zrange[1]),float(zrange[2]))
                                    h3_0.SetFillColor(1)
                                    h3_1.SetFillColor(2)
                                    h3_m1.SetFillColor(3)
                                    h3_2.SetFillColor(4)
                                    h3_m2.SetFillColor(5)
                                    legend=ROOT.TLegend(0.1,0.58,0.2,0.78)
                                    legend.AddEntry(h3_0,"d_TDAC=0","f")
                                    legend.AddEntry(h3_1,"d_TDAC=1","f")
                                    legend.AddEntry(h3_m1,"d_TDAC=-1","f")
                                    legend.AddEntry(h3_2,"d_TDAC=2","f")
                                    legend.AddEntry(h3_m2,"d_TDAC=-2","f")

                            #print par_pixels2.split() 

                        row+=1
                        column=0
                        bin_num=len(par_pixels.split())
                        bin_num_2=len(par_pixels2.split())
    #                    print bin_num_2

                        for parameter,parameter2 in zip(par_pixels.split(),par_pixels2.split()):
    #                        par_list2 = par_pixels2.split()
                            column+=1
                            if "Histo2d" in Hist_Type:
                                h.Fill(column,row,float(parameter))
                                h2.Fill(column,row,float(parameter2))
                                h3.Fill(float(parameter)-float(parameter2),1)
    #                            print parameter2
                                if int(xrange[0]) == 80 and int(xrange2[0]) == 80:
                                    diff_pixelconfig(float(parameter),float(parameter2),float(cf_json_1['FE-I4B']['PixelConfig'][row-1][parName][column-1]),float(cf_json_2['FE-I4B']['PixelConfig'][row-1][parName][column-1]),h3_0,h3_1,h3_m1,h3_2,h3_m2)
                            elif "Histo1d" in Hist_Type:
                                if column-1 < bin_num :
                                    h.Fill(x_start+(column-1)*binsize,float(parameter));
                                if column-1 < bin_num_2 :
                                    h2.Fill(x_start+(column-1)*binsize,float(parameter2));

                    count += 1
                if "Histo1d" in Hist_Type:
                    continue
                 #   print "skip"
    #                c1.cd()
    #                h.Draw()
    #                c2.cd()
    #                h2.Draw()
                elif "Histo2d" in Hist_Type:
                    c1.cd()
                    h.Draw("colz")
                    h.SetOption("colz")
                    c2.cd()
                    h2.Draw("colz")
                    h2.SetOption("colz")
                    if int(xrange[0]) == int(xrange2[0]):
                        c3.cd()
                        h3.Draw()
                        h3.Write()
                        c4.cd()
                        h4.Add(h3_0)
                        h4.Add(h3_1)
                        h4.Add(h3_m1)
                        h4.Add(h3_2)
                        h4.Add(h3_m2)
                        h3.Draw()                    
                        h4.Draw("same")
                        h4.Write()
                        legend.Draw()
                        c4.Print(output_pdf)
                h.Write()
                h2.Write()
               # print count
    PRECANVAS.Print('{0}]'.format(output_pdf))

if __name__=="__main__":
    args=sys.argv
    main(args[1],args[2],args[3])
