#pragma once

#include <glib-object.h>

G_BEGIN_DECLS

#define NAUTILUS_CODE_TYPE_MENU_PROVIDER (nautilus_code_menu_provider_get_type())

G_DECLARE_FINAL_TYPE(NautilusCodeMenuProvider, nautilus_code_menu_provider, NAUTILUS_CODE, MENU_PROVIDER, GObject)

void nautilus_code_menu_provider_load (GTypeModule *module);

G_END_DECLS