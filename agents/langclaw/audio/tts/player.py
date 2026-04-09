"""Audio Player - Seamless audio playback using Windows built-in"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

class AudioPlayer:
    @staticmethod
    def play(filepath: Path) -> bool:
        """Play audio file - uses PowerShell MediaPlayer (most reliable)"""
        try:
            if sys.platform == "win32":
                # Use PowerShell MediaPlayer (reliable, no COM issues)
                return AudioPlayer._play_powershell_mediaplayer(filepath)
            
            elif sys.platform == "darwin":
                subprocess.Popen(["afplay", str(filepath)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            else:
                subprocess.Popen(["xdg-open", str(filepath)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
                
        except Exception as e:
            print(f"   ⚠️ Playback error: {e}")
        
        # Ultimate fallback - open file
        try:
            os.startfile(str(filepath))
            return True
        except:
            return False
    
    @staticmethod
    def _play_powershell_mediaplayer(filepath: Path) -> bool:
        """Play using PowerShell MediaPlayer (hidden, works reliably)"""
        try:
            # PowerShell script using System.Windows.Media.MediaPlayer
            ps_script = f'''
            Add-Type -AssemblyName presentationCore
            Add-Type -AssemblyName system
            $player = New-Object System.Windows.Media.MediaPlayer
            $player.Open("{filepath}")
            
            # Wait for media to open
            Start-Sleep -Milliseconds 500
            $player.Play()
            
            # Get duration and wait
            $duration = 0
            if ($player.NaturalDuration.HasTimeSpan) {{
                $duration = $player.NaturalDuration.TimeSpan.TotalSeconds
            }}
            
            if ($duration -gt 0) {{
                $waited = 0
                while ($waited -lt $duration -and $player.Position.TotalSeconds -lt $duration - 0.5) {{
                    Start-Sleep -Milliseconds 200
                    $waited += 0.2
                }}
            }} else {{
                Start-Sleep -Seconds 3
            }}
            
            $player.Close()
            $player = $null
            [System.GC]::Collect()
            '''
            
            # Run PowerShell completely hidden
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0x08000000
            )
            return True
            
        except Exception as e:
            return False
    
    @staticmethod
    def play_simple(filepath: Path) -> bool:
        """Simple playback - just open the file (user sees player)"""
        try:
            if sys.platform == "win32":
                os.startfile(str(filepath))
                return True
            elif sys.platform == "darwin":
                subprocess.Popen(["afplay", str(filepath)])
                return True
            else:
                subprocess.Popen(["xdg-open", str(filepath)])
                return True
        except:
            return False
