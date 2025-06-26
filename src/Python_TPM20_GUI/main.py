import wx
import tab1_setup as t1
import tab2_crypto as t2
import tab3_provider as t3
import tab4_policy as t4
import tab5_attest as t5
import misc_dialogs as misc
import shell_util as exec_cmd
import images as img
import subprocess
import wx.lib.inspection

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="OPTIGA"+ u"\u1d40\u1d39"+" TPM 2.0 Explorer", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetBackgroundColour(wx.WHITE)
        self.winsize = (1280, 720)
        
        # Base window dimensions (reference size for scaling)
        self.base_width = 1280
        self.base_height = 720

        # Create title and font
        self.main_font_size = 16
        self.title_font_size = 30
        self.main_font = wx.Font(self.main_font_size, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.title_font = wx.Font(self.title_font_size, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.SetFont(self.main_font)

        # Create all the button widgets first
        self.button1 = wx.Button(self, -1, 'Setup and Basic Features')
        self.button2 = wx.Button(self, -1, 'Cryptographic Functions')
        self.button3 = wx.Button(self, -1, 'OpenSSL-Provider')
        self.button4 = wx.Button(self, -1, 'Data Sealing with Policy')
        self.button5 = wx.Button(self, -1, 'Attestation')
        # Title
        self.title_screen = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="OPTIGA" + u"\u1d40\u1d39" + " TPM 2.0 Explorer")
        self.title_screen.SetFont(self.title_font)
        
        # Save image paths
        self.image_paths = {
            "tpm": "../images/tpm_slb_9670.png",
            "ifx": "../images/250px-Infineon-Logo.png",
            "tab1": "../images/setup.png",
            "tab2": "../images/crypto.png",
            "tab3": "../images/engine.png",
            "tab4": "../images/policy.png",
            "tab5": "../images/attest.png",
        }
        
        # Images
        self.tpm_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["tpm"]))
        self.ifx_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["ifx"]))
        self.tab1_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["tab1"]))
        self.tab2_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["tab2"]))
        self.tab3_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["tab3"]))
        self.tab4_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["tab4"]))
        self.tab5_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.image_paths["tab5"]))
        
        #Window size choice list
        size_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.size_label = wx.StaticText(self, label="Window Size:")
        self.winsize_choice = wx.Choice(self, choices=["1280x720", "1024x600", "800x400"])
        self.winsize_choice.SetSelection(0)  # default 1280x720
        size_sizer.Add(self.size_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        size_sizer.Add(self.winsize_choice, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        horisizer = wx.BoxSizer(wx.HORIZONTAL)
        gdsizer = wx.GridSizer(rows=4, cols=3, vgap=0, hgap=5)
        

        horisizer.Add(self.tpm_image, 0, wx.LEFT | wx.TOP, 17)
        horisizer.AddStretchSpacer(1)
        horisizer.Add(self.title_screen, 0, wx.ALIGN_CENTER)
        horisizer.AddStretchSpacer(1)
        horisizer.Add(self.ifx_image, 0, wx.TOP, 10)

        gdsizer.Add(self.tab1_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer.Add(self.tab2_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer.Add(self.tab3_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)

        gdsizer.Add(self.button1, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer.Add(self.button2, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer.Add(self.button3, 1, wx.EXPAND | wx.ALL, 30)

        gdsizer.Add(self.tab4_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer.Add(self.tab5_image, 0, wx.ALIGN_CENTRE | wx.TOP, 5)
        gdsizer.AddSpacer(1)

        gdsizer.Add(self.button4, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer.Add(self.button5, 1, wx.EXPAND | wx.ALL, 30)
        gdsizer.Add(size_sizer, 0, wx.ALIGN_CENTRE | wx.TOP, 5)

        mainsizer.Add(horisizer, 0, wx.EXPAND | wx.TOP, 20)
        mainsizer.Add(-1, 31)
        mainsizer.Add(gdsizer, 1, wx.EXPAND)
        
        #Original sizer values
        self.orig_values = {
            'spacer': 31,
            'horisizer_borders': {
                'tpm': (wx.LEFT | wx.TOP, 17),
                'ifx': (wx.TOP, 10)
            },
            'grid_borders': {
                'images': (wx.ALIGN_CENTRE | wx.TOP, 5),
                'buttons': (wx.ALL, 30),
                'choice': (wx.ALIGN_CENTRE | wx.TOP, 5)
            },
            'grid_gaps': (0, 5)  # (vgap, hgap)
        }

        # Bind events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button5)
        self.winsize_choice.Bind(wx.EVT_CHOICE, self.OnWinSizeChange)


        # Set tooltips
        self.button1.SetToolTip(wx.ToolTip("Take ownership here."))
        self.button2.SetToolTip(wx.ToolTip("Hashing, Encryption, Decryption, Verification & Signing"))
        self.button3.SetToolTip(wx.ToolTip("Using TPM and OpenSSL to establish a client-server connection"))
        self.button4.SetToolTip(wx.ToolTip("Making use of policies to seal and unseal objects"))
        self.button5.SetToolTip(wx.ToolTip("Using endorsement key hierarchies to prove/attest"))

        self.SetSizer(mainsizer)
        
        self.Centre()
        self.AdjustWinSize(1280, 720)
        self.Check_IFX_TPM()
        
    def Check_IFX_TPM(self):
            cmd =" ls /dev/tpm0"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            retcode = ps_command.wait()
            if( command_output.decode() != "/dev/tpm0\n"):
                misc.Not_IFX_TPM_Dlg(self, "TPM Device Not Found").ShowModal()
                self.Disable_Buttons()              
                return

            cmd =" tpm2_getcap properties-fixed | grep -A2 'MANUFACTURER' | grep value | grep -Eo '[A-Z]*'"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            
            retcode = ps_command.wait()
            if (not "IFX" in command_output.decode()):
                misc.Not_IFX_TPM_Dlg(self, "Insert Infineon IRIDIUM Module").ShowModal()
                self.Disable_Buttons()    
                return
            
    def Disable_Buttons(self):
            self.button1.Disable()
            self.button2.Disable()
            self.button3.Disable()
            self.button4.Disable()
            self.button5.Disable()
            
                    
    def OnCloseWindow(self, evt):
        self.Destroy()

    def OnButtonClick(self, evt):
        event_obj = evt.GetEventObject()
        if (event_obj == self.FindWindowByLabel(label='Setup and Basic Features')):
            self.activetab = t1.Tab1Frame(self, "Basic")
        elif (event_obj == self.FindWindowByLabel(label='Cryptographic Functions')):
            self.activetab = t2.Tab2Frame(self, "Crypto")
        elif (event_obj == self.FindWindowByLabel(label='OpenSSL-Provider')):
            self.activetab = t3.Tab3Frame(self, "Provider")
        elif (event_obj == self.FindWindowByLabel(label='Data Sealing with Policy')):
            self.activetab = t4.Tab4Frame(self, "Data Sealing with Policy")
        elif (event_obj == self.FindWindowByLabel(label='Attestation')):
            self.activetab = t5.Tab5Frame(self, "Attest")
        else:
            return
        self.Hide()
        
    def OnWinSizeChange(self, event):
        selected = self.winsize_choice.GetStringSelection()
        width, height = map(int, selected.split("x"))
        self.winsize = (width, height)
        self.AdjustWinSize(width, height)

    def AdjustWinSize(self, width, height):
        # Calculate scaling factors
        width_scale = width / self.base_width
        height_scale = height / self.base_height
        scale_factor = min(width_scale, height_scale)  # Maintain aspect ratio
        
        # Set window properties
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        self.SetSize((width, height))
        
        # Font Scaling
        new_main_font = wx.Font(int(self.main_font_size * scale_factor),
                              wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        new_title_font = wx.Font(int(self.title_font_size * scale_factor),
                               wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.SetFont(new_main_font)
        self.title_screen.SetFont(new_title_font)

        # Button Scaling
        button_font = wx.Font(int(self.main_font_size * scale_factor),
                             wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        for button in [self.button1, self.button2, self.button3, self.button4, self.button5]:
            # Scale physical dimensions
            button.SetMinSize((
                int(button.GetSize().width * width_scale),
                int(button.GetSize().height * height_scale)
            ))
            # Scale font
            button.SetFont(button_font)

        # Image Scaling
        def scale_image(path, widget):
            img = wx.Image(path, wx.BITMAP_TYPE_PNG)
            orig_w, orig_h = img.GetSize()
            new_w = int(orig_w * width_scale)
            new_h = int(orig_h * height_scale)
            
            # Preserve aspect ratio if needed
            if abs(width_scale - height_scale) > 0.1:  # Significant difference
                new_h = int(orig_h * width_scale)  # Match width scaling
            
            img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
            widget.SetBitmap(wx.Bitmap(img))

        # Scale all images
        for key, widget in [
            ("tpm", self.tpm_image),
            ("ifx", self.ifx_image),
            ("tab1", self.tab1_image),
            ("tab2", self.tab2_image),
            ("tab3", self.tab3_image),
            ("tab4", self.tab4_image),
            ("tab5", self.tab5_image)
        ]:
            scale_image(self.image_paths[key], widget)

        # Sizer Adjustments
        self.UpdateSizerItems(scale_factor)
        
        #Choice list
        new_choice_font = wx.Font(int(self.main_font_size * scale_factor),
                             wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.winsize_choice.SetFont(new_choice_font)
        self.size_label.SetFont(new_choice_font)

        # Final Layout
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Layout()
        self.Refresh()

    def UpdateSizerItems(self, scale_factor):
        spacer_item = self.GetSizer().GetItem(1)
        spacer_item.AssignSpacer((-1, int(self.orig_values['spacer'] * scale_factor)))
        
        horisizer = self.GetSizer().GetItem(0).GetSizer()
        
        item = horisizer.GetItem(0)
        flags, border = self.orig_values['horisizer_borders']['tpm']
        item.SetBorder(int(border * scale_factor))
        
        item = horisizer.GetItem(horisizer.GetItemCount()-1)
        flags, border = self.orig_values['horisizer_borders']['ifx']
        item.SetBorder(int(border * scale_factor))
        
        gdsizer = self.GetSizer().GetItem(2).GetSizer()
        vgap, hgap = self.orig_values['grid_gaps']
        gdsizer.SetVGap(int(vgap * scale_factor))
        gdsizer.SetHGap(int(hgap * scale_factor))
        
        for i in range(gdsizer.GetItemCount()):
            item = gdsizer.GetItem(i)
            widget = item.GetWindow()
            
            if widget in [self.tab1_image, self.tab2_image, self.tab3_image, 
                          self.tab4_image, self.tab5_image]:
                flags, border = self.orig_values['grid_borders']['images']
                item.SetBorder(int(border * scale_factor))
                
            elif widget in [self.button1, self.button2, self.button3, 
                           self.button4, self.button5]:
                flags, border = self.orig_values['grid_borders']['buttons']
                item.SetBorder(int(border * scale_factor))
                
            elif widget == self.winsize_choice:
                flags, border = self.orig_values['grid_borders']['choice']
                item.SetBorder(int(border * scale_factor))

class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame(None, title="Main")
        self.SetTopWindow(dlg)
        dlg.Centre()
#         wx.lib.inspection.InspectionTool().Show()
        dlg.Show()


# Always executes as this is the main file anyway
# Note: This changes the working directory to /working_space, thus all created objects will be there
# Navigation always starts from the /working_space folder.
if __name__ == "__main__":
    exec_cmd.checkDir()
    app = Main() 
    app.MainLoop()
