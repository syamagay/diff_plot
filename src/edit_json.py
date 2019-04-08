import json,sys,collections

def main():
    args=sys.argv
    Yarr_DIR='/home/yamagaya/Desktop/Yarr-sw/LatestYarr2/src'
    
    parName=args[1]
    par=args[2]
    scan_type=args[3]
    
    f=open('{0}/configs/scans/fei4/std_{1}.json'.format(Yarr_DIR,scan_type),'r')
    
    print f
    j=json.load(f,object_pairs_hook=collections.OrderedDict)
    
    before_par=j["scan"]["prescan"][parName]
    
    j["scan"]["prescan"][parName]=int(par)
    
    print('{}'.format(json.dumps(j,indent=4)))
    
    fw=open('{0}/configs/scans/fei4/std_{1}.json'.format(Yarr_DIR,scan_type),'w')
    json.dump(j,fw,indent=4)
    print before_par
    
if __name__=="__main__":
    main()
    
    
