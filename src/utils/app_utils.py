def center_window_to_display(window, width, height, scale_factor=1.0):
    """Centers the window to the main display/monitor"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 1.5) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"