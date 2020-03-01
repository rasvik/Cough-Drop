// set up basic variables for app

const record = document.querySelector('.record');
const stop = document.querySelector('.stop');
const mainSection = document.querySelector('.main-controls');
const play = document.querySelector('.play');
const continueButton = document.querySelector('.continue')
// disable stop button while not recording
//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record
stop.disabled = true;

// visualiser setup - create web audio api context and canvas
//
//let audioCtx;
//const canvasCtx = canvas.getContext("2d");

//main block for doing the audio recording
if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.');

  const constraints = { audio: true };
  let chunks = [];

  let onSuccess = function(stream) {
    audioContext = new AudioContext();

		//update the format
		//document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;

		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

    rec = new Recorder(input,{numChannels:1})

    //visualize(stream);

    record.onclick = function() {
      rec.record()
      console.log("recorder started");
      record.style.background = "red";

      stop.disabled = false;
      record.disabled = true;
    }

    stop.onclick = function() {
      rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();
      record.style.background = "";
      record.style.color = "";
      stop.disabled = true;
      record.disabled = false;
      rec.exportWAV(exportFile);
    }

    play.onclick = function(){audio.play();}

      continueButton.onclick = function(e) {
        document.location.href = "/result";
      }

function exportFile(blob) {
fetch('/uploadData', {
        method: "POST",
        body: blob
        });
}
  }

  let onError = function(err) {
    console.log('The following error occured: ' + err);
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);

} else {
   console.log('getUserMedia not supported on your browser!');
}


//window.onresize = function() {
//  canvas.width = mainSection.offsetWidth;
//}

window.onresize();