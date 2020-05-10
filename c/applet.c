/**
 * Port of my python3 applet to C, purely for faster startup times.
 * Really, really wish Python could start up faster.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <gtk/gtk.h>
#include <gdk/gdk.h>
#include <glib.h>

#include <xcb/xcb.h>

int display_height=0;
int display_width=0;
char *btnsize="32"; /* change icon size here. Part of filename so a string*/
char *app_name="TabletPC_Applet_Menu"; /* so fvwm can apply its rules to it*/

/* a custom widget for a button that has a different action when held. */
GtkWidget *HoldButton;

/**
 * This takes care of most of the GObject boilerplate such as defining
 * the my_button_get_type() function, declaring the
 * my_button_parent_class pointer, and providing prototypes for
 * my_button_init() and my_button_class_init(). 
 * (-- https://wiki.gnome.org/HowDoI/CustomWidgets )
 */
G_DEFINE_TYPE (HoldButton, hold_button, GTK_TYPE_BUTTON);
/* that's a button that can be clicked, or for a different function
   clicked and held for >= 500ms.
   (Still needs to be implemented. For the Python version I borrowed
   someone else's code, but I'll have to teach myself how it works here.)
*/
guint held_signal_id=g_signal_new("held",
                                  G_TYPE_OBJECT, G_SIGNAL_RUN_LAST,
                                  0, NULL, NULL,
                                  g_cclosure_marshal_VOID__POINTER,
                                  G_TYPE_NONE, 1, G_TYPE_POINTER);
/*                                  G_TYPE_NONE, 0); */

/* to do: design holdbutton. initializer, clicked vs. pressed actions */

static void activate (GtkApplication* applet, gpointer user_data)
{
  GtkWidget *window;
  GtkStyleContext *styleContext;
  GtkCssProvider *cssProvider;
  window = gtk_application_window_new (applet);
  gtk_window_set_title (GTK_WINDOW (window), "Tablet Controls");
  
  cssProvider=gtk_css_provider_new();
  gtk_css_provider_load_from_path(cssProvider,"./style.css",NULL);

  GdkScreen *screen=gdk_screen_get_default();
  if(screen == NULL)
  {
    fprintf(stderr,"Error: gdk_screen_get_default() returned NULL!\nExiting.");
    exit(1);
  }
  
  styleContext=gtk_style_context_new();
  gtk_style_context_add_provider_for_screen(screen,
                                            GTK_STYLE_PROVIDER(cssProvider),
                                            GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);

  gchar *css="button {\n background: #424242;\n border-color: #282828;\n}\nbutton:active {\n background: #242424;\n border-color: #808080;\n}\n";

  /* NULL instead of GError location*/
  gtk_css_provider_load_from_data(cssProvider,css,-1,NULL);
  
  /* 
  * Yeah, yeah, I know it's deprecated. I don't care, because it's the only
  * way I can find to do it.
  */
  gtk_window_set_wmclass(GTK_WINDOW (window), app_name, app_name);

  GtkWidget *vbox=gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0); /* 0 spacing */
  gtk_container_add (GTK_CONTAINER (window), vbox);

  /* todo: populate with buttons next. */
  /* todo: implement click and hold button press */
  GtkWidget *button;
  
/*  gtk_window_set_default_size (GTK_WINDOW (window), 200, 200);*/
  gtk_widget_show_all (window);
}

int main (int argc, char **argv)
{
  /* we need to use XCB (or could have used Xlib) to get display geometry.*/
  xcb_screen_t *screen;
  xcb_screen_iterator_t iter;
  int screen_num; /* gets set by xcb_connect */
  
  xcb_connection_t *dispcon = xcb_connect (NULL, &screen_num);

  
/*  const xcb_setup_t *setup = xcb_get_setup (dispcon);*/
  /* in the python version I looked at root window dimensions. Here I am
     looking at actual screen dimensions. */
  /* Get the screen number */
  iter = xcb_setup_roots_iterator (xcb_get_setup (dispcon));
  for (; iter.rem; --screen_num, xcb_screen_next (&iter))
  {
    if (screen_num == 0)
    {
      screen = iter.data;
      break;
    }
  }
  xcb_flush (dispcon);
  
/*  screen = xcb_setup_roots_iterator(setup).data; */
  printf("Width:\t%d\nHeight:\t%d\n",screen->width_in_pixels,screen->height_in_pixels);
  display_width=screen->width_in_pixels;
  display_height=screen->height_in_pixels;
  /* we're all done using XCB now. We got what we needed.*/
  xcb_disconnect (dispcon);
  
  /* GTK applet initialization stuff */
  GtkApplication *applet;
  int status;  

  applet = gtk_application_new ("org.wyatt8740.tabletpc_applet_menu", G_APPLICATION_FLAGS_NONE);
  g_signal_connect (applet, "activate", G_CALLBACK (activate), NULL);
  status = g_application_run (G_APPLICATION (applet), argc, argv);
  g_object_unref (applet);

  return status;
}
