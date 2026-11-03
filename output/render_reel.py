"""Original brush illustrations, Pillow animation and FFmpeg H.264 encoding."""
from pathlib import Path
import argparse, math, subprocess, json
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT=Path('/usr/share/fonts/truetype/open-sans')
BG='#FBF6EF'; INK='#463936'; PINK='#E9C8CB'; MUTED='#816B65'
W,H=540,960
SCENES=[(0,3),(3,6),(6,12),(12,17),(17,22),(22,25)]
def font(s,b=False): return ImageFont.truetype(str(FONT/('OpenSans-Semibold.ttf' if b else 'OpenSans-Regular.ttf')),s)
def txt(d,text,y,size=27,color=INK,b=False):
    for line in text.split('\n'):
        box=d.textbbox((0,0),line,font=font(size,b)); d.text(((W-(box[2]-box[0]))/2,y),line,font=font(size,b),fill=color); y+=size*1.4

def brush(kind):
    im=Image.new('RGBA',(200,430)); d=ImageDraw.Draw(im)
    # Distinct silhouettes: broad powder dome, narrow tapered blender, angled blush.
    cx=100
    d.rounded_rectangle((87,195,113,405),radius=12,fill='#C69A8F')
    d.rounded_rectangle((91,210,96,390),radius=2,fill='#E0BEB3')
    d.rounded_rectangle((83,153,117,220),radius=5,fill='#C5A087')
    for y in (160,167,211):d.line((84,y,116,y),fill='#E9D3BE',width=2)
    if kind==0:
        d.polygon([(83,167),(56,105),(55,62),(65,35),(85,19),(112,17),(136,32),(146,58),(145,105),(117,167)],fill='#705A50')
        d.ellipse((55,17,146,107),fill='#887167')
    elif kind==1:
        d.polygon([(83,164),(77,94),(81,58),(91,34),(102,27),(115,44),(123,77),(119,125),(117,164)],fill='#81695E')
        d.ellipse((81,28,120,85),fill='#998176')
    else:
        d.polygon([(83,166),(58,99),(61,64),(128,25),(145,44),(145,95),(117,166)],fill='#86665F')
        d.polygon([(61,64),(128,25),(142,41),(137,65),(65,99)],fill='#B28C83')
    # Fine bristle strokes remain illustrative rather than photorealistic claims.
    for x in range(85,117,5): d.line((x,110,x+(x-100)//3,151),fill='#AD9385',width=1)
    return im
BRUSHES=[brush(i) for i in range(3)]
def frame(t):
    idx=next(i for i,(a,b) in enumerate(SCENES) if a<=t<b)
    a,b=SCENES[idx]; u=(t-a)/(b-a)
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.ellipse((-130,200,420,760),fill='#F4E3DF')
    d.ellipse((360,-120,660,190),fill='#F0DEDA')
    txt(d,'B E A U T Y   /   B A S I C S',100,14,MUTED,True)
    # Animated entrance: lift and dissolve all scene content into the cream canvas.
    content=Image.new('RGBA',(W,H)); c=ImageDraw.Draw(content)
    if idx in (0,1,5):
        titles={0:('New to makeup?',"Don’t buy a full brush\nset just yet."),1:('Start with these','3 essentials.'),5:('Save this beginner','brush guide!')}
        title,sub=titles[idx];txt(c,title,185,32,INK,True);txt(c,sub,235,29,INK,True)
        for k in range(3):
            size=(130,280); art=BRUSHES[k].resize(size,Image.Resampling.LANCZOS)
            art=art.rotate((-12,0,12)[k]+math.sin(t*.9+k)*1.5,resample=Image.Resampling.BICUBIC)
            content.alpha_composite(art,(65+k*140,375+int(5*math.sin(t+k))))
        txt(c,'A small kit. A confident start.',717,18,MUTED)
        if idx==5:
            c.rounded_rectangle((145,783,395,830),radius=24,fill=INK)
            txt(c,'SAVE FOR LATER',795,16,'#FBF6EF',True)
    else:
        k=idx-2
        titles=['Fluffy Powder\nBrush','Blending Eyeshadow\nBrush','Blush Brush']
        desc=['For setting powder.','For soft, seamless\nblending.','For a natural flush\nof color.']
        txt(c,f'0{k+1}  /  THE ESSENTIALS',176,16,MUTED,True)
        txt(c,titles[k],218,30,INK,True)
        scale=1+.06*u
        art=BRUSHES[k].resize((int(155*scale),int(335*scale)),Image.Resampling.LANCZOS)
        art=art.rotate(-9+5*u,resample=Image.Resampling.BICUBIC,expand=True)
        content.alpha_composite(art,((W-art.width)//2,355-int(u*9)))
        txt(c,desc[k],721,24,INK)
        txt(c,'BRUSH SHAPE ILLUSTRATION',807,11,MUTED)
    ease=1-(1-min(1,(t-a)/.45))**3
    content=Image.Image.transform(content,content.size,Image.Transform.AFFINE,(1,0,0,0,1,-int((1-ease)*22)))
    alpha=min(1,(t-a)/.28,(b-t)/.18)
    content.putalpha(content.getchannel('A').point(lambda p:int(p*max(0,alpha))))
    im.paste(content,(0,0),content)
    d=ImageDraw.Draw(im)
    d.line((60,869,480,869),fill='#E6D7D0',width=2)
    d.line((60,869,60+int(420*t/25),869),fill='#AD7D7B',width=3)
    txt(d,'BEGINNER BRUSH GUIDE',891,11,MUTED)
    return im

def main():
    p=argparse.ArgumentParser(); p.add_argument('--width',type=int,default=1080);p.add_argument('--fps',type=int,default=30);p.add_argument('--output',type=Path,default=ROOT/'output/final_beauty_brush_reel.mp4'); args=p.parse_args()
    source=ROOT/'makeup_brushes.png.png'
    if source.exists():
        with Image.open(source) as pic: pic.load(); print('Source readable:',pic.size,flush=True)
        print('This illustration edition does not assign types to unverified photographic brushes.',flush=True)
    else: print('Source image absent. Using original, clearly marked brush illustrations.',flush=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    height=args.width*16//9
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(args.fps),'-i','-','-vf',f'scale={args.width}:{height}:flags=lanczos','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(args.output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(25*args.fps):
            proc.stdin.write(frame(n/args.fps).tobytes())
            if n%args.fps==0: print(f'Rendering {n//args.fps}/25s',flush=True)
    finally: proc.stdin.close()
    if proc.wait(): raise RuntimeError('FFmpeg encoding failed')
    # Contact sheet sampled at the readable part of each scene.
    sheet=Image.new('RGB',(540*3,960*2),BG)
    for i,t in enumerate([1,4,8,14,19,23]): sheet.paste(frame(t),((i%3)*540,(i//3)*960))
    sheet.resize((810,960)).save(args.output.parent/'storyboard_preview.jpg',quality=92)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(args.output)]))
    (args.output.parent/'validation.json').write_text(json.dumps(probe,indent=2))
    print('DONE',args.output, args.output.stat().st_size,flush=True)
if __name__=='__main__': main()
