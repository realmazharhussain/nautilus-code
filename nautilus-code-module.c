#include <nautilus-extension.h>
#include "nautilus-code.h"

void
nautilus_module_initialize (GTypeModule *module)
{
    nautilus_code_menu_provider_load(module);
}

void
nautilus_module_shutdown ()
{
}

void nautilus_module_list_types (const GType **types,
                                 int *num_types)
{
    static GType type_list[1];
    type_list[0] = NAUTILUS_CODE_TYPE_MENU_PROVIDER;
    types[0] = type_list;
    *num_types = 1;
}