import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage.filters import uniform_filter

def local_variation_coefficient(arr, r1, r2):
    c1 = uniform_filter(arr, (r1, r2))
    c2 = uniform_filter(arr**2, (r1, r2))
    valid_cell = np.where(((c2 - c1**2) > 0) & (c1 != 0.0))
    c3 = np.zeros_like(c1)
    c3[valid_cell] = (((c2[valid_cell] - c1[valid_cell]**2)**0.5)/c1[valid_cell])
    return c3

def main():

        ## read image as float32
        imgTmp0 = cv2.imread('crop_img.tif',-1)
        imgTmp32 = imgTmp0.astype(np.float32)

        ## constants
        row = imgTmp0.shape[0]
        col = imgTmp0.shape[1]
        r1 = 3
        r2 = 3
        threshold = 0.8

        #######################################################################
        ########################## FPGAで実行する処理 ##########################
        #######################################################################

        nflg = 0
        for i in range(0,row-(r1-1)):
            for j in range(0,col-(r2-1)):
                imgCrp = imgTmp32[slice(i,i+r1),slice(j,j+r2)]
                c1 = np.mean(imgCrp)
                c2 = np.mean(imgCrp**2)
                c3 = ((c2 - c1**2)**0.5)/c1
                flg = c3 - threshold > 0
                nflg = nflg + flg
        
        print('Number of objects detected =', nflg)
        
        #######################################################################
        #######################################################################

        ## Ship detection
        wk_rsd = np.zeros_like(imgTmp32).astype(np.float32)
        wk_bin = np.zeros_like(imgTmp32).astype(np.uint8)

        ## compute relative standard deviation (=local variation coefficient)
        wk_rsd = local_variation_coefficient(imgTmp32,r1,r2)
    
        ## detection by constatnt thresholding
        i_detect = np.where(wk_rsd >= threshold)
        wk_bin[i_detect] = 255 # stored as uint8

        ## save binarized image
        cv2.imwrite('bin_img' + '.tif',wk_bin)

        print('Number of objects detected =', (np.array(i_detect, dtype=np.int32)).shape[1])

        # ## label connected compoents
        # label = cv2.connectedComponentsWithStats(wk_bin)
        # n = label[0] - 1 # label number (*label[0] is background so do not count)
        # cog = np.delete(label[3], 0, 0) # delete cog of label[0]
        
        # print('Number of objects detected =', n)
        
        fig = plt.figure(figsize=(14,7))
        ax = fig.add_subplot(121)
        plt.imshow(np.uint8(imgTmp0/np.max(imgTmp0)*255),cmap=plt.cm.gray)
        plt.title('Original image')
        plt.xlabel('Range cell')
        plt.ylabel('Azi1muth cell')
        ax = fig.add_subplot(122)
        plt.imshow(wk_bin,cmap=plt.cm.gray)
        plt.title('Binary image')
        plt.xlabel('Range cell')
        plt.ylabel('Azimuth cell')
        plt.show()

if __name__ == '__main__':

    main()
