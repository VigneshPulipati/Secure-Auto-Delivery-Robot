#!/usr/bin/env python3

import cv2

try:
    from pyzbar.pyzbar import decode
except ImportError:
    decode = None


class QRScanner:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index
        self.camera = None

    def start(self):

        self.camera = cv2.VideoCapture(
            self.camera_index
        )

        if not self.camera.isOpened():

            raise RuntimeError(
                "Unable to open camera."
            )

    def scan(self):

        if self.camera is None:

            raise RuntimeError(
                "Camera has not been started."
            )

        success, frame = self.camera.read()

        if not success:

            return None, frame

        if decode is None:

            return None, frame

        qr_codes = decode(frame)

        for qr in qr_codes:

            try:
                data = qr.data.decode("utf-8")
            except UnicodeDecodeError:
                continue

            return data, frame

        return None, frame

    def release(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None

        cv2.destroyAllWindows()


def main():

    scanner = QRScanner()

    try:

        scanner.start()

        print("QR scanner started.")
        print("Press Q to quit.")

        while True:

            data, frame = scanner.scan()

            if frame is not None:

                cv2.imshow(
                    "Robot QR Scanner",
                    frame
                )

            if data:

                print("QR detected:")
                print(data)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                break

    finally:

        scanner.release()


if __name__ == "__main__":
    main()
