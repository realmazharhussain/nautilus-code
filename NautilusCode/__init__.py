from .program_list import progs
from gi.repository import Nautilus, GObject

class Extension (GObject.Object, Nautilus.MenuProvider):

  def get_background_items (self, *args):
    current_folder = args[-1]
    folder_path = current_folder.get_location().get_path()
    return  progs.get_menu_items(folder_path)

  def get_file_items (self, *args):
    selected_files = args[-1]

    if len(selected_files) != 1 or not selected_files[0].is_directory():
        return

    return self.get_background_items(selected_files[0])
