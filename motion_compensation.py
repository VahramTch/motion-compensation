import cv2
import numpy as np
import sys
import image_slicer
from PIL import Image
np.set_printoptions(threshold=sys.maxsize)

vidcap = cv2.VideoCapture('patagonia.mp4')
success,image = vidcap.read()


def sad(a,b):
    sum=0

    diff = [[0 for i in range(16)] for j in range(16)]
    
    for i in range(0,16):
        for j in range(1,16):
            diff[i][j]=abs(int(a[i][j])-int(b[i][j]))
            sum+=diff[i][j]
    return sum



def diff_frame(i,frame2,frame1):
    framediff=cv2.absdiff(frame2,frame1)
    cv2.imshow("diff_frame_%d"% i, framediff)
    print(i,"First Step Done!")


def pred(countt,frame2,frame1):
     #frame1--->reference  frame2--->target
     gframe1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
     gframe2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
     height, width = gframe2.shape
     k=16
     i_height = int(height / k)#45
     i_width = int(width /k)#80
     

     #macroblocks
     blocks = []
     x=[]
     y=[]
     blocks2 = []
     x2=[]
     y2=[]
     for x1 in range(0, i_height):
         for y1 in range(0,i_width):
             tmp_image=gframe2[int(x1*k):int((x1+1)*k), int(y1*k):int((y1+1)*k)] #x=x*k y=y*k
             blocks.append(tmp_image)
             x.append(int(x1*k))
             y.append(int(y1*k))
             tmp_image2=gframe1[int(x1*k):int((x1+1)*k), int(y1*k):int((y1+1)*k)] #x=x*k y=y*k
             blocks2.append(tmp_image2)
             x2.append(int(x1*k))
             y2.append(int(y1*k)) 

     #motion compensation   
     kappa=[]
     for i in range(len(blocks)):
         flag=0
         if np.array_equal(blocks[i],blocks2[i]):
             kappa.append(blocks[i])
             continue
         a1=x[i]-16
         b1=y[i]-16
         a2=x[i]+32
         b2=y[i]+32
         if a1<0:
             a1=0
         if b1<0:
             b1=0
         if a2>height:
             a2=height
         if b2>width:
             b2=width
             
         min=150000
         bestm=0
         bestn=0
         besta=0
         bestb=0
         
         for m in range(a1,a2):
             if flag==1:continue
             for n in range(b1,b2):
                 az=m+16
                 bz=n+16
                 
                 if az>a2 or bz>b2 :
                     flag=1
                     break

                 candfr1=gframe1[m:az,n:bz]
                 p=sad(candfr1,blocks[i])

                 if p < min:
                      min=p
                      bestm=m
                      bestn=n
                      besta=az
                      bestb=bz
             
         
         kappa.append(gframe1[bestm:besta,bestn:bestb])


     vis=[0 for i in range(i_height)]
     for j in range(i_height):
         vis[j]=kappa[0]
         for i in range(i_width):
              vis[j]=np.hstack((vis[j],kappa[(j-1)*i_width+i]))
              
         
     hor=vis[0]
     for i in range(len(vis)):
         hor=np.vstack((hor,vis[i]))


     cv2.imshow("error_frame_%d"% countt, hor)     
     print(countt,"Second Step Done!")

     
count=0
while success:
  success,image = vidcap.read()

  if count==71:
      diff_frame(count,image,Previousimage)
      pred(count,image,Previousimage)

  


  count=count+1
  Previousimage=image  

print("# of frames:",count)
