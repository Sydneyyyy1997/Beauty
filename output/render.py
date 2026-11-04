#!/usr/bin/env python3
"""Run from any directory: python render.py [--final]. FFmpeg required.
Optional replacements: media/shot01.mp4 (3s), shot02.mp4 (5s), shot03.mp4 (7s), shot04.mp4 (9s), shot05.mp4 (1s); media/mix.wav (25s).
All source footage should be clean, without subtitles; audio from clips is ignored.
"""
from pathlib import Path
import subprocess,sys
O=Path(__file__).resolve().parent;W=O/'render_work';W.mkdir(exist_ok=True)
final='--final' in sys.argv;media=O/'media';assets=O/'assets'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
if final and not (all((media/f'shot{i:02}.mp4').exists() for i in range(1,6)) and (media/'mix.wav').exists()):raise SystemExit('Final export requires all five replacement shots and final mix.wav.')
for i,d in enumerate([3,5,7,9,1],1):
 p=media/f'shot{i:02}.mp4'; inp=['-i',str(p)] if p.exists() else ['-loop','1','-i',str(assets/f'shot{i:02}.png')]
 vf='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30'
 if not p.exists():vf+=",scale=1102:1960,crop=1080:1920:x='11+5*sin(t*1.7)':y='20+4*cos(t*1.4)'"
 run(inp+['-t',str(d),'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(W/f'{i}.mp4')])
(W/'concat.txt').write_text(''.join(f"file '{W/i}'\n" for i in ['1.mp4','2.mp4','3.mp4','4.mp4','5.mp4']))
mix=media/'mix.wav';mix=mix if mix.exists() else assets/'mix.wav'
# Always include the dramatization disclosure, including on final footage.
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
vf=f"ass='{O/'subtitles.ass'}',drawtext=fontfile='{font}':text='AI-generated dramatization':fontsize=28:fontcolor=white:box=1:boxcolor=black@0.65:x=70:y=135"
run(['-f','concat','-safe','0','-i',str(W/'concat.txt'),'-i',str(mix),'-vf',vf,'-t','25','-r','30','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(O/('final.mp4' if final else 'preview.mp4'))])
print('Export complete')
