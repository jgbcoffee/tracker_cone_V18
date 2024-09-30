import cv2

class VideoCaptureApp:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        # Release resources after loop ends
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    display_camera = VideoCaptureApp()
    display_camera.run()
