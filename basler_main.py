from pypylon import pylon
import cv2
import rtde_receive
import data_acquisition

class PylonImageCapture:
    def __init__(self):
        self.pylon_camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.pylon_camera.Open()

        self.pylon_camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        grab_result = self.pylon_camera.RetrieveResult(200, pylon.TimeoutHandling_ThrowException)
        grab_result.Release()
        self.pylon_camera.StopGrabbing()

    def capture_image(self):
        self.pylon_camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        grab_result = self.pylon_camera.RetrieveResult(200, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
                print( grab_result.Array.shape )
                img = grab_result.Array
                img = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            raise Exception("Image capture failed")

        self.pylon_camera.StopGrabbing()
        grab_result.Release()

        return img
    

def main():
    rtde_r = rtde_receive.RTDEReceiveInterface("172.28.60.10")
    image_capture = PylonImageCapture()
    data_collector = data_acquisition.DataAcquisition(image_capture.capture_image, rtde_r, "basler_data/")
    data_collector.perform_data_acquisition()


if __name__ == "__main__":
    main()


