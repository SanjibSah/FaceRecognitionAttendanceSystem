import face_recognition
import numpy as np
import cv2
import os

from Attendence_System import settings

def FaceEncoding(path, label):
	img = face_recognition.load_image_file(path)
	img_encoding = face_recognition.face_encodings(img)[0]
	

	embed_filepath = os.path.join(settings.EMBEDDING_ROOT, 'embed_data.csv')
	label_filepath = os.path.join(settings.EMBEDDING_ROOT, 'label_data.csv')
	
	with open(embed_filepath, "ab") as f:
		np.savetxt(f, [img_encoding], delimiter=',')

	with open(label_filepath, "ab") as f:
		np.savetxt(f, [label], delimiter=',')	


def Recognizer(details):
	video = cv2.VideoCapture(0)

	known_face_encodings = []
	known_face_names = []
	names = []


	embed_filepath = os.path.join(settings.EMBEDDING_ROOT, 'embed_data.csv')
	label_filepath = os.path.join(settings.EMBEDDING_ROOT, 'label_data.csv')

	with open(embed_filepath, "rb") as f:
		known_face_encodings = np.loadtxt(f, delimiter=',')

	with open(label_filepath, "rb") as f:
		known_face_names = np.loadtxt(f, delimiter=',')	

	

	face_locations = []
	face_encodings = []


	while True:	
	
		check, frame = video.read()
		small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5)
		rgb_small_frame = small_frame[:,:,::-1]

		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
		
		face_names = []
		
		

		for face_encoding in face_encodings:

			matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

			face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)	
			
			try:
				matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

				face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
				best_match_index = np.argmin(face_distances)

				if matches[best_match_index]:
					name = known_face_names[best_match_index]

					face_names.append(str(int(name)))
					if name not in names:
						names.append(str(int(name)))
			except:
				pass

		if len(face_names) == 0:
			for (top,right,bottom,left) in face_locations:
				top*=2
				right*=2
				bottom*=2
				left*=2

				cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

				# cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
		else:
			for (top,right,bottom,left), name in zip(face_locations, face_names):
				top*=2
				right*=2
				bottom*=2
				left*=2

				cv2.rectangle(frame, (left,top),(right,bottom), (0,255,0), 2)

				# cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, name, (left, top), font, 0.8, (255,255,255),1)

		cv2.imshow("Face Recognition Panel",frame)

		if cv2.waitKey(1) == ord('s'):
			break

	video.release()
	cv2.destroyAllWindows()
	return names