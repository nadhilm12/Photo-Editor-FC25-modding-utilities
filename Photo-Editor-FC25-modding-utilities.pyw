###################################################
#
#    Photo-Editor-FC25-modding-utilities
#
###################################################

# Import the necessary libraries for GUI functionality and image processing
import os  # For interacting with the file system
import ttkbootstrap as ttkb  # A modern-themed Tkinter-based GUI framework
from ttkbootstrap.constants import *  # Import constants from ttkbootstrap (such as INFO, SUCCESS, etc.)
from tkinter import filedialog, messagebox, colorchooser  # Standard Tkinter modules for dialogs
from PIL import Image, ImageColor  # Pillow library for image manipulation
from rembg import remove  # Library for background removal
import subprocess  # For running external command-line commands (magick)

# Definition of the main class for the GUI application
class ImageToolGUI:
    # Constructor: called when an ImageToolGUI object is created
    def __init__(self, root):
        """
        Initialize the ImageToolGUI application.

        Parameters:
        - root (ttkb.Window): The main window object of the application.
        """
        self.root = root  # Store a reference to the main window
        self.root.title("🖼️ Image Tool - Resize, BG Remove & DDS")  # Set the window title
        self.root.geometry("720x620")  # Set the window size
        self.root.resizable(False, False)  # Prevent the window from being resized

        # Variables to store user input data
        # StringVars are used to bind text data to Entry widgets
        self.file_path = ttkb.StringVar()
        self.output_dir = ttkb.StringVar()

        # BooleanVars are used to bind the status of Checkbuttons (checked or not)
        self.resize_enabled = ttkb.BooleanVar(value=False)
        self.bg_enabled = ttkb.BooleanVar(value=False)
        self.dds_enabled = ttkb.BooleanVar(value=False)

        # StringVars for image size input, with default values
        self.width = ttkb.StringVar(value="800")
        self.height = ttkb.StringVar(value="600")

        # StringVars for background removal options
        self.bg_mode = ttkb.StringVar(value="transparent")  # Default mode: transparent
        self.bg_color = ttkb.StringVar(value="#FFFFFF")  # Default color: white

        # StringVar for DDS compression format, with default value
        self.dds_format = ttkb.StringVar(value="DXT1")

        # Call the method to create all GUI components
        self.create_widgets()

    # Method to create and place all widgets on the window
    def create_widgets(self):
        """
        Build the entire user interface (UI) of the application.

        The UI is divided into several LabelFrames for better organization:
        1. Input & Output: For selecting the source file and output directory.
        2. Resize Image: For enabling the resize feature.
        3. Remove Background: For removing the image background.
        4. Convert PNG to DDS: For converting the image to DDS format.
        5. Actions: Contains the main control buttons and progress bar.
        """
        # Main frame with padding
        frm_main = ttkb.Frame(self.root, padding=15)
        frm_main.pack(fill="both", expand=True)

        # --- Input & Output Section ---
        # LabelFrame to group file-related widgets
        frm_file = ttkb.LabelFrame(frm_main, text="📁 Input & Output", padding=10)
        frm_file.pack(fill="x", pady=(0, 15))

        # Widget for selecting the input file
        ttkb.Label(frm_file, text="Select File (.PNG/.JPEG)").grid(row=0, column=0, sticky="w")
        ttkb.Entry(frm_file, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttkb.Button(frm_file, text="Browse File", command=self.browse_file, bootstyle=INFO).grid(row=0, column=2)

        # Widget for selecting the output directory
        ttkb.Label(frm_file, text="Select Output Directory").grid(row=1, column=0, sticky="w", pady=5)
        ttkb.Entry(frm_file, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=5)
        ttkb.Button(frm_file, text="Browse Folder", command=self.browse_folder, bootstyle=INFO).grid(row=1, column=2)

        # --- Resize Image Section ---
        # LabelFrame to group resize options
        frm_resize = ttkb.LabelFrame(frm_main, text="🔧 Resize Image", padding=10)
        frm_resize.pack(fill="x", pady=8)

        # Checkbutton to enable/disable resize
        ttkb.Checkbutton(frm_resize, text="Enable Resize", variable=self.resize_enabled).grid(row=0, column=0, sticky="w")

        # Frame to contain size input
        size_frame = ttkb.Frame(frm_resize)
        size_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky="w")
        ttkb.Label(size_frame, text="New Size:").pack(side="left")
        ttkb.Entry(size_frame, textvariable=self.width, width=6).pack(side="left", padx=(10, 2))
        ttkb.Label(size_frame, text="x").pack(side="left")
        ttkb.Entry(size_frame, textvariable=self.height, width=6).pack(side="left", padx=(2, 10))

        # --- Remove Background Section ---
        # LabelFrame to group background removal options
        frm_bg = ttkb.LabelFrame(frm_main, text="🧼 Remove Background", padding=10)
        frm_bg.pack(fill="x", pady=8)

        # Checkbutton to enable/disable the feature
        ttkb.Checkbutton(frm_bg, text="Enable Background Removal", variable=self.bg_enabled).grid(row=0, column=0, sticky="w")

        # Radiobutton to select background mode (transparent or solid color)
        ttkb.Radiobutton(frm_bg, text="Transparent", variable=self.bg_mode, value="transparent").grid(row=1, column=0, sticky="w", padx=30)
        ttkb.Radiobutton(frm_bg, text="Solid Color:", variable=self.bg_mode, value="solid").grid(row=2, column=0, sticky="w", padx=30)
        ttkb.Entry(frm_bg, textvariable=self.bg_color, width=10).grid(row=2, column=1, padx=(0, 10))
        ttkb.Button(frm_bg, text="Choose Color", command=self.choose_color, bootstyle=PRIMARY).grid(row=2, column=2, sticky="w")

        # --- Convert PNG to DDS Section ---
        # LabelFrame to group DDS conversion options
        frm_dds = ttkb.LabelFrame(frm_main, text="🌀 Convert PNG to DDS", padding=10)
        frm_dds.pack(fill="x", pady=8)

        # Checkbutton to enable/disable DDS conversion
        ttkb.Checkbutton(frm_dds, text="Enable DDS Conversion", variable=self.dds_enabled).grid(row=0, column=0, sticky="w")

        # Frame to contain the compression format dropdown
        compress_frame = ttkb.Frame(frm_dds)
        compress_frame.grid(row=1, column=0, columnspan=3, sticky="w")
        ttkb.Label(compress_frame, text="Compression Format:").pack(side="left")
        # Combobox to select DDS compression format
        ttkb.Combobox(compress_frame, textvariable=self.dds_format,
                      values=["DXT1", "DXT3", "DXT5", "BC4", "BC5", "BC6H", "BC7"], width=10).pack(side="left", padx=10)

        # --- Actions Section ---
        # Frame for the main action buttons
        frm_action = ttkb.Frame(frm_main)
        frm_action.pack(fill="x", pady=15)

        # Button to start the process
        ttkb.Button(frm_action, text="🚀 Start Process", command=self.start_processing, bootstyle=SUCCESS).pack(side="left", padx=5)
        # Button to reset all settings
        ttkb.Button(frm_action, text="🔁 Reset", command=self.reset_all, bootstyle=WARNING).pack(side="left", padx=5)
        # Button to open the output folder
        ttkb.Button(frm_action, text="📂 Open Output Folder", command=self.open_output_folder, bootstyle=SECONDARY).pack(side="left", padx=5)

        # Progressbar to display process status
        self.progress = ttkb.Progressbar(frm_main, orient="horizontal", mode="determinate", length=680, bootstyle=INFO)
        self.progress.pack(pady=10)

    # --- Implementation of Action Functions ---
    def browse_file(self):
        """
        Open a file dialog to select an image file.
        The selected file path will be set to the variable self.file_path.
        """
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.file_path.set(path)

    def browse_folder(self):
        """
        Open a directory dialog to select the output folder.
        The selected folder path will be set to the variable self.output_dir.
        """
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def choose_color(self):
        """
        Open a color picker dialog.
        If a color is selected, its hexadecimal value will be set to the variable self.bg_color.
        """
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color.set(color)

    def reset_all(self):
        """
        Reset all input variables and Checkbutton statuses to default values.
        This clears the form and resets the progress bar.
        """
        self.file_path.set("")
        self.output_dir.set("")
        self.resize_enabled.set(False)
        self.bg_enabled.set(False)
        self.dds_enabled.set(False)
        self.width.set("800")
        self.height.set("600")
        self.bg_mode.set("transparent")
        self.bg_color.set("#FFFFFF")
        self.dds_format.set("DXT1")
        self.progress['value'] = 0

    def open_output_folder(self):
        """
        Open the output folder in the system's file explorer.
        This will only work if an output directory has been selected.
        """
        if self.output_dir.get():
            os.startfile(self.output_dir.get())

    def start_processing(self):
        """
        The main function that orchestrates the entire image processing workflow.

        Workflow:
        1. Validate input: Ensure the file and folder exist.
        2. Open image: Load the image into memory.
        3. Remove background (optional): Use `rembg` to remove the background.
           If "solid" mode is selected, replace the transparent background with a solid color.
        4. Resize image (optional): Resize the image according to user input.
        5. Save PNG file: Save the processed result as a PNG file.
        6. Convert to DDS (optional): Use `subprocess` and `magick` for conversion.
        7. Display status: Update the progress bar and show a final message.
        """
        input_path = self.file_path.get()
        output_dir = self.output_dir.get()

        # Validate input
        if not os.path.isfile(input_path):
            messagebox.showerror("Error", "Invalid input file!")
            return
        if not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Invalid output directory!")
            return

        # Set the progress bar to 0 and update the GUI
        self.progress['value'] = 0
        self.root.update_idletasks()

        try:
            # Step 1: Load the image
            image = Image.open(input_path).convert("RGBA")
            self.progress['value'] = 20
            self.root.update_idletasks()

            # Step 2: Remove Background (if enabled)
            if self.bg_enabled.get():
                image = remove(image)
                if self.bg_mode.get() == "solid":
                    # Fill the transparent background with a solid color
                    color = ImageColor.getcolor(self.bg_color.get(), "RGBA")
                    bg = Image.new("RGBA", image.size, color)
                    bg.paste(image, mask=image.split()[3])
                    image = bg

            self.progress['value'] = 40
            self.root.update_idletasks()

            # Step 3: Resize Image (if enabled)
            if self.resize_enabled.get():
                image = image.resize((int(self.width.get()), int(self.height.get())))

            self.progress['value'] = 60
            self.root.update_idletasks()

            # Step 4: Save the processed PNG file
            output_png = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + "_processed.png")
            image.save(output_png)

            self.progress['value'] = 80
            self.root.update_idletasks()

            # Step 5: Convert to DDS (if enabled)
            if self.dds_enabled.get():
                output_dds = output_png.replace(".png", ".dds")
                # Run the ImageMagick (`magick`) command via subprocess
                subprocess.run(["magick", output_png, "-define", f"dds:compression={self.dds_format.get().lower()}", output_dds])

            self.progress['value'] = 100
            self.root.update_idletasks()

            # Show a success message
            messagebox.showinfo("Completed", "Process completed!")

        except Exception as e:
            # Handle any errors that occur
            messagebox.showerror("Error", str(e))
            self.progress['value'] = 0

# Main entry point of the application
if __name__ == '__main__':
    # Create the main window object with the 'cyborg' theme
    app = ttkb.Window(themename="cyborg")
    # Create an instance of the GUI class
    gui = ImageToolGUI(app)
    # Start the main event loop
    app.mainloop()