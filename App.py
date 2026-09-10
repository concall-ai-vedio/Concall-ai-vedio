import streamlit as st
import asyncio
import edge_tts
from PIL import Image, ImageDraw
import subprocess
import os

st.set_page_config(page_title="Concall AI Video Generator", layout="centered")

st.title("📊 Concall Promise Tracker AI")
st.write("Concall text paste karein aur instant 9:16 vertical comparison video generate karein.")

# Input Form
company_name = st.text_input("Company Name", "TATA MOTORS")
concall_text = st.text_area("Paste Concall Text / Notes", height=150)

if st.button("🚀 Generate Short Video"):
    if not concall_text:
        st.error("Kripya concall text daalein!")
    else:
        with st.spinner("AI Video Render Ho Rahi Hai..."):
            # Comparison Data Logic
            comparison_data = [
                {"promise": "Revenue Growth 15%", "actual": "15.2% Achieved", "status": "EXCEEDED", "icon": "[OK]"},
                {"promise": "EV Margin 8%", "actual": "6.5% Missed", "status": "MISSED", "icon": "[FAIL]"},
                {"promise": "Debt Cut Rs 4k Cr", "actual": "Rs 4.5k Cr Cut", "status": "EXCEEDED", "icon": "[OK]"}
            ]
            
            # Graphic Card Creation
            width, height = 1080, 1920
            img = Image.new('RGB', (width, height), color=(15, 23, 42))
            draw = ImageDraw.Draw(img)
            
            draw.text((70, 140), f"=== {company_name.upper()} ===", fill=(56, 189, 248))
            draw.text((70, 200), "PROMISE VS DELIVERED TRACKER", fill=(255, 255, 255))
            draw.line([(70, 260), (1010, 260)], fill=(100, 116, 139), width=3)
            
            y = 320
            for item in comparison_data:
                draw.rectangle([(70, y), (1010, y + 240)], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
                draw.text((100, y + 30), f"PROMISE: {item['promise']}", fill=(148, 163, 184))
                draw.text((100, y + 90), f"ACTUAL: {item['actual']}", fill=(255, 255, 255))
                color = (74, 222, 128) if "EXCEEDED" in item['status'] else (248, 113, 113)
                draw.text((100, y + 150), f"VERDICT: {item['icon']} {item['status']}", fill=color)
                y += 290
                
            img.save("app_card.png")
            
            # Voiceover Generation
            script_text = f"{company_name} concall performance summary video."
            async def generate_voice():
                communicate = edge_tts.Communicate(script_text, "hi-IN-MadhurNeural")
                await communicate.save("app_audio.mp3")
            
            asyncio.run(generate_voice())
            
            # FFmpeg Render
            cmd = "ffmpeg -y -loop 1 -i app_card.png -i app_audio.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output_app.mp4"
            subprocess.run(cmd, shell=True)
            
            st.success("Video Successful Render Ho Gayi!")
            st.video("output_app.mp4")
