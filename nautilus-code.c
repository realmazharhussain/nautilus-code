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
               const char       *command_start,
               NautilusFileInfo *folder,
               const char        selected)
{
        GFile *folder_file = nautilus_file_info_get_location (folder);
        const char *folder_path = g_file_get_path (folder_file);

        GString *command = g_string_new(command_start);
        command = g_string_append(command, " ");
        command = g_string_append(command, folder_path);

        GString *item_name = g_string_new("NautilusCode::");
        if (selected) item_name = g_string_append (item_name, "Selection::");
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
        g_signal_connect (item, "activate", G_CALLBACK(run_command), command->str);
        return item;
}

static GList*
get_menu_items (NautilusFileInfo *folder,
                const char        selected)
{
    GList *items = NULL;

    const char *code_path = g_find_program_in_path("code");
    const char *codium_path = g_find_program_in_path("codium");
    const char *vscodium_path = g_find_program_in_path("vscodium");
    const char *code_oss_path = g_find_program_in_path("code-oss");

    const char *vscode_flatpak_path = g_find_program_in_path("com.visualstudio.code");
    const char *vscodium_flatpak_path = g_find_program_in_path("com.vscodium.codium");
    const char *code_oss_flatpak_path = g_find_program_in_path("com.visualstudio.code-oss");

    const char *gnome_builder_path = g_find_program_in_path("gnome-builder");
    const char *gnome_builder_flatpak_path = g_find_program_in_path("org.gnome.Builder");

    if (code_oss_path != NULL)
    {
        if (code_oss_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("Code-OSS (native)", "Code - OSS (native)", "code-oss", folder, selected) );
            items = g_list_append (items, new_menu_item ("Code-OSS (flatpak)", "Code - OSS (flatpak)", "com.visualstudio.code-oss", folder, selected) );
        }
        else
        {
            items = g_list_append (items, new_menu_item ("Code-OSS", "Code - OSS", "code-oss", folder, selected) );
        }

        if (vscode_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("VSCode", "Visual Studio Code", "com.visualstudio.code", folder, selected) );
        }
    }
    else if (code_path != NULL)
    {
        if (vscode_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("VSCode (native)", "Visual Studio Code (native)", "code", folder, selected) );
            items = g_list_append (items, new_menu_item ("VSCode (flatpak)", "Visual Studio Code (flatpak)", "com.visualstudio.code", folder, selected) );
        }
        else
        {
            items = g_list_append (items, new_menu_item ("VSCode", "Visual Studio Code", "code", folder, selected) );
        }

        if (code_oss_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("Code-OSS", "Code - OSS", "com.visualstudio.code-oss", folder, selected) );
        }
    }
    else
    {
        if (vscode_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("VSCode", "Visual Studio Code", "com.visualstudio.code", folder, selected) );
        }
        if (code_oss_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("Code-OSS", "Code - OSS", "com.visualstudio.code-oss", folder, selected) );
        }
    }

    if (vscodium_path != NULL)
    {
        if (vscodium_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("VSCodium (native)", "Visual Studio Codium (native)", "vscodium", folder, selected) );
            items = g_list_append (items, new_menu_item ("VSCodium (flatpak)", "Visual Studio Codium (flatpak)", "com.vscodium.codium", folder, selected) );
        }
        else
        {
            items = g_list_append (items, new_menu_item ("VSCodium", "Visual Studio Codium", "vscodium", folder, selected) );
        }
    }
    else if (codium_path != NULL)
    {
        if (vscodium_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("VSCodium (native)", "Visual Studio Codium (native)", "codium", folder, selected) );
            items = g_list_append (items, new_menu_item ("VSCodium (flatpak)", "Visual Studio Codium (flatpak)", "com.vscodium.codium", folder, selected) );
        }
        else
        {
            items = g_list_append (items, new_menu_item ("VSCodium", "Visual Studio Codium", "codium", folder, selected) );
        }
    }
    else if (vscodium_flatpak_path != NULL)
    {
        items = g_list_append (items, new_menu_item ("VSCodium", "Visual Studio Codium", "com.vscodium.codium", folder, selected) );
    }

    if (gnome_builder_path != NULL)
    {
        if (gnome_builder_flatpak_path != NULL)
        {
            items = g_list_append (items, new_menu_item ("Builder (native)", "GNOME Builder (native)", "gnome-builder --project", folder, selected) );
            items = g_list_append (items, new_menu_item ("Builder (flatpak)", "GNOME Builder (flatpak)", "org.gnome.Builder --project", folder, selected) );
        }
        else
        {
            items = g_list_append (items, new_menu_item ("Builder", "GNOME Builder", "gnome-builder --project", folder, selected) );
        }
    }
    else if (gnome_builder_flatpak_path != NULL)
    {
        items = g_list_append (items, new_menu_item ("Builder", "GNOME Builder", "org.gnome.Builder --project", folder, selected) );
    }

    return items;
}

GList*
get_background_items (NautilusMenuProvider *provider,
                      GtkWidget            *window,
                      NautilusFileInfo     *current_folder)
{
    const char selected = FALSE;
    return get_menu_items (current_folder, selected);
}

GList*
get_file_items (NautilusMenuProvider *provider,
                GtkWidget            *window,
                GList                *files)
{
    const char selected = TRUE;

    if (g_list_length(files) == 1)
    {
        NautilusFileInfo *selected_file = g_list_first(files)->data; // get first element of the list 'files'
        if (nautilus_file_info_is_directory(selected_file))
        {
            return get_menu_items (selected_file, selected);
        }
    }
    return (GList *) NULL;
}

static void
menu_provider_iface_init (NautilusMenuProviderInterface *iface)
{
    iface->get_file_items       = get_file_items;
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
