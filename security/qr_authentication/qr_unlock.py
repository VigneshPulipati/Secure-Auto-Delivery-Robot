import cv2
import json
from pyzbar.pyzbar import decode
from servo_control import open_box, close_box

DATABASE_FILE = "delivery_database.json"

# Load database
def load_database():
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

database = load_database()

cap = cv2.VideoCapture(0)

print("Robot ready. Waiting for QR...")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        break

    qr_codes = decode(frame)

    for qr in qr_codes:

        delivery_id = qr.data.decode('utf-8')

        print("Scanned:", delivery_id)

        if delivery_id in database:

            print("Valid delivery")

            open_box()
            close_box()

            database[delivery_id]["status"] = "delivered"

            with open(DATABASE_FILE, "w") as f:
                json.dump(database, f, indent=4)

        else:

            print("Invalid QR")

    cv2.imshow("QR Scanner", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
