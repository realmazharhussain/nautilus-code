#include <nautilus-extension.h>
#include "nautilus-code.h"

struct _NautilusCodeMenuProvider
{
    GObject parent_instance;
};

static void menu_provider_iface_init (NautilusMenuProviderInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (NautilusCodeMenuProvider, nautilus_code_menu_provider, G_TYPE_OBJECT, 0,
                                G_IMPLEMENT_INTERFACE_DYNAMIC (NAUTILUS_TYPE_MENU_PROVIDER,
                                                               menu_provider_iface_init)
                               )

static void 
run_command (NautilusMenuItem *item,
             const char       *command)
{
    
    g_spawn_command_line_async (command, NULL);
}

static NautilusMenuItem*
new_menu_item (const char       *short_name,
               const char       *full_name,
               const char       *command,
               NautilusFileInfo *current_folder)
{
        GFile *folder_file = nautilus_file_info_get_location (current_folder);
        const char *folder_path = g_file_get_path (folder_file);

        GString *command_string = g_string_new(command);
        command_string = g_string_append(command_string, " ");
        command_string = g_string_append(command_string, folder_path);

        GString *item_name = g_string_new("NautilusCode::");
        item_name = g_string_append(item_name, short_name);

        GString *label = g_string_new("Open in ");
        label = g_string_append(label, short_name);

        GString *tip = g_string_new("Open in ");
        tip = g_string_append(tip, full_name);

        NautilusMenuItem *item = nautilus_menu_item_new(item_name->str,
                                                        label->str,
                                                        tip->str,
                                                        NULL
                                                       );
        g_signal_connect (item, "activate", G_CALLBACK(run_command), command_string->str);
        return item;
}

GList*
get_background_items (NautilusMenuProvider *provider,
                      GtkWidget *window,
                      NautilusFileInfo *currnet_folder)
{
    GList *items = NULL;
    char *command;

    command = NULL;
    if (g_find_program_in_path("code") != NULL)
        command = "code";
    else if (g_find_program_in_path("visual-studio-code") != NULL)
        command = "visual-studio-code";

    if (command != NULL)
    {
        items = g_list_append (items, new_menu_item ("VSCode", "Visual Studio Code", command, currnet_folder) );
    }

    command = NULL;
    if (g_find_program_in_path("gnome-builder") != NULL)
        command = "gnome-builder --project";
    else if (g_find_program_in_path("org.gnome.Builder") != NULL)
        command = "org.gnome.Builder --project";

    if (command != NULL)
    {
        items = g_list_append (items, new_menu_item ("Builder", "GNOME Builder", command, currnet_folder) );
    }

    return items;
}

static void
menu_provider_iface_init (NautilusMenuProviderInterface *iface)
{
    iface->get_background_items = get_background_items;
}

void
nautilus_code_menu_provider_load(GTypeModule *module)
{
    nautilus_code_menu_provider_register_type (module);
}

static void
nautilus_code_menu_provider_init (NautilusCodeMenuProvider *self)
{
}

static void
nautilus_code_menu_provider_class_init (NautilusCodeMenuProviderClass *klass)
{
}

static void
nautilus_code_menu_provider_class_finalize(NautilusCodeMenuProviderClass *klass)
{
}