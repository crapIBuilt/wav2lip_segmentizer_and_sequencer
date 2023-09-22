#use this to add chunks to asset files: ffmpeg -i asmongold.mp4 -segment_time 00:00:15 -f segment -reset_timestamps 1 %03d.mp4
from time import sleep
from pydub import AudioSegment
from natsort import os_sorted
import os
import sys
import glob
import random
import ffmpeg

person = sys.argv[0]
base_path = str(os.getcwd())
wav_file = base_path + '/input/audio.wav'
remove_old = 'rm ' + base_path + '/clips/content.txt'
os.system(remove_old)
temp_mv = 'mv audio.wav ' + wav_file
os.system(temp_mv)
popcoin = 'rm ' + base_path + '/clips/' + '*.mp4'
os.system(popcoin)
del_p = base_path + '/clips/*.mp4'
os.system(del_p)

def get_duration_ffmpeg(dur_file_path):
   probe = ffmpeg.probe(dur_file_path)
   stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
   duration = float(stream['duration'])
   return duration
if (person == 'asmongold'):
  asmon_path = base_path + '/asmon/'
  files = os.listdir(asmon_path)
  file_chose = str(random.choice(files))
  directory = '/asmon/'
video_file = base_path + '/' + directory + '/' + file_chose
ckpt_path = base_path + '/wav2lip.pth'
os.system('echo Y | rm *.wav && echo Y | rm *.mp4')

aud_dur = float(get_duration_ffmpeg(wav_file))
vidd = base_path + '/asmon/*.mp4'
files = glob.glob(vidd)
video = files
random.shuffle(video)
vids_to_use = []
onk = 0
video_durations = []
while (aud_dur > 0.05):
  dur_file_path = video[onk]
  dur = float(get_duration_ffmpeg(dur_file_path))
  dur2 = float(get_duration_ffmpeg(dur_file_path)) * 1000
  video_durations.append(dur2)
  aud_dur -= dur
  vids_to_use.append(dur_file_path)
  onk += 1
cur_time = 0.000
starts = []
ends = []
incc = 0
for t in video_durations:
  tt = float(t)
  toil = float(t)
  if (incc > 0):
    longg = cur_time + 0.0001
    starts.append(str(longg))
  else:
    starts.append(str(cur_time))
  cur_time += tt
  ends.append(str(cur_time))
  incc += 1
i = 0
finished_clips = []
content_path = base_path + '/clips/content.txt'
file1 = open(content_path, "a")
for x in starts:
  ppp = float(ends[i])
  namme = str(i) + '.wav'
  ppppp = float(x)
  pppp = vids_to_use[i]
  wavv = AudioSegment.from_mp3(wav_file)
  extract = wavv[ppppp:ppp]
  extract.export(namme, format="wav")
  i += 1
check_path = base_path + '/results/result_voice.mp4'
increment = 0
for bgh in vids_to_use:
  audio = str(increment) + '.wav'
  wav2lip2 = 'conda run -n wav2lip python inference.py --checkpoint_path ' + ckpt_path + ' --face ' + bgh + ' --audio ' + audio
  os.system(wav2lip2)
  check_file = os.path.isfile(check_path)
  while (check_file == False):
    wav2lip2 = 'conda run -n wav2lip python inference.py --checkpoint_path ' + ckpt_path + ' --face ' + bgh + ' --audio ' + audio
    os.system(wav2lip2)
  poth = 'mv ' + base_path + '/results/result_voice.mp4 ' + base_path + '/clips/' + str(increment) + '.mp4'
  os.system(poth)
  print(wav2lip2)
  finished_clips00 = "file '" + base_path + "/clips/" + str(increment) + ".mp4'"
  file1.write(finished_clips00)
  file1.write("\n")
  increment += 1
file1.close()
merger_comm = 'cd clips && ffmpeg -f concat -safe 0 -i content.txt -reset_timestamps 1 output.mp4'
os.system(merger_comm)
final_move = 'mv ' + base_path + '/clips/output.mp4 ' + base_path + '/output_joined.mp4'
os.system(final_move)
