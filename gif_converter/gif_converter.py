import os
import subprocess
import dearpygui.dearpygui as dpg
import sys
import argparse
from moviepy.editor import VideoFileClip, ImageSequenceClip
from PIL import Image

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def convert_to_gif(input_path, output_path, fps=None, trim=None, force_output_size_length=False):
    """Converts video/image sequence to GIF using MoviePy and ffmpeg."""

    try:
        if any(input_path.lower().endswith(ext) for ext in ['.mp4', '.mov', '.avi', '.webm', '.mkv']):  # Check if video
            clip = VideoFileClip(input_path)

            if trim:
                trim_parts = trim.split(",")
                if len(trim_parts) >= 2:
                    start_time = trim_parts[0]
                    end_time_or_max_size = trim_parts[1]

                    clip = clip.subclip(start_time, end_time_or_max_size) # trim clip

                    if len(trim_parts) == 3 and force_output_size_length:
                        max_size = int(trim_parts[2]) * 1024 * 1024 # Convert MB to bytes
                        # Resize to fit size constraint
                        width, height = clip.size
                        import math
                        original_size = clip.write_gif(output_path, fps=fps, verbose=False)
                        if original_size > max_size:
                            ratio = math.sqrt(max_size / original_size)
                            new_width = int(width * ratio)
                            new_height = int(height * ratio)
                            clip = clip.resize((new_width, new_height))

                elif len(trim_parts) == 1:
                    start_time = trim_parts[0]
                    clip = clip.subclip(start_time, clip.duration) # trim from start to end

            clip.write_gif(output_path, fps=fps, verbose=False) # verbose=False to suppress output
            clip.close()
        elif any(input_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']): # check if it is an image
            image = Image.open(input_path)
            image.save(output_path, format="GIF", append_images=[], loop=0) # save image as gif
        else: # assume it is an imagesequence
            try: # attempt to create a gif from images
                images = []
                # Assuming all files in the directory are part of the sequence
                for filename in sorted(os.listdir(os.path.dirname(input_path))):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                        filepath = os.path.join(os.path.dirname(input_path), filename)
                        images.append(Image.open(filepath))
                clip = ImageSequenceClip(images, fps=fps)
                clip.write_gif(output_path, fps=fps, verbose=False)
                clip.close()
            except Exception as e:
                print(f"Error converting: {e}")
                return False

        return True
    except Exception as e:
        print(f"Error converting: {e}")
        return False



def process_files(file_paths, output_folder, new_folder_name, fps, trim, force_output_size_length):
    for file_path in file_paths:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if new_folder_name:
            output_dir = os.path.join(output_folder, new_folder_name)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{base_name}.gif")
        else:
            output_path = os.path.join(output_folder, f"{base_name}.gif")

        if convert_to_gif(file_path, output_path, fps, trim, force_output_size_length):
            print(f"Converted {file_path} to {output_path}")
        else:
            print(f"Failed to convert {file_path}")


def gui_mode():
    def select_files_callback(sender, app_data):
        selected_files = app_data["selections"]
        dpg.set_value("file_list", selected_files)

    def convert_callback(sender, app_data):
        file_paths = dpg.get_value("file_list")
        output_folder = dpg.get_value("output_folder")
        new_folder_name = dpg.get_value("new_folder_name")
        fps = dpg.get_value("fps")
        trim = dpg.get_value("trim")
        force_output_size_length = dpg.get_value("force_output_size_length")

        if not file_paths:
            print("No files selected.")
            return

        if not output_folder:
            print("No output folder selected.")
            return

        process_files(file_paths, output_folder, new_folder_name, fps, trim, force_output_size_length)

    with dpg.init_context():
        with dpg.window(label="GIF Converter", width=600, height=400):
            dpg.add_file_dialog(
                directory_selector=False,
                show=False,
                callback=select_files_callback,
                tag="file_dialog",
                filters="*.*",  # Add specific filters if needed
            )
            dpg.add_button(label="Select Files", callback=lambda: dpg.show_item("file_dialog"))
            dpg.add_text(tag="file_list", default_value="")
            dpg.add_input_text(label="Output Folder", tag="output_folder", default_value="")
            dpg.add_button(label="Browse", callback=lambda: dpg.show_item("output_folder_dialog"))
            dpg.add_file_dialog(
                directory_selector=True,
                show=False,
                callback=lambda s, a: dpg.set_value("output_folder", a["file_path"]),
                tag="output_folder_dialog",
            )


            dpg.add_input_text(label="New Folder Name (Optional)", tag="new_folder_name")
            dpg.add_input_float(label="FPS", tag="fps", default_value=30.0)  # Default FPS
            dpg.add_input_text(label="Trim (start,end or start,max_size)", tag="trim", default_value="")
            dpg.add_checkbox(label="Force Output Size/Length", tag="force_output_size_length", default_value=False)
            dpg.add_button(label="Convert", callback=convert_callback)

        dpg.create_viewport(title="GIF Converter", width=600, height=400)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

def main():
    parser = argparse.ArgumentParser(description="Convert files to GIF.")
    parser.add_argument("input_files", nargs="*", help="Input file(s) or folder")
    parser.add_argument("-o", "--output_folder", help="Output folder")
    parser.add_argument("-n", "--new_folder_name", help="New folder name")
    parser.add_argument("-f", "--fps", type=float, help="Frames per second")
    parser.add_argument("-t", "--trim", help="Trim (start,end or start,max_size)")
    parser.add_argument("-fo", "--forceoutputsizeandlength", action="store_true", help="Force output size and length")
    parser.add_argument("--nogui", action="store_true", help="Run in command-line mode")

    args = parser.parse_args()
    
    if not check_ffmpeg():
        print("FFmpeg is required. Please install it using: pip install ffmpeg_installer")
        sys.exit(1) # exit code 1 to indicate failure

    if not args.nogui and sys.platform == "win32": # only start GUI on windows
        gui_mode()
    else:
        if not args.input_files or not args.output_folder:
            parser.print_help()
            return

        input_files = []
        for item in args.input_files:
            if os.path.isdir(item):
                for root, _, files in os.walk(item):
                    for file in files:
                        input_files.append(os.path.join(root, file))
            else:
                input_files.append(item)

        process_files(input_files, args.output_folder, args.new_folder_name, args.fps, args.trim, args.forceoutputsizeandlength)

if __name__ == "__main__":
    main()