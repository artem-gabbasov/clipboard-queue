import tkinter as tk
import threading

# This class manages a badge (small info window) that can be displayed in a corner of the screen using Tkinter.
class BadgeManager:
    def __init__(self, /, frame_color="green", border_thickness=10, width=200, height=200):
        self.frame_color = frame_color
        self.border_thickness = border_thickness
        self.width = width
        self.height = height

        # Internal state variables
        self.root = None
        self.is_running = False

    def cleanup_state(self):
        # Reset the state variables to ensure the manager can be reused
        self.root = None
        self.is_running = False

    def create_badge(self):
        if self.is_running:
            #TODO: add logs describing that the thread is already running
            return  # Prevent starting multiple threads
        
        self.is_running = True

        # Create and start the Tkinter thread
        badge_thread = threading.Thread(target=self.draw_badge)
        badge_thread.daemon = True  # This ensures the thread will exit when the program exits
        badge_thread.start()

    def remove_badge(self):
        if self.root and self.is_running:
            self.root.event_generate("<<Close>>")  # Trigger the close event to remove the badge
        #TODO: add the else-clause to provide logs in case the thread is not running

    # Draw the badge on the screen
    # This method creates a Tkinter window that acts as a badge, drawing a border around it.
    # It runs in a separate thread to avoid blocking the main program.
    def draw_badge(self):
        self.root = None
        try:
            self.root = tk.Tk()

            # Set the window dimensions
            self.root.geometry(f"{self.width}x{self.height}+0+0")

            # Remove window decorations (no title bar)
            self.root.overrideredirect(True)

            # Create a canvas to draw on
            canvas = tk.Canvas(self.root, width=self.width, height=self.height)
            canvas.pack()

            # Draw a border around the screen (rectangular)
            canvas.create_rectangle(
                0, 0, self.width, self.height, outline=self.frame_color, width=self.border_thickness
            )

            # Bind the close event to remove the badge
            self.root.bind("<<Close>>", lambda _: self.root.after(0, self.root.destroy))

            # Start the Tkinter event loop
            self.root.mainloop()
        #TODO: add exception handling to log errors if the badge cannot be created
        except Exception as e:
            print(f"Error creating badge: {e}")
        finally:
            # Clean up the root window after closing to avoid the Tcl_AsyncDelete error
            del self.root
            self.cleanup_state()

    # Make it a context manager to ensure proper cleanup
    def __enter__(self):
        self.create_badge()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.remove_badge()
