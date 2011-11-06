# Author: Rajat Saxena<rajat.saxena.work@gmail.com>
# License: GNU GPL v3


#importing various modules
import pygtk
pygtk.require("2.0")
from BeautifulSoup import BeautifulSoup
import sys
import gtk
import zencoding
import zencoding.zen_core as zencode
import os
import gtksourceview2

class editor:
    def __init__(self):
        self.filename = "./interface.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.filename)

        #getting objects from glade file
        self.win = self.builder.get_object("mainwin")
        #self.html = self.builder.get_object("html")
        #self.css = self.builder.get_object("css")
        #self.js = self.builder.get_object("js")
        self.check_js = self.builder.get_object("check_js")
        self.do = self.builder.get_object("do")
        self.status = self.builder.get_object("status")
        self.scrollhtml = self.builder.get_object("scrollhtml")
        self.scrollcss = self.builder.get_object("scrollcss")
        self.scrolljs = self.builder.get_object("scrolljs")

        #creating gtksourceview
        self.html = gtk.TextView()
        self.css = gtk.TextView()
        self.js = gtk.TextView()

        self.langmanager = gtksourceview2.LanguageManager()
        self.langhtml = self.langmanager.get_language("html")
        self.langcss = self.langmanager.get_language("css")
        self.langjs = self.langmanager.get_language("javascript")

        self.htmlbuffer = gtksourceview2.Buffer()
        self.cssbuffer = gtksourceview2.Buffer()
        self.jsbuffer = gtksourceview2.Buffer()

        #setting languages
        self.htmlbuffer.set_language(self.langhtml)
        self.cssbuffer.set_language(self.langcss)
        self.jsbuffer.set_language(self.langjs)

        self.html = gtksourceview2.View(self.htmlbuffer)
        self.html.set_show_line_numbers(True)
        self.html.set_auto_indent(True)
        self.html.set_tab_width(4)


        self.css = gtksourceview2.View(self.cssbuffer)
        self.css.set_show_line_numbers(True)
        self.css.set_auto_indent(True)
        self.css.set_tab_width(4)

        self.js = gtksourceview2.View(self.jsbuffer)
        self.js.set_show_line_numbers(True)
        self.js.set_auto_indent(True)
        self.js.set_tab_width(4)

        #adding gtksourceview to scrollboxes
        self.scrollhtml.add(self.html)
        self.scrollcss.add(self.css)
        self.scrolljs.add(self.js)

        #getting html template
        template = open("html_template.html")
        self.template_string = ""
        for each in template:
                self.template_string = self.template_string + each

        #creating project folder
        try:
                os.mkdir("project")
        except OSError:
                pass
        os.chdir("project")

        #main window's settings
        self.win.set_size_request(900,450)
        self.win.connect("destroy",self.destroy)

        #setting do button's properties
        self.do.set_size_request(50,20)
        self.check_js.set_size_request(50,20)
        self.html.set_size_request(300,370)
        self.css.set_size_request(300,370)
        self.js.set_size_request(300,370)
        self.status.set_size_request(900,2)
        self.do.connect("clicked",self.process)

        #setting text views' styles
        #self.html.modify_base(gtk.STATE_NORMAL,gtk.gdk.color_parse('pink'))
        
        
        #enabling wrap mode
        self.html.set_wrap_mode(gtk.WRAP_WORD)

        #other settings
        self.status.set_text("Editing...")
        self.html.connect('key_press_event',self.keyevents)

        #reading data and filling text boxes
        self.prefill() 

        #window
        self.win.set_title("Wildebeest Editor")
        self.win.show_all()

    def destroy(self,widget):
        gtk.main_quit()
    
    #This function is doing various things in html view on key events
    def keyevents(self,widget,event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & gtk.gdk.CONTROL_MASK:
                if event.keyval == 101:
                        print("Ctrl+E")
                        html_buffer = self.html.get_buffer()
                        if html_buffer.get_has_selection():
                                bounds=html_buffer.get_selection_bounds()
                                pzentext = html_buffer.get_slice(bounds[0],bounds[1])
                                html_buffer.delete(bounds[0],bounds[1])
                                converted_text = zencode.expand_abbreviation(pzentext,'html','xhtml')
                                if converted_text:
                                        pzentext=converted_text.replace("|","")
                                html_buffer.insert_at_cursor(pzentext)
                                print(pzentext)
                if event.keyval == 119:
                        print("Ctrl+W")
        if event.keyval==65293:
                html_buffer = self.html.get_buffer() 
                html_buffer.insert_at_cursor("\t")
        print(str(event.keyval));
                          
    #This is the function for prefilling fields
    def prefill(self):
        try:
                #filling html textview
                prehtml = open("webfile.html","r")
                string = ""
                for each in prehtml:
                        string = string+each
                #print(string)
                soup = BeautifulSoup(string)
                prehtmltext = soup.body
                print(prehtmltext.renderContents())
                prehtml.close()

                html_buffer = self.html.get_buffer() 
                html_buffer.set_text(prehtmltext.renderContents())

                #filling css textview
                precss = open("style.css","r")
                string = ""
                for each in precss:
                        string = string+each
                print(string)
                precss.close()
                css_buffer = self.css.get_buffer()
                css_buffer.set_text(string)

                #filling js textview
                prejs = open("script.js","r")
                string = ""
                for each in prejs:
                        string = string+each
                print(string)
                prejs.close()

                js_buffer = self.js.get_buffer()
                js_buffer.set_text(string)

        except:
                pass

    #This is the function for doing obvious thing i.e. saving data to files
    def process(self,widget):



        #Getting text from all the textview widgets
        html_buffer = self.html.get_buffer()
        js_buffer = self.js.get_buffer()
        css_buffer = self.css.get_buffer()
        texthtml = html_buffer.get_text(html_buffer.get_start_iter(),html_buffer.get_end_iter())
        textcss = css_buffer.get_text(css_buffer.get_start_iter(),css_buffer.get_end_iter())
        textjs = js_buffer.get_text(js_buffer.get_start_iter(),js_buffer.get_end_iter())

        #This is the module for auto refreshing the page 
        script = '''
        /* Just remove this function.It was introduced by Wildebeest editor */
        
                function refresh(){
                        window.location.reload(true);
                }
                setTimeout(refresh,1000)
        
        /* End of wildebeest editor's auto reloading function */
        '''

        if self.check_js.get_active():
                script = ""
        #if texthtml == "":
        #        sys.exit(0)

        #Formatting the template and storing to "webfile.html"
        
        self.string_to_be_saved = self.template_string.replace("{{ texthtml }}",texthtml)
        print(self.string_to_be_saved)
        
        #Saving data to script.js
        jsfile = open("script.js","w")
        for each in textjs:
                jsfile.write(each)
        jsfile.close()

        #Saving data to style.css
        cssfile = open("style.css","w")
        for each in textcss:
                cssfile.write(each)
        cssfile.close()

        #Saving data to autoreload.js
        reloadfile = open("autoreload.js","w")
        for each in script:
                reloadfile.write(each)
        reloadfile.close()

        #Saving data to html page named "webfile.html"
        webfile = open("webfile.html","w")
        for each in self.string_to_be_saved:
            webfile.write(each)
        webfile.close()

        

if __name__ == "__main__":
    editor = editor()
    gtk.main()
        
