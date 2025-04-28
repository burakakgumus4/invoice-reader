import cv2
from paddleocr import PaddleOCR


class OcrResults:
    def __init__(self, results):
        texts, boxes, scores = [], [], []
        if results[0]:
            for result in results:
                for line in result:
                    bbox = line[0]
                    text, score = line[1]
                    texts.append(text)
                    scores.append(score)
                    boxes.append(bbox)

        self.texts = texts
        self.boxes = boxes
        self.scores = scores

    def __len__(self):
        return len(self.boxes)
    
    def __iter__(self):
        return iter(zip(self.boxes, self.texts, self.scores))


class Paddle:
    def __init__(self, use_angle_cls=True, lang='en', show_log=False, use_gpu=True):
        self.reader = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, show_log=show_log, use_gpu=use_gpu)

    def convert_paddle_to_easyocr(self, results):
        easyocr_format = []
        if results:
            for result in results[0]:
                bbox = result[0]
                easyocr_bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
                text = result[1][0]
                confidence = result[1][1]
                easyocr_format.append((easyocr_bbox, text, confidence))

        return easyocr_format

    def perform_ocr(self, frame, visualize=True, class_format=True):
        results = self.reader.ocr(frame, cls=True)
        if visualize and results:
            for idx in range(len(results)):
                res = results[idx]
                for line in res:
                    box = line[0]
                    text = line[1][0]
                    score = line[1][1]
                    top_left = tuple(map(int, box[0]))
                    bottom_right = tuple(map(int, box[2]))
                    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                    cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if class_format:
            results = OcrResults(results)

        return frame, results


def run():
    ocr = Paddle()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        frame_with_ocr, result = ocr.perform_ocr(frame)
        cv2.imshow("Webcam OCR", frame_with_ocr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def image_run():
    ocr = Paddle()
    frame = cv2.imread('demo/images/6.jpg')
    if frame is None:
        print("Error: Could not load image.")
        return
    frame, result = ocr.perform_ocr(frame)
    print(result.texts)
    cv2.imshow("Image OCR", frame)
    cv2.imwrite("demo_output.jpg", frame)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
    # image_run()
