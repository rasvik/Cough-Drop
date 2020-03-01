import numpy as np
from flask import Flask, redirect, url_for, render_template, request, jsonify
import librosa
from keras.models import load_model
import tensorflow as tf
import os, shutil
from scipy.io import wavfile as wav
import wave
from keras.models import Sequential

app = Flask(__name__)

model = load_model("coughDetectV1.h5")
model._make_predict_function()
graph = tf.get_default_graph()
currentDiagnosis= 39;
@app.route("/")
def home():
	return render_template('index.html')


@app.route('/uploadData', methods=['POST'])
def uploadData():
	print("heyoooo")

	f = open('./file.wav', 'wb')
	f.write(request.data)
	f.close()
	#print(request.data)
	#print(request.headers)
	#print(request.files)

	#print(request.view_args)
	#with open('file.wav', 'wb') as f:
	#	f.write(request.data)
	#rate, data = wav.read('file.wav')
	#wav.write('file2.wav', rate, data)

	currentDiagnosis = preprocess_voice("file.wav")
	print(currentDiagnosis)
	return "Success"

@app.route('/result')
def result():
	ndata = {'result': str(preprocess_voice("file.wav"))}
	print(ndata)

	return render_template('result.html', data = ndata)

def preprocess_voice(filename):
	x, sr = librosa.load(filename, sr=16000)
	print(x)
	print("ASDFGYUIUYTRFDESDFGHJK")
	if os.path.exists('temp_events'):
		shutil.rmtree('temp_events')
	split_silence = librosa.effects.split(x, top_db=20)
	running_average = []
	n=0
	for clip in split_silence:
		mfcc = []
		if len(x[clip[0]:clip[1]]) > 3000:
			if not os.path.exists('temp_events'):
				os.mkdir('temp_events')
			librosa.output.write_wav('temp_events/event_'+str(n)+'.wav', x[clip[0]:clip[1]], 16000)
			for k in librosa.feature.mfcc(x[clip[0]:clip[1]], sr=sr, n_mfcc=20):
				mfcc.append(np.mean(k))

			#print(np.array(mfcc))
			#print(np.array(mfcc).reshape(20, 1))
			#print(np.array(mfcc).reshape(20, 1).T)
			mfcc = np.array(mfcc)
			print(mfcc.shape)
			global graph
			with graph.as_default():
				running_average.append(model.predict(mfcc.reshape(20, 1).T))
			n+=1
	print(running_average)
	avg_val = sum(running_average)/len(running_average)
	maxval = max(running_average)
	print(avg_val, maxval)
	running_average = []
	return maxval[0][0]
if __name__ == "__main__":
	app.run(debug=True)
