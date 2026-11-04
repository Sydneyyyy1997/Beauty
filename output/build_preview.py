from pathlib import Path
import json,subprocess, shutil, wave, numpy as np
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).resolve().parent if Path(__file__).name=='build_preview.py' else Path('/workspace/output'); O.mkdir(exist_ok=True); A=O/'assets'; A.mkdir(exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
# Time-locked lines, with space for reactions and the end card. No time stretching.
lines=[(3.15,7.55,'A',"It’s always sold out! I can never get my shade."),(8.12,9.14,'B','Honestly?'),(9.30,11.14,'B','The shade range is too good.'),(11.30,12.73,'B','I can’t decide.'),(12.85,14.75,'B','So I bought two shades.'),(15.05,18.38,'C','Nothing. I love it. This is my blush today.'),(18.40,21.22,'Interviewer','Oh, it looks just like a second skin.'),(21.25,24.00,'C','Yes, but I hate waiting for a restock!')]
# Use visibly schematic boards, never simulated consumer footage.
def text(d,xy,t,size=42,color='#f4eee8',bold=False):
 d.text(xy,t,font=ImageFont.truetype(FB if bold else F,size),fill=color)
def board(n,title,desc,skin='#af795f',coat='#998079'):
 im=Image.new('RGB',(1080,1920),'#20252b');d=ImageDraw.Draw(im)
 for x,h in [(0,660),(240,760),(520,620),(790,730)]:
  d.rectangle((x,330,x+220,330+h),fill='#333c43');d.rectangle((x+25,390,x+195,650),fill='#53636a')
 d.rectangle((0,1050,1080,1920),fill='#292d33')
 text(d,(70,80),'STREET BEAUTY / RHYTHM STUDY',29,'#d5c4ba',True)
 # Disclosure is added as a fixed overlay by render.py.
 text(d,(70,230),title,58,bold=True)
 if n in [1,2,3,4]:
  # Flat cutout bust with no face or lip-sync claim.
  d.ellipse((355,470,730,950),fill='#29252a');d.ellipse((395,545,690,935),fill=skin)
  d.rounded_rectangle((270,930,810,1450),radius=130,fill=coat)
  d.rectangle((950,1060,1080,1110),fill='#b99c83');d.line((915,1060,770,925),fill='#b5b8ba',width=30);d.ellipse((715,860,815,970),fill='#13161a')
  if n==3:
   for x in (390,540):d.rounded_rectangle((x,1150,x+75,1340),radius=15,fill='#c5aea0')
   text(d,(300,1390),'UNLABELED PROP PLACEHOLDERS',23)
  if n==4:d.ellipse((595,755,660,800),fill='#c88186')
  if n==1:d.rectangle((150,1170,310,1370),fill='#cabda6');d.arc((170,1110,290,1230),180,360,fill='#cabda6',width=10)
 else:
  d.rounded_rectangle((100,680,980,1100),radius=32,fill='#d7a291');text(d,(260,800),'Sold out',108,'#20252b',True)
  text(d,(245,955),'STORY GRAPHIC / NOT LIVE STOCK',27,'#20252b')
 text(d,(70,1480),desc,32,'#d7b9a8')
 text(d,(70,1780),'PLACEHOLDER VISUAL + TEMP SYNTHETIC VOICES',25,'#d7b9a8',True)
 im.save(A/f'shot{n:02}.png')
board(1,'01 / THE QUESTION','Store exit + three quick reactions')
board(2,'02 / ALWAYS SOLD OUT','A / amused frustration / medium shot','#a86c50','#bd916b')
board(3,'03 / TWO SHADES','B / hesitate, smile, raise two props','#e0b89b','#7e9693')
board(4,'04 / SECOND SKIN','C / cheek blush + off-camera interviewer','#76503f','#9e7b92')
board(5,'THE ONLY DOWNSIDE','Dramatized end card / no inventory claim')
# Basic temporary voices; not production speech.
N=25*48000; mix=np.zeros(N,dtype=np.float64); speech=[]
for i,(st,en,speaker,t) in enumerate(lines):
 p=A/f'voice{i:02}.wav'; txt=A/f'voice{i:02}.txt';txt.write_text(t.replace('’',"'"))
 voice={'A':'slt','B':'slt','C':'slt','Interviewer':'rms'}[speaker]
 run(['ffmpeg','-y','-f','lavfi','-i',f'flite=textfile={txt}:voice={voice}','-ar','48000',str(p)])
 with wave.open(str(p)) as w:a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 # Flite duration parameter changes phoneme durations during synthesis, not playback speed.
 if len(a)/48000 > en-st:
  ratio=(en-st)/(len(a)/48000)
  run(['ffmpeg','-y','-f','lavfi','-i',f'flite=textfile={txt}:voice={voice}:nb_samples=1024','-ar','48000',str(p)])
  # Keep human-readable pacing: adjust the text of long C segment above instead of squeezing audio.
 speech.append({'start':st,'end':en,'speaker':speaker,'text':t,'actual_duration':len(a)/48000})
 print(i,round(len(a)/48000,3),'slot',en-st,flush=True)
 idx=round(st*48000)
 if idx+len(a)>N:raise ValueError('Voice exceeds timeline')
 if len(a)/48000>en-st+0.12: print('NEEDS_TIMING_ADJUSTMENT',i,flush=True)
 mix[idx:idx+len(a)]+=a*.85
# Original generated instrumental bed + synthetic street texture, no third-party samples.
rng=np.random.default_rng(42);t=np.arange(N)/48000
bed=np.zeros(N)
for beat in np.arange(0,25,.5):
 k=int(beat*48000); dur=min(12000,N-k);u=np.arange(dur)/48000
 bed[k:k+dur]+=.016*np.sin(2*np.pi*90*u)*np.exp(-u*35)
for k0 in np.arange(0,25,2):
 k=int(k0*48000);dur=min(96000,N-k);u=np.arange(dur)/48000
 for f in [261.63,329.63,392]:bed[k:k+dur]+=.003*np.sin(2*np.pi*f*u)*np.exp(-u*2)
noise=rng.normal(0,1,N); noise=np.convolve(noise,np.ones(100)/100,mode='same')*.018
mix+=bed+noise;mix*=np.minimum(t/0.15,1)*np.minimum((25-t)/.25,1)
with wave.open(str(A/'mix.wav'),'w') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
(O/'dialogue_timing.json').write_text(json.dumps(speech,indent=2))
def tc(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
cues=[(0,3,'What do you hate most\nabout Fenty Beauty?')]+[(s,e,tx) for s,e,sp,tx in lines]+[(24,25,'The only downside?\nGetting your hands on it.')]
# Explicit line breaks, always <=2 lines.
wraps={lines[0][3]:'It’s always sold out!\nI can never get my shade.',lines[5][3]:'Nothing. I love it.\nThis is my blush today.',lines[6][3]:'Oh, it looks just like\na second skin.',lines[7][3]:'Yes, but I hate waiting\nfor a restock!'}
(O/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{tc(s)} --> {tc(e)}\n{wraps.get(tx,tx)}' for i,(s,e,tx) in enumerate(cues))+'\n')
# ASS emphasis and safe positioning.
head='''[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,DejaVu Sans,49,&H00FFFFFF,&H000000FF,&H0020252B,&H0020252B,0,0,0,0,100,100,0,0,3,14,0,2,90,90,285,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''
def ass_tc(t):return tc(t)[:-1].replace(',','.')
for s,e,tx in cues:
 tx=wraps.get(tx,tx).replace('\n',r'\N')
 for term in ['always sold out','my shade']:tx=tx.replace(term,r'{\b1\c&H009FC9F0&}'+term+r'{\b0\c&H00FFFFFF&}')
 head+=f'Dialogue: 0,{ass_tc(s)},{ass_tc(e)},Default,,0,0,0,,{tx}\n'
(O/'subtitles.ass').write_text(head)
shutil.copy('work/build.py',O/'build_preview.py')
