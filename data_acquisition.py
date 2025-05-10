#!/usr/bin/env python


import csv
import numpy as np
import cv2
import rtde_receive

class DataAcquisition:
    def __init__(self, image_capture, rtde_r, counter=0):
        self.counter = counter
        self.image_capture = image_capture
        self.rtde_r = rtde_r
        self.joint_list = []

    def perform_data_acquisition(self):
        key = 0
        while key != 27: # ESC key
            image = self.image_capture()
            cv2.imshow("Image", image)
            key = cv2.waitKey(10)
            if key == 115: # 's' key
                print( "Saving image: ", str(self.counter))
                cv2.imwrite(str(self.counter).zfill(4) + ".png", image)
                actual_tcp_pose = self.rtde_r.getActualTCPPose()
                self.joint_list.append(actual_tcp_pose)
                with open('robot_poses.csv', mode='w') as joint_file:
                    joint_writer = csv.writer(joint_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for row in self.joint_list:
                        joint_writer.writerow(row)
                self.counter += 1
        
