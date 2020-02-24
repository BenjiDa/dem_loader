
import os
import math
import lxml
import ftplib

'''function to download all .laz files in .txt file downloaded from the National Map viewer.
This is ment to expidite the download procedure if you have many separate files you need to view. 
Depending how many files this can take quite a while.'''


f = open('cartExport_20200221_110640_2.txt', "r")
lines = f.readlines()
for line in lines:

    file = line[116:166] #just select the .laz file name
    print(file)
    ftp = ftplib.FTP('rockyftp.cr.usgs.gov') # Root of USGS ftp server
    ftp.login()
    ftp.cwd('/vdelivery/Datasets/Staged/Elevation/LPC/Projects/USGS_LPC_CA_NoCAL_Wildfires_B2_2018/laz/') #laz file directory
    ftp.retrbinary('RETR '+ file ,open(file,'wb').write, 1024) 
    
f.close()
ftp.quit()