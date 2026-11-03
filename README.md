# Beauty beginner brush Reel

A silent 25-second, 9:16 English Reel for Instagram and Facebook. Cream and blush palette, animated original brush illustrations, gentle pan/zoom, lift/fade text transitions, and mobile-readable captions.

## Source audit
The requested root image `makeup_brushes.png.png` was **absent** at production time. The repository initially contained only this README. No photograph was invented or downloaded. The video instead uses original Pillow illustrations with distinct powder, blending and angled blush silhouettes. Each teaching shot is explicitly labeled “BRUSH SHAPE ILLUSTRATION”. These are conceptual shapes, not claims about a photographed product. If the source is supplied later, inspect it before changing any brush assignments. This script validates an image if present but deliberately keeps this illustration edition.

## Reproduce
Requirements: Python 3.12+, Pillow, system FFmpeg with libx264, FFprobe, and Open Sans fonts in `/usr/share/fonts/truetype/open-sans/`. No MoviePy or NumPy needed. Tested: Python 3.12.14, Pillow 12.3.0, FFmpeg 7.1.5. MoviePy was unavailable.

```sh
python render_reel.py
# Lower-resolution alternative:
python render_reel.py --width 540 --output output/final_beauty_brush_reel_540.mp4
```

The animation is drawn at 540×960 and scaled with Lanczos to a 1080×1920 delivery master, 30 fps, H.264, yuv420p, faststart, no audio track. Total 750 frames, 25 seconds. Fonts and graphics are rendered together to avoid external subtitle dependencies. All media are generated locally; no external images or music are used.

Outputs: `output/final_beauty_brush_reel.mp4`, `output/storyboard_preview.jpg`, `output/validation.json`. Rendering logs are in `work/render.log`. The validation JSON comes directly from FFprobe.

## Storyboard
| Time | English text / visuals |
| --- | --- |
| 0–3s | New to makeup? Don’t buy a full brush set just yet. Three illustrated brushes gently float. |
| 3–6s | Start with these 3 essentials. Trio continues with subtle movement. |
| 6–12s | 1. Fluffy Powder Brush — For setting powder. Broad domed brush slowly enlarges and pans. |
| 12–17s | 2. Blending Eyeshadow Brush — For soft, seamless blending. Slim tapered illustration. |
| 17–22s | 3. Blush Brush — For a natural flush of color. Angled cheek-brush illustration. |
| 22–25s | Save this beginner brush guide! Trio and save prompt. |

Shot numbers are styled as 01, 02, 03 above the corresponding titles. Each scene has a short lift/fade entrance and fade exit. Important text stays away from top/bottom platform UI areas; platform overlays can vary.

## Instagram caption
New to makeup? Start small ✨ You don’t need a full brush set to begin. A fluffy powder brush, a blending eyeshadow brush, and a blush brush are a simple starting point. Build your kit as you discover what you love. Save this guide for your next beauty shop!

#MakeupForBeginners #MakeupBrushes #BeginnerMakeup #MakeupTips #BeautyEssentials

## Preview
Open the MP4 in a browser or video player. `storyboard_preview.jpg` shows all six scenes. This is the illustration edition because the requested photo was missing.
