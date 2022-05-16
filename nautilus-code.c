#include <nautilus-extension.h>
#include "nautilus-code.h"

#define get_path g_find_program_in_path

struct _NautilusCodeMenuProvider
{
    GObject parent_instance;
};

static void menu_provider_iface_init (NautilusMenuProviderInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (NautilusCodeMenuProvider, nautilus_code_menu_provider, G_TYPE_OBJECT, 0,
                                G_IMPLEMENT_INTERFACE_DYNAMIC (NAUTILUS_TYPE_MENU_PROVIDER,
                                                               menu_provider_iface_init)
                               )

typedef struct
{
    char *pkg_type;
    char *command;
} Package;

typedef struct
{
    char    *name;
    char    *flatpak_command;
    char    *native_command;
    char    *arguments;
    char    *additional_command;
    Package *additional_package;
} Program;

static void 
run_command (NautilusMenuItem *item,
             char             *command)
{
    
    g_spawn_command_line_async (command, NULL);
}

static NautilusMenuItem*
new_menu_item (char *name,
               char *command,
               char  selection_mode)
{
        GString *item_name = g_string_new ("NautilusCode::");
        if (selection_mode) item_name = g_string_append (item_name, "Selection::");
        item_name = g_string_append (item_name, name);

        GString *label = g_string_new ("Open in ");
        label = g_string_append (label, name);
        GString *tip = label;

        NautilusMenuItem *item = nautilus_menu_item_new(item_name->str,
                                                        label->str,
                                                        tip->str,
                                                        NULL
                                                       );
        g_signal_connect (item, "activate", G_CALLBACK(run_command), command);

        return item;
}

static GList*
add_if_installed(GList            *list,
                 Program          *prog,
                 NautilusFileInfo *folder,
                 char              selection_mode)
{
    GFile *folder_file = nautilus_file_info_get_location(folder);
    char  *folder_path = g_file_get_path(folder_file);

    GString *argument_string = g_string_new (" ");
    argument_string = g_string_append (argument_string, folder_path);
    if (prog->arguments) {
        argument_string = g_string_prepend (argument_string, prog->arguments);
        argument_string = g_string_prepend (argument_string, " ");
    }

    char *native_path;
    if (prog->native_command) {
        native_path = get_path(prog->native_command);
        if (!native_path && prog->additional_command)
            native_path = get_path(prog->additional_command);
        if (native_path) {
            GString *command = g_string_new (native_path);
            command = g_string_append (command, argument_string->str);
            list = g_list_append(list, new_menu_item(prog->name, command->str, selection_mode));
        }
    }

    if (prog->flatpak_command) {
        char *flatpak_path = get_path (prog->flatpak_command);
        if (flatpak_path) {
            GString *name = g_string_new (prog->name);
            if (native_path) name = g_string_append (name, " (flatpak)");
            GString *command = g_string_new (flatpak_path);
            command = g_string_append (command, argument_string->str);
            list = g_list_append(list, new_menu_item(name->str, command->str, selection_mode));
        }
    }

    if (prog->additional_package) {
        char *pkg_path = get_path(prog->additional_package->command);
        if (pkg_path) {
            GString *name = g_string_new (prog->name);
            name = g_string_append (name, " (");
            name = g_string_append (name, prog->additional_package->pkg_type);
            name = g_string_append (name, ")");

            GString *command = g_string_new (pkg_path);
            command = g_string_append (command, argument_string->str);

            list = g_list_append(list, new_menu_item(name->str, command->str, selection_mode));
        }
    }

    return list;
}

static GList*
get_menu_items (NautilusFileInfo *folder,
                char              selection_mode)
{
    #define add_program(prog) items = add_if_installed(items, &prog, folder, selection_mode)

    GList *items = NULL;

    // Program:            Name,            Flatpak ID,           Command
    Program code_oss = {"Code-OSS", "com.visualstudio.code-oss", "code-oss"};
    add_program(code_oss);

    Program vscode = {"VSCode", "com.visualstudio.code", "code"};
    if (get_path(code_oss.native_command))
        vscode.native_command = NULL;
    add_program(vscode);

    Program code_insiders = {"VSCode (Insiders)", NULL, "code-insiders"};
    add_program(code_insiders);

    Program vscodium = {"VSCodium", "com.vscodium.codium", "vscodium"};
    vscodium.additional_command = "codium";
    add_program(vscodium);

    Program gnome_builder = {"Builder", "org.gnome.Builder", "gnome-builder"};
    gnome_builder.arguments = "--project";
    add_program(gnome_builder);

    Program sublime_text = {"Sublime Text", "com.sublimetext.three", "subl"};
    add_program(sublime_text);

    Package phpstorm_eap = {"EAP", "phpstorm-eap"};
    Program phpstorm = {"PhpStorm", "com.jetbrains.PhpStorm", "phpstorm"};
    phpstorm.additional_package = &phpstorm_eap;
    add_program(phpstorm);

    return items;
}

GList*
get_background_items (NautilusMenuProvider *provider,
                      GtkWidget            *window,
                      NautilusFileInfo     *current_folder)
{
    char selection_mode = FALSE;
    return get_menu_items (current_folder, selection_mode);
}

GList*
get_file_items (NautilusMenuProvider *provider,
                GtkWidget            *window,
                GList                *files)
{
    char selection_mode = TRUE;

    if (g_list_length(files) == 1)
    {
        NautilusFileInfo *selected_file = g_list_first(files)->data; // get first element of the list 'files'
        if (nautilus_file_info_is_directory(selected_file))
        {
            return get_menu_items (selected_file, selection_mode);
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
