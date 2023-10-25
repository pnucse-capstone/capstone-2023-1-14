#detect_and_track.py
from ultralytics import YOLO
from typing import List, Dict
import supervision as sv    # 0.13.0 version
import cv2
import os

MODEL = "runs/detect/train5/weights/best.pt"
# MODEL = "yolov8s.pt"
CLASS_ID = [1, 2, 3, 4, 5, 6, 7]  # class_ids of interest


def detections_to_txt(file_name: str, detections: sv.Detections, CLASS_NAMES_DICT) -> None:
    """
    input: detections of a single frame
    opens a txt file with append mode and add/write
    every new detection on a new line
    """
    # If the file doesn't exist, create and open it for writing
    if not os.path.exists(file_name):               
        open(file_name, 'w').close() 

    # opens the file with 'append' mode
    with open(file_name, 'a') as file:

        for i in range(len(detections)):
            line = f''
            confidence = detections.confidence[i] if detections.confidence is not None else None
            class_id = detections.class_id[i] if detections.class_id is not None else None
            tracker_id = detections.tracker_id[i] if detections.tracker_id is not None else None
            
            if tracker_id is not None:
                line += f'Tracker ID: {tracker_id}'  
            if class_id is not None:
                line += f', Class: {CLASS_NAMES_DICT[class_id]}'  
            if confidence is not None:
                line += f', Confidence: {confidence:.2f}'  
            
            print(line)
            file.write(line + '\n')
  
def detections_list(detections:sv.Detections, CLASS_NAMES_DICT) -> List[Dict]:

    detect_list = []
    
    for i in range(len(detections)):
        # create a dictionary variable that will contain the info of one detected object
        detect_dict = {}
        
        confidence = detections.confidence[i] if detections.confidence is not None else None
        class_id = detections.class_id[i] if detections.class_id is not None else None
        tracker_id = detections.tracker_id[i] if detections.tracker_id is not None else None

        if tracker_id is not None:       
            detect_dict['Track ID: '] = tracker_id
        if class_id is not None:       
            detect_dict['Class: '] = CLASS_NAMES_DICT[class_id]
        if confidence is not None:
            detect_dict['Confidence: '] = confidence
           
        detect_list.append(detect_dict)
    
    return detect_list

def process_video_frame(video_path, output_video_path, output_text_file):
    model=YOLO(MODEL)
    model.fuse()
    CLASS_NAMES_DICT = model.model.names

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")
    
    # create output video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'Mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))
    
    # create VideoInfo, ByteTracker and BoxAnnotator instance
    video_info = sv.VideoInfo.from_video_path(video_path)    
    byte_tracker = sv.ByteTrack(track_thresh=0.15, match_thresh= 0.2, frame_rate=video_info.fps)
    box_annotator = sv.BoxAnnotator()
    
    # initial setting of variables
    count = 0
    detections = sv.Detections.empty()
    labels = []

    try:
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # Check if it was successfully read
            if not ret:
                break
            
            # frame sampling: applying YOLO model once every n frames
            count += 1        
            if count % 6 == 1: 
                # model prediction on single frame and conversion to supervision Detections
                results = model(frame)[0]
                
            # converting the Yolo detections to a supervision's object Detections 
            detections = sv.Detections.from_ultralytics(results)
            
            # filter detections           
            filtered_detections = sv.Detections.empty()
            for i in range(len(detections)):
                if detections[i].class_id in CLASS_ID:
                    filtered_detections = sv.Detections.merge([filtered_detections, detections[i]])
                else: continue
                
            # tracking detections
            filtered_detections = byte_tracker.update_with_detections(detections=filtered_detections)
            
            labels = [
                f"{CLASS_NAMES_DICT[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _ in filtered_detections
            ]
            # annotate and write frame
            frame = box_annotator.annotate(scene=frame, detections=filtered_detections, labels=labels)
            detect_list = detections_list(filtered_detections, CLASS_NAMES_DICT)
  
           # 저장 및 출력
            out.write(frame)
            detections_to_txt(output_text_file, filtered_detections, CLASS_NAMES_DICT)
            yield frame , detect_list

    finally:
        # Release the video capture object and close any OpenCV windows
        cap.release()
        out.release()

