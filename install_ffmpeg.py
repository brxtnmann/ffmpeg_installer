import os
import subprocess
import platform
import shutil
import urllib.request
import zipfile
import sys

def install_ffmpeg():
    system = platform.system()
    if system == "Windows":
        # Windows installation (example - adapt as needed)
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"  # Example URL. Find a good source.
        ffmpeg_zip = "ffmpeg.zip"
        try:
            print("Downloading FFmpeg...")
            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
            print("Extracting FFmpeg...")
            with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
                zip_ref.extractall(".") # Extract to current directory
            os.remove(ffmpeg_zip)
            print("FFmpeg downloaded and extracted.")

            # Determine FFmpeg bin directory (Windows)
            try:
                # Assuming FFmpeg is extracted to the current directory
                for root, dirs, files in os.walk("."): # search in the current directory
                    for dir in dirs:
                        if dir.lower().startswith("ffmpeg"): # find a directory starting with ffmpeg
                            ffmpeg_bin_dir = os.path.join(root, dir, "bin")
                            break # exit inner loop
                    if ffmpeg_bin_dir: # if it is not None
                        break # exit outer loop
                if not ffmpeg_bin_dir: # if it is still None
                    raise Exception("ffmpeg bin directory not found.")
            except Exception as e:
                print(f"Error finding FFmpeg bin directory: {e}")
                return # exit the function

            if ffmpeg_bin_dir:
                try:
                    if ffmpeg_bin_dir not in os.environ["PATH"]:
                        os.environ["PATH"] += ";" + ffmpeg_bin_dir
                        print("FFmpeg added to PATH. You may need to restart your terminal or computer.")
                    else:
                        print("FFmpeg is already in PATH.")
                except Exception as e:
                    print(f"Error adding to PATH: {e}")

        except Exception as e:
            print(f"Error installing FFmpeg: {e}")

    elif system == "Linux" or system == "Darwin":  # macOS and Linux
        try:
            # Linux/macOS installation (example - adapt for your distro)
            if system == "Linux":
                print("Installing FFmpeg (using apt - adapt for your distro)...")
                subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"], check=True) # or yum or other package manager
            elif system == "Darwin":
                print("Installing FFmpeg (using brew)...")
                subprocess.run(["brew", "install", "ffmpeg"], check=True)

            print("FFmpeg installed.")

            # Try to find ffmpeg bin directory
            try:
                result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True, check=False) # check if ffmpeg exists
                if result.returncode == 0:
                    ffmpeg_bin_dir = os.path.dirname(result.stdout.strip())
                else:
                    ffmpeg_bin_dir = None # if not found
            except Exception as e:
                print(f"Error finding FFmpeg bin directory: {e}")
                return

            if ffmpeg_bin_dir:
                try:
                    if ffmpeg_bin_dir not in os.environ["PATH"]:
                        os.environ["PATH"] += ":" + ffmpeg_bin_dir # : for *nix systems
                        print("FFmpeg added to PATH. You may need to restart your terminal or computer.")
                    else:
                        print("FFmpeg is already in PATH.")
                except Exception as e:
                    print(f"Error adding to PATH: {e}")

        except Exception as e:
            print(f"Error installing FFmpeg: {e}")

    else:
        print(f"FFmpeg installation not supported on {system}.")


def main():
    install_ffmpeg()
    # Check if ffmpeg is working
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        print("FFmpeg installation verified.")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"FFmpeg not found or not working: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()