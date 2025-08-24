from utils.pages import lines_page

__module_name__ = "Shells and Commands"
__show_splash__ = False


def build_title_screen():
    return lines_page([f"[bold yellow]{__module_name__}[/bold yellow]"])


__pages__ = [build_title_screen()]
