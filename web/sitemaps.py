from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from .models import (
    Project, Book, Printable, Music, Multimedia, DigitalArt, CAD, Software, 
    Business, Image, Websitetemplate, Mobiletemplate, Desktoptemplate, Microsofttemplate, Adobetemplate
)

# class BaseSitemap(Sitemap):
#     protocol = 'https'  # Use 'https' for production if your site is secure.

#     def location(self, obj):
#         # Use reverse to generate the relative URL.
#         return reverse(self.view_name, args=[obj.pk])

# Sitemap class for Project model
class ProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse('viewproject', args=[obj.pk])

# Sitemap class for Book model
class BookSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Book.objects.all()

    def location(self, obj):
        return reverse('viewbook', args=[obj.pk])

# Sitemap class for Adobetemplate model
class AdobetemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Adobetemplate.objects.all()

    def location(self, obj):
        return reverse('viewadobetemplate', args=[obj.id])

# Sitemap class for Printable model
class PrintableSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Printable.objects.all()

    def location(self, obj):
        return reverse('viewprintable', args=[obj.pk])

# Sitemap class for Music model
class MusicSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Music.objects.all()

    def location(self, obj):
        return reverse('viewmusic', args=[obj.pk])

# Sitemap class for Multimedia model
class MultimediaSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Multimedia.objects.all()

    def location(self, obj):
        return reverse('viewmultimedia', args=[obj.pk])

# Sitemap class for DigitalArt model
class DigitalArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return DigitalArt.objects.all()

    def location(self, obj):
        return reverse('viewdigitalArt', args=[obj.pk])

# Sitemap class for CAD model
class CADSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return CAD.objects.all()

    def location(self, obj):
        return reverse('viewCAD', args=[obj.pk])

# Sitemap class for Software model
class SoftwareSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Software.objects.all()

    def location(self, obj):
        return reverse('viewsoftware', args=[obj.pk])

# Sitemap class for Business model
class BusinessSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Business.objects.all()

    def location(self, obj):
        return reverse('viewbusiness', args=[obj.pk])

# Sitemap class for Image model
class ImageSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    def items(self):
        return Image.objects.all()

    def location(self, obj):
        return reverse('viewimage', args=[obj.pk])

# Sitemap class for Websitetemplate model
class WebsitetemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Websitetemplate.objects.all()

    def location(self, obj):
        return reverse('viewwebsitetemplate', args=[obj.id])

# Sitemap class for Mobiletemplate model
class MobiletemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Mobiletemplate.objects.all()

    def location(self, obj):
        return reverse('viewmobiletemplate', args=[obj.id])

# Sitemap class for Desktoptemplate model
class DesktoptemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Desktoptemplate.objects.all()

    def location(self, obj):
        return reverse('viewdesktoptemplate', args=[obj.id])

# Sitemap class for Microsofttemplate model
class MicrosofttemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return Microsofttemplate.objects.all()

    def location(self, obj):
        return reverse('viewmicrosofttemplate', args=[obj.id])

# Sitemap class for static Home page
class HomeSitemap(Sitemap):
    priority = 0.9  # Adjust priority based on the importance of your static pages
    changefreq = "monthly"  # Adjust based on how often these pages are updated
    
    def items(self):
        return ['home']

    def location(self, obj):
        return reverse('home')

# Sitemap class for static About page
class AboutSitemap(Sitemap):
    priority = 0.8  # Adjust priority based on the importance of your static pages
    changefreq = "monthly"  # Adjust based on how often these pages are updated
    
    def items(self):
        return ['aboutus']

    def location(self, obj):
        return reverse('aboutus')

# Sitemap class for static Contact page
class ContactSitemap(Sitemap):
    priority = 0.8  # Adjust priority based on the importance of your static pages
    changefreq = "monthly"  # Adjust based on how often these pages are updated
    
    def items(self):
        return ['contactpost']

    def location(self, obj):
        return reverse('contactpost')


# Sitemap class for static Website Project page
class WebsiteProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['websiteproject']  # The view name for the static page
    
    def location(self, obj):
        return reverse('websiteproject')  # Generate the URL using reverse()

# Sitemap class for static Mobile Project page
class MobileProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mobileproject']
    
    def location(self, obj):
        return reverse('mobileproject')

# Sitemap class for static Desktop Project page
class DesktopProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['desktopproject']
    
    def location(self, obj):
        return reverse('desktopproject')

# Sitemap class for static Artificial Project page
class ArtificialProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['artificialproject']
    
    def location(self, obj):
        return reverse('artificialproject')

# Sitemap class for static Embedded Project page
class EmbeddedProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['embededproject']
    
    def location(self, obj):
        return reverse('embededproject')

# Sitemap class for static IoT Project page
class IoTProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['iotproject']
    
    def location(self, obj):
        return reverse('iotproject')

# Sitemap class for static Virtual Reality Project page
class VirtualRealityProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['virtualrealityproject']
    
    def location(self, obj):
        return reverse('virtualrealityproject')

# Sitemap class for static Cyber Project page
class CyberProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['cyberproject']
    
    def location(self, obj):
        return reverse('cyberproject')

# Sitemap class for static Image page
class ImageSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['image']
    
    def location(self, obj):
        return reverse('image')
    
# Sitemap class for static Web Template page
class WebTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['webtemplate']  # The view name for the static page
    
    def location(self, obj):
        return reverse('webtemplate')  # Generate the URL using reverse()

# Sitemap class for static HTML CSS Template page
class HtmlCssTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['htmlcsstemplate']
    
    def location(self, obj):
        return reverse('htmlcsstemplate')

# Sitemap class for static React Template page
class ReactTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['reacttemplate']
    
    def location(self, obj):
        return reverse('reacttemplate')

# Sitemap class for static VueJs Template page
class VueJsTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['vueJs_template']
    
    def location(self, obj):
        return reverse('vueJs_template')

# Sitemap class for static Elm page
class ElmSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['elm']
    
    def location(self, obj):
        return reverse('elm')

# Sitemap class for static Swift page
class SwiftSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['swift']
    
    def location(self, obj):
        return reverse('swift')

# Sitemap class for static JQuery page
class JQuerySitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['JQuery']
    
    def location(self, obj):
        return reverse('JQuery')

# Sitemap class for static Flutter Template page
class FlutterTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['flutter_template']
    
    def location(self, obj):
        return reverse('flutter_template')

# Sitemap class for static Svelte page
class SvelteSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['svelte']
    
    def location(self, obj):
        return reverse('svelte')

# Sitemap class for static Materialize CSS page
class MaterializeCssSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['materialize_CSS']
    
    def location(self, obj):
        return reverse('materialize_CSS')

# Sitemap class for static Foundation page
class FoundationSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['foundation']
    
    def location(self, obj):
        return reverse('foundation')

# Sitemap class for static Angular Template page
class AngularTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['angular_template']
    
    def location(self, obj):
        return reverse('angular_template')

# Sitemap class for static Tailwind CSS page
class TailwindCssSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['tailwind_CSS']
    
    def location(self, obj):
        return reverse('tailwind_CSS')

# Sitemap class for static Bootstrap Template page
class BootstrapTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['bootstrap_template']
    
    def location(self, obj):
        return reverse('bootstrap_template')
    
# Sitemap class for static Mobile Template page
class MobileTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mobiletemplate']
    
    def location(self, obj):
        return reverse('mobiletemplate')

# Sitemap class for static React Native Template page
class ReactNativeTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['reactnativetemplate']
    
    def location(self, obj):
        return reverse('reactnativetemplate')

# Sitemap class for static Flutter Mobile Template page
class FlutterMobileTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['flutter_mobile_template']
    
    def location(self, obj):
        return reverse('flutter_mobile_template')

# Sitemap class for static SwiftUI page
class SwiftUISitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['swiftUI']
    
    def location(self, obj):
        return reverse('swiftUI')

# Sitemap class for static Jetpack Compose page
class JetpackComposeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['jetpack_Compose']
    
    def location(self, obj):
        return reverse('jetpack_Compose')

# Sitemap class for static Ionic Framework page
class IonicFrameworkSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['ionic_Framework']
    
    def location(self, obj):
        return reverse('ionic_Framework')

# Sitemap class for static Xamarin page
class XamarinSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['xamarin']
    
    def location(self, obj):
        return reverse('xamarin')

# Sitemap class for static PhoneGap page
class PhoneGapSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['phoneGap']
    
    def location(self, obj):
        return reverse('phoneGap')

# Sitemap class for static NativeScript page
class NativeScriptSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['nativeScript']
    
    def location(self, obj):
        return reverse('nativeScript')

# Sitemap class for static Framework Seven page
class FrameworkSevenSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['framework_seven']
    
    def location(self, obj):
        return reverse('framework_seven')

# Sitemap class for static Onsen UI page
class OnsenUISitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['onsen_UI']
    
    def location(self, obj):
        return reverse('onsen_UI')

# Sitemap class for static jQuery Mobile page
class JQueryMobileSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['jQuery_Mobile']
    
    def location(self, obj):
        return reverse('jQuery_Mobile')

# Sitemap class for static Sencha Touch page
class SenchaTouchSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['sencha_Touch']
    
    def location(self, obj):
        return reverse('sencha_Touch')

# Sitemap class for static Kivy Template page
class KivyTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Kivy_template']
    
    def location(self, obj):
        return reverse('Kivy_template')

# Sitemap class for static Bootstrap Mobile Templates page
class BootstrapMobileTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['bootstrap_Mobile_Templates']
    
    def location(self, obj):
        return reverse('bootstrap_Mobile_Templates')

# Sitemap class for static Quasar Framework page
class QuasarFrameworkSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['quasar_Framework']
    
    def location(self, obj):
        return reverse('quasar_Framework')
    
# Sitemap class for static Desktop Template page
class DesktopTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['desktoptemplate']
    
    def location(self, obj):
        return reverse('desktoptemplate')

# Sitemap class for static Kivy Template page
class KivyTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['kivytemplate']
    
    def location(self, obj):
        return reverse('kivytemplate')

# Sitemap class for static PyQt Template page
class PyQtTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['pyqttemplate']
    
    def location(self, obj):
        return reverse('pyqttemplate')

# Sitemap class for static C Template page
class CTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['ctemplate']
    
    def location(self, obj):
        return reverse('ctemplate')

# Sitemap class for static Tkinter Template page
class TkinterTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['tkintertemplate']
    
    def location(self, obj):
        return reverse('tkintertemplate')

# Sitemap class for static C# Desktop App page
class CSharpDesktopAppSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['chashdesktopapp']
    
    def location(self, obj):
        return reverse('chashdesktopapp')

# Sitemap class for static Java Desktop App page
class JavaDesktopAppSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['javadesktopapp']
    
    def location(self, obj):
        return reverse('javadesktopapp')

# Sitemap class for static C++ Desktop App page
class CPlusDesktopAppSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['cplusdesktopapp']
    
    def location(self, obj):
        return reverse('cplusdesktopapp')

# Sitemap class for static Electron Desktop App page
class ElectronDesktopAppSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['electrondesktopapp']
    
    def location(self, obj):
        return reverse('electrondesktopapp')

# Sitemap class for static Swift Desktop App page
class SwiftDesktopAppSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['swiftdesktopapp']
    
    def location(self, obj):
        return reverse('swiftdesktopapp')

# Sitemap class for static Rust Desktop App page
class RustDesktopAppSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['rustdesktopapp']
    
    def location(self, obj):
        return reverse('rustdesktopapp')

# Sitemap class for static Microsoft Template page
class MicrosoftTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['microsofttemplate']
    
    def location(self, obj):
        return reverse('microsofttemplate')

# Sitemap class for static Word Template page
class WordTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wordtemplate']
    
    def location(self, obj):
        return reverse('wordtemplate')

# Sitemap class for static Excel Template page
class ExcelTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['excelltemplate']
    
    def location(self, obj):
        return reverse('excelltemplate')

# Sitemap class for static PowerPoint Template page
class PowerPointTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['powerpointtemplate']
    
    def location(self, obj):
        return reverse('powerpointtemplate')

# Sitemap class for static Publisher Template page
class PublisherTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['publishertemplate']
    
    def location(self, obj):
        return reverse('publishertemplate')
    
# Sitemap class for Adobe Template page
class AdobeTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['adobetemplate']
    
    def location(self, obj):
        return reverse('adobetemplate')

# Sitemap class for Photoshop Template page
class PhotoshopTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['photoshoptemplate']
    
    def location(self, obj):
        return reverse('photoshoptemplate')

# Sitemap class for Premiere Template page
class PremiereTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['primiertemplate']
    
    def location(self, obj):
        return reverse('primiertemplate')

# Sitemap class for Illustrator Template page
class IllustratorTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['illustratortemplate']
    
    def location(self, obj):
        return reverse('illustratortemplate')

# Sitemap class for InDesign Adobe page
class InDesignAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['InDesignadobe']
    
    def location(self, obj):
        return reverse('InDesignadobe')

# Sitemap class for XD Adobe page
class XDadobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['XDadobe']
    
    def location(self, obj):
        return reverse('XDadobe')

# Sitemap class for Lightroom Adobe page
class LightroomAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Lightroomadobe']
    
    def location(self, obj):
        return reverse('Lightroomadobe')

# Sitemap class for Lightroom Classic Adobe page
class LightroomClassicAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['LightroomClassicadobe']
    
    def location(self, obj):
        return reverse('LightroomClassicadobe')

# Sitemap class for After Effects Adobe page
class AfterEffectsAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['AfterEffectsadobe']
    
    def location(self, obj):
        return reverse('AfterEffectsadobe')

# Sitemap class for Animate Adobe page
class AnimateAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Animateadobe']
    
    def location(self, obj):
        return reverse('Animateadobe')

# Sitemap class for Dreamweaver Adobe page
class DreamweaverAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Dreamweaveradobe']
    
    def location(self, obj):
        return reverse('Dreamweaveradobe')

# Sitemap class for Audition Adobe page
class AuditionAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Auditionadobe']
    
    def location(self, obj):
        return reverse('Auditionadobe')

# Sitemap class for Bridge Adobe page
class BridgeAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Bridgeadobe']
    
    def location(self, obj):
        return reverse('Bridgeadobe')

# Sitemap class for Dimension Adobe page
class DimensionAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Dimensionadobe']
    
    def location(self, obj):
        return reverse('Dimensionadobe')

# Sitemap class for Fresco Adobe page
class FrescoAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Frescoadobe']
    
    def location(self, obj):
        return reverse('Frescoadobe')

# Sitemap class for Character Animator Adobe page
class CharacterAnimatorAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['CharacterAnimatoradobe']
    
    def location(self, obj):
        return reverse('CharacterAnimatoradobe')

# Sitemap class for Media Encoder Adobe page
class MediaEncoderAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['MediaEncoderadobe']
    
    def location(self, obj):
        return reverse('MediaEncoderadobe')

# Sitemap class for Rush Adobe page
class RushAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Rushadobe']
    
    def location(self, obj):
        return reverse('Rushadobe')

# Sitemap class for Spark Adobe page
class SparkAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Sparkadobe']
    
    def location(self, obj):
        return reverse('Sparkadobe')

# Sitemap class for Substance 3D Painter Adobe page
class Substance3DPainterAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Substance3DPainteradobe']
    
    def location(self, obj):
        return reverse('Substance3DPainteradobe')

# Sitemap class for Substance 3D Designer Adobe page
class Substance3DDesignerAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Substance3DDesigneradobe']
    
    def location(self, obj):
        return reverse('Substance3DDesigneradobe')

# Sitemap class for Substance 3D Sampler Adobe page
class Substance3DSamplerAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Substance3DSampleradobe']
    
    def location(self, obj):
        return reverse('Substance3DSampleradobe')

# Sitemap class for Substance 3D Stager Adobe page
class Substance3DStagerAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Substance3DStageradobe']
    
    def location(self, obj):
        return reverse('Substance3DStageradobe')

# Sitemap class for Acrobat Pro DC Adobe page
class AcrobatProDCAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['AcrobatProDCadobe']
    
    def location(self, obj):
        return reverse('AcrobatProDCadobe')

# Sitemap class for Sign Adobe page
class SignAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Signadobe']
    
    def location(self, obj):
        return reverse('Signadobe')

# Sitemap class for FrameMaker Adobe page
class FrameMakerAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['FrameMakeradobe']
    
    def location(self, obj):
        return reverse('FrameMakeradobe')

# Sitemap class for Engage Adobe page
class EngageAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Engageadobe']
    
    def location(self, obj):
        return reverse('Engageadobe')

# Sitemap class for Presenter Adobe page
class PresenterAdobeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Presenteradobe']
    
    def location(self, obj):
        return reverse('Presenteradobe')
    
# Sitemap class for Template page
class TemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['template']
    
    def location(self, obj):
        return reverse('template')

# Sitemap class for Project page
class ProjectSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['project']
    
    def location(self, obj):
        return reverse('project')

# Sitemap class for Course page
class CourseSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['course']
    
    def location(self, obj):
        return reverse('course')

# Sitemap class for Ebooks page
class EbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['ebooks']
    
    def location(self, obj):
        return reverse('ebooks')

# Sitemap class for Music page
class MusicSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['music']
    
    def location(self, obj):
        return reverse('music')

# Sitemap class for Video page
class VideoSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['video']
    
    def location(self, obj):
        return reverse('video')

# Sitemap class for Art page
class ArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['art']
    
    def location(self, obj):
        return reverse('art')

# Sitemap class for CAD page
class CadSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['cad']
    
    def location(self, obj):
        return reverse('cad')

# Sitemap class for Printable page
class PrintableSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['printable']
    
    def location(self, obj):
        return reverse('printable')

# Sitemap class for Software page
class SoftwareSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['software']
    
    def location(self, obj):
        return reverse('software')

# Sitemap class for Business page
class BusinessSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['business']
    
    def location(self, obj):
        return reverse('business')
    
# Sitemap class for Novels page
class NovelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['novels']
    
    def location(self, obj):
        return reverse('novels')

# Sitemap class for Short Stories page
class ShortStoriesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['short_stories']
    
    def location(self, obj):
        return reverse('short_stories')

# Sitemap class for Poetry page
class PoetrySitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['poetry']
    
    def location(self, obj):
        return reverse('poetry')

# Sitemap class for Flash Fiction page
class FlashFictionSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['flash_fiction']
    
    def location(self, obj):
        return reverse('flash_fiction')

# Sitemap class for Self Help Book page
class SelfHelpBookSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['self_help_book']
    
    def location(self, obj):
        return reverse('self_help_book')

# Sitemap class for Biographies page
class BiographiesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['biographies']
    
    def location(self, obj):
        return reverse('biographies')

# Sitemap class for Personal Development Books page
class PersonalDevelopmentBooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['personal_development_books']
    
    def location(self, obj):
        return reverse('personal_development_books')

# Sitemap class for History Books page
class HistoryBooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['history_books']
    
    def location(self, obj):
        return reverse('history_books')

# Sitemap class for True Crime page
class TrueCrimeSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['true_crime']
    
    def location(self, obj):
        return reverse('true_crime')

# Sitemap class for Textbooks page
class TextbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['textbooks']
    
    def location(self, obj):
        return reverse('textbooks')

# Sitemap class for Research Papers page
class ResearchPapersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['research_papers']
    
    def location(self, obj):
        return reverse('research_papers')

# Sitemap class for Study Guides page
class StudyGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['study_guides']
    
    def location(self, obj):
        return reverse('study_guides')

# Sitemap class for How To Guides & Tutorials page
class HowToGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['how_to_guides_tutorials']
    
    def location(self, obj):
        return reverse('how_to_guides_tutorials')

# Sitemap class for Business Strategy Guides page
class BusinessStrategyGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['business_strategy_guides']
    
    def location(self, obj):
        return reverse('business_strategy_guides')

# Sitemap class for Marketing and Sales E-books page
class MarketingAndSalesEbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['marketing_and_sales_e_books']
    
    def location(self, obj):
        return reverse('marketing_and_sales_e_books')

# Sitemap class for Entrepreneurship Guides page
class EntrepreneurshipGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['entrepreneurship_guides']
    
    def location(self, obj):
        return reverse('entrepreneurship_guides')

# Sitemap class for Financial Planning page
class FinancialPlanningSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['financial_planning']
    
    def location(self, obj):
        return reverse('financial_planning')

# Sitemap class for Nutrition Guides page
class NutritionGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['nutrition_guides']
    
    def location(self, obj):
        return reverse('nutrition_guides')

# Sitemap class for Workout and Fitness Plans page
class WorkoutAndFitnessPlansSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['workout_and_fitness_plans']
    
    def location(self, obj):
        return reverse('workout_and_fitness_plans')

# Sitemap class for Mental Health & Wellness page
class MentalHealthWellnessSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mental_health_wellness']
    
    def location(self, obj):
        return reverse('mental_health_wellness')

# Sitemap class for Meditation and Mindfulness E-books page
class MeditationAndMindfulnessEbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['meditation_and_mindfulness_e_books']
    
    def location(self, obj):
        return reverse('meditation_and_mindfulness_e_books')

# Sitemap class for Coding and Programming Tutorials page
class CodingAndProgrammingTutorialsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['coding_and_programming_tutorials']
    
    def location(self, obj):
        return reverse('coding_and_programming_tutorials')

# Sitemap class for Software Manuals page
class SoftwareManualsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['software_manuals']
    
    def location(self, obj):
        return reverse('software_manuals')

# Sitemap class for IT and Networking Guides page
class ITAndNetworkingGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['IT_and_networking_guides']
    
    def location(self, obj):
        return reverse('IT_and_networking_guides')

# Sitemap class for Artificial Intelligence & Machine Learning page
class AImachineLearningSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['artificial_intelligence_machine_learning']
    
    def location(self, obj):
        return reverse('artificial_intelligence_machine_learning')

# Sitemap class for Photography Tutorials page
class PhotographyTutorialsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['photography_tutorials']
    
    def location(self, obj):
        return reverse('photography_tutorials')

# Sitemap class for Painting and Drawing Guides page
class PaintingAndDrawingGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['painting_and_drawing_guides']
    
    def location(self, obj):
        return reverse('painting_and_drawing_guides')

# Sitemap class for Writing and Storytelling Techniques page
class WritingAndStorytellingTechniquesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['writing_and_storytelling_techniques']
    
    def location(self, obj):
        return reverse('writing_and_storytelling_techniques')

# Sitemap class for Crafting DIY Projects page
class CraftingDIYProjectsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['crafting_DIY_projects']
    
    def location(self, obj):
        return reverse('crafting_DIY_projects')

# Sitemap class for Recipe Collections page
class RecipeCollectionsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['recipe_collections']
    
    def location(self, obj):
        return reverse('recipe_collections')

# Sitemap class for Specialized Diet Guides page
class SpecializedDietGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['specialized_diet_guides']
    
    def location(self, obj):
        return reverse('specialized_diet_guides')

# Sitemap class for Meal Planning and Prep page
class MealPlanningAndPrepSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['meal_planning_and_prep']
    
    def location(self, obj):
        return reverse('meal_planning_and_prep')

# Sitemap class for Parenting Advice page
class ParentingAdviceSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['parenting_advice']
    
    def location(self, obj):
        return reverse('parenting_advice')

# Sitemap class for Marriage and Relationship Counseling page
class MarriageAndRelationshipCounselingSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['marriage_and_relationship_counseling']
    
    def location(self, obj):
        return reverse('marriage_and_relationship_counseling')

# Sitemap class for Family Planning Guides page
class FamilyPlanningGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['family_planning_guides']
    
    def location(self, obj):
        return reverse('family_planning_guides')

# Sitemap class for Childcare and Development page
class ChildcareAndDevelopmentSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['childcare_and_development']
    
    def location(self, obj):
        return reverse('childcare_and_development')

# Sitemap class for Travel Guides page
class TravelGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['travel_guides']
    
    def location(self, obj):
        return reverse('travel_guides')

# Sitemap class for Destination Reviews page
class DestinationReviewsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['destination_reviews']
    
    def location(self, obj):
        return reverse('destination_reviews')

# Sitemap class for Adventure Stories page
class AdventureStoriesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['adventure_stories']
    
    def location(self, obj):
        return reverse('adventure_stories')

# Sitemap class for Travel Planning and Budgeting page
class TravelPlanningAndBudgetingSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['travel_planning_and_budgeting']
    
    def location(self, obj):
        return reverse('travel_planning_and_budgeting')

# Sitemap class for Personal Finance E-books page
class PersonalFinanceEbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['personal_finance_e_books']
    
    def location(self, obj):
        return reverse('personal_finance_e_books')

# Sitemap class for Investment Strategies page
class InvestmentStrategiesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['investment_strategies']
    
    def location(self, obj):
        return reverse('investment_strategies')

# Sitemap class for Retirement Planning page
class RetirementPlanningSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['retirement_planning']
    
    def location(self, obj):
        return reverse('retirement_planning')

# Sitemap class for Budgeting Tips page
class BudgetingTipsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['budgeting_tips']
    
    def location(self, obj):
        return reverse('budgeting_tips')

# Sitemap class for Religious Texts page
class ReligiousTextsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['religious_texts']
    
    def location(self, obj):
        return reverse('religious_texts')

# Sitemap class for Spiritual Growth Guides page
class SpiritualGrowthGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['spiritual_growth_guides']
    
    def location(self, obj):
        return reverse('spiritual_growth_guides')

# Sitemap class for Meditation and Mindfulness Books page
class MeditationAndMindfulnessBooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['meditation_and_mindfulness_books']
    
    def location(self, obj):
        return reverse('meditation_and_mindfulness_books')

# Sitemap class for Philosophy and Life Purpose E-books page
class PhilosophyAndLifePurposeEbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['philosophy_and_life_purpose_e_books']
    
    def location(self, obj):
        return reverse('philosophy_and_life_purpose_e_books')

# Sitemap class for Time Management and Productivity page
class TimeManagementAndProductivitySitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['time_management_and_productivity']
    
    def location(self, obj):
        return reverse('time_management_and_productivity')

# Sitemap class for Self Improvement and Motivation page
class SelfImprovementAndMotivationSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['self_improvement_and_motivation']
    
    def location(self, obj):
        return reverse('self_improvement_and_motivation')

# Sitemap class for Life Coaching Guides page
class LifeCoachingGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['life_coaching_guides']
    
    def location(self, obj):
        return reverse('life_coaching_guides')

# Sitemap class for Work Life Balance page
class WorkLifeBalanceSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['work_life_balance']
    
    def location(self, obj):
        return reverse('work_life_balance')

# Sitemap class for Legal Guides and Contracts page
class LegalGuidesAndContractsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['legal_guides_and_contracts']
    
    def location(self, obj):
        return reverse('legal_guides_and_contracts')

# Sitemap class for HR and Employment Handbooks page
class HRAndEmploymentHandbooksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['HR_and_employment_handbooks']
    
    def location(self, obj):
        return reverse('HR_and_employment_handbooks')

# Sitemap class for Professional Development page
class ProfessionalDevelopmentSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['professional_development']
    
    def location(self, obj):
        return reverse('professional_development')

# Sitemap class for Real Estate Investment Guides page
class RealEstateInvestmentGuidesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['real_estate_investment_guides']
    
    def location(self, obj):
        return reverse('real_estate_investment_guides')

# Sitemap class for Property Management Manuals page
class PropertyManagementManualsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['property_management_manuals']
    
    def location(self, obj):
        return reverse('property_management_manuals')

# Sitemap class for Buying and Selling Homes page
class BuyingAndSellingHomesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['buying_and_selling_homes']
    
    def location(self, obj):
        return reverse('buying_and_selling_homes')
    
# Sitemap class for Single Tracks page
class SingleTracksSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['single_tracks']
    
    def location(self, obj):
        return reverse('single_tracks')

# Sitemap class for Full Albums page
class FullAlbumsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['full_albums']
    
    def location(self, obj):
        return reverse('full_albums')

# Sitemap class for Extended Plays page
class ExtendedPlaysSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['extended_plays']
    
    def location(self, obj):
        return reverse('extended_plays')

# Sitemap class for Instrumental Versions page
class InstrumentalVersionsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['instrumental_versions']
    
    def location(self, obj):
        return reverse('instrumental_versions')

# Sitemap class for Beats for Rappers and Singers page
class BeatsForRappersAndSingersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['beats_for_rappers_and_singers']
    
    def location(self, obj):
        return reverse('beats_for_rappers_and_singers')

# Sitemap class for Lo-fi Beats page
class LoFiBeatsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['lo_fi_beats']
    
    def location(self, obj):
        return reverse('lo_fi_beats')

# Sitemap class for Background Instrumentals for Videos page
class BackgroundInstrumentalsForVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['background_instrumentals_for_videos']
    
    def location(self, obj):
        return reverse('background_instrumentals_for_videos')

# Sitemap class for Royalty-Free Music page
class RoyaltyFreeMusicSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['royalty_free_music']
    
    def location(self, obj):
        return reverse('royalty_free_music')

# Sitemap class for Environmental Sounds page
class EnvironmentalSoundsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['environmental_sounds']
    
    def location(self, obj):
        return reverse('environmental_sounds')

# Sitemap class for Foley Sounds page
class FoleySoundsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['foley_sounds']
    
    def location(self, obj):
        return reverse('foley_sounds')

# Sitemap class for Sci-Fi and Futuristic Sounds page
class SciFiAndFuturisticSoundsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['sci_fi_and_futuristic_sounds']
    
    def location(self, obj):
        return reverse('sci_fi_and_futuristic_sounds')

# Sitemap class for Horror and Thriller Effects page
class HorrorAndThrillerEffectsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['horror_and_thriller_effects']
    
    def location(self, obj):
        return reverse('horror_and_thriller_effects')

# Sitemap class for Drum Loops page
class DrumLoopsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['drum_loops']
    
    def location(self, obj):
        return reverse('drum_loops')

# Sitemap class for Melodic Loops page
class MelodicLoopsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['melodic_loops']
    
    def location(self, obj):
        return reverse('melodic_loops')

# Sitemap class for Vocal Samples page
class VocalSamplesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['vocal_samples']
    
    def location(self, obj):
        return reverse('vocal_samples')

# Sitemap class for Synth and Bass Loops page
class SynthAndBassLoopsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['synth_and_bass_loops']
    
    def location(self, obj):
        return reverse('synth_and_bass_loops')

# Sitemap class for Background Music for Videos page
class BackgroundMusicForVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['background_music_for_videos']
    
    def location(self, obj):
        return reverse('background_music_for_videos')

# Sitemap class for Music for Podcasts page
class MusicForPodcastsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['music_for_podcasts']
    
    def location(self, obj):
        return reverse('music_for_podcasts')

# Sitemap class for Royalty-Free Soundtracks for Commercials page
class RoyaltyFreeSoundtracksForCommercialsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['royalty_free_soundtracks_for_commercials']
    
    def location(self, obj):
        return reverse('royalty_free_soundtracks_for_commercials')

# Sitemap class for Ambient Music for Relaxation and Meditation page
class AmbientMusicForRelaxationAndMeditationSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['ambient_music_for_relaxation_and_meditation']
    
    def location(self, obj):
        return reverse('ambient_music_for_relaxation_and_meditation')

# Sitemap class for Talk Shows page
class TalkShowsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['talk_shows']
    
    def location(self, obj):
        return reverse('talk_shows')

# Sitemap class for Interview Series page
class InterviewSeriesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['interview_series']
    
    def location(self, obj):
        return reverse('interview_series')

# Sitemap class for Educational Podcasts page
class EducationalPodcastsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['educational_podcasts']
    
    def location(self, obj):
        return reverse('educational_podcasts')

# Sitemap class for Storytelling and Fictional Audio Series page
class StorytellingAndFictionalAudioSeriesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['storytelling_and_fictional_audio_series']
    
    def location(self, obj):
        return reverse('storytelling_and_fictional_audio_series')

# Sitemap class for Nature-Inspired Soundscapes page
class NatureInspiredSoundscapesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['nature_inspired_soundscapes']
    
    def location(self, obj):
        return reverse('nature_inspired_soundscapes')
    
# Sitemap class for Nature and Landscape Footage page
class NatureAndLandscapeFootageSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['nature_and_landscape_footage']
    
    def location(self, obj):
        return reverse('nature_and_landscape_footage')

# Sitemap class for Urban and City Life Footage page
class UrbanAndCityLifeFootageSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['urban_and_city_life_footage']
    
    def location(self, obj):
        return reverse('urban_and_city_life_footage')

# Sitemap class for Aerial Drone Videos page
class AerialDroneVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['aerial_drone_videos']
    
    def location(self, obj):
        return reverse('aerial_drone_videos')

# Sitemap class for Slow Motion and Time Lapse Videos page
class SlowMotionAndTimeLapseVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['slow_motion_and_time_lapse_videos']
    
    def location(self, obj):
        return reverse('slow_motion_and_time_lapse_videos')

# Sitemap class for Intros and Outros for YouTube Videos page
class IntrosAndOutrosForYouTubeVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['intros_and_outros_for_YouTube_videos']
    
    def location(self, obj):
        return reverse('intros_and_outros_for_YouTube_videos')

# Sitemap class for Two Animations page
class TwoAnimationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['two_animations']
    
    def location(self, obj):
        return reverse('two_animations')

# Sitemap class for Three Animations page
class ThreeAnimationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['three_animations']
    
    def location(self, obj):
        return reverse('three_animations')

# Sitemap class for Explainer Videos page
class ExplainerVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['explainer_videos']
    
    def location(self, obj):
        return reverse('explainer_videos')

# Sitemap class for Motion Graphics for Commercials page
class MotionGraphicsForCommercialsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['motion_graphics_for_commercials']
    
    def location(self, obj):
        return reverse('motion_graphics_for_commercials')

# Sitemap class for Personal Vlogs page
class PersonalVlogsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['personal_vlogs']
    
    def location(self, obj):
        return reverse('personal_vlogs')

# Sitemap class for Travel Videos page
class TravelVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['travel_videos']
    
    def location(self, obj):
        return reverse('travel_videos')

# Sitemap class for Lifestyle Vlogs page
class LifestyleVlogsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['lifestyl_vlogs']
    
    def location(self, obj):
        return reverse('lifestyl_vlogs')

# Sitemap class for Daily Video Blogs page
class DailyVideoBlogsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['daily_video_blogs']
    
    def location(self, obj):
        return reverse('daily_video_blogs')

# Sitemap class for Wedding Videos page
class WeddingVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wedding_videos']
    
    def location(self, obj):
        return reverse('wedding_videos')

# Sitemap class for Corporate Event Videos page
class CorporateEventVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['corporate_event_videos']
    
    def location(self, obj):
        return reverse('corporate_event_videos')

# Sitemap class for Party and Celebration Videos page
class PartyAndCelebrationVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['party_and_celebration_videos']
    
    def location(self, obj):
        return reverse('party_and_celebration_videos')

# Sitemap class for Award Ceremony Video page
class AwardCeremonyVideoSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['award_ceremony_Video']
    
    def location(self, obj):
        return reverse('award_ceremony_Video')

# Sitemap class for Business Presentations page
class BusinessPresentationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['business_presentations']
    
    def location(self, obj):
        return reverse('business_presentations')

# Sitemap class for Sales Pitches page
class SalesPitchesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['sales_pitches']
    
    def location(self, obj):
        return reverse('sales_pitches')

# Sitemap class for Educational or Academic Presentations page
class EducationalOrAcademicPresentationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['educational_or_academic_presentations']
    
    def location(self, obj):
        return reverse('educational_or_academic_presentations')

# Sitemap class for Product Promo Videos page
class ProductPromoVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['product_promo_videos']
    
    def location(self, obj):
        return reverse('product_promo_videos')

# Sitemap class for Service Advertisement Videos page
class ServiceAdvertisementVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['service_advertisement_videos']
    
    def location(self, obj):
        return reverse('service_advertisement_videos')

# Sitemap class for Brand Story Videos page
class BrandStoryVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['brand_story_videos']
    
    def location(self, obj):
        return reverse('brand_story_videos')

# Sitemap class for Social Media Ads page
class SocialMediaAdsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['social_media_ads']
    
    def location(self, obj):
        return reverse('social_media_ads')

# Sitemap class for Official Music Videos page
class OfficialMusicVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['official_music_videos']
    
    def location(self, obj):
        return reverse('official_music_videos')

# Sitemap class for Lyric Videos page
class LyricVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['lyric_videos']
    
    def location(self, obj):
        return reverse('lyric_videos')

# Sitemap class for Animated Music Videos page
class AnimatedMusicVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['animated_music_videos']
    
    def location(self, obj):
        return reverse('animated_music_videos')

# Sitemap class for Performance Videos page
class PerformanceVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['performance_videos']
    
    def location(self, obj):
        return reverse('performance_videos')

# Sitemap class for Fiction Short Films page
class FictionShortFilmsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fiction_short_films']
    
    def location(self, obj):
        return reverse('fiction_short_films')

# Sitemap class for Mini Documentaries page
class MiniDocumentariesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mini_documentaries']
    
    def location(self, obj):
        return reverse('mini_documentaries')

# Sitemap class for Biographical Documentaries page
class BiographicalDocumentariesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['biographical_documentaries']
    
    def location(self, obj):
        return reverse('biographical_documentaries')

# Sitemap class for Indie Films page
class IndieFilmsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['indie_films']
    
    def location(self, obj):
        return reverse('indie_films')

# Sitemap class for Adventure Videos page
class AdventureVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['adventure_videos']
    
    def location(self, obj):
        return reverse('adventure_videos')

# Sitemap class for Interactive Tutorials page
class InteractiveTutorialsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['interactive_tutorials']
    
    def location(self, obj):
        return reverse('interactive_tutorials')

# Sitemap class for Interactive Quizzes or Assessments page
class InteractiveQuizzesOrAssessmentsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['interactive_quizzes_or_assessments']
    
    def location(self, obj):
        return reverse('interactive_quizzes_or_assessments')

# Sitemap class for Gamified Videos page
class GamifiedVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['gamified_videos']
    
    def location(self, obj):
        return reverse('gamified_videos')

# Sitemap class for Customer Testimonial Videos page
class CustomerTestimonialVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['customer_testimonial_videos']
    
    def location(self, obj):
        return reverse('customer_testimonial_videos')

# Sitemap class for Product Review Videos page
class ProductReviewVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['product_review_videos']
    
    def location(self, obj):
        return reverse('product_review_videos')

# Sitemap class for User Generated Content Videos page
class UserGeneratedContentVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['user_generated_content_videos']
    
    def location(self, obj):
        return reverse('user_generated_content_videos')

# Sitemap class for Virtual Reality Experiences page
class VirtualRealityExperiencesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['virtual_reality_experiences']
    
    def location(self, obj):
        return reverse('virtual_reality_experiences')

# Sitemap class for Degree Video Tours page
class DegreeVideoToursSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['degree_video_tours']
    
    def location(self, obj):
        return reverse('degree_video_tours')

# Sitemap class for Immersive Event Videos page
class ImmersiveEventVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['immersive_event_videos']
    
    def location(self, obj):
        return reverse('immersive_event_videos')

# Sitemap class for Cinematic Sequences page
class CinematicSequencesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['cinematic_sequences']
    
    def location(self, obj):
        return reverse('cinematic_sequences')

# Sitemap class for Aerial Drone Footage page
class AerialDroneFootageSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['aerial_drone_footage']
    
    def location(self, obj):
        return reverse('aerial_drone_footage')

# Sitemap class for Scenic Landscape Shots page
class ScenicLandscapeShotsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['scenic_landscape_shots']
    
    def location(self, obj):
        return reverse('scenic_landscape_shots')

# Sitemap class for Epic Slow Motion Videos page
class EpicSlowMotionVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['epic_slow_motion_videos']
    
    def location(self, obj):
        return reverse('epic_slow_motion_videos')

# Sitemap class for Urban Timelapse Videos page
class UrbanTimelapseVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['urban_timelapse_videos']
    
    def location(self, obj):
        return reverse('urban_timelapse_videos')

# Sitemap class for Nature and Sky Timelapse page
class NatureAndSkyTimelapseSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['nature_and_sky_timelapse']
    
    def location(self, obj):
        return reverse('nature_and_sky_timelapse')

# Sitemap class for Construction Progress Timelapse page
class ConstructionProgressTimelapseSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['construction_progress_timelapse']
    
    def location(self, obj):
        return reverse('construction_progress_timelapse')

# Sitemap class for Yoga and Meditation Videos page
class YogaAndMeditationVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['yoga_and_meditation_videos']
    
    def location(self, obj):
        return reverse('yoga_and_meditation_videos')

# Sitemap class for Healthy Lifestyle Tips page
class HealthyLifestyleTipsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['healthy_lifestyle_tips']
    
    def location(self, obj):
        return reverse('healthy_lifestyle_tips')

# Sitemap class for Exercise and Wellness Programs page
class ExerciseAndWellnessProgramsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['exercise_and_wellness_programs']
    
    def location(self, obj):
        return reverse('exercise_and_wellness_programs')

# Sitemap class for Product Feature Demonstrations page
class ProductFeatureDemonstrationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['product_feature_demonstrations']
    
    def location(self, obj):
        return reverse('product_feature_demonstrations')

# Sitemap class for Physical Product Unboxing and Reviews page
class PhysicalProductUnboxingAndReviewsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['physical_product_unboxing_and_reviews']
    
    def location(self, obj):
        return reverse('physical_product_unboxing_and_reviews')

# Sitemap class for Animated YouTube Intros page
class AnimatedYouTubeIntrosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['animated_YouTube_intros']
    
    def location(self, obj):
        return reverse('animated_YouTube_intros')

# Sitemap class for Branding Outros for Videos page
class BrandingOutrosForVideosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['branding_outros_for_videos']
    
    def location(self, obj):
        return reverse('branding_outros_for_videos')

# Sitemap class for Social Media Content Intros page
class SocialMediaContentIntrosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['social_media_content_intros']
    
    def location(self, obj):
        return reverse('social_media_content_intros')
    
class HandDrawnDigitalIllustrationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['hand_drawn_digital_illustrations']
    
    def location(self, obj):
        return reverse('hand_drawn_digital_illustrations')

class CharacterDesignSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['character_design']
    
    def location(self, obj):
        return reverse('character_design')

class WebsiteDesignTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['website_design_templates']
    
    def location(self, obj):
        return reverse('website_design_templates')

class MobileAppDesignTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mobile_app_design_templates']
    
    def location(self, obj):
        return reverse('mobile_app_design_templates')

class EditorialIllustrationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['editorial_illustrations']
    
    def location(self, obj):
        return reverse('editorial_illustrations')

class ChildrenBookIllustrationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['children_book_illustrations']
    
    def location(self, obj):
        return reverse('children_book_illustrations')

class PostersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['posters']
    
    def location(self, obj):
        return reverse('posters')

class FlyersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['flyers']
    
    def location(self, obj):
        return reverse('flyers')

class BrochuresSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['brochures']
    
    def location(self, obj):
        return reverse('brochures')

class InfographicsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['infographics']
    
    def location(self, obj):
        return reverse('infographics')

class DigitalAdvertisementsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['digital_advertisements']
    
    def location(self, obj):
        return reverse('digital_advertisements')

class BrandLogosSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['brand_logos']
    
    def location(self, obj):
        return reverse('brand_logos')

class IconSetsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['icon_sets']
    
    def location(self, obj):
        return reverse('icon_sets')

class CustomLogosForBusinessesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_logos_for_businesses']
    
    def location(self, obj):
        return reverse('custom_logos_for_businesses')

class MonogramsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['monograms']
    
    def location(self, obj):
        return reverse('monograms')

class ScalableVectorIllustrationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['scalable_vector_illustrations']
    
    def location(self, obj):
        return reverse('scalable_vector_illustrations')

class FlatDesignElementsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['flat_design_elements']
    
    def location(self, obj):
        return reverse('flat_design_elements')

class IconsAndSymbolsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['icons_and_symbols']
    
    def location(self, obj):
        return reverse('icons_and_symbols')

class GeometricPatternsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['geometric_patterns']
    
    def location(self, obj):
        return reverse('geometric_patterns')

class ThreeModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['three_models']
    
    def location(self, obj):
        return reverse('three_models')

class ThreeCharacterDesignSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['three_character_design']
    
    def location(self, obj):
        return reverse('three_character_design')
    
# Additional Static Pages
class ProductVisualizationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['product_visualizations']
    
    def location(self, obj):
        return reverse('product_visualizations')

class CustomFontsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_fonts']
    
    def location(self, obj):
        return reverse('custom_fonts')

class HandLetteringDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['hand_lettering_designs']
    
    def location(self, obj):
        return reverse('hand_lettering_designs')

class CalligraphyArtworkSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['calligraphy_artwork']
    
    def location(self, obj):
        return reverse('calligraphy_artwork')

class DisplayTypefacesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['display_typefaces']
    
    def location(self, obj):
        return reverse('display_typefaces')

class WireframeKitsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wireframe_kits']
    
    def location(self, obj):
        return reverse('wireframe_kits')

class PrototypeDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['prototype_designs']
    
    def location(self, obj):
        return reverse('prototype_designs')

class InteractiveMockupsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['interactive_mockups']
    
    def location(self, obj):
        return reverse('interactive_mockups')

class BusinessCardsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['business_cards']
    
    def location(self, obj):
        return reverse('business_cards')

class WeddingInvitationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wedding_invitations']
    
    def location(self, obj):
        return reverse('wedding_invitations')

class GreetingCardsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['greeting_cards']
    
    def location(self, obj):
        return reverse('greeting_cards')

class CalendarsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['calendars']
    
    def location(self, obj):
        return reverse('calendars')

class PlannersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['planners']
    
    def location(self, obj):
        return reverse('planners')

class SeamlessPatternsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['seamless_patterns']
    
    def location(self, obj):
        return reverse('seamless_patterns')

class TextileAndFabricPatternsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['textile_and_fabric_patterns']
    
    def location(self, obj):
        return reverse('textile_and_fabric_patterns')

class WallpaperDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wallpaper_designs']
    
    def location(self, obj):
        return reverse('wallpaper_designs')

class PackagingPatternsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['packaging_patterns']
    
    def location(self, obj):
        return reverse('packaging_patterns')

class UIUXIconsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['UI_UX_icons']
    
    def location(self, obj):
        return reverse('UI_UX_icons')

class AppIconsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['app_icons']
    
    def location(self, obj):
        return reverse('app_icons')

class SocialMediaIconsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['social_media_icons']
    
    def location(self, obj):
        return reverse('social_media_icons')

class CustomIconSetsForWebsitesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_icon_sets_for_websites']
    
    def location(self, obj):
        return reverse('custom_icon_sets_for_websites')

class RealisticPortraitPaintingsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['realistic_portrait_paintings']
    
    def location(self, obj):
        return reverse('realistic_portrait_paintings')

class FantasyLandscapePaintingsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fantasy_landscape_paintings']
    
    def location(self, obj):
        return reverse('fantasy_landscape_paintings')

class ConceptArtForGamesOrFilmsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['Concept_art_for_games_or_films']
    
    def location(self, obj):
        return reverse('Concept_art_for_games_or_films')

class AbstractDigitalArtworkSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['abstract_digital_artwork']
    
    def location(self, obj):
        return reverse('abstract_digital_artwork')

class CompositePhotoArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['composite_photo_art']
    
    def location(self, obj):
        return reverse('composite_photo_art')

class SurrealPhotoManipulationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['surreal_photo_manipulations']
    
    def location(self, obj):
        return reverse('surreal_photo_manipulations')

class ProductPhotoRetouchingSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['product_photo_retouching']
    
    def location(self, obj):
        return reverse('product_photo_retouching')

class FashionAndBeautyRetouchingSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fashion_and_beauty_retouching']
    
    def location(self, obj):
        return reverse('fashion_and_beauty_retouching')

class DigitalCollagesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['digital_collages']
    
    def location(self, obj):
        return reverse('digital_collages')

class MixedMediaArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mixed_media_art']
    
    def location(self, obj):
        return reverse('mixed_media_art')

class ScrapbookDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['scrapbook_designs']
    
    def location(self, obj):
        return reverse('scrapbook_designs')

class CharacterConceptArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['character_concept_art']
    
    def location(self, obj):
        return reverse('character_concept_art')

class CreatureAndMonsterDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['creature_and_monster_designs']
    
    def location(self, obj):
        return reverse('creature_and_monster_designs')

class StoryboardArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['storyboard_art']
    
    def location(self, obj):
        return reverse('storyboard_art')

class ComicBookIllustrationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['comic_book_illustrations']
    
    def location(self, obj):
        return reverse('comic_book_illustrations')

class MangaStyleCharactersAndStoryPanelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['manga_style_characters_and_story_panels']
    
    def location(self, obj):
        return reverse('manga_style_characters_and_story_panels')

class DigitalComicStripsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['digital_comic_strips']
    
    def location(self, obj):
        return reverse('digital_comic_strips')

class TshirtGraphicsAndMockupsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['t_shirt_graphics_and_mockups']
    
    def location(self, obj):
        return reverse('t_shirt_graphics_and_mockups')

class CustomMerchandiseDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_merchandise_designs']
    
    def location(self, obj):
        return reverse('custom_merchandise_designs')

class ApparelPatternsAndPrintsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['apparel_patterns_and_prints']
    
    def location(self, obj):
        return reverse('apparel_patterns_and_prints')

class ThemedPhotoCollectionsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['themed_photo_collections']
    
    def location(self, obj):
        return reverse('themed_photo_collections')

class HighResolutionStockImagesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['high_resolution_stock_images']
    
    def location(self, obj):
        return reverse('high_resolution_stock_images')

class ConceptualPhotographySitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['conceptual_photography']
    
    def location(self, obj):
        return reverse('conceptual_photography')

class ArtPrintsForHomeDecorSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['art_prints_for_home_decor']
    
    def location(self, obj):
        return reverse('art_prints_for_home_decor')

class MotivationalPostersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['motivational_posters']
    
    def location(self, obj):
        return reverse('motivational_posters')

class AbstractAndMinimalistArtSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['abstract_and_minimalist_art']
    
    def location(self, obj):
        return reverse('abstract_and_minimalist_art')

class InstagramPostTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['instagram_post_templates']
    
    def location(self, obj):
        return reverse('instagram_post_templates')

class FacebookBannerDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['facebook_banner_designs']
    
    def location(self, obj):
        return reverse('facebook_banner_designs')

class PinterestGraphicTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['pinterest_graphic_templates']
    
    def location(self, obj):
        return reverse('pinterest_graphic_templates')

class StoryHighlightIconsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['story_highlight_icons']
    
    def location(self, obj):
        return reverse('story_highlight_icons')
    
class CharacterModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['character_models']

    def location(self, obj):
        return reverse('character_models')

class VehicleModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['vehicle_models']

    def location(self, obj):
        return reverse('vehicle_models')

class FurnitureAndHomeDecorModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['furniture_and_home_decor_models']

    def location(self, obj):
        return reverse('furniture_and_home_decor_models')

class ProductPrototypesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['product_prototypes']

    def location(self, obj):
        return reverse('product_prototypes')

class HouseAndBuildingDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['house_and_building_designs']

    def location(self, obj):
        return reverse('house_and_building_designs')

class InteriorAndExteriorArchitecturalModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['interior_and_exterior_architectural_models']

    def location(self, obj):
        return reverse('interior_and_exterior_architectural_models')

class FloorPlansAndLayoutsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['floor_plans_and_layouts']

    def location(self, obj):
        return reverse('floor_plans_and_layouts')

class UrbanPlanningModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['urban_planning_models']

    def location(self, obj):
        return reverse('urban_planning_models')

class ArchitecturalRenderingsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['architectural_renderings']

    def location(self, obj):
        return reverse('architectural_renderings')

class ToysAndFigurinesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['toys_and_figurines']

    def location(self, obj):
        return reverse('toys_and_figurines')

class CustomJewelryDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_jewelry_designs']

    def location(self, obj):
        return reverse('custom_jewelry_designs')

class GadgetsAndAccessoriesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['gadgets_and_accessories']

    def location(self, obj):
        return reverse('gadgets_and_accessories')

class HomeDecorAndFunctionalObjectsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['home_decor_and_functional_objects']

    def location(self, obj):
        return reverse('home_decor_and_functional_objects')

class MechanicalPartDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mechanical_part_designs']

    def location(self, obj):
        return reverse('mechanical_part_designs')

class IndustrialEquipmentModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['industrial_equipment_models']

    def location(self, obj):
        return reverse('industrial_equipment_models')

class EngineeringDiagramsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['engineering_diagrams']

    def location(self, obj):
        return reverse('engineering_diagrams')

class CNCLaserCuttingTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['CNC_and_laser_cutting_templates']

    def location(self, obj):
        return reverse('CNC_and_laser_cutting_templates')

class ModernAndClassicFurnitureModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['modern_and_classic_furniture_models']

    def location(self, obj):
        return reverse('modern_and_classic_furniture_models')

class KitchenAndBathroomDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['kitchen_and_bathroom_designs']

    def location(self, obj):
        return reverse('kitchen_and_bathroom_designs')

class CustomCabinetryAndShelvingUnitsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_cabinetry_and_shelving_units']

    def location(self, obj):
        return reverse('custom_cabinetry_and_shelving_units')

class ThreedRoomAndSpaceLayoutsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['threed_room_and_space_layouts']

    def location(self, obj):
        return reverse('threed_room_and_space_layouts')

class ConsumerElectronicsPrototypesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['consumer_electronics_prototypes']

    def location(self, obj):
        return reverse('consumer_electronics_prototypes')

class FashionAndAccessoryDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fashion_and_accessory_designs']

    def location(self, obj):
        return reverse('fashion_and_accessory_designs')

class HomeAppliancePrototypesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['home_appliance_prototypes']

    def location(self, obj):
        return reverse('home_appliance_prototypes')

class WearableTechnologyPrototypesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wearable_technology_prototypes']

    def location(self, obj):
        return reverse('wearable_technology_prototypes')

class ThreedCharactersAndCreaturesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['threed_characters_and_creatures']

    def location(self, obj):
        return reverse('threed_characters_and_creatures')

class EnvironmentalModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['environmental_models']

    def location(self, obj):
        return reverse('environmental_models')

class WWEaponsAndGearSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wweapons_and_gear']

    def location(self, obj):
        return reverse('wweapons_and_gear')

class VehicleModelsForGamingSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['vehicle_models_for_gaming']

    def location(self, obj):
        return reverse('vehicle_models_for_gaming')

class AnatomyAndBodyPartModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['anatomy_and_body_part_models']

    def location(self, obj):
        return reverse('anatomy_and_body_part_models')

class MolecularAndChemicalModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['molecular_and_chemical_models']

    def location(self, obj):
        return reverse('molecular_and_chemical_models')

class MedicalEquipmentAndDeviceDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['medical_equipment_and_device_designs']

    def location(self, obj):
        return reverse('medical_equipment_and_device_designs')

class ScientificVisualizationModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['scientific_visualization_models']

    def location(self, obj):
        return reverse('scientific_visualization_models')

class CarAndTruckModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['car_and_truck_models']

    def location(self, obj):
        return reverse('car_and_truck_models')

class AircraftAndDroneDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['aircraft_and_drone_designs']

    def location(self, obj):
        return reverse('aircraft_and_drone_designs')

class ShipAndBoatModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['ship_and_boat_models']

    def location(self, obj):
        return reverse('ship_and_boat_models')
    
class PublicTransportationModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['public_transportation_models']

    def location(self, obj):
        return reverse('public_transportation_models')

class RingAndEarringDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['ring_and_earring_designs']

    def location(self, obj):
        return reverse('ring_and_earring_designs')

class PendantAndNecklaceModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['pendant_and_necklace_models']

    def location(self, obj):
        return reverse('pendant_and_necklace_models')

class CustomAndPersonalizedJewelryDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_and_personalized_jewelry_designs']

    def location(self, obj):
        return reverse('custom_and_personalized_jewelry_designs')

class ThreedPrintableJewelryPrototypesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['threed_printable_jewelry_prototypes']

    def location(self, obj):
        return reverse('threed_printable_jewelry_prototypes')

class VRReadyThreeModelsForVirtualEnvironmentsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['VR_ready_three_models_for_virtual_environments']

    def location(self, obj):
        return reverse('VR_ready_three_models_for_virtual_environments')

class ARModelsForAppsAndInteractiveExperiencesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['AR_models_for_apps_and_interactive_experiences']

    def location(self, obj):
        return reverse('AR_models_for_apps_and_interactive_experiences')

class ArchitecturalWalkthroughsForVRSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['architectural_walkthroughs_for_VR']

    def location(self, obj):
        return reverse('architectural_walkthroughs_for_VR')

class HeavyMachineryModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['heavy_machinery_models']

    def location(self, obj):
        return reverse('heavy_machinery_models')

class IndustrialEquipmentSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['industrial_equipment']

    def location(self, obj):
        return reverse('industrial_equipment')

class MechanicalComponentsAndAssembliesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mechanical_components_and_assemblies']

    def location(self, obj):
        return reverse('mechanical_components_and_assemblies')

class FantasyAndSciFiCharacterModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fantasy_and_sci_fi_character_models']

    def location(self, obj):
        return reverse('fantasy_and_sci_fi_character_models')

class CartoonAndStylizedCharactersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['cartoon_and_stylized_characters']

    def location(self, obj):
        return reverse('cartoon_and_stylized_characters')

class MonsterAndCreatureModelsForGamesAndFilmsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['monster_and_creature_models_for_games_and_films']

    def location(self, obj):
        return reverse('monster_and_creature_models_for_games_and_films')

class AThreedClothingAndAccessoryModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['A_threed_clothing_and_accessory_models']

    def location(self, obj):
        return reverse('A_threed_clothing_and_accessory_models')

class FashionPrototypesForManufacturingSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fashion_prototypes_for_manufacturing']

    def location(self, obj):
        return reverse('fashion_prototypes_for_manufacturing')

class ShoeAndBagDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['shoe_and_bag_designs']

    def location(self, obj):
        return reverse('shoe_and_bag_designs')

class FullyRiggedThreedCharactersForAnimationSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['fully_rigged_threed_characters_for_animation']

    def location(self, obj):
        return reverse('fully_rigged_threed_characters_for_animation')

class MotionCaptureReadyModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['motion_capture_ready_models']

    def location(self, obj):
        return reverse('motion_capture_ready_models')

class CustomRiggingSetupsForSpecificSoftwareSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_rigging_setups_for_specific_software']

    def location(self, obj):
        return reverse('custom_rigging_setups_for_specific_software')

class NaturalLandscapesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['natural_landscapes']

    def location(self, obj):
        return reverse('natural_landscapes')

class CityAndUrbanEnvironmentsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['city_and_urban_environments']

    def location(self, obj):
        return reverse('city_and_urban_environments')

class VirtualEnvironmentsForGamesAndSimulationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['virtual_environments_for_games_and_simulations']

    def location(self, obj):
        return reverse('virtual_environments_for_games_and_simulations')

class EngineModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['engine_models']

    def location(self, obj):
        return reverse('engine_models')

class GearAndMechanicalComponentDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['gear_and_mechanical_component_designs']

    def location(self, obj):
        return reverse('gear_and_mechanical_component_designs')

class CADFilesForMechanicalSystemsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['CAD_files_for_mechanical_systems']

    def location(self, obj):
        return reverse('CAD_files_for_mechanical_systems')

class DIYAssemblyInstructionsForFurnitureSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['DIY_assembly_instructions_for_furniture']

    def location(self, obj):
        return reverse('DIY_assembly_instructions_for_furniture')

class CustomFurnitureDesignsWithCADPlansSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_furniture_designs_with_CAD_plans']

    def location(self, obj):
        return reverse('custom_furniture_designs_with_CAD_plans')

class CNCCutPlansForModularFurnitureSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['CNC_cut_plans_for_modular_furniture']

    def location(self, obj):
        return reverse('CNC_cut_plans_for_modular_furniture')

class ThreedModelsOfPropsForFilmSetsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['threed_models_of_props_for_film_sets']

    def location(self, obj):
        return reverse('threed_models_of_props_for_film_sets')

class SciFiOrFantasySetDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['sci_fi_or_fantasy_set_designs']

    def location(self, obj):
        return reverse('sci_fi_or_fantasy_set_designs')

class HistoricalPropReplicasSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['historical_prop_replicas']

    def location(self, obj):
        return reverse('historical_prop_replicas')

class RobotDesignAndAssemblyPlansSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['robot_design_and_assembly_plans']

    def location(self, obj):
        return reverse('robot_design_and_assembly_plans')

class DroneAndUAVDesignsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['drone_and_UAV_designs']

    def location(self, obj):
        return reverse('drone_and_UAV_designs')

class IndustrialAutomationModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['industrial_automation_models']

    def location(self, obj):
        return reverse('industrial_automation_models')

class ThreedFloorPlansSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['threed_floor_plans']

    def location(self, obj):
        return reverse('threed_floor_plans')

class InteriorAndExteriorVisualizationSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['interior_and_exterior_visualization']

    def location(self, obj):
        return reverse('interior_and_exterior_visualization')

class ThreedTopographicalMapsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['threed_topographical_maps']

    def location(self, obj):
        return reverse('threed_topographical_maps')

class TerrainModelsForGamesAndSimulationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['terrain_models_for_games_and_simulations']

    def location(self, obj):
        return reverse('terrain_models_for_games_and_simulations')

class LandscapeElevationModelsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['landscape_elevation_models']

    def location(self, obj):
        return reverse('landscape_elevation_models')
    
class InvitationsAndGreetingCardsTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['invitations_and_greeting_cards_templates']

    def location(self, obj):
        return reverse('invitations_and_greeting_cards_templates')

class BusinessCardsTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['business_cards_template']

    def location(self, obj):
        return reverse('business_cards_template')

class WeddingTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['wedding_templates']

    def location(self, obj):
        return reverse('wedding_templates')

class DigitalPlannersSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['digital_planners']

    def location(self, obj):
        return reverse('digital_planners')

class SEOToolsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['SEO_tools']

    def location(self, obj):
        return reverse('SEO_tools')

class EmailMarketingTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['email_marketing_templates']

    def location(self, obj):
        return reverse('email_marketing_templates')

class WebsiteThemesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['website_themes']

    def location(self, obj):
        return reverse('website_themes')

class CustomScriptsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['custom_scripts']

    def location(self, obj):
        return reverse('custom_scripts')

class SoftwareApplicationsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['software_applications']

    def location(self, obj):
        return reverse('software_applications')

class PluginsAndExtensionsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['plugins_and_extensions']

    def location(self, obj):
        return reverse('plugins_and_extensions')

class ArchitecturalPlansSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['architectural_plans']

    def location(self, obj):
        return reverse('architectural_plans')

class MobileAppsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mobile_apps']

    def location(self, obj):
        return reverse('mobile_apps')

class SoftwareAsAServiceSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['software_as_a_Service']

    def location(self, obj):
        return reverse('software_as_a_Service')

class CopywritingTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['copywriting_templates']

    def location(self, obj):
        return reverse('copywriting_templates')

class BusinessTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['business_templates']

    def location(self, obj):
        return reverse('business_templates')

class MarketingMaterialsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['marketing_materials']

    def location(self, obj):
        return reverse('marketing_materials')

class AnalyticsToolsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['analytics_tools']

    def location(self, obj):
        return reverse('analytics_tools')

class CRMTemplatesSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['CRM_templates']

    def location(self, obj):
        return reverse('CRM_templates')
    
class MyProductSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['myproduct']

    def location(self, obj):
        return reverse('myproduct')

class WebsitePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['websitepost']

    def location(self, obj):
        return reverse('websitepost')

class MobilePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mobilepost']

    def location(self, obj):
        return reverse('mobilepost')

class DesktopPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['desktoppost']

    def location(self, obj):
        return reverse('desktoppost')

class EmbeddedPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['embededpost']

    def location(self, obj):
        return reverse('embededpost')

class GraphicsPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['graphicspost']

    def location(self, obj):
        return reverse('graphicspost')

class BookPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['bookpost']

    def location(self, obj):
        return reverse('bookpost')

class PrintablePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['printablepost']

    def location(self, obj):
        return reverse('printablepost')

class MusicPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['musicpost']

    def location(self, obj):
        return reverse('musicpost')

class MultimediaPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['multimediapost']

    def location(self, obj):
        return reverse('multimediapost')

class DigitalArtPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['digitalArtpost']

    def location(self, obj):
        return reverse('digitalArtpost')

class CADPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['CADpost']

    def location(self, obj):
        return reverse('CADpost')

class SoftwarePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['softwarepost']

    def location(self, obj):
        return reverse('softwarepost')

class BusinessPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['businesspost']

    def location(self, obj):
        return reverse('businesspost')

class ProjectPostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['projectpost']

    def location(self, obj):
        return reverse('projectpost')

class ImagePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['imagepost']

    def location(self, obj):
        return reverse('imagepost')

class WebsiteTemplatePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['websitetemplatepost']

    def location(self, obj):
        return reverse('websitetemplatepost')

class MobileTemplatePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['mobiletemplatepost']

    def location(self, obj):
        return reverse('mobiletemplatepost')

class DesktopTemplatePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['desktoptemplatepost']

    def location(self, obj):
        return reverse('desktoptemplatepost')

class MicrosoftTemplatePostSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['microsofttemplatepost']

    def location(self, obj):
        return reverse('microsofttemplatepost')

class AdobePostTemplateSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['adobeposttemplate']

    def location(self, obj):
        return reverse('adobeposttemplate')

class AllProductSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['allproduct']

    def location(self, obj):
        return reverse('allproduct')
    
class HelpSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['help']

    def location(self, obj):
        return reverse('help')

class TermsConditionsSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['terms_conditions']

    def location(self, obj):
        return reverse('terms_conditions')
    
class SignupSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['signup']

    def location(self, obj):
        return reverse('signup')

class SigninSitemap(Sitemap):
    changefreq = "weekly"  # Set the indexing frequency to every week
    priority = 0.5  # You can adjust the priority (0.0 to 1.0) based on importance
    
    def items(self):
        return ['signin']

    def location(self, obj):
        return reverse('signin')


# Register all sitemaps
sitemaps = {
    'projects': ProjectSitemap,
    'books': BookSitemap,
    'adobetemplates': AdobetemplateSitemap,
    'printables': PrintableSitemap,
    'musics': MusicSitemap,
    'multimedia': MultimediaSitemap,
    'digitalarts': DigitalArtSitemap,
    'cads': CADSitemap,
    'softwares': SoftwareSitemap,
    'businesses': BusinessSitemap,
    'images': ImageSitemap,
    'websitetemplates': WebsitetemplateSitemap,
    'mobiletemplates': MobiletemplateSitemap,
    'desktoptemplates': DesktoptemplateSitemap,
    'microsofttemplates': MicrosofttemplateSitemap,
    'home': HomeSitemap,
    'aboutus': AboutSitemap,
    'contactpost': ContactSitemap,
    'websiteproject': WebsiteProjectSitemap,
    'mobileproject': MobileProjectSitemap,
    'desktopproject': DesktopProjectSitemap,
    'artificialproject': ArtificialProjectSitemap,
    'embededproject': EmbeddedProjectSitemap,
    'iotproject': IoTProjectSitemap,
    'virtualrealityproject': VirtualRealityProjectSitemap,
    'cyberproject': CyberProjectSitemap,
    'image': ImageSitemap,
    'webtemplate': WebTemplateSitemap,
    'htmlcsstemplate': HtmlCssTemplateSitemap,
    'reacttemplate': ReactTemplateSitemap,
    'vueJs_template': VueJsTemplateSitemap,
    'elm': ElmSitemap,
    'swift': SwiftSitemap,
    'JQuery': JQuerySitemap,
    'flutter_template': FlutterTemplateSitemap,
    'svelte': SvelteSitemap,
    'materialize_CSS': MaterializeCssSitemap,
    'foundation': FoundationSitemap,
    'angular_template': AngularTemplateSitemap,
    'tailwind_CSS': TailwindCssSitemap,
    'bootstrap_template': BootstrapTemplateSitemap,
    'mobiletemplate': MobileTemplateSitemap,
    'reactnativetemplate': ReactNativeTemplateSitemap,
    'flutter_mobile_template': FlutterMobileTemplateSitemap,
    'swiftUI': SwiftUISitemap,
    'jetpack_Compose': JetpackComposeSitemap,
    'ionic_Framework': IonicFrameworkSitemap,
    'xamarin': XamarinSitemap,
    'phoneGap': PhoneGapSitemap,
    'nativeScript': NativeScriptSitemap,
    'framework_seven': FrameworkSevenSitemap,
    'onsen_UI': OnsenUISitemap,
    'jQuery_Mobile': JQueryMobileSitemap,
    'sencha_Touch': SenchaTouchSitemap,
    'Kivy_template': KivyTemplateSitemap,
    'bootstrap_Mobile_Templates': BootstrapMobileTemplatesSitemap,
    'quasar_Framework': QuasarFrameworkSitemap,
    'desktoptemplate': DesktopTemplateSitemap,
    'kivytemplate': KivyTemplateSitemap,
    'pyqttemplate': PyQtTemplateSitemap,
    'ctemplate': CTemplateSitemap,
    'tkintertemplate': TkinterTemplateSitemap,
    'chashdesktopapp': CSharpDesktopAppSitemap,
    'javadesktopapp': JavaDesktopAppSitemap,
    'cplusdesktopapp': CPlusDesktopAppSitemap,
    'electrondesktopapp': ElectronDesktopAppSitemap,
    'swiftdesktopapp': SwiftDesktopAppSitemap,
    'rustdesktopapp': RustDesktopAppSitemap,
    'microsofttemplate': MicrosoftTemplateSitemap,
    'wordtemplate': WordTemplateSitemap,
    'excelltemplate': ExcelTemplateSitemap,
    'powerpointtemplate': PowerPointTemplateSitemap,
    'publishertemplate': PublisherTemplateSitemap,
    'adobetemplate': AdobeTemplateSitemap,
    'photoshoptemplate': PhotoshopTemplateSitemap,
    'primiertemplate': PremiereTemplateSitemap,
    'illustratortemplate': IllustratorTemplateSitemap,
    'InDesignadobe': InDesignAdobeSitemap,
    'XDadobe': XDadobeSitemap,
    'Lightroomadobe': LightroomAdobeSitemap,
    'LightroomClassicadobe': LightroomClassicAdobeSitemap,
    'AfterEffectsadobe': AfterEffectsAdobeSitemap,
    'Animateadobe': AnimateAdobeSitemap,
    'Dreamweaveradobe': DreamweaverAdobeSitemap,
    'Auditionadobe': AuditionAdobeSitemap,
    'Bridgeadobe': BridgeAdobeSitemap,
    'Dimensionadobe': DimensionAdobeSitemap,
    'Frescoadobe': FrescoAdobeSitemap,
    'CharacterAnimatoradobe': CharacterAnimatorAdobeSitemap,
    'MediaEncoderadobe': MediaEncoderAdobeSitemap,
    'Rushadobe': RushAdobeSitemap,
    'Sparkadobe': SparkAdobeSitemap,
    'Substance3DPainteradobe': Substance3DPainterAdobeSitemap,
    'Substance3DDesigneradobe': Substance3DDesignerAdobeSitemap,
    'Substance3DSampleradobe': Substance3DSamplerAdobeSitemap,
    'Substance3DStageradobe': Substance3DStagerAdobeSitemap,
    'AcrobatProDCadobe': AcrobatProDCAdobeSitemap,
    'Signadobe': SignAdobeSitemap,
    'FrameMakeradobe': FrameMakerAdobeSitemap,
    'Engageadobe': EngageAdobeSitemap,
    'Presenteradobe': PresenterAdobeSitemap,
    'template': TemplateSitemap,
    'project': ProjectSitemap,
    'course': CourseSitemap,
    'ebooks': EbooksSitemap,
    'music': MusicSitemap,
    'video': VideoSitemap,
    'art': ArtSitemap,
    'cad': CadSitemap,
    'printable': PrintableSitemap,
    'software': SoftwareSitemap,
    'business': BusinessSitemap,
    'novels': NovelsSitemap,
    'short_stories': ShortStoriesSitemap,
    'poetry': PoetrySitemap,
    'flash_fiction': FlashFictionSitemap,
    'self_help_book': SelfHelpBookSitemap,
    'biographies': BiographiesSitemap,
    'personal_development_books': PersonalDevelopmentBooksSitemap,
    'history_books': HistoryBooksSitemap,
    'true_crime': TrueCrimeSitemap,
    'textbooks': TextbooksSitemap,
    'research_papers': ResearchPapersSitemap,
    'study_guides': StudyGuidesSitemap,
    'how_to_guides_tutorials': HowToGuidesSitemap,
    'business_strategy_guides': BusinessStrategyGuidesSitemap,
    'marketing_and_sales_e_books': MarketingAndSalesEbooksSitemap,
    'entrepreneurship_guides': EntrepreneurshipGuidesSitemap,
    'financial_planning': FinancialPlanningSitemap,
    'nutrition_guides': NutritionGuidesSitemap,
    'workout_and_fitness_plans': WorkoutAndFitnessPlansSitemap,
    'mental_health_wellness': MentalHealthWellnessSitemap,
    'meditation_and_mindfulness_e_books': MeditationAndMindfulnessEbooksSitemap,
    'coding_and_programming_tutorials': CodingAndProgrammingTutorialsSitemap,
    'software_manuals': SoftwareManualsSitemap,
    'IT_and_networking_guides': ITAndNetworkingGuidesSitemap,
    'artificial_intelligence_machine_learning': AImachineLearningSitemap,
    'photography_tutorials': PhotographyTutorialsSitemap,
    'painting_and_drawing_guides': PaintingAndDrawingGuidesSitemap,
    'writing_and_storytelling_techniques': WritingAndStorytellingTechniquesSitemap,
    'crafting_DIY_projects': CraftingDIYProjectsSitemap,
    'recipe_collections': RecipeCollectionsSitemap,
    'specialized_diet_guides': SpecializedDietGuidesSitemap,
    'meal_planning_and_prep': MealPlanningAndPrepSitemap,
    'parenting_advice': ParentingAdviceSitemap,
    'marriage_and_relationship_counseling': MarriageAndRelationshipCounselingSitemap,
    'family_planning_guides': FamilyPlanningGuidesSitemap,
    'childcare_and_development': ChildcareAndDevelopmentSitemap,
    'travel_guides': TravelGuidesSitemap,
    'destination_reviews': DestinationReviewsSitemap,
    'adventure_stories': AdventureStoriesSitemap,
    'travel_planning_and_budgeting': TravelPlanningAndBudgetingSitemap,
    'personal_finance_e_books': PersonalFinanceEbooksSitemap,
    'investment_strategies': InvestmentStrategiesSitemap,
    'retirement_planning': RetirementPlanningSitemap,
    'budgeting_tips': BudgetingTipsSitemap,
    'religious_texts': ReligiousTextsSitemap,
    'spiritual_growth_guides': SpiritualGrowthGuidesSitemap,
    'meditation_and_mindfulness_books': MeditationAndMindfulnessBooksSitemap,
    'philosophy_and_life_purpose_e_books': PhilosophyAndLifePurposeEbooksSitemap,
    'time_management_and_productivity': TimeManagementAndProductivitySitemap,
    'self_improvement_and_motivation': SelfImprovementAndMotivationSitemap,
    'life_coaching_guides': LifeCoachingGuidesSitemap,
    'work_life_balance': WorkLifeBalanceSitemap,
    'legal_guides_and_contracts': LegalGuidesAndContractsSitemap,
    'HR_and_employment_handbooks': HRAndEmploymentHandbooksSitemap,
    'professional_development': ProfessionalDevelopmentSitemap,
    'real_estate_investment_guides': RealEstateInvestmentGuidesSitemap,
    'property_management_manuals': PropertyManagementManualsSitemap,
    'buying_and_selling_homes': BuyingAndSellingHomesSitemap,
    'single_tracks': SingleTracksSitemap,
    'full_albums': FullAlbumsSitemap,
    'extended_plays': ExtendedPlaysSitemap,
    'instrumental_versions': InstrumentalVersionsSitemap,
    'beats_for_rappers_and_singers': BeatsForRappersAndSingersSitemap,
    'lo_fi_beats': LoFiBeatsSitemap,
    'background_instrumentals_for_videos': BackgroundInstrumentalsForVideosSitemap,
    'royalty_free_music': RoyaltyFreeMusicSitemap,
    'environmental_sounds': EnvironmentalSoundsSitemap,
    'foley_sounds': FoleySoundsSitemap,
    'sci_fi_and_futuristic_sounds': SciFiAndFuturisticSoundsSitemap,
    'horror_and_thriller_effects': HorrorAndThrillerEffectsSitemap,
    'drum_loops': DrumLoopsSitemap,
    'melodic_loops': MelodicLoopsSitemap,
    'vocal_samples': VocalSamplesSitemap,
    'synth_and_bass_loops': SynthAndBassLoopsSitemap,
    'background_music_for_videos': BackgroundMusicForVideosSitemap,
    'music_for_podcasts': MusicForPodcastsSitemap,
    'royalty_free_soundtracks_for_commercials': RoyaltyFreeSoundtracksForCommercialsSitemap,
    'ambient_music_for_relaxation_and_meditation': AmbientMusicForRelaxationAndMeditationSitemap,
    'talk_shows': TalkShowsSitemap,
    'interview_series': InterviewSeriesSitemap,
    'educational_podcasts': EducationalPodcastsSitemap,
    'storytelling_and_fictional_audio_series': StorytellingAndFictionalAudioSeriesSitemap,
    'nature_inspired_soundscapes': NatureInspiredSoundscapesSitemap,
    'nature_and_landscape_footage': NatureAndLandscapeFootageSitemap,
    'urban_and_city_life_footage': UrbanAndCityLifeFootageSitemap,
    'aerial_drone_videos': AerialDroneVideosSitemap,
    'slow_motion_and_time_lapse_videos': SlowMotionAndTimeLapseVideosSitemap,
    'intros_and_outros_for_YouTube_videos': IntrosAndOutrosForYouTubeVideosSitemap,
    'two_animations': TwoAnimationsSitemap,
    'three_animations': ThreeAnimationsSitemap,
    'explainer_videos': ExplainerVideosSitemap,
    'motion_graphics_for_commercials': MotionGraphicsForCommercialsSitemap,
    'personal_vlogs': PersonalVlogsSitemap,
    'travel_videos': TravelVideosSitemap,
    'lifestyl_vlogs': LifestyleVlogsSitemap,
    'daily_video_blogs': DailyVideoBlogsSitemap,
    'wedding_videos': WeddingVideosSitemap,
    'corporate_event_videos': CorporateEventVideosSitemap,
    'party_and_celebration_videos': PartyAndCelebrationVideosSitemap,
    'award_ceremony_Video': AwardCeremonyVideoSitemap,
    'business_presentations': BusinessPresentationsSitemap,
    'sales_pitches': SalesPitchesSitemap,
    'educational_or_academic_presentations': EducationalOrAcademicPresentationsSitemap,
    'product_promo_videos': ProductPromoVideosSitemap,
    'service_advertisement_videos': ServiceAdvertisementVideosSitemap,
    'brand_story_videos': BrandStoryVideosSitemap,
    'social_media_ads': SocialMediaAdsSitemap,
    'official_music_videos': OfficialMusicVideosSitemap,
    'lyric_videos': LyricVideosSitemap,
    'animated_music_videos': AnimatedMusicVideosSitemap,
    'performance_videos': PerformanceVideosSitemap,
    'fiction_short_films': FictionShortFilmsSitemap,
    'mini_documentaries': MiniDocumentariesSitemap,
    'biographical_documentaries': BiographicalDocumentariesSitemap,
    'indie_films': IndieFilmsSitemap,
    'adventure_videos': AdventureVideosSitemap,
    'interactive_tutorials': InteractiveTutorialsSitemap,
    'interactive_quizzes_or_assessments': InteractiveQuizzesOrAssessmentsSitemap,
    'gamified_videos': GamifiedVideosSitemap,
    'customer_testimonial_videos': CustomerTestimonialVideosSitemap,
    'product_review_videos': ProductReviewVideosSitemap,
    'user_generated_content_videos': UserGeneratedContentVideosSitemap,
    'virtual_reality_experiences': VirtualRealityExperiencesSitemap,
    'degree_video_tours': DegreeVideoToursSitemap,
    'immersive_event_videos': ImmersiveEventVideosSitemap,
    'cinematic_sequences': CinematicSequencesSitemap,
    'aerial_drone_footage': AerialDroneFootageSitemap,
    'scenic_landscape_shots': ScenicLandscapeShotsSitemap,
    'epic_slow_motion_videos': EpicSlowMotionVideosSitemap,
    'urban_timelapse_videos': UrbanTimelapseVideosSitemap,
    'nature_and_sky_timelapse': NatureAndSkyTimelapseSitemap,
    'construction_progress_timelapse': ConstructionProgressTimelapseSitemap,
    'yoga_and_meditation_videos': YogaAndMeditationVideosSitemap,
    'healthy_lifestyle_tips': HealthyLifestyleTipsSitemap,
    'exercise_and_wellness_programs': ExerciseAndWellnessProgramsSitemap,
    'product_feature_demonstrations': ProductFeatureDemonstrationsSitemap,
    'physical_product_unboxing_and_reviews': PhysicalProductUnboxingAndReviewsSitemap,
    'animated_YouTube_intros': AnimatedYouTubeIntrosSitemap,
    'branding_outros_for_videos': BrandingOutrosForVideosSitemap,
    'social_media_content_intros': SocialMediaContentIntrosSitemap,
    'hand_drawn_digital_illustrations': HandDrawnDigitalIllustrationsSitemap,
    'character_design': CharacterDesignSitemap,
    'website_design_templates': WebsiteDesignTemplatesSitemap,
    'mobile_app_design_templates': MobileAppDesignTemplatesSitemap,
    'editorial_illustrations': EditorialIllustrationsSitemap,
    'children_book_illustrations': ChildrenBookIllustrationsSitemap,
    'posters': PostersSitemap,
    'flyers': FlyersSitemap,
    'brochures': BrochuresSitemap,
    'infographics': InfographicsSitemap,
    'digital_advertisements': DigitalAdvertisementsSitemap,
    'brand_logos': BrandLogosSitemap,
    'icon_sets': IconSetsSitemap,
    'custom_logos_for_businesses': CustomLogosForBusinessesSitemap,
    'monograms': MonogramsSitemap,
    'scalable_vector_illustrations': ScalableVectorIllustrationsSitemap,
    'flat_design_elements': FlatDesignElementsSitemap,
    'icons_and_symbols': IconsAndSymbolsSitemap,
    'geometric_patterns': GeometricPatternsSitemap,
    'three_models': ThreeModelsSitemap,
    'three_character_design': ThreeCharacterDesignSitemap,
    'product_visualizations': ProductVisualizationsSitemap,
    'custom_fonts': CustomFontsSitemap,
    'hand_lettering_designs': HandLetteringDesignsSitemap,
    'calligraphy_artwork': CalligraphyArtworkSitemap,
    'display_typefaces': DisplayTypefacesSitemap,
    'wireframe_kits': WireframeKitsSitemap,
    'prototype_designs': PrototypeDesignsSitemap,
    'interactive_mockups': InteractiveMockupsSitemap,
    'business_cards': BusinessCardsSitemap,
    'wedding_invitations': WeddingInvitationsSitemap,
    'greeting_cards': GreetingCardsSitemap,
    'calendars': CalendarsSitemap,
    'planners': PlannersSitemap,
    'seamless_patterns': SeamlessPatternsSitemap,
    'textile_and_fabric_patterns': TextileAndFabricPatternsSitemap,
    'wallpaper_designs': WallpaperDesignsSitemap,
    'packaging_patterns': PackagingPatternsSitemap,
    'UI_UX_icons': UIUXIconsSitemap,
    'app_icons': AppIconsSitemap,
    'social_media_icons': SocialMediaIconsSitemap,
    'custom_icon_sets_for_websites': CustomIconSetsForWebsitesSitemap,
    'realistic_portrait_paintings': RealisticPortraitPaintingsSitemap,
    'fantasy_landscape_paintings': FantasyLandscapePaintingsSitemap,
    'Concept_art_for_games_or_films': ConceptArtForGamesOrFilmsSitemap,
    'abstract_digital_artwork': AbstractDigitalArtworkSitemap,
    'composite_photo_art': CompositePhotoArtSitemap,
    'surreal_photo_manipulations': SurrealPhotoManipulationsSitemap,
    'product_photo_retouching': ProductPhotoRetouchingSitemap,
    'fashion_and_beauty_retouching': FashionAndBeautyRetouchingSitemap,
    'digital_collages': DigitalCollagesSitemap,
    'mixed_media_art': MixedMediaArtSitemap,
    'scrapbook_designs': ScrapbookDesignsSitemap,
    'character_concept_art': CharacterConceptArtSitemap,
    'creature_and_monster_designs': CreatureAndMonsterDesignsSitemap,
    'storyboard_art': StoryboardArtSitemap,
    'comic_book_illustrations': ComicBookIllustrationsSitemap,
    'manga_style_characters_and_story_panels': MangaStyleCharactersAndStoryPanelsSitemap,
    'digital_comic_strips': DigitalComicStripsSitemap,
    't_shirt_graphics_and_mockups': TshirtGraphicsAndMockupsSitemap,
    'custom_merchandise_designs': CustomMerchandiseDesignsSitemap,
    'apparel_patterns_and_prints': ApparelPatternsAndPrintsSitemap,
    'themed_photo_collections': ThemedPhotoCollectionsSitemap,
    'high_resolution_stock_images': HighResolutionStockImagesSitemap,
    'conceptual_photography': ConceptualPhotographySitemap,
    'art_prints_for_home_decor': ArtPrintsForHomeDecorSitemap,
    'motivational_posters': MotivationalPostersSitemap,
    'abstract_and_minimalist_art': AbstractAndMinimalistArtSitemap,
    'instagram_post_templates': InstagramPostTemplatesSitemap,
    'facebook_banner_designs': FacebookBannerDesignsSitemap,
    'pinterest_graphic_templates': PinterestGraphicTemplatesSitemap,
    'story_highlight_icons': StoryHighlightIconsSitemap,
    'character_models': CharacterModelsSitemap,
    'vehicle_models': VehicleModelsSitemap,
    'furniture_and_home_decor_models': FurnitureAndHomeDecorModelsSitemap,
    'product_prototypes': ProductPrototypesSitemap,
    'house_and_building_designs': HouseAndBuildingDesignsSitemap,
    'interior_and_exterior_architectural_models': InteriorAndExteriorArchitecturalModelsSitemap,
    'floor_plans_and_layouts': FloorPlansAndLayoutsSitemap,
    'urban_planning_models': UrbanPlanningModelsSitemap,
    'architectural_renderings': ArchitecturalRenderingsSitemap,
    'toys_and_figurines': ToysAndFigurinesSitemap,
    'custom_jewelry_designs': CustomJewelryDesignsSitemap,
    'gadgets_and_accessories': GadgetsAndAccessoriesSitemap,
    'home_decor_and_functional_objects': HomeDecorAndFunctionalObjectsSitemap,
    'mechanical_part_designs': MechanicalPartDesignsSitemap,
    'industrial_equipment_models': IndustrialEquipmentModelsSitemap,
    'engineering_diagrams': EngineeringDiagramsSitemap,
    'CNC_and_laser_cutting_templates': CNCLaserCuttingTemplatesSitemap,
    'modern_and_classic_furniture_models': ModernAndClassicFurnitureModelsSitemap,
    'kitchen_and_bathroom_designs': KitchenAndBathroomDesignsSitemap,
    'custom_cabinetry_and_shelving_units': CustomCabinetryAndShelvingUnitsSitemap,
    'threed_room_and_space_layouts': ThreedRoomAndSpaceLayoutsSitemap,
    'consumer_electronics_prototypes': ConsumerElectronicsPrototypesSitemap,
    'fashion_and_accessory_designs': FashionAndAccessoryDesignsSitemap,
    'home_appliance_prototypes': HomeAppliancePrototypesSitemap,
    'wearable_technology_prototypes': WearableTechnologyPrototypesSitemap,
    'threed_characters_and_creatures': ThreedCharactersAndCreaturesSitemap,
    'environmental_models': EnvironmentalModelsSitemap,
    'wweapons_and_gear': WWEaponsAndGearSitemap,
    'vehicle_models_for_gaming': VehicleModelsForGamingSitemap,
    'anatomy_and_body_part_models': AnatomyAndBodyPartModelsSitemap,
    'molecular_and_chemical_models': MolecularAndChemicalModelsSitemap,
    'medical_equipment_and_device_designs': MedicalEquipmentAndDeviceDesignsSitemap,
    'scientific_visualization_models': ScientificVisualizationModelsSitemap,
    'car_and_truck_models': CarAndTruckModelsSitemap,
    'aircraft_and_drone_designs': AircraftAndDroneDesignsSitemap,
    'ship_and_boat_models': ShipAndBoatModelsSitemap,
    'public_transportation_models': PublicTransportationModelsSitemap,
    'ring_and_earring_designs': RingAndEarringDesignsSitemap,
    'pendant_and_necklace_models': PendantAndNecklaceModelsSitemap,
    'custom_and_personalized_jewelry_designs': CustomAndPersonalizedJewelryDesignsSitemap,
    'threed_printable_jewelry_prototypes': ThreedPrintableJewelryPrototypesSitemap,
    'VR_ready_three_models_for_virtual_environments': VRReadyThreeModelsForVirtualEnvironmentsSitemap,
    'AR_models_for_apps_and_interactive_experiences': ARModelsForAppsAndInteractiveExperiencesSitemap,
    'architectural_walkthroughs_for_VR': ArchitecturalWalkthroughsForVRSitemap,
    'heavy_machinery_models': HeavyMachineryModelsSitemap,
    'industrial_equipment': IndustrialEquipmentSitemap,
    'mechanical_components_and_assemblies': MechanicalComponentsAndAssembliesSitemap,
    'fantasy_and_sci_fi_character_models': FantasyAndSciFiCharacterModelsSitemap,
    'cartoon_and_stylized_characters': CartoonAndStylizedCharactersSitemap,
    'monster_and_creature_models_for_games_and_films': MonsterAndCreatureModelsForGamesAndFilmsSitemap,
    'A_threed_clothing_and_accessory_models': AThreedClothingAndAccessoryModelsSitemap,
    'fashion_prototypes_for_manufacturing': FashionPrototypesForManufacturingSitemap,
    'shoe_and_bag_designs': ShoeAndBagDesignsSitemap,
    'fully_rigged_threed_characters_for_animation': FullyRiggedThreedCharactersForAnimationSitemap,
    'motion_capture_ready_models': MotionCaptureReadyModelsSitemap,
    'custom_rigging_setups_for_specific_software': CustomRiggingSetupsForSpecificSoftwareSitemap,
    'natural_landscapes': NaturalLandscapesSitemap,
    'city_and_urban_environments': CityAndUrbanEnvironmentsSitemap,
    'virtual_environments_for_games_and_simulations': VirtualEnvironmentsForGamesAndSimulationsSitemap,
    'engine_models': EngineModelsSitemap,
    'gear_and_mechanical_component_designs': GearAndMechanicalComponentDesignsSitemap,
    'CAD_files_for_mechanical_systems': CADFilesForMechanicalSystemsSitemap,
    'DIY_assembly_instructions_for_furniture': DIYAssemblyInstructionsForFurnitureSitemap,
    'custom_furniture_designs_with_CAD_plans': CustomFurnitureDesignsWithCADPlansSitemap,
    'CNC_cut_plans_for_modular_furniture': CNCCutPlansForModularFurnitureSitemap,
    'threed_models_of_props_for_film_sets': ThreedModelsOfPropsForFilmSetsSitemap,
    'sci_fi_or_fantasy_set_designs': SciFiOrFantasySetDesignsSitemap,
    'historical_prop_replicas': HistoricalPropReplicasSitemap,
    'robot_design_and_assembly_plans': RobotDesignAndAssemblyPlansSitemap,
    'drone_and_UAV_designs': DroneAndUAVDesignsSitemap,
    'industrial_automation_models': IndustrialAutomationModelsSitemap,
    'threed_floor_plans': ThreedFloorPlansSitemap,
    'interior_and_exterior_visualization': InteriorAndExteriorVisualizationSitemap,
    'threed_topographical_maps': ThreedTopographicalMapsSitemap,
    'terrain_models_for_games_and_simulations': TerrainModelsForGamesAndSimulationsSitemap,
    'landscape_elevation_models': LandscapeElevationModelsSitemap,
    'invitations_and_greeting_cards_templates': InvitationsAndGreetingCardsTemplatesSitemap,
    'business_cards_template': BusinessCardsTemplateSitemap,
    'wedding_templates': WeddingTemplatesSitemap,
    'digital_planners': DigitalPlannersSitemap,
    'SEO_tools': SEOToolsSitemap,
    'email_marketing_templates': EmailMarketingTemplatesSitemap,
    'website_themes': WebsiteThemesSitemap,
    'custom_scripts': CustomScriptsSitemap,
    'software_applications': SoftwareApplicationsSitemap,
    'plugins_and_extensions': PluginsAndExtensionsSitemap,
    'architectural_plans': ArchitecturalPlansSitemap,
    'mobile_apps': MobileAppsSitemap,
    'software_as_a_Service': SoftwareAsAServiceSitemap,
    'copywriting_templates': CopywritingTemplatesSitemap,
    'business_templates': BusinessTemplatesSitemap,
    'marketing_materials': MarketingMaterialsSitemap,
    'analytics_tools': AnalyticsToolsSitemap,
    'CRM_templates': CRMTemplatesSitemap,
    'myproduct': MyProductSitemap,
    'websitepost': WebsitePostSitemap,
    'mobilepost': MobilePostSitemap,
    'desktoppost': DesktopPostSitemap,
    'embededpost': EmbeddedPostSitemap,
    'graphicspost': GraphicsPostSitemap,
    'bookpost': BookPostSitemap,
    'printablepost': PrintablePostSitemap,
    'musicpost': MusicPostSitemap,
    'multimediapost': MultimediaPostSitemap,
    'digitalArtpost': DigitalArtPostSitemap,
    'CADpost': CADPostSitemap,
    'softwarepost': SoftwarePostSitemap,
    'businesspost': BusinessPostSitemap,
    'projectpost': ProjectPostSitemap,
    'imagepost': ImagePostSitemap,
    'websitetemplatepost': WebsiteTemplatePostSitemap,
    'mobiletemplatepost': MobileTemplatePostSitemap,
    'desktoptemplatepost': DesktopTemplatePostSitemap,
    'microsofttemplatepost': MicrosoftTemplatePostSitemap,
    'adobeposttemplate': AdobePostTemplateSitemap,
    'allproduct': AllProductSitemap,
    'help': HelpSitemap,
    'terms_conditions': TermsConditionsSitemap,
    'signup': SignupSitemap,
    'signin': SigninSitemap,
}
