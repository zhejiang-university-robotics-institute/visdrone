from os.path import join
import json
import os

dataDir = '.'
for dataType in ['val2017', 'train2017']: #

    dataset = dict()
    set_img_base_path = join(dataDir,'sequences/' + dataType)
    set_ann_base_path = join(dataDir,'annotations/' + dataType )
    txtList = os.listdir(set_ann_base_path)

    for txtlist in txtList:
        videoName = txtlist.split('.')[0]
        video_crop_base_path = join(dataType, videoName)
        if len(txtList) > 0:
            dataset[video_crop_base_path] = dict()
        with open(set_ann_base_path +'/' + txtlist, 'r') as f:
            boxList = f.readlines()
            imgList = os.listdir(set_img_base_path +'/'+ videoName )
            imgList.sort()
            for imgid, img in enumerate(imgList):
                imgName = img.split('.')[0]
                rect = boxList[imgid].split(',')
                rect = [int(element) for element in rect]
                bbox = [rect[0], rect[1], rect[0]+rect[2], rect[1]+rect[3]]
                if rect[2] <= 0 or rect[3] <= 0:  # lead nan error in cls.
                    continue
                dataset[video_crop_base_path]['{}'.format(imgName.strip('img'))] = {'000000': bbox}

    print('save json (dataset), please wait 20 seconds~')
    json.dump(dataset, open('{}.json'.format(dataType), 'w'), indent=4, sort_keys=True)
    print('done!')

