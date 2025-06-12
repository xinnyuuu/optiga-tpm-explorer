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
        wx.Frame.__init__(self, parent, title="OPTIGA"+ u"\u1d40\u1d39"+" TPM 2.0 Explorer", 
                         style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        
        # Base configuration values (preserving original font sizes)
        self.base_resolution = (1280, 720)  # Reference resolution
        self.base_font_size = 16            # Original button font size
        self.base_title_size = 30            # Original title font size
        self.base_spacing = 5                # Reference spacing unit
        
        # Initialize settings
        self.SetBackgroundColour(wx.WHITE)
        self.resolution = self.base_resolution
        self.scale_factor = 1.0  # Default scale factor
        
        # Create all UI components
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
        
        # Apply initial scaling
        self.scale_components(self.scale_factor)
        self.SetSizer(self.mainsizer)
        self.mainsizer.Fit(self)
        self.Centre()
        self.Check_IFX_TPM()
        
    def create_widgets(self):
        """Create all UI components with original font sizes"""
        # Set main font (preserving original size)
        main_menu_font = wx.Font(self.base_font_size, wx.FONTFAMILY_SWISS, 
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        
        # Create buttons
        self.button1 = wx.Button(self, -1, 'Setup and Basic Features')
        self.button2 = wx.Button(self, -1, 'Cryptographic Functions')
        self.button3 = wx.Button(self, -1, 'OpenSSL-Provider')
        self.button4 = wx.Button(self, -1, 'Data Sealing with Policy')
        self.button5 = wx.Button(self, -1, 'Attestation')
        
        # Resolution selector
        self.resolution_choice = wx.Choice(self, choices=["1280x720", "1024x600", "800x400"])
        self.resolution_choice.SetSelection(0)
        
        # Create title with original font size
        self.title_screen = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, 
                                        label="OPTIGA"+ u"\u1d40\u1d39"+" TPM 2.0 Explorer")
        title_font = wx.Font(self.base_title_size, wx.FONTFAMILY_SWISS, 
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.title_screen.SetFont(title_font)
        
        # Load all images
        self.tpm_image = self.load_image('../images/tpm_slb_9670.png')
        self.ifx_image = self.load_image('../images/250px-Infineon-Logo.png')
        self.tab1_image = self.load_image('../images/setup.png')
        self.tab2_image = self.load_image('../images/crypto.png')
        self.tab3_image = self.load_image('../images/engine.png')
        self.tab4_image = self.load_image('../images/policy.png')
        self.tab5_image = self.load_image('../images/attest.png')
        
        # Store all image widgets for later scaling
        self.image_widgets = [
            self.tpm_image, self.ifx_image, 
            self.tab1_image, self.tab2_image, self.tab3_image,
            self.tab4_image, self.tab5_image
        ]

    def load_image(self, path):
        """Load image from file and return StaticBitmap"""
        image = wx.Image(path, wx.BITMAP_TYPE_PNG)
        return wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image))

    def setup_layout(self):
        """Initialize layout with proportional spacers"""
        # Resolution selector layout
        res_sizer = wx.BoxSizer(wx.HORIZONTAL)
        res_sizer.AddStretchSpacer(1)
        res_sizer.Add(wx.StaticText(self, label="Resolution: "), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        res_sizer.Add(self.resolution_choice, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # Main sizer structure
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        horisizer = wx.BoxSizer(wx.HORIZONTAL)
        horisizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.gdsizer = wx.GridSizer(rows=4, cols=3, vgap=0, hgap=5)
        
        # Add components with proportional spacing
        horisizer.AddSpacer(int(25 * self.scale_factor))
        horisizer.Add(self.tpm_image, 0, wx.TOP, int(17 * self.scale_factor))
        horisizer.AddSpacer(int(175 * self.scale_factor))
        horisizer.Add(self.title_screen, 0, wx.ALIGN_CENTRE)
        horisizer.AddSpacer(int(145 * self.scale_factor))
        horisizer.Add(self.ifx_image, 0, wx.TOP, int(10 * self.scale_factor))
        
        horisizer2.AddSpacer(int(1278 * self.scale_factor))

        self.gdsizer.Add(self.tab1_image, 0, wx.ALIGN_CENTRE | wx.TOP, int(5 * self.scale_factor))
        self.gdsizer.Add(self.tab2_image, 0, wx.ALIGN_CENTRE | wx.TOP, int(5 * self.scale_factor))
        self.gdsizer.Add(self.tab3_image, 0, wx.ALIGN_CENTRE | wx.TOP, int(5 * self.scale_factor))

        self.gdsizer.Add(self.button1, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(self.button2, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(self.button3, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))

        self.gdsizer.Add(self.tab4_image, 0, wx.ALIGN_CENTRE | wx.TOP, int(5 * self.scale_factor))
        self.gdsizer.Add(self.tab5_image, 0, wx.ALIGN_CENTRE | wx.TOP, int(5 * self.scale_factor))
        self.gdsizer.AddSpacer(1)

        self.gdsizer.Add(self.button4, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(self.button5, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(res_sizer, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        
        self.mainsizer.Add(horisizer, 0, wx.EXPAND | wx.TOP, int(20 * self.scale_factor))
        self.mainsizer.Add(horisizer2)
        self.mainsizer.AddSpacer(int(31 * self.scale_factor))
        self.mainsizer.Add(self.gdsizer, 1, wx.EXPAND)
        
    def bind_events(self):
        """Connect UI events to handlers"""
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button5)
        self.resolution_choice.Bind(wx.EVT_CHOICE, self.OnResolutionChange)

        # Set tooltips
        self.button1.SetToolTip(wx.ToolTip("Take ownership here."))
        self.button2.SetToolTip(wx.ToolTip("Hashing, Encryption, Decryption, Verification & Signing"))
        self.button3.SetToolTip(wx.ToolTip("Using TPM and OpenSSL to establish a client-server connection"))
        self.button4.SetToolTip(wx.ToolTip("Making use of policies to seal and unseal objects"))
        self.button5.SetToolTip(wx.ToolTip("Using endorsement key hierarchies to prove/attest"))
        
    def scale_components(self, scale_factor):
        """Scale components proportionally while preserving font sizes"""
        self.scale_factor = scale_factor
        
        # Scale images proportionally
        for image_widget in self.image_widgets:
            bmp = image_widget.GetBitmap()
            img = bmp.ConvertToImage()
            orig_width, orig_height = img.GetWidth(), img.GetHeight()
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            
            if new_width > 0 and new_height > 0:
                img = img.Scale(new_width, new_height, wx.IMAGE_QUALITY_HIGH)
                image_widget.SetBitmap(wx.Bitmap(img))
        
        # Remove existing sizer completely
        self.SetSizer(None)
        
        # Create fresh sizers
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.gdsizer = wx.GridSizer(rows=4, cols=3, vgap=0, hgap=5)
        
        # Create resolution selector layout again
        res_sizer = wx.BoxSizer(wx.HORIZONTAL)
        res_sizer.AddStretchSpacer(1)
        res_sizer.Add(wx.StaticText(self, label="Resolution: "), 0, 
                      wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        res_sizer.Add(self.resolution_choice, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # Create horizontal sizers
        horisizer = wx.BoxSizer(wx.HORIZONTAL)
        horisizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Add components to horizontal sizer
        horisizer.AddSpacer(int(25 * self.scale_factor))
        horisizer.Add(self.tpm_image, 0, wx.TOP, int(17 * self.scale_factor))
        horisizer.AddSpacer(int(175 * self.scale_factor))
        horisizer.Add(self.title_screen, 0, wx.ALIGN_CENTRE)
        horisizer.AddSpacer(int(145 * self.scale_factor))
        horisizer.Add(self.ifx_image, 0, wx.TOP, int(10 * self.scale_factor))
        
        horisizer2.AddSpacer(int(1278 * self.scale_factor))
        
        # Add components to grid sizer
        self.gdsizer.Add(self.tab1_image, 0, wx.ALIGN_CENTRE | wx.TOP, 
                         int(5 * self.scale_factor))
        self.gdsizer.Add(self.tab2_image, 0, wx.ALIGN_CENTRE | wx.TOP, 
                         int(5 * self.scale_factor))
        self.gdsizer.Add(self.tab3_image, 0, wx.ALIGN_CENTRE | wx.TOP, 
                         int(5 * self.scale_factor))
        
        self.gdsizer.Add(self.button1, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(self.button2, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(self.button3, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        
        self.gdsizer.Add(self.tab4_image, 0, wx.ALIGN_CENTRE | wx.TOP, 
                         int(5 * self.scale_factor))
        self.gdsizer.Add(self.tab5_image, 0, wx.ALIGN_CENTRE | wx.TOP, 
                         int(5 * self.scale_factor))
        self.gdsizer.AddSpacer(1)
        
        self.gdsizer.Add(self.button4, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(self.button5, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        self.gdsizer.Add(res_sizer, 1, wx.EXPAND | wx.ALL, int(30 * self.scale_factor))
        
        # Build final layout
        self.mainsizer.Add(horisizer, 0, wx.EXPAND | wx.TOP, int(20 * self.scale_factor))
        self.mainsizer.Add(horisizer2)
        self.mainsizer.AddSpacer(int(31 * self.scale_factor))
        self.mainsizer.Add(self.gdsizer, 1, wx.EXPAND)
        
        # Apply new layout
        self.SetSizer(self.mainsizer)
        self.Layout()
        self.Fit()
        self.Centre()
            
    def OnResolutionChange(self, event):
        """Handle resolution selection changes"""
        choice = self.resolution_choice.GetStringSelection()
        width, height = map(int, choice.split('x'))
        
        # Calculate proportional scaling factor
        scale_factor_w = width / self.base_resolution[0]
        scale_factor_h = height / self.base_resolution[1]
        scale_factor = min(scale_factor_w, scale_factor_h)
        
        # Apply new scaling
        self.scale_components(scale_factor)
        self.SetSize((width, height))
        self.resolution = (width, height)
        self.Centre()
    
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


class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame(None, title="Main")
        self.SetTopWindow(dlg)
        dlg.Centre()
#         wx.lib.inspection.InspectionTool().Show()
        dlg.Show()

if __name__ == "__main__":
    app = Main()
    app.MainLoop()
