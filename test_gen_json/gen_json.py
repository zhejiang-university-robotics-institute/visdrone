import os
import json

# Delete list_file.txt generated last time before using

class VOT:
    def __init__(self, dataDir=None):
        self.topDir = dataDir
        
        self.cameraMotion, self.illumChange, self.motionChange = dict(), dict(), dict()
        self.sizeChange, self.occlusion = dict(), dict()
        self.gtRect, self.imgNames, self.videoDir, self.initRect = dict(), dict(), dict(), dict()
    
    def fileName(self):
        path_list = os.listdir("{}/initialization".format(self.topDir))
        path_name = []
        for file in path_list:
            path_name.append(file.split(".")[0])
            
        for file_name in path_name:
            with open("list_file.txt", "a") as f:
                f.write(file_name + '\n')
            f.close()
            
    def readVideoNames(self):
        with open("list_file.txt", "r") as f:
            names = f.read().splitlines()
        f.close()
        return names
    
    def loadAnns(self):
        gtRect, videoDir, initRect = {}, {}, {}
        names = self.readVideoNames()
        for name in names:
            gtRect[name] = []
            with open("{}/initialization/{}.txt".format(self.topDir, name), "r") as f:
                videoDir[name] = name
                for line in f:
                    line = line.strip()
                    bBox =[x for x in line.split(",")]
                    for i in range(len(bBox)):
                        bBox[i] = float(bBox[i])
                    bBox = [bBox[0], bBox[1], bBox[0], bBox[1]+bBox[3]-1, bBox[0]+bBox[2]-1, bBox[1]+bBox[3]-1, 
                            bBox[0]+bBox[2]-1, bBox[1]]
                    gtRect[name].append(bBox)
            initRect[name] = gtRect[name][0]
            f.close()
        #self.gtRect = gtRect
        self.videoDir = videoDir
        self.initRect = initRect
    
    def getImgNames(self):
        imgNames = {}
        #imgNames, cameraMotion, illumChange, motionChange, sizeChange, occlusion = {}, {}, {}, {}, {}, {}
        names = self.readVideoNames()
        for name in names:
            path_list = os.listdir("{}/sequences/{}".format(self.topDir, name))
            path_list.sort()
            imgNames[name] = []
            #cameraMotion[name] = []
            #illumChange[name] = []
            #motionChange[name] = []
            #sizeChange[name] = []
            #occlusion[name] = []
            for file in path_list:
                imgNames[name].append("sequences/{}/{}".format(name, file))
                #cameraMotion[name].append(0)
                #illumChange[name].append(0)
                #motionChange[name].append(0)
                #sizeChange[name].append(0)
                #occlusion[name].append(0)
        self.imgNames = imgNames
        #self.cameraMotion = cameraMotion
        #self.illumChange = illumChange
        #self.motionChange = motionChange
        #self.sizeChange = sizeChange
        #self.occlusion = occlusion

def main():
    dataDir = '.'
    dataType = 'VOT2018-LT'
    dataset = VOT(dataDir)
    dataset.fileName()
    dataset.loadAnns()
    dataset.getImgNames()
    names = dataset.readVideoNames()
    #tags = ["video_dir", "init_rect", "img_names", "gt_rect", "camera_motion", "illum_change", 
    #        "motion_change", "size_change", "occlusion"]
    jsonFile = dict()
    for name in names:
        dt = dict()
        dt["video_dir"] = dataset.videoDir[name]
        dt["init_rect"] = dataset.initRect[name]
        dt["img_names"] = dataset.imgNames[name]
        '''
        dt["gt_rect"] = dataset.gtRect[name]
        dt["camera_motion"] = dataset.cameraMotion[name]
        dt["illum_change"] = dataset.illumChange[name]
        dt["motion_change"] = dataset.motionChange[name]
        dt["size_change"] = dataset.sizeChange[name]
        dt["occlusion"] = dataset.occlusion[name]
        '''
        jsonFile[name] = dt
    json.dump(jsonFile, open('{}.json'.format(dataType), 'w'))
    print('done!')
    
if __name__ == '__main__':
    main()