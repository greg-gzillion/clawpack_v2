"""Export to other applications"""
name = "/exportapp"

def run(args):
    if not args:
        print("Usage: /exportapp <filename> <app>")
        print("Apps: word, excel, powerpoint, browser, email, cloud")
        print("Example: /exportapp mydoc.docx word")
        print("Example: /exportapp report.pdf email")
        return
    
    from pathlib import Path
    import subprocess
    import webbrowser
    
    parts = args.split()
    source = parts[0]
    app = parts[1].lower() if len(parts) > 1 else ""
    
    p = Path(source)
    if not p.exists():
        print(f"❌ File not found: {source}")
        return
    
    print(f"\n📤 Exporting {p.name} to {app}...")
    
    # Export to Microsoft Word
    if app == "word":
        try:
            # SECURE: Use cmd /c start with shell=False (prevents command injection)
	subprocess.run(['cmd', '/c', 'start', 'winword', str(p.absolute())], shell=False)
            print(f"✅ Opening in Microsoft Word")
        except:
            print(f"❌ Could not open Word")
    
    # Export to Excel (for CSV files)
    elif app == "excel":
        try:
            subprocess.run(['cmd', '/c', 'start', 'excel', str(p.absolute())], shell=False)  # SECURE: No shell injection
            print(f"✅ Opening in Microsoft Excel")
        except:
            print(f"❌ Could not open Excel")
    
    # Export to PowerPoint
    elif app == "powerpoint":
        try:
            subprocess.run(['cmd', '/c', 'start', 'powerpnt', str(p.absolute())], shell=False)  # SECURE: No shell injection
            print(f"✅ Opening in PowerPoint")
        except:
            print(f"❌ Could not open PowerPoint")
    
    # Export to web browser (for HTML files)
    elif app == "browser":
        webbrowser.open(str(p.absolute()))
        print(f"✅ Opening in web browser")
    
    # Export to email (attach file)
    elif app == "email":
        mailto = f"mailto:?subject=Document from DocuClaw&body=Please find attached document&attachment={p.absolute()}"
        webbrowser.open(mailto)
        print(f"✅ Opening email client with attachment")
    
    # Export to cloud (copy to cloud folder)
    elif app == "cloud":
        cloud_paths = [
            Path.home() / "OneDrive",
            Path.home() / "Dropbox",
            Path.home() / "Google Drive",
            Path.home() / "iCloudDrive"
        ]
        copied = False
        for cloud in cloud_paths:
            if cloud.exists():
                dest = cloud / p.name
                import shutil
                shutil.copy2(p, dest)
                print(f"✅ Copied to {cloud.name}: {dest}")
                copied = True
                break
        if not copied:
            print(f"❌ No cloud folder found (OneDrive, Dropbox, Google Drive)")
    
    else:
        # Try default application
        try:
            os.startfile(str(p.absolute()))
            print(f"✅ Opening with default application")
        except:
            print(f"❌ Could not open {p.name}")


