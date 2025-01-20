from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

from .views import change_password

from web.views import PaymentViewWebsitetemplate, PaymentViewMobiletemplate, PaymentViewDesktoptemplate, PaymentViewMicrosofttemplate, PaymentViewAdobetemplate, PaymentViewWebsite, PaymentViewMobile, PaymentViewDesktop, PaymentViewEmbeded, PaymentViewGraphics, PaymentViewProject, PaymentViewImage, PurchasedView, PaymentViewBook, PaymentViewPrintable, PaymentViewMusic, PaymentViewMultimedia, PaymentViewDigitalArt, PaymentViewCAD, PaymentViewSoftware, PaymentViewBusiness
# from web.views import *

from .views import delete_viewed_notifications

from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps

from .views import (
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)

urlpatterns = [
    path('admin/', views.admin, name = "admin"),
    path('signup/', views.signup, name = "signup"),
    path('signin/', views.signin, name = "signin"),
	path('logout/', views.logout, name="logout"),
    path('change-password/', change_password, name='change_password'),
    
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='web/registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='web/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='web/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='web/registration/password_reset_complete.html'), name='password_reset_complete'),
 
    path("",views.home,name = "home"),
    path("aboutus/",views.aboutus,name = "aboutus"),
    path("base1/",views.base1,name = "base1"),
    path("base/",views.base,name = "base"),
    path("contactus/",views.contactus,name = "contactus"),
    path("contactpost/",views.contactpost,name = "contactpost"),
    path('subscribe/', views.subscribe,name='subscribe'),
    path("contactlist/",views.contactlist,name = "contactlist"),
    path("viewcontact/<int:id>/",views.viewcontact,name = "viewcontact"),
    path('deletecontact/<int:id>/', views.deletecontact, name = "deletecontact"),
    path("dashboard/",views.dashboard,name = "dashboard"),
    path("masterdashboard/",views.masterdashboard,name = "masterdashboard"),
    path("services/",views.services,name = "services"),
    
    # url for success message
    path("signupsucces/",views.signupsucces,name = "signupsucces"),
    path("logedout/",views.logedout,name = "logedout"),
    
    # path("courses/",views.courses,name = "courses"),
    
    # courses to be tought
    path("computercs/",views.computercs,name = "computercs"),
    path("computereng/",views.computereng,name = "computereng"),
    path("electrical/",views.electrical,name = "electrical"),
    path("civil/",views.civil,name = "civil"),
    path("mechanical/",views.mechanical,name = "mechanical"),
    path("artificial/",views.artificial,name = "artificial"),
    path("softwareeng/",views.softwareeng,name = "softwareeng"),
    path("embeded/",views.embeded,name = "embeded"),
    path("website/",views.website,name = "website"),
    path("mobileapp/",views.mobileapp,name = "mobileapp"),
    path("virtualreality/",views.virtualreality,name = "virtualreality"),
    path("security/",views.security,name = "security"),
    path("desktopapp/",views.desktopapp,name = "desktopapp"),
    path("multmedia/",views.multmedia,name = "multmedia"),
    path("graphics/",views.graphics,name = "graphics"),
    path("iot/",views.iot,name = "iot"),
    path("security/",views.security,name = "security"),
    path("nertworking/",views.nertworking,name = "nertworking"),
    
    # for frontend development
    path("wfrontend/",views.wfrontend,name = "wfrontend"),
    
    path("htmlcss/",views.htmlcss,name = "htmlcss"),
    path("javascript/",views.javascript,name = "javascript"),
    path("vuejs/",views.vuejs,name = "vuejs"),
    path("reactjs/",views.reactjs,name = "reactjs"),
    path("bootstrap/",views.bootstrap,name = "bootstrap"),
    path("angularjs/",views.angularjs,name = "angularjs"),
    
    # for backend website development
    path("wbackend/",views.wbackend,name = "wbackend"),
    
    path("django/",views.django,name = "django"),
    path("flask/",views.flask,name = "flask"),
    path("php/",views.php,name = "php"),
    path("laravel/",views.laravel,name = "laravel"),
    path("rub/",views.rub,name = "rub"),
    
    # for full stack website development
    path("wfullstack/",views.wfullstack,name = "wfullstack"),
    
    path("djangohtml/",views.djangohtml,name = "djangohtml"),
    path("flaskhtml/",views.flaskhtml,name = "flaskhtml"),
    path("phphtml/",views.phphtml,name = "phphtml"),
    path("laravelhtml/",views.laravelhtml,name = "laravelhtml"),
    path("djangoreact/",views.djangoreact,name = "djangoreact"),
    
# for mobile application
    
    #for mobile application front end
    path("mfrontend/",views.mfrontend,name = "mfrontend"),
    
    path("reactnative/",views.reactnative,name = "reactnative"),
    path("kivy/",views.kivy,name = "kivy"),
    path("fluter/",views.fluter,name = "fluter"),

    
    #mobile application backend
    path("mbackend/",views.mbackend,name = "mbackend"),
    
    path("mdjango/",views.mdjango,name = "mdjango"),
    path("mflask/",views.mflask,name = "mflask"),
    path("mfirebase/",views.mfirebase,name = "mfirebase"),
    
    #mobile application full stack development
    path("mfullstack/",views.mfullstack,name = "mfullstack"),
    
    path("reactnativedjango/",views.reactnativedjango,name = "reactnativedjango"),
    path("reactnativeflask/",views.reactnativeflask,name = "reactnativeflask"),
    path("reactnativefirebase/",views.reactnativefirebase,name = "reactnativefirebase"),
    
    #for desktop application
    path("cdeskapp/",views.cdeskapp,name = "cdeskapp"),
    path("pdeskapp/",views.pdeskapp,name = "pdeskapp"),
    path("kdeskapp/",views.kdeskapp,name = "kdeskapp"),
    
#artificial intelligence
    #for machine learning
    # path("machine/",views.machine,name = "machine"),
    
    # path("vision/",views.vision,name = "vision"),
    # path("natural/",views.natural,name = "natural"),
    # path("datascience/",views.datascience,name = "datascience"),
    # path("vision/",views.vision,name = "vision"),
    # path("natural/",views.natural,name = "natural"),
    # path("datascience/",views.datascience,name = "datascience"),
    
    #for deep learning.
    # path("deep/",views.deep,name = "deep"),       
    
    # path("vision/",views.vision,name = "vision"),
    # path("natural/",views.natural,name = "natural"),
    # path("datascience/",views.datascience,name = "datascience"),
    # path("vision/",views.vision,name = "vision"),
    # path("natural/",views.natural,name = "natural"),
    # path("datascience/",views.datascience,name = "datascience"),
    
    #for embeded system
    path("cembeded/",views.cembeded,name = "cembeded"),
    path("aembeded/",views.aembeded,name = "aembeded"),
    path("pembeded/",views.pembeded,name = "pembeded"),
    path("mpembeded/",views.mpembeded,name = "mpembeded"),
    
    #for graphics designing
    path("photoshop/",views.photoshop,name = "photoshop"),
    path("illustrator/",views.illustrator,name = "illustrator"),
    
    # FOR PROJECT
    path("websiteproject/",views.websiteproject,name = "websiteproject"),
    path("mobileproject/",views.mobileproject,name = "mobileproject"),
    path("desktopproject/",views.desktopproject,name = "desktopproject"),
    path("artificialproject/",views.artificialproject,name = "artificialproject"),
    path("embededproject/",views.embededproject,name = "embededproject"),
    path("iotproject/",views.iotproject,name = "iotproject"),
    path("virtualrealityproject/",views.virtualrealityproject,name = "virtualrealityproject"),
    path("cyberproject/",views.cyberproject,name = "cyberproject"),
    
    # FOR IMAGE
    path("image/",views.image,name = "image"),
    
    
    
    
    # template download
    path("webtemplate/",views.webtemplate,name = "webtemplate"),
    
    path("htmlcsstemplate/",views.htmlcsstemplate,name = "htmlcsstemplate"),
    path("reacttemplate/",views.reacttemplate,name = "reacttemplate"),
    path("vueJs_template/",views.vueJs_template,name = "vueJs_template"),
    path("elm/",views.elm,name = "elm"),
    path("swift/",views.swift,name = "swift"),
    path("JQuery/",views.JQuery,name = "JQuery"),
    path("flutter_template/",views.flutter_template,name = "flutter_template"),
    path("svelte/",views.svelte,name = "svelte"),
    path("materialize_CSS/",views.materialize_CSS,name = "materialize_CSS"),
    path("foundation/",views.foundation,name = "foundation"),
    path("angular_template/",views.angular_template,name = "angular_template"),
    path("tailwind_CSS/",views.tailwind_CSS,name = "tailwind_CSS"),
    path("bootstrap_template/",views.bootstrap_template,name = "bootstrap_template"),
    
    
    
    path("mobiletemplate/",views.mobiletemplate,name = "mobiletemplate"),
    path("reactnativetemplate/",views.reactnativetemplate,name = "reactnativetemplate"),
    
    path("flutter_mobile_template/",views.flutter_mobile_template,name = "flutter_mobile_template"),
    path("swiftUI/",views.swiftUI,name = "swiftUI"),
    path("jetpack_Compose/",views.jetpack_Compose,name = "jetpack_Compose"),
    path("ionic_Framework/",views.ionic_Framework,name = "ionic_Framework"),
    path("xamarin/",views.xamarin,name = "xamarin"),
    path("phoneGap/",views.phoneGap,name = "phoneGap"),
    path("nativeScript/",views.nativeScript,name = "nativeScript"),
    path("framework_seven/",views.framework_seven,name = "framework_seven"),
    path("onsen_UI/",views.onsen_UI,name = "onsen_UI"),
    path("jQuery_Mobile/",views.jQuery_Mobile,name = "jQuery_Mobile"),
    path("sencha_Touch/",views.sencha_Touch,name = "sencha_Touch"),
    path("Kivy_template/",views.Kivy_template,name = "Kivy_template"),
    path("bootstrap_Mobile_Templates/",views.bootstrap_Mobile_Templates,name = "bootstrap_Mobile_Templates"),
    path("quasar_Framework/",views.quasar_Framework,name = "quasar_Framework"),
    
    
    path("desktoptemplate/",views.desktoptemplate,name = "desktoptemplate"),
    
    path("kivytemplate/",views.kivytemplate,name = "kivytemplate"),
    path("pyqttemplate/",views.pyqttemplate,name = "pyqttemplate"),
    path("ctemplate/",views.ctemplate,name = "ctemplate"),
    path("tkintertemplate/",views.tkintertemplate,name = "tkintertemplate"),
    
    
    path("chashdesktopapp/",views.chashdesktopapp,name = "chashdesktopapp"),
    path("javadesktopapp/",views.javadesktopapp,name = "javadesktopapp"),
    path("cplusdesktopapp/",views.cplusdesktopapp,name = "cplusdesktopapp"),
    path("electrondesktopapp/",views.electrondesktopapp,name = "electrondesktopapp"),
    path("swiftdesktopapp/",views.swiftdesktopapp,name = "swiftdesktopapp"),
    path("rustdesktopapp/",views.rustdesktopapp,name = "rustdesktopapp"),
    
    path("microsofttemplate/",views.microsofttemplate,name = "microsofttemplate"),
    
    path("wordtemplate/",views.wordtemplate,name = "wordtemplate"),
    path("excelltemplate/",views.excelltemplate,name = "excelltemplate"),
    path("powerpointtemplate/",views.powerpointtemplate,name = "powerpointtemplate"),
    path("publishertemplate/",views.publishertemplate,name = "publishertemplate"),
    
    path("adobetemplate/",views.adobetemplate,name = "adobetemplate"),
    
    path("photoshoptemplate/",views.photoshoptemplate,name = "photoshoptemplate"),
    path("primiertemplate/",views.primiertemplate,name = "primiertemplate"),
    path("illustratortemplate/",views.illustratortemplate,name = "illustratortemplate"),
    
    path("InDesignadobe/",views.InDesignadobe,name = "InDesignadobe"),
    path("XDadobe/",views.XDadobe,name = "XDadobe"),
    path("Lightroomadobe/",views.Lightroomadobe,name = "Lightroomadobe"),
    path("LightroomClassicadobe/",views.LightroomClassicadobe,name = "LightroomClassicadobe"),
    path("AfterEffectsadobe/",views.AfterEffectsadobe,name = "AfterEffectsadobe"),
    path("Animateadobe/",views.Animateadobe,name = "Animateadobe"),
    path("Dreamweaveradobe/",views.Dreamweaveradobe,name = "Dreamweaveradobe"),
    path("Auditionadobe/",views.Auditionadobe,name = "Auditionadobe"),
    path("Bridgeadobe/",views.Bridgeadobe,name = "Bridgeadobe"),
    path("Dimensionadobe/",views.Dimensionadobe,name = "Dimensionadobe"),
    path("Frescoadobe/",views.Frescoadobe,name = "Frescoadobe"),
    path("CharacterAnimatoradobe/",views.CharacterAnimatoradobe,name = "CharacterAnimatoradobe"),
    path("MediaEncoderadobe/",views.MediaEncoderadobe,name = "MediaEncoderadobe"),
    path("Rushadobe/",views.Rushadobe,name = "Rushadobe"),
    path("Sparkadobe/",views.Sparkadobe,name = "Sparkadobe"),
    path("Substance3DPainteradobe/",views.Substance3DPainteradobe,name = "Substance3DPainteradobe"),
    path("Substance3DDesigneradobe/",views.Substance3DDesigneradobe,name = "Substance3DDesigneradobe"),
    path("Substance3DSampleradobe/",views.Substance3DSampleradobe,name = "Substance3DSampleradobe"),
    path("Substance3DStageradobe/",views.Substance3DStageradobe,name = "Substance3DStageradobe"),
    path("AcrobatProDCadobe/",views.AcrobatProDCadobe,name = "AcrobatProDCadobe"),
    path("Signadobe/",views.Signadobe,name = "Signadobe"),
    path("FrameMakeradobe/",views.FrameMakeradobe,name = "FrameMakeradobe"),
    path("Engageadobe/",views.Engageadobe,name = "Engageadobe"),
    path("Presenteradobe/",views.Presenteradobe,name = "Presenteradobe"),
   
    path("template/",views.template,name = "template"),
    path("project/",views.project,name = "project"),
    path("course/",views.course,name = "course"),
    path("ebooks/",views.ebooks,name = "ebooks"),
    path("music/",views.music,name = "music"),
    path("video/",views.video,name = "video"),
    path("art/",views.art,name = "art"),
    path("cad/",views.cad,name = "cad"),
    path("printable/",views.printable,name = "printable"),
    path("software/",views.software,name = "software"),
    path("business/",views.business,name = "business"),
    
    
    
    
    # FOR BOOKS
    path("novels/",views.novels,name = "novels"),
    path("short_stories/",views.short_stories,name = "short_stories"),
    path("poetry/",views.poetry,name = "poetry"),
    path("flash_fiction/",views.flash_fiction,name = "flash_fiction"),
    path("self_help_book/",views.self_help_book,name = "self_help_book"),
    path("biographies/",views.biographies,name = "biographies"),
    path("personal_development_books/",views.personal_development_books,name = "personal_development_books"),
    path("history_books/",views.history_books,name = "history_books"),
    path("true_crime/",views.true_crime,name = "true_crime"),
    path("textbooks/",views.textbooks,name = "textbooks"),
    path("research_papers/",views.research_papers,name = "research_papers"),
    path("study_guides/",views.study_guides,name = "study_guides"),
    path("how_to_guides_tutorials/",views.how_to_guides_tutorials,name = "how_to_guides_tutorials"),
    path("business_strategy_guides/",views.business_strategy_guides,name = "business_strategy_guides"),
    path("marketing_and_sales_e_books/",views.marketing_and_sales_e_books,name = "marketing_and_sales_e_books"),
    path("entrepreneurship_guides/",views.entrepreneurship_guides,name = "entrepreneurship_guides"),
    path("financial_planning/",views.financial_planning,name = "financial_planning"),
    path("nutrition_guides/",views.nutrition_guides,name = "nutrition_guides"),
    path("workout_and_fitness_plans/",views.workout_and_fitness_plans,name = "workout_and_fitness_plans"),
    path("mental_health_wellness/",views.mental_health_wellness,name = "mental_health_wellness"),
    path("meditation_and_mindfulness_e_books/",views.meditation_and_mindfulness_e_books,name = "meditation_and_mindfulness_e_books"),
    path("coding_and_programming_tutorials/",views.coding_and_programming_tutorials,name = "coding_and_programming_tutorials"),
    path("software_manuals/",views.software_manuals,name = "software_manuals"),
    path("IT_and_networking_guides/",views.IT_and_networking_guides,name = "IT_and_networking_guides"),
    path("artificial_intelligence_machine_learning/",views.artificial_intelligence_machine_learning,name = "artificial_intelligence_machine_learning"),
    path("photography_tutorials/",views.photography_tutorials,name = "photography_tutorials"),
    path("painting_and_drawing_guides/",views.painting_and_drawing_guides,name = "painting_and_drawing_guides"),
    path("writing_and_storytelling_techniques/",views.writing_and_storytelling_techniques,name = "writing_and_storytelling_techniques"),
    path("crafting_DIY_projects/",views.crafting_DIY_projects,name = "crafting_DIY_projects"),
    path("recipe_collections/",views.recipe_collections,name = "recipe_collections"),
    path("specialized_diet_guides/",views.specialized_diet_guides,name = "specialized_diet_guides"),
    path("meal_planning_and_prep/",views.meal_planning_and_prep,name = "meal_planning_and_prep"),
    path("parenting_advice/",views.parenting_advice,name = "parenting_advice"),
    path("marriage_and_relationship_counseling/",views.marriage_and_relationship_counseling,name = "marriage_and_relationship_counseling"),
    path("family_planning_guides/",views.family_planning_guides,name = "family_planning_guides"),
    path("childcare_and_development/",views.childcare_and_development,name = "childcare_and_development"),
    path("travel_guides/",views.travel_guides,name = "travel_guides"),
    path("destination_reviews/",views.destination_reviews,name = "destination_reviews"),
    path("adventure_stories/",views.adventure_stories,name = "adventure_stories"),
    path("travel_planning_and_budgeting/",views.travel_planning_and_budgeting,name = "travel_planning_and_budgeting"),
    path("personal_finance_e_books/",views.personal_finance_e_books,name = "personal_finance_e_books"),
    path("investment_strategies/",views.investment_strategies,name = "investment_strategies"),
    path("retirement_planning/",views.retirement_planning,name = "retirement_planning"),
    path("budgeting_tips/",views.budgeting_tips,name = "budgeting_tips"),
    path("religious_texts/",views.religious_texts,name = "religious_texts"),
    path("spiritual_growth_guides/",views.spiritual_growth_guides,name = "spiritual_growth_guides"),
    path("meditation_and_mindfulness_books/",views.meditation_and_mindfulness_books,name = "meditation_and_mindfulness_books"),
    path("philosophy_and_life_purpose_e_books/",views.philosophy_and_life_purpose_e_books,name = "philosophy_and_life_purpose_e_books"),
    path("time_management_and_productivity/",views.time_management_and_productivity,name = "time_management_and_productivity"),
    path("self_improvement_and_motivation/",views.self_improvement_and_motivation,name = "self_improvement_and_motivation"),
    path("life_coaching_guides/",views.life_coaching_guides,name = "life_coaching_guides"),
    path("work_life_balance/",views.work_life_balance,name = "work_life_balance"),
    path("legal_guides_and_contracts/",views.legal_guides_and_contracts,name = "legal_guides_and_contracts"),
    path("HR_and_employment_handbooks/",views.HR_and_employment_handbooks,name = "HR_and_employment_handbooks"),
    path("professional_development/",views.professional_development,name = "professional_development"),
    path("real_estate_investment_guides/",views.real_estate_investment_guides,name = "real_estate_investment_guides"),
    path("property_management_manuals/",views.property_management_manuals,name = "property_management_manuals"),
    path("buying_and_selling_homes/",views.buying_and_selling_homes,name = "buying_and_selling_homes"),
    
    
    # FOR MUSIC
    path("single_tracks/",views.single_tracks,name = "single_tracks"),
    path("full_albums/",views.full_albums,name = "full_albums"),
    path("extended_plays/",views.extended_plays,name = "extended_plays"),
    path("instrumental_versions/",views.instrumental_versions,name = "instrumental_versions"),
    path("beats_for_rappers_and_singers/",views.beats_for_rappers_and_singers,name = "beats_for_rappers_and_singers"),
    path("lo_fi_beats/",views.lo_fi_beats,name = "lo_fi_beats"),
    path("background_instrumentals_for_videos/",views.background_instrumentals_for_videos,name = "background_instrumentals_for_videos"),
    path("royalty_free_music/",views.royalty_free_music,name = "royalty_free_music"),
    path("environmental_sounds/",views.environmental_sounds,name = "environmental_sounds"),
    path("foley_sounds/",views.foley_sounds,name = "foley_sounds"),
    path("sci_fi_and_futuristic_sounds/",views.sci_fi_and_futuristic_sounds,name = "sci_fi_and_futuristic_sounds"),
    path("horror_and_thriller_effects/",views.horror_and_thriller_effects,name = "horror_and_thriller_effects"),
    path("drum_loops/",views.drum_loops,name = "drum_loops"),
    path("melodic_loops/",views.melodic_loops,name = "melodic_loops"),
    path("vocal_samples/",views.vocal_samples,name = "vocal_samples"),
    path("synth_and_bass_loops/",views.synth_and_bass_loops,name = "synth_and_bass_loops"),
    path("background_music_for_videos/",views.background_music_for_videos,name = "background_music_for_videos"),
    path("music_for_podcasts/",views.music_for_podcasts,name = "music_for_podcasts"),
    path("royalty_free_soundtracks_for_commercials/",views.royalty_free_soundtracks_for_commercials,name = "royalty_free_soundtracks_for_commercials"),
    path("ambient_music_for_relaxation_and_meditation/",views.ambient_music_for_relaxation_and_meditation,name = "ambient_music_for_relaxation_and_meditation"),
    path("talk_shows/",views.talk_shows,name = "talk_shows"),
    path("interview_series/",views.interview_series,name = "interview_series"),
    path("educational_podcasts/",views.educational_podcasts,name = "educational_podcasts"),
    path("storytelling_and_fictional_audio_series/",views.storytelling_and_fictional_audio_series,name = "storytelling_and_fictional_audio_series"),
    path("nature_inspired_soundscapes/",views.nature_inspired_soundscapes,name = "nature_inspired_soundscapes"),
    
    #FOR VIDEOS AND MULTIMEDIA
    path("nature_and_landscape_footage/",views.nature_and_landscape_footage,name = "nature_and_landscape_footage"),
    path("urban_and_city_life_footage/",views.urban_and_city_life_footage,name = "urban_and_city_life_footage"),
    path("aerial_drone_videos/",views.aerial_drone_videos,name = "aerial_drone_videos"),
    path("slow_motion_and_time_lapse_videos/",views.slow_motion_and_time_lapse_videos,name = "slow_motion_and_time_lapse_videos"),
    path("intros_and_outros_for_YouTube_videos/",views.intros_and_outros_for_YouTube_videos,name = "intros_and_outros_for_YouTube_videos"),
    path("two_animations/",views.two_animations,name = "two_animations"),
    path("three_animations/",views.three_animations,name = "three_animations"),
    path("explainer_videos/",views.explainer_videos,name = "explainer_videos"),
    path("motion_graphics_for_commercials/",views.motion_graphics_for_commercials,name = "motion_graphics_for_commercials"),
    path("personal_vlogs/",views.personal_vlogs,name = "personal_vlogs"),
    path("travel_videos/",views.travel_videos,name = "travel_videos"),
    path("lifestyl_vlogs/",views.lifestyl_vlogs,name = "lifestyl_vlogs"),
    path("daily_video_blogs/",views.daily_video_blogs,name = "daily_video_blogs"),
    path("wedding_videos/",views.wedding_videos,name = "wedding_videos"),
    path("corporate_event_videos/",views.corporate_event_videos,name = "corporate_event_videos"),
    path("party_and_celebration_videos/",views.party_and_celebration_videos,name = "party_and_celebration_videos"),
    path("award_ceremony_Video/",views.award_ceremony_Video,name = "award_ceremony_Video"),
    path("business_presentations/",views.business_presentations,name = "business_presentations"),
    path("sales_pitches/",views.sales_pitches,name = "sales_pitches"),
    path("educational_or_academic_presentations/",views.educational_or_academic_presentations,name = "educational_or_academic_presentations"),
    path("product_promo_videos/",views.product_promo_videos,name = "product_promo_videos"),
    path("service_advertisement_videos/",views.service_advertisement_videos,name = "service_advertisement_videos"),
    path("brand_story_videos/",views.brand_story_videos,name = "brand_story_videos"),
    path("social_media_ads/",views.social_media_ads,name = "social_media_ads"),
    path("official_music_videos/",views.official_music_videos,name = "official_music_videos"),
    path("lyric_videos/",views.lyric_videos,name = "lyric_videos"),
    path("animated_music_videos/",views.animated_music_videos,name = "animated_music_videos"),
    path("performance_videos/",views.performance_videos,name = "performance_videos"),
    path("fiction_short_films/",views.fiction_short_films,name = "fiction_short_films"),
    path("mini_documentaries/",views.mini_documentaries,name = "mini_documentaries"),
    path("biographical_documentaries/",views.biographical_documentaries,name = "biographical_documentaries"),
    path("indie_films/",views.indie_films,name = "indie_films"),
    path("adventure_videos/",views.adventure_videos,name = "adventure_videos"),
    path("interactive_tutorials/",views.interactive_tutorials,name = "interactive_tutorials"),
    path("interactive_quizzes_or_assessments/",views.interactive_quizzes_or_assessments,name = "interactive_quizzes_or_assessments"),
    path("gamified_videos/",views.gamified_videos,name = "gamified_videos"),
    path("customer_testimonial_videos/",views.customer_testimonial_videos,name = "customer_testimonial_videos"),
    path("product_review_videos/",views.product_review_videos,name = "product_review_videos"),
    path("user_generated_content_videos/",views.user_generated_content_videos,name = "user_generated_content_videos"),
    path("virtual_reality_experiences/",views.virtual_reality_experiences,name = "virtual_reality_experiences"),
    path("degree_video_tours/",views.degree_video_tours,name = "degree_video_tours"),
    path("immersive_event_videos/",views.immersive_event_videos,name = "immersive_event_videos"),
    path("cinematic_sequences/",views.cinematic_sequences,name = "cinematic_sequences"),
    path("aerial_drone_footage/",views.aerial_drone_footage,name = "aerial_drone_footage"),
    path("scenic_landscape_shots/",views.scenic_landscape_shots,name = "scenic_landscape_shots"),
    path("epic_slow_motion_videos/",views.epic_slow_motion_videos,name = "epic_slow_motion_videos"),
    path("urban_timelapse_videos/",views.urban_timelapse_videos,name = "urban_timelapse_videos"),
    path("nature_and_sky_timelapse/",views.nature_and_sky_timelapse,name = "nature_and_sky_timelapse"),
    path("construction_progress_timelapse/",views.construction_progress_timelapse,name = "construction_progress_timelapse"),
    path("yoga_and_meditation_videos/",views.yoga_and_meditation_videos,name = "yoga_and_meditation_videos"),
    path("healthy_lifestyle_tips/",views.healthy_lifestyle_tips,name = "healthy_lifestyle_tips"),
    path("exercise_and_wellness_programs/",views.exercise_and_wellness_programs,name = "exercise_and_wellness_programs"),
    path("product_feature_demonstrations/",views.product_feature_demonstrations,name = "product_feature_demonstrations"),
    path("physical_product_unboxing_and_reviews/",views.physical_product_unboxing_and_reviews,name = "physical_product_unboxing_and_reviews"),
    path("animated_YouTube_intros/",views.animated_YouTube_intros,name = "animated_YouTube_intros"),
    path("branding_outros_for_videos/",views.branding_outros_for_videos,name = "branding_outros_for_videos"),
    path("social_media_content_intros/",views.social_media_content_intros,name = "social_media_content_intros"),
    
    #  FOR Digital Art & Design
    path("hand_drawn_digital_illustrations/",views.hand_drawn_digital_illustrations,name = "hand_drawn_digital_illustrations"),
    path("character_design/",views.character_design,name = "character_design"),
    path("website_design_templates/",views.website_design_templates,name = "website_design_templates"),
    path("mobile_app_design_templates/",views.mobile_app_design_templates,name = "mobile_app_design_templates"),
    path("editorial_illustrations/",views.editorial_illustrations,name = "editorial_illustrations"),
    path("children_book_illustrations/",views.children_book_illustrations,name = "children_book_illustrations"),
    path("posters/",views.posters,name = "posters"),
    path("flyers/",views.flyers,name = "flyers"),
    path("brochures/",views.brochures,name = "brochures"),
    path("infographics/",views.infographics,name = "infographics"),
    path("digital_advertisements/",views.digital_advertisements,name = "digital_advertisements"),
    path("brand_logos/",views.brand_logos,name = "brand_logos"),
    path("icon_sets/",views.icon_sets,name = "icon_sets"),
    path("custom_logos_for_businesses/",views.custom_logos_for_businesses,name = "custom_logos_for_businesses"),
    path("monograms/",views.monograms,name = "monograms"),
    path("scalable_vector_illustrations/",views.scalable_vector_illustrations,name = "scalable_vector_illustrations"),
    path("flat_design_elements/",views.flat_design_elements,name = "flat_design_elements"),
    path("icons_and_symbols/",views.icons_and_symbols,name = "icons_and_symbols"),
    path("geometric_patterns/",views.geometric_patterns,name = "geometric_patterns"),
    path("three_models/",views.three_models,name = "three_models"),
    path("three_character_design/",views.three_character_design,name = "three_character_design"),
    
    path("product_visualizations/",views.product_visualizations,name = "product_visualizations"),
    path("custom_fonts/",views.custom_fonts,name = "custom_fonts"),
    path("hand_lettering_designs/",views.hand_lettering_designs,name = "hand_lettering_designs"),
    path("calligraphy_artwork/",views.calligraphy_artwork,name = "calligraphy_artwork"),
    path("display_typefaces/",views.display_typefaces,name = "display_typefaces"),
    path("wireframe_kits/",views.wireframe_kits,name = "wireframe_kits"),
    path("prototype_designs/",views.prototype_designs,name = "prototype_designs"),
    path("interactive_mockups/",views.interactive_mockups,name = "interactive_mockups"),
    path("business_cards/",views.business_cards,name = "business_cards"),
    path("wedding_invitations/",views.wedding_invitations,name = "wedding_invitations"),
    path("greeting_cards/",views.greeting_cards,name = "greeting_cards"),
    path("calendars/",views.calendars,name = "calendars"),
    path("planners/",views.planners,name = "planners"),
    path("seamless_patterns/",views.seamless_patterns,name = "seamless_patterns"),
    path("textile_and_fabric_patterns/",views.textile_and_fabric_patterns,name = "textile_and_fabric_patterns"),
    path("wallpaper_designs/",views.wallpaper_designs,name = "wallpaper_designs"),
    path("packaging_patterns/",views.packaging_patterns,name = "packaging_patterns"),
    path("UI_UX_icons/",views.UI_UX_icons,name = "UI_UX_icons"),
    path("app_icons/",views.app_icons,name = "app_icons"),
    path("social_media_icons/",views.social_media_icons,name = "social_media_icons"),
    path("custom_icon_sets_for_websites/",views.custom_icon_sets_for_websites,name = "custom_icon_sets_for_websites"),
    path("realistic_portrait_paintings/",views.realistic_portrait_paintings,name = "realistic_portrait_paintings"),
    path("fantasy_landscape_paintings/",views.fantasy_landscape_paintings,name = "fantasy_landscape_paintings"),
    path("Concept_art_for_games_or_films/",views.Concept_art_for_games_or_films,name = "Concept_art_for_games_or_films"),
    path("abstract_digital_artwork/",views.abstract_digital_artwork,name = "abstract_digital_artwork"),
    path("composite_photo_art/",views.composite_photo_art,name = "composite_photo_art"),
    path("surreal_photo_manipulations/",views.surreal_photo_manipulations,name = "surreal_photo_manipulations"),
    path("product_photo_retouching/",views.product_photo_retouching,name = "product_photo_retouching"),
    path("fashion_and_beauty_retouching/",views.fashion_and_beauty_retouching,name = "fashion_and_beauty_retouching"),
    path("digital_collages/",views.digital_collages,name = "digital_collages"),
    path("mixed_media_art/",views.mixed_media_art,name = "mixed_media_art"),
    path("scrapbook_designs/",views.scrapbook_designs,name = "scrapbook_designs"),
    path("character_concept_art/",views.character_concept_art,name = "character_concept_art"),
    path("creature_and_monster_designs/",views.creature_and_monster_designs,name = "creature_and_monster_designs"),
    path("storyboard_art/",views.storyboard_art,name = "storyboard_art"),
    path("comic_book_illustrations/",views.comic_book_illustrations,name = "comic_book_illustrations"),
    path("manga_style_characters_and_story_panels/",views.manga_style_characters_and_story_panels,name = "manga_style_characters_and_story_panels"),
    path("digital_comic_strips/",views.digital_comic_strips,name = "digital_comic_strips"),
    path("t_shirt_graphics_and_mockups/",views.t_shirt_graphics_and_mockups,name = "t_shirt_graphics_and_mockups"),
    path("custom_merchandise_designs/",views.custom_merchandise_designs,name = "custom_merchandise_designs"),
    path("apparel_patterns_and_prints/",views.apparel_patterns_and_prints,name = "apparel_patterns_and_prints"),
    path("themed_photo_collections/",views.themed_photo_collections,name = "themed_photo_collections"),
    path("high_resolution_stock_images/",views.high_resolution_stock_images,name = "high_resolution_stock_images"),
    path("conceptual_photography/",views.conceptual_photography,name = "conceptual_photography"),
    path("art_prints_for_home_decor/",views.art_prints_for_home_decor,name = "art_prints_for_home_decor"),
    path("motivational_posters/",views.motivational_posters,name = "motivational_posters"),
    path("abstract_and_minimalist_art/",views.abstract_and_minimalist_art,name = "abstract_and_minimalist_art"),
    path("instagram_post_templates/",views.instagram_post_templates,name = "instagram_post_templates"),
    path("facebook_banner_designs/",views.facebook_banner_designs,name = "facebook_banner_designs"),
    path("pinterest_graphic_templates/",views.pinterest_graphic_templates,name = "pinterest_graphic_templates"),
    path("story_highlight_icons/",views.story_highlight_icons,name = "story_highlight_icons"),
    
    # 3D & CAD Designs
    path("character_models/",views.character_models,name = "character_models"),
    path("vehicle_models/",views.vehicle_models,name = "vehicle_models"),
    path("furniture_and_home_decor_models/",views.furniture_and_home_decor_models,name = "furniture_and_home_decor_models"),
    path("product_prototypes/",views.product_prototypes,name = "product_prototypes"),
    path("house_and_building_designs/",views.house_and_building_designs,name = "house_and_building_designs"),
    path("interior_and_exterior_architectural_models/",views.interior_and_exterior_architectural_models,name = "interior_and_exterior_architectural_models"),
    path("floor_plans_and_layouts/",views.floor_plans_and_layouts,name = "floor_plans_and_layouts"),
    path("urban_planning_models/",views.urban_planning_models,name = "urban_planning_models"),
    path("architectural_renderings/",views.architectural_renderings,name = "architectural_renderings"),
    path("toys_and_figurines/",views.toys_and_figurines,name = "toys_and_figurines"),
    path("custom_jewelry_designs/",views.custom_jewelry_designs,name = "custom_jewelry_designs"),
    path("gadgets_and_accessories/",views.gadgets_and_accessories,name = "gadgets_and_accessories"),
    path("home_decor_and_functional_objects/",views.home_decor_and_functional_objects,name = "home_decor_and_functional_objects"),
    path("mechanical_part_designs/",views.mechanical_part_designs,name = "mechanical_part_designs"),
    path("industrial_equipment_models/",views.industrial_equipment_models,name = "industrial_equipment_models"),
    path("engineering_diagrams/",views.engineering_diagrams,name = "engineering_diagrams"),
    path("CNC_and_laser_cutting_templates/",views.CNC_and_laser_cutting_templates,name = "CNC_and_laser_cutting_templates"),
    path("modern_and_classic_furniture_models/",views.modern_and_classic_furniture_models,name = "modern_and_classic_furniture_models"),
    path("kitchen_and_bathroom_designs/",views.kitchen_and_bathroom_designs,name = "kitchen_and_bathroom_designs"),
    path("custom_cabinetry_and_shelving_units/",views.custom_cabinetry_and_shelving_units,name = "custom_cabinetry_and_shelving_units"),
    path("threed_room_and_space_layouts/",views.threed_room_and_space_layouts,name = "threed_room_and_space_layouts"),
    path("consumer_electronics_prototypes/",views.consumer_electronics_prototypes,name = "consumer_electronics_prototypes"),
    path("fashion_and_accessory_designs/",views.fashion_and_accessory_designs,name = "fashion_and_accessory_designs"),
    path("home_appliance_prototypes/",views.home_appliance_prototypes,name = "home_appliance_prototypes"),
    path("wearable_technology_prototypes/",views.wearable_technology_prototypes,name = "wearable_technology_prototypes"),
    path("threed_characters_and_creatures/",views.threed_characters_and_creatures,name = "threed_characters_and_creatures"),
    path("environmental_models/",views.environmental_models,name = "environmental_models"),
    path("wweapons_and_gear/",views.wweapons_and_gear,name = "wweapons_and_gear"),
    path("vehicle_models_for_gaming/",views.vehicle_models_for_gaming,name = "vehicle_models_for_gaming"),
    path("anatomy_and_body_part_models/",views.anatomy_and_body_part_models,name = "anatomy_and_body_part_models"),
    path("molecular_and_chemical_models/",views.molecular_and_chemical_models,name = "molecular_and_chemical_models"),
    path("medical_equipment_and_device_designs/",views.medical_equipment_and_device_designs,name = "medical_equipment_and_device_designs"),
    path("scientific_visualization_models/",views.scientific_visualization_models,name = "scientific_visualization_models"),
    path("car_and_truck_models/",views.car_and_truck_models,name = "car_and_truck_models"),
    path("aircraft_and_drone_designs/",views.aircraft_and_drone_designs,name = "aircraft_and_drone_designs"),
    path("ship_and_boat_models/",views.ship_and_boat_models,name = "ship_and_boat_models"),
    path("public_transportation_models/",views.public_transportation_models,name = "public_transportation_models"),
    path("ring_and_earring_designs/",views.ring_and_earring_designs,name = "ring_and_earring_designs"),
    path("pendant_and_necklace_models/",views.pendant_and_necklace_models,name = "pendant_and_necklace_models"),
    path("custom_and_personalized_jewelry_designs/",views.custom_and_personalized_jewelry_designs,name = "custom_and_personalized_jewelry_designs"),
    path("threed_printable_jewelry_prototypes/",views.threed_printable_jewelry_prototypes,name = "threed_printable_jewelry_prototypes"),
    path("VR_ready_three_models_for_virtual_environments/",views.VR_ready_three_models_for_virtual_environments,name = "VR_ready_three_models_for_virtual_environments"),
    path("AR_models_for_apps_and_interactive_experiences/",views.AR_models_for_apps_and_interactive_experiences,name = "AR_models_for_apps_and_interactive_experiences"),
    path("architectural_walkthroughs_for_VR/",views.architectural_walkthroughs_for_VR,name = "architectural_walkthroughs_for_VR"),
    path("heavy_machinery_models/",views.heavy_machinery_models,name = "heavy_machinery_models"),
    path("industrial_equipment/",views.industrial_equipment,name = "industrial_equipment"),
    path("mechanical_components_and_assemblies/",views.mechanical_components_and_assemblies,name = "mechanical_components_and_assemblies"),
    path("fantasy_and_sci_fi_character_models/",views.fantasy_and_sci_fi_character_models,name = "fantasy_and_sci_fi_character_models"),
    path("cartoon_and_stylized_characters/",views.cartoon_and_stylized_characters,name = "cartoon_and_stylized_characters"),
    path("monster_and_creature_models_for_games_and_films/",views.monster_and_creature_models_for_games_and_films,name = "monster_and_creature_models_for_games_and_films"),
    path("A_threed_clothing_and_accessory_models/",views.A_threed_clothing_and_accessory_models,name = "A_threed_clothing_and_accessory_models"),
    path("fashion_prototypes_for_manufacturing/",views.fashion_prototypes_for_manufacturing,name = "fashion_prototypes_for_manufacturing"),
    path("shoe_and_bag_designs/",views.shoe_and_bag_designs,name = "shoe_and_bag_designs"),
    path("fully_rigged_threed_characters_for_animation/",views.fully_rigged_threed_characters_for_animation,name = "fully_rigged_threed_characters_for_animation"),
    path("motion_capture_ready_models/",views.motion_capture_ready_models,name = "motion_capture_ready_models"),
    path("custom_rigging_setups_for_specific_software/",views.custom_rigging_setups_for_specific_software,name = "custom_rigging_setups_for_specific_software"),
    path("natural_landscapes/",views.natural_landscapes,name = "natural_landscapes"),
    path("city_and_urban_environments/",views.city_and_urban_environments,name = "city_and_urban_environments"),
    path("virtual_environments_for_games_and_simulations/",views.virtual_environments_for_games_and_simulations,name = "virtual_environments_for_games_and_simulations"),
    path("engine_models/",views.engine_models,name = "engine_models"),
    path("gear_and_mechanical_component_designs/",views.gear_and_mechanical_component_designs,name = "gear_and_mechanical_component_designs"),
    path("CAD_files_for_mechanical_systems/",views.CAD_files_for_mechanical_systems,name = "CAD_files_for_mechanical_systems"),
    path("DIY_assembly_instructions_for_furniture/",views.DIY_assembly_instructions_for_furniture,name = "DIY_assembly_instructions_for_furniture"),
    path("custom_furniture_designs_with_CAD_plans/",views.custom_furniture_designs_with_CAD_plans,name = "custom_furniture_designs_with_CAD_plans"),
    path("CNC_cut_plans_for_modular_furniture/",views.CNC_cut_plans_for_modular_furniture,name = "CNC_cut_plans_for_modular_furniture"),
    path("threed_models_of_props_for_film_sets/",views.threed_models_of_props_for_film_sets,name = "threed_models_of_props_for_film_sets"),
    path("sci_fi_or_fantasy_set_designs/",views.sci_fi_or_fantasy_set_designs,name = "sci_fi_or_fantasy_set_designs"),
    path("historical_prop_replicas/",views.historical_prop_replicas,name = "historical_prop_replicas"),
    path("robot_design_and_assembly_plans/",views.robot_design_and_assembly_plans,name = "robot_design_and_assembly_plans"),
    path("drone_and_UAV_designs/",views.drone_and_UAV_designs,name = "drone_and_UAV_designs"),
    path("industrial_automation_models/",views.industrial_automation_models,name = "industrial_automation_models"),   
    path("A_threed_clothing_and_accessory_models/",views.A_threed_clothing_and_accessory_models,name = "A_threed_clothing_and_accessory_models"), 
    path("threed_floor_plans/",views.threed_floor_plans,name = "threed_floor_plans"),
    path("interior_and_exterior_visualization/",views.interior_and_exterior_visualization,name = "interior_and_exterior_visualization"),
    path("threed_topographical_maps/",views.threed_topographical_maps,name = "threed_topographical_maps"),
    path("terrain_models_for_games_and_simulations/",views.terrain_models_for_games_and_simulations,name = "terrain_models_for_games_and_simulations"),
    path("landscape_elevation_models/",views.landscape_elevation_models,name = "landscape_elevation_models"),
    
    # Printable & Customizable Content
    path("invitations_and_greeting_cards_templates/",views.invitations_and_greeting_cards_templates,name = "invitations_and_greeting_cards_templates"),
    path("business_cards_template/",views.business_cards_template,name = "business_cards_template"),
    path("wedding_templates/",views.wedding_templates,name = "wedding_templates"),
    path("digital_planners/",views.digital_planners,name = "digital_planners"),
    path("SEO_tools/",views.SEO_tools,name = "SEO_tools"),
    
    # below not worked on
    path("email_marketing_templates/",views.email_marketing_templates,name = "email_marketing_templates"),
    path("website_themes/",views.website_themes,name = "website_themes"),
    path("custom_scripts/",views.custom_scripts,name = "custom_scripts"),

    # Software & Tools
    path("software_applications/",views.software_applications,name = "software_applications"),
    path("plugins_and_extensions/",views.plugins_and_extensions,name = "plugins_and_extensions"),
    path("architectural_plans/",views.architectural_plans,name = "architectural_plans"),
    path("mobile_apps/",views.mobile_apps,name = "mobile_apps"),
    path("software_as_a_Service/",views.software_as_a_Service,name = "software_as_a_Service"),
    path("copywriting_templates/",views.copywriting_templates,name = "copywriting_templates"),
    
    # Business & Marketing Tools
    path("business_templates/",views.business_templates,name = "business_templates"),
    path("marketing_materials/",views.marketing_materials,name = "marketing_materials"),
    path("analytics_tools/",views.analytics_tools,name = "analytics_tools"),
    path("CRM_templates/",views.CRM_templates,name = "CRM_templates"),
 
    
    # MWISHO
    
    path("myproduct/",views.myproduct,name = "myproduct"),

    # download image
    
    # url posting the course and template url
    path("websitepost/",views.websitepost,name = "websitepost"),
    path("mobilepost/",views.mobilepost,name = "mobilepost"),
    path("desktoppost/",views.desktoppost,name = "desktoppost"),
    path("embededpost/",views.embededpost,name = "embededpost"),
    path("graphicspost/",views.graphicspost,name = "graphicspost"),
    
    path("bookpost/",views.bookpost,name = "bookpost"),
    path("printablepost/",views.printablepost,name = "printablepost"),
    path("musicpost/",views.musicpost,name = "musicpost"),
    path("multimediapost/",views.multimediapost,name = "multimediapost"),
    path("digitalArtpost/",views.digitalArtpost,name = "digitalArtpost"),
    path("CADpost/",views.CADpost,name = "CADpost"),
    path("softwarepost/",views.softwarepost,name = "softwarepost"),
    path("businesspost/",views.businesspost,name = "businesspost"),
    
    # POSTING PROJECT
    path("projectpost/",views.projectpost,name = "projectpost"),
    
    # POSTING IMAGE
    path("imagepost/",views.imagepost,name = "imagepost"),
    
    # for posting templates
    path("websitetemplatepost/",views.websitetemplatepost,name = "websitetemplatepost"),
    path("mobiletemplatepost/",views.mobiletemplatepost,name = "mobiletemplatepost"),
    path("desktoptemplatepost/",views.desktoptemplatepost,name = "desktoptemplatepost"),
    path("microsofttemplatepost/",views.microsofttemplatepost,name = "microsofttemplatepost"),
    path("adobeposttemplate/",views.adobeposttemplate,name = "adobeposttemplate"),
    path("allproduct/",views.allproduct,name = "allproduct"),
    
    # url for viewing course
    path('viewwebsite/<str:pk>/', views.viewwebsite.as_view(), name = "viewwebsite"),
    path('viewmobile/<str:pk>/', views.viewmobile.as_view(), name = "viewmobile"),
    path('viewdesktop/<str:pk>/', views.viewdesktop.as_view(), name = "viewdesktop"),
    path('viewembeded/<str:pk>/', views.viewembeded.as_view(), name = "viewembeded"),
    path('viewgraphics/<str:pk>/', views.viewgraphics.as_view(), name = "viewgraphics"),
    
    # VIEW PROJECT
    path('viewproject/<str:pk>/', views.viewproject.as_view(), name = "viewproject"),
    
    # VIEW OTHER DIGITAL PRODUCT
    path('viewbook/<str:pk>/', views.viewbook.as_view(), name = "viewbook"),
    path('viewprintable/<str:pk>/', views.viewprintable.as_view(), name = "viewprintable"),
    path('viewmusic/<str:pk>/', views.viewmusic.as_view(), name = "viewmusic"),
    path('viewmultimedia/<str:pk>/', views.viewmultimedia.as_view(), name = "viewmultimedia"),
    path('viewdigitalArt/<str:pk>/', views.viewdigitalArt.as_view(), name = "viewdigitalArt"),
    path('viewCAD/<str:pk>/', views.viewCAD.as_view(), name = "viewCAD"),
    path('viewsoftware/<str:pk>/', views.viewsoftware.as_view(), name = "viewsoftware"),
    path('viewbusiness/<str:pk>/', views.viewbusiness.as_view(), name = "viewbusiness"),
    
    # VIEW IMAGE
    path('viewimage/<str:pk>/', views.viewimage.as_view(), name = "viewimage"),
    
    # url for viewing templates
    path("viewwebsitetemplate/<int:id>/",views.viewwebsitetemplate,name = "viewwebsitetemplate"),
    path("viewmobiletemplate/<int:id>/",views.viewmobiletemplate,name = "viewmobiletemplate"),
    path("viewdesktoptemplate/<int:id>/",views.viewdesktoptemplate,name = "viewdesktoptemplate"),
    path("viewmicrosofttemplate/<int:id>/",views.viewmicrosofttemplate,name = "viewmicrosofttemplate"),
    path("viewadobetemplate/<int:id>/",views.viewadobetemplate,name = "viewadobetemplate"),
    
    path("view_notifications/<int:id>/",views.view_notifications,name = "view_notifications"),
    
    # url for deleting course
    path('deletewebsite/<int:id>/', views.deletewebsite, name = "deletewebsite"),
    path('deletemobile/<int:id>/', views.deletemobile, name = "deletemobile"),
    path('deletedesktop/<int:id>/', views.deletedesktop, name = "deletedesktop"),
    path('deleteembeded/<int:id>/', views.deleteembeded, name = "deleteembeded"),
    path('deletegraphics/<int:id>/', views.deletegraphics, name = "deletegraphics"),
    
    # DELETE PROJECT
    path('deleteproject/<int:id>/', views.deleteproject, name = "deleteproject"),
    
    # DELETE OTHER DIGITAL PRODUCT
    path('deletebook/<int:id>/', views.deletebook, name = "deletebook"),
    path('deleteprintable/<int:id>/', views.deleteprintable, name = "deleteprintable"),
    path('deletemusic/<int:id>/', views.deletemusic, name = "deletemusic"),
    path('deletemultimedia/<int:id>/', views.deletemultimedia, name = "deletemultimedia"),
    path('deletedigitalArt/<int:id>/', views.deletedigitalArt, name = "deletedigitalArt"),
    path('deleteCAD/<int:id>/', views.deleteCAD, name = "deleteCAD"),
    path('deletesoftware/<int:id>/', views.deletesoftware, name = "deletesoftware"),
    path('deletebusiness/<int:id>/', views.deletebusiness, name = "deletebusiness"),
    
    # DELETE IMAGE
    path('deleteimage/<int:id>/', views.deleteimage, name = "deleteimage"),
    
    # url for deleting template
    path('deletewebsitetemplate/<int:id>/', views.deletewebsitetemplate, name = "deletewebsitetemplate"),
    path('deletemobiletemplate/<int:id>/', views.deletemobiletemplate, name = "deletemobiletemplate"),
    path('deletedesktoptemplate/<int:id>/', views.deletedesktoptemplate, name = "deletedesktoptemplate"),
    path('deletemicrosofttemplate/<int:id>/', views.deletemicrosofttemplate, name = "deletemicrosofttemplate"),
    path('deleteadobetemplate/<int:id>/', views.deleteadobetemplate, name = "deleteadobetemplate"),
    
    # url for updating courses
    path('updatewebsite/<int:id>/', views.updatewebsite, name = "updatewebsite"),
    path('updatemobile/<int:id>/', views.updatemobile, name = "updatemobile"),
    path('updatedesktop/<int:id>/', views.updatedesktop, name = "updatedesktop"),
    path('updateembeded/<int:id>/', views.updateembeded, name = "updateembeded"),
    path('updategraphics/<int:id>/', views.updategraphics, name = "updategraphics"),
    
    # UPDATING PROJECT
    path('updateproject/<int:id>/', views.updateproject, name = "updateproject"),
    
    # UPDATING OTHER DOGITAL PRODUCT
    path('updatebook/<int:id>/', views.updatebook, name = "updatebook"),
    path('updateprintable/<int:id>/', views.updateprintable, name = "updateprintable"),
    path('updatemusic/<int:id>/', views.updatemusic, name = "updatemusic"),
    path('updatemultimedia/<int:id>/', views.updatemultimedia, name = "updatemultimedia"),
    path('updatedigitalArt/<int:id>/', views.updatedigitalArt, name = "updatedigitalArt"),
    path('updateCAD/<int:id>/', views.updateCAD, name = "updateCAD"),
    path('updatesoftware/<int:id>/', views.updatesoftware, name = "updatesoftware"),
    path('updatebusiness/<int:id>/', views.updatebusiness, name = "updatebusiness"),
    
    # UPDATING IMAGE
    path('updateimage/<int:id>/', views.updateimage, name = "updateimage"),
    
    # url for updating templates
    path('updatewebsitetemplate/<int:id>/', views.updatewebsitetemplate, name = "updatewebsitetemplate"),
    path('updatemobiletemplate/<int:id>/', views.updatemobiletemplate, name = "updatemobiletemplate"),
    path('updatedesktoptemplate/<int:id>/', views.updatedesktoptemplate, name = "updatedesktoptemplate"),
    path('updatemicrosofttemplate/<int:id>/', views.updatemicrosofttemplate, name = "updatemicrosofttemplate"),
    path('updateadobetemplate/<int:id>/', views.updateadobetemplate, name = "updateadobetemplate"),
    
    path('updatecard/<int:id>/', views.updatecard, name = "updatecard"),
    
    # FOR PAYMENT
    path('pesapal/transaction/completed/', views.payment_completed, name='payment_completed'),
    
    path('process_websitetemplate_purchase/<int:template_id>/', views.process_websitetemplate_purchase, name = "process_websitetemplate_purchase"),
    path('process_mobiletemplate_purchase/<int:mobiletemplate_id>/', views.process_mobiletemplate_purchase, name = "process_mobiletemplate_purchase"),
    path('process_desktoptemplate_purchase/<int:desktoptemplate_id>/', views.process_desktoptemplate_purchase, name = "process_desktoptemplate_purchase"),
    path('process_microsofttemplate_purchase/<int:microsofttemplate_id>/', views.process_microsofttemplate_purchase, name = "process_microsofttemplate_purchase"),
    path('process_adobetemplate_purchase/<int:adobetemplate_id>/', views.process_adobetemplate_purchase, name = "process_adobetemplate_purchase"),
    path('process_project_purchase/<int:product_id>/', views.process_project_purchase, name = "process_project_purchase"),
    path('process_book_purchase/<int:product_id>/', views.process_book_purchase, name = "process_book_purchase"),
    path('process_printable_purchase/<int:product_id>/', views.process_printable_purchase, name = "process_printable_purchase"),
    path('process_music_purchase/<int:product_id>/', views.process_music_purchase, name = "process_music_purchase"),
    path('process_multimedia_purchase/<int:product_id>/', views.process_multimedia_purchase, name = "process_multimedia_purchase"),
    path('process_digitalArt_purchase/<int:product_id>/', views.process_digitalArt_purchase, name = "process_digitalArt_purchase"),
    path('process_CAD_purchase/<int:product_id>/', views.process_CAD_purchase, name = "process_CAD_purchase"),
    path('process_software_purchase/<int:product_id>/', views.process_software_purchase, name = "process_software_purchase"),
    path('process_business_purchase/<int:product_id>/', views.process_business_purchase, name = "process_business_purchase"),
    path('process_image_purchase/<int:product_id>/', views.process_image_purchase, name = "process_image_purchase"),
    
    path('paymentwebsitetemplate/<int:product_id>/', PaymentViewWebsitetemplate.as_view(), name='paymentwebsitetemplate'),
    path('paymentmobiletemplate/<int:product_id>/', PaymentViewMobiletemplate.as_view(), name='paymentmobiletemplate'),
    path('paymentdesktoptemplate/<int:product_id>/', PaymentViewDesktoptemplate.as_view(), name='paymentdesktoptemplate'),
    path('paymentmicrosofttemplate/<int:product_id>/', PaymentViewMicrosofttemplate.as_view(), name='paymentmicrosofttemplate'),
    path('paymentadobetemplate/<int:product_id>/', PaymentViewAdobetemplate.as_view(), name='paymentadobetemplate'),
    
    path('paymentwebsite/<int:course_id>/', PaymentViewWebsite.as_view(), name='paymentwebsite'),
    path('paymentmobile/<int:course_id>/', PaymentViewMobile.as_view(), name='paymentmobile'),
    path('paymentdesktop/<int:course_id>/', PaymentViewDesktop.as_view(), name='paymentdesktop'),
    path('paymentembeded/<int:course_id>/', PaymentViewEmbeded.as_view(), name='paymentembeded'),
    path('paymentgraphics/<int:course_id>/', PaymentViewGraphics.as_view(), name='paymentgraphics'),
    
    path('paymentproject/<int:product_id>/', PaymentViewProject.as_view(), name='paymentproject'),
    path('paymentimage/<int:product_id>/', PaymentViewImage.as_view(), name='paymentimage'),
    
    
    path('paymentbook/<int:product_id>/', PaymentViewBook.as_view(), name='paymentbook'),
    path('paymentprintable/<int:product_id>/', PaymentViewPrintable.as_view(), name='paymentprintable'),
    path('paymentmusic/<int:product_id>/', PaymentViewMusic.as_view(), name='paymentmusic'),
    path('paymentmultimedia/<int:product_id>/', PaymentViewMultimedia.as_view(), name='paymentmultimedia'),
    path('paymentdigitalArt/<int:product_id>/', PaymentViewDigitalArt.as_view(), name='paymentdigitalArt'),
    path('paymentCAD/<int:product_id>/', PaymentViewCAD.as_view(), name='paymentCAD'),
    path('paymentsoftware/<int:product_id>/', PaymentViewSoftware.as_view(), name='paymentsoftware'),
    path('paymentbusiness/<int:product_id>/', PaymentViewBusiness.as_view(), name='paymentbusiness'),
    
    # MY PRODUCT
    path('mybought/', PurchasedView.as_view(), name='mybought'),
    
    # WITHDRAW
    path('withdraw', views.withdraw, name = "withdraw"),
    path('mycard', views.mycard, name = "mycard"),
    path('master_withdraw', views.master_withdraw, name = "master_withdraw"),
    
    path('mypayment', views.mypayment, name = "mypayment"),
    path('masterpayment', views.masterpayment, name = "masterpayment"),
    path("viewmypayment/<int:id>/",views.viewmypayment,name = "viewmypayment"),
    path("viewmasterpayment/<int:id>/",views.viewmasterpayment,name = "viewmasterpayment"),
    path('update_status/<int:id>/<str:status>/', views.update_status, name='update_status'),
    path('update_master_status/<int:id>/<str:status>/', views.update_master_status, name='update_master_status'),
    
    path('allpayment', views.allpayment, name = "allpayment"),
    
    path('completed_transaction', views.completed_transaction, name = "completed_transaction"),
    path('pending_transaction', views.pending_transaction, name = "pending_transaction"),
    path('failed_transaction', views.failed_transaction, name = "failed_transaction"),
    path('my_transaction', views.my_transaction, name = "my_transaction"),
    
    path('allusers', views.allusers, name = "allusers"),
    path('staffusers', views.staffusers, name = "staffusers"),
    path('adminusers', views.adminusers, name = "adminusers"),
    
    path('useramount', views.useramount, name = "useramount"),
    
    path('help', views.help, name = "help"),
    path('terms_conditions', views.terms_conditions, name = "terms_conditions"),
    
    path('delete-viewed-notifications/', delete_viewed_notifications, name='delete_viewed_notifications'),
    
    #FOR SEACH
    path('search_all_product/', views.search_all_product, name='search_all_product'),
    
    # FOR SUBSCRIPTION
    path('subscription/', views.subscription, name='subscription'),
    path('successsubscription/', views.successsubscription, name='successsubscription'),
    
    # URL FOR SITEMAP
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

