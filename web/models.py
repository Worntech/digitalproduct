from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from django.utils.text import slugify

import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# user table--------------------------------------------------------------------
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        if not first_name:
            raise ValueError("Your First Name is required")
        if not last_name:
            raise ValueError("Your Last Name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, first_name, last_name, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

     

class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


def validate_file_size(value):
    limit = 1024 * 1024 * 1024  # 1024 MB in bytes
    if value.size > limit:
        raise ValidationError(f"The maximum file size allowed is 1024MB. Your file is {value.size / (1024 * 1024):.2f}MB.")
    
class Staff(models.Model):
    myrole = (
            ('CEO', 'CEO'),
			('Finance Officer', 'Finance Officer'),
			('Marketing Officer', 'Marketing Officer'),
            ('normal user', 'normal user'),
			)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    staff_role = models.CharField(max_length=200, null=True, choices=myrole)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    profile_picture = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional")
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

class Contact(models.Model):
    Full_Name = models.CharField(max_length=100, null=True)
    Subject = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=200, null=True)
    Phone = models.CharField(max_length=100, null=True)
    Message = models.TextField(null=True)  # Changed to TextField for longer messages
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Subscription(models.Model):
    email = models.EmailField(unique=True)  # Ensure each email is unique
    date_subscribed = models.DateTimeField(auto_now_add=True)  # Automatically set the date when subscribed

    def __str__(self):
        return self.email

# for the courses to be uploaded
class Website(models.Model):
    courses = (
            ('Frontend', 'Frontend'),
			('Backend', 'Backend'),
			('Fullstack', 'Fullstack'), 
			)
    part = (
            ('html and css', 'html and css'),
			('javascript', 'javascript'),
			('React js', 'React js'),
            ('Vue js', 'Vue js'),
			('Bootstrap', 'Bootstrap'),
			('Angular js', 'Angular js'),
            ('Django', 'Django'),
			('Flask', 'Flask'),
			('Php', 'Php'),
            ('Laravel', 'Laravel'),
			('Rub', 'Rub'),
			('Django, html and css', 'Django, html and css'),
            ('Flask, html and css', 'Flask, html and css'),
			('Django and react js', 'Django and react js'),
			('Php, html and css', 'Php, html and css'),
            ('Php and react js', 'Php and react js'),
			('Laravel, html and css', 'Laravel, html and css'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Course = models.CharField(max_length=200, null=True, choices=courses)
    Part = models.CharField(max_length=200, null=True, choices=part)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/")
    Video = models.FileField(upload_to="home/")
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Commentwebsite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Website', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.first_name
    
class Mobile(models.Model):
    courses = (
            ('Frontend', 'Frontend'),
			('Backend', 'Backend'),
			('Fullstack', 'Fullstack'),
			)
    part = (
            ('React native', 'React native'),
			('Kivy', 'Kivy'),
			('Fluter', 'Fluter'),
            ('React native and firebase', 'React native and firebase'),
            ('React native and django', 'React native and django'),
            ('React native and flask', 'React native and flask'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Course = models.CharField(max_length=200, null=True, choices=courses)
    Part = models.CharField(max_length=200, null=True, choices=part)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/")
    Video = models.FileField(upload_to="home/")
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Commentmobile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Mobile', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username


class Desktop(models.Model):
    courses = (
            ('C++', 'C++'),
			('Kivy', 'Kivy'),
			('Pyqt', 'Pyqt'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Course = models.CharField(max_length=200, null=True, choices=courses)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/")
    Video = models.FileField(upload_to="home/")
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Commentdesktop(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Desktop', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.Full_Name
    
    
class Embeded(models.Model):
    courses = (
            ('C++', 'C++'),
			('Arduino', 'Arduino'),
			('Python', 'Python'),
            ('Micropython', 'Micropython'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Course = models.CharField(max_length=200, null=True, choices=courses)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/")
    Video = models.FileField(upload_to="home/")
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Commentembeded(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Embeded', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.Full_Name
    
class Graphics(models.Model):
    courses = (
            ('Adobe photoshop', 'Adobe photoshop'),
			('Adobe illustrator', 'Adobe illustrator'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Course = models.CharField(max_length=200, null=True, choices=courses)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/")
    Video = models.FileField(upload_to="home/")
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
class Commentgraphics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Graphics', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.Full_Name
    
    
# models for project

class Project(models.Model):
    type = (
            ('website', 'website'),
			('mobile', 'mobile'),
            ('desktop', 'desktop'),
			('artificial', 'artificial'),
            ('embeded', 'embeded'),
			('iot', 'iot'),
            ('virtual reality', 'virtual reality'),
			('cyber', 'cyber'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Explanation = models.CharField(max_length=500)
    Type = models.CharField(max_length=200, null=True, choices=type)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Project = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
      
class Commentproject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Project', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.Full_Name

# MODEL FOR IMAGE
class Image(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Image_download = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Commentimage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Image', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.Full_Name
    
class Book(models.Model):
    category = (
            ('Novels', 'Novels'),
            ('Short stories', 'Short stories'),
            ('Poetry', 'Poetry'),
            ('Flash fiction', 'Flash fiction'),
            ('Self help', 'Self help'),
            ('Biographies & Memoirs', 'Biographies & Memoirs'),
            ('Personal development', 'Personal development'),
            ('History', 'History'),
            ('True crime', 'True crime'),
            ('Textbooks', 'Textbooks'),
            ('Research papers & white papers', 'Research papers & white papers'),
            ('Study guides', 'Study guides'),
            ('How-to guides & tutorials', 'How-to guides & tutorials'),
            ('Business strategy guides', 'Business strategy guides'),
            ('Marketing and sales e-books', 'Marketing and sales e-books'),
            ('Entrepreneurship guides', 'Entrepreneurship guides'),
            ('Financial planning', 'Financial planning'),
            ('Nutrition guides', 'Nutrition guides'),
            ('Workout and fitness plans', 'Workout and fitness plans'),
            ('Mental health & wellness', 'Mental health & wellness'),
            ('Meditation and mindfulness e-books', 'Meditation and mindfulness e-books'),
            ('Coding and programming tutorials', 'Coding and programming tutorials'),
            ('Software manuals', 'Software manuals'),
            ('IT and networking guides', 'IT and networking guides'),
            ('Artificial intelligence & machine learning', 'Artificial intelligence & machine learning'),
            ('Photography tutorials', 'Photography tutorials'),
            ('Painting and drawing guides', 'Painting and drawing guides'),
            ('Writing and storytelling techniques', 'Writing and storytelling techniques'),
            ('Crafting & DIY projects', 'Crafting & DIY projects'),
            ('Recipe collections', 'Recipe collections'),
            ('Specialized diet guides', 'Specialized diet guides'),
            ('Meal planning and prep', 'Meal planning and prep'),
            ('Parenting advice', 'Parenting advice'),
            ('Marriage and relationship counseling', 'Marriage and relationship counseling'),
            ('Family planning guides', 'Family planning guides'),
            ('Childcare and development', 'Childcare and development'),
            ('Travel guides', 'Travel guides'),
            ('Destination reviews', 'Destination reviews'),
            ('Adventure stories', 'Adventure stories'),
            ('Travel planning and budgeting', 'Travel planning and budgeting'),
            ('Personal finance e-books', 'Personal finance e-books'),
            ('Investment strategies', 'Investment strategies'),
            ('Retirement planning', 'Retirement planning'),
            ('Budgeting tips', 'Budgeting tips'),
            ('Meditation and mindfulness books', 'Meditation and mindfulness books'),
            ('Philosophy and life purpose e-books', 'Philosophy and life purpose e-books'),
            ('Time management and productivity', 'Time management and productivity'),
            ('Self-improvement and motivation', 'Self-improvement and motivation'),
            ('Life coaching guides', 'Life coaching guides'),
            ('Work-life balance', 'Work-life balance'),
            ('Legal guides and contracts', 'Legal guides and contracts'),
            ('HR and employment handbooks', 'HR and employment handbooks'),
            ('Professional development', 'Professional development'),
            ('Real estate investment guides', 'Real estate investment guides'),
            ('Property management manuals', 'Property management manuals'),
            ('Buying and selling homes', 'Buying and selling homes'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Book = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Commentbook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Book', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
 
class Printable(models.Model):
    category = (
            ('Invitations and greeting cards templates', 'Invitations and greeting cards templates'),
            ('Business cards template', 'Business cards template'),
            ('Wedding templates', 'Wedding templates'),
            ('Digital planners', 'Digital planners'),
            ('SEO tools', 'SEO tools'),
            ('Email marketing templates', 'Email marketing templates'),
            ('Website themes', 'Website themes'),
            ('Custom scripts', 'Custom scripts'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewPrintable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Printable', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Commentprintable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Printable', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    
class Music(models.Model):
    category = (
            ('Single tracks', 'Single tracks'),
            ('Full albums', 'Full albums'),
            ('EPs (Extended Plays)', 'EPs (Extended Plays)'),
            ('Instrumental versions', 'Instrumental versions'),
            ('Beats for rappers and singers', 'Beats for rappers and singers'),
            ('Lo-fi beats', 'Lo-fi beats'),
            ('Background instrumentals for videos', 'Background instrumentals for videos'),
            ('Royalty-free music', 'Royalty-free music'),
            ('Environmental sounds', 'Environmental sounds'),
            ('Foley sounds', 'Foley sounds'),
            ('Sci-fi and futuristic sounds', 'Sci-fi and futuristic sounds'),
            ('Horror and thriller effects', 'Horror and thriller effects'),
            ('Drum loops', 'Drum loops'),
            ('Melodic loops', 'Melodic loops'),
            ('Vocal samples', 'Vocal samples'),
            ('Synth and bass loops', 'Synth and bass loops'),
            ('Background music for videos', 'Background music for videos'),
            ('Music for podcasts', 'Music for podcasts'),
            ('Royalty-free soundtracks for commercials', 'Royalty-free soundtracks for commercials'),
            ('Ambient music for relaxation and meditation', 'Ambient music for relaxation and meditation'),
            ('Talk shows', 'Talk shows'),
            ('Interview series', 'Interview series'),
            ('Educational podcasts', 'Educational podcasts'),
            ('Storytelling and fictional audio series', 'Storytelling and fictional audio series'),
            ('Nature-inspired soundscapes', 'Nature-inspired soundscapes'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Audio = models.FileField(upload_to="home/", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewMusic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Music', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Commentmusic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Music', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    
class Multimedia(models.Model):
    category = (
            ('Nature and landscape footage', 'Nature and landscape footage'),
            ('Urban and city life footage', 'Urban and city life footage'),
            ('Aerial drone videos', 'Aerial drone videos'),
            ('Slow-motion and time-lapse videos', 'Slow-motion and time-lapse videos'),
            ('After Effects templates', 'After Effects templates'),
            ('Premiere Pro templates', 'Premiere Pro templates'),
            ('Intros and outros for YouTube videos', 'Intros and outros for YouTube videos'),
            ('2D animations', '2D animations'),
            ('3D animations', '3D animations'),
            ('Explainer videos', 'Explainer videos'),
            ('Motion graphics for commercials', 'Motion graphics for commercials'),
            ('Personal vlogs', 'Personal vlogs'),
            ('Travel videos', 'Travel videos'),
            ('Lifestyle vlogs', 'Lifestyle vlogs'),
            ('Daily video blogs', 'Daily video blogs'),
            ('Wedding videos', 'Wedding videos'),
            ('Corporate event videos', 'Corporate event videos'),
            ('Party and celebration videos', 'Party and celebration videos'),
            ('Award ceremony Video', 'Award ceremony Video'),
            ('Business presentations', 'Business presentations'),
            ('Sales pitches', 'Sales pitches'),
            ('Educational or academic presentations', 'Educational or academic presentations'),
            ('Product promo videos', 'Product promo videos'),
            ('Service advertisement videos', 'Service advertisement videos'),
            ('Brand story videos', 'Brand story videos'),
            ('Social media ads', 'Social media ads'),
            ('Official music videos', 'Official music videos'),
            ('Lyric videos', 'Lyric videos'),
            ('Animated music videos', 'Animated music videos'),
            ('Performance videos', 'Performance videos'),
            ('Fiction short films', 'Fiction short films'),
            ('Mini-documentaries', 'Mini-documentaries'),
            ('Biographical documentaries', 'Biographical documentaries'),
            ('Indie films', 'Indie films'),
            ('adventure videos', 'adventure videos'),
            ('Interactive tutorials', 'Interactive tutorials'),
            ('Interactive quizzes or assessments', 'Interactive quizzes or assessments'),
            ('Gamified videos', 'Gamified videos'),
            ('Customer testimonial videos', 'Customer testimonial videos'),
            ('Product review videos', 'Product review videos'),
            ('User-generated content videos', 'User-generated content videos'),
            ('Virtual reality experiences', 'Virtual reality experiences'),
            ('360-degree video tours', '360-degree video tours'),
            ('Immersive event videos', 'Immersive event videos'),
            ('Cinematic sequences', 'Cinematic sequences'),
            ('Aerial drone footage', 'Aerial drone footage'),
            ('Scenic landscape shots', 'Scenic landscape shots'),
            ('Epic slow-motion videos', 'Epic slow-motion videos'),
            ('Urban timelapse videos', 'Urban timelapse videos'),
            ('Nature and sky timelapse', 'Nature and sky timelapse'),
            ('Construction progress timelapse', 'Construction progress timelapse'),
            ('Yoga and meditation videos', 'Yoga and meditation videos'),
            ('Healthy lifestyle tips', 'Healthy lifestyle tips'),
            ('Exercise and wellness programs', 'Exercise and wellness programs'),
            ('Product feature demonstrations', 'Product feature demonstrations'),
            ('Physical product unboxing and reviews', 'Physical product unboxing and reviews'),
            ('Animated YouTube intros', 'Animated YouTube intros'),
            ('Branding outros for videos', 'Branding outros for videos'),
            ('Social media content intros', 'Social media content intros'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewMultimedia(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Multimedia', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Commentmultimedia(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Multimedia', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    
class DigitalArt(models.Model):
    category = (
            ('Hand-drawn digital illustrations', 'Hand-drawn digital illustrations'),
            ('Character design', 'Character design'),
            ('Website design templates', 'Website design templates'),
            ('Mobile app design templates', 'Mobile app design templates'),
            ('Editorial illustrations', 'Editorial illustrations'),
            ('Children’s book illustrations', 'Children’s book illustrations'),
            ('Posters', 'Posters'),
            ('Flyers', 'Flyers'),
            ('Brochures', 'Brochures'),
            ('Infographics', 'Infographics'),
            ('Digital advertisements', 'Digital advertisements'),
            ('Brand logos', 'Brand logos'),
            ('Icon sets', 'Icon sets'),
            ('Custom logos for businesses', 'Custom logos for businesses'),
            ('Monograms', 'Monograms'),
            ('Scalable vector illustrations', 'Scalable vector illustrations'),
            ('Flat design elements', 'Flat design elements'),
            ('Icons and symbols', 'Icons and symbols'),
            ('Geometric patterns', 'Geometric patterns'),
            ('3D models', '3D models'),
            ('Architectural renderings', 'Architectural renderings'),
            ('3D character design', '3D character design'),
            ('Product visualizations', 'Product visualizations'),
            ('Custom fonts', 'Custom fonts'),
            ('Hand-lettering designs', 'Hand-lettering designs'),
            ('Calligraphy artwork', 'Calligraphy artwork'),
            ('Display typefaces', 'Display typefaces'),
            ('Wireframe kits', 'Wireframe kits'),
            ('Prototype designs', 'Prototype designs'),
            ('Interactive mockups', 'Interactive mockups'),
            ('Business cards', 'Business cards'),
            ('Wedding invitations', 'Wedding invitations'),
            ('Greeting cards', 'Greeting cards'),
            ('Calendars', 'Calendars'),
            ('Planners', 'Planners'),
            ('Seamless patterns', 'Seamless patterns'),
            ('Textile and fabric patterns', 'Textile and fabric patterns'),
            ('Wallpaper designs', 'Wallpaper designs'),
            ('Packaging patterns', 'Packaging patterns'),
            ('UI/UX icons', 'UI/UX icons'),
            ('App icons', 'App icons'),
            ('Social media icons', 'Social media icons'),
            ('Custom icon sets for websites', 'Custom icon sets for websites'),
            ('Realistic portrait paintings', 'Realistic portrait paintings'),
            ('Fantasy landscape paintings', 'Fantasy landscape paintings'),
            ('Concept art for games or films', 'Concept art for games or films'),
            ('Abstract digital artwork', 'Abstract digital artwork'),
            ('Composite photo art', 'Composite photo art'),
            ('Surreal photo manipulations', 'Surreal photo manipulations'),
            ('Product photo retouching', 'Product photo retouching'),
            ('Fashion and beauty retouching', 'Fashion and beauty retouching'),
            ('Digital collages', 'Digital collages'),
            ('Mixed media art', 'Mixed media art'),
            ('Scrapbook designs', 'Scrapbook designs'),
            ('Character concept art', 'Character concept art'),
            ('Creature and monster designs', 'Creature and monster designs'),
            ('Storyboard art', 'Storyboard art'),
            ('Comic book illustrations', 'Comic book illustrations'),
            ('Manga-style characters and story panels', 'Manga-style characters and story panels'),
            ('Digital comic strips', 'Digital comic strips'),
            ('T-shirt graphics and mockups', 'T-shirt graphics and mockups'),
            ('Custom merchandise designs', 'Custom merchandise designs'),
            ('Apparel patterns and prints', 'Apparel patterns and prints'),
            ('Themed photo collections', 'Themed photo collections'),
            ('High-resolution stock images', 'High-resolution stock images'),
            ('Conceptual photography', 'Conceptual photography'),
            ('Art prints for home decor', 'Art prints for home decor'),
            ('Motivational posters', 'Motivational posters'),
            ('Abstract and minimalist art', 'Abstract and minimalist art'),
            ('Instagram post templates', 'Instagram post templates'),
            ('Facebook banner designs', 'Facebook banner designs'),
            ('Pinterest graphic templates', 'Pinterest graphic templates'),
            ('Story highlight icons', 'Story highlight icons'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewDigitalArt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('DigitalArt', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class CommentdigitalArt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('DigitalArt', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    

class CAD(models.Model):
    category = (
            ('Character models', 'Character models'),
            ('Vehicle models', 'Vehicle models'),
            ('Furniture and home decor models', 'Furniture and home decor models'),
            ('Product prototypes', 'Product prototypes'),
            ('House and building designs', 'House and building designs'),
            ('Interior and exterior architectural models', 'Interior and exterior architectural models'),
            ('Floor plans and layouts', 'Floor plans and layouts'),
            ('Urban planning models', 'Urban planning models'),
            ('Architectural renderings', 'Architectural renderings'),
            ('Toys and figurines', 'Toys and figurines'),
            ('Custom jewelry designs', 'Custom jewelry designs'),
            ('Gadgets and accessories', 'Gadgets and accessories'),
            ('Home decor and functional objects', 'Home decor and functional objects'),
            ('Mechanical part designs', 'Mechanical part designs'),
            ('Industrial equipment models', 'Industrial equipment models'),
            ('Engineering diagrams', 'Engineering diagrams'),
            ('CNC and laser cutting templates', 'CNC and laser cutting templates'),
            ('Modern and classic furniture models', 'Modern and classic furniture models'),
            ('Kitchen and bathroom designs', 'Kitchen and bathroom designs'),
            ('Custom cabinetry and shelving units', 'Custom cabinetry and shelving units'),
            ('3D room and space layouts', '3D room and space layouts'),
            ('Consumer electronics prototypes', 'Consumer electronics prototypes'),
            ('Fashion and accessory designs', 'Fashion and accessory designs'),
            ('Home appliance prototypes', 'Home appliance prototypes'),
            ('Wearable technology prototypes', 'Wearable technology prototypes'),
            ('3D characters and creatures', '3D characters and creatures'),
            ('Environmental models', 'Environmental models'),
            ('Weapons and gear', 'Weapons and gear'),
            ('Vehicle models for gaming', 'Vehicle models for gaming'),
            ('Anatomy and body part models', 'Anatomy and body part models'),
            ('Molecular and chemical models', 'Molecular and chemical models'),
            ('Medical equipment and device designs', 'Medical equipment and device designs'),
            ('Scientific visualization models', 'Scientific visualization models'),
            ('Car and truck models', 'Car and truck models'),
            ('Aircraft and drone designs', 'Aircraft and drone designs'),
            ('Ship and boat models', 'Ship and boat models'),
            ('Public transportation models', 'Public transportation models'),
            ('Ring and earring designs', 'Ring and earring designs'),
            ('Pendant and necklace models', 'Pendant and necklace models'),
            ('Custom and personalized jewelry designs', 'Custom and personalized jewelry designs'),
            ('3D printable jewelry prototypes', '3D printable jewelry prototypes'),
            ('VR-ready 3D models for virtual environments', 'VR-ready 3D models for virtual environments'),
            ('AR models for apps and interactive experiences', 'AR models for apps and interactive experiences'),
            ('Architectural walkthroughs for VR', 'Architectural walkthroughs for VR'),
            ('Heavy machinery models', 'Heavy machinery models'),
            ('Industrial equipment', 'Industrial equipment'),
            ('Mechanical components and assemblies', 'Mechanical components and assemblies'),
            ('Fantasy and sci-fi character models', 'Fantasy and sci-fi character models'),
            ('Cartoon and stylized characters', 'Cartoon and stylized characters'),
            ('Monster and creature models for games and films', 'Monster and creature models for games and films'),
            ('A3D clothing and accessory models', 'A3D clothing and accessory models'),
            ('Fashion prototypes for manufacturing', 'Fashion prototypes for manufacturing'),
            ('Shoe and bag designs', 'Shoe and bag designs'),
            ('Fully rigged 3D characters for animation', 'Fully rigged 3D characters for animation'),
            ('Motion capture-ready models', 'Motion capture-ready models'),
            ('Custom rigging setups for specific software', 'Custom rigging setups for specific software'),
            ('Natural landscapes', 'Natural landscapes'),
            ('City and urban environments', 'City and urban environments'),
            ('Virtual environments for games and simulations', 'Virtual environments for games and simulations'),
            ('Engine models', 'Engine models'),
            ('Gear and mechanical component designs', 'Gear and mechanical component designs'),
            ('CAD files for mechanical systems', 'CAD files for mechanical systems'),
            ('DIY assembly instructions for furniture', 'DIY assembly instructions for furniture'),
            ('Custom furniture designs with CAD plans', 'Custom furniture designs with CAD plans'),
            ('CNC-cut plans for modular furniture', 'CNC-cut plans for modular furniture'),
            ('3D models of props for film sets', '3D models of props for film sets'),
            ('Sci-fi or fantasy set designs', 'Sci-fi or fantasy set designs'),
            ('Historical prop replicas', 'Historical prop replicas'),
            ('Robot design and assembly plans', 'Robot design and assembly plans'),
            ('Drone and UAV designs', 'Drone and UAV designs'),
            ('Industrial automation models', 'Industrial automation models'),
            ('A3D clothing and accessory models', 'A3D clothing and accessory models'),
            ('3D floor plans', '3D floor plans'),
            ('Interior and exterior visualization', 'Interior and exterior visualization'),
            ('3D topographical maps', '3D topographical maps'),
            ('Terrain models for games and simulations', 'Terrain models for games and simulations'),
            ('Landscape elevation models', 'Landscape elevation models'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewCAD(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('CAD', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class CommentCAD(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('CAD', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    
class Software(models.Model):
    category = (
            ('Software applications', 'Software applications'),
            ('Plugins and extensions', 'Plugins and extensions'),
            ('Architectural plans', 'Architectural plans'),
            ('Mobile apps', 'Mobile apps'),
            ('SaaS products (Software as a Service)', 'SaaS products (Software as a Service)'),
            ('Copywriting templates', 'Copywriting templates'),
            
            # not worked on
            ('Website themes', 'Website themes'),
            ('Custom scripts', 'Custom scripts'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewSoftware(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Software', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
      
class Commentsoftware(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Software', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    
class Business(models.Model):
    category = (
            ('Business templates', 'Business templates'),
            ('Marketing materials', 'Marketing materials'),
            ('Analytics tools', 'Analytics tools'),
            ('CRM templates', 'CRM templates'),
            
            # not worked on
            ('SEO tools', 'SEO tools'),
            ('Email marketing templates', 'Email marketing templates'),
            ('Website themes', 'Website themes'),
            ('Custom scripts', 'Custom scripts'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Category = models.CharField(max_length=200, null=True, choices=category)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Product = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ReviewBusiness(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Commentbusiness(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Title = models.ForeignKey('Business', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username

# for the template to upload
class Websitetemplate(models.Model):
    template = (
            ('Html and css', 'Html and css'),
			('React js', 'React js'),
			('Vue Js', 'Vue Js'),
            ('Elm', 'Elm'),
            ('Swift', 'Swift'),
			('JQuery', 'JQuery'),
            ('Flutter', 'Flutter'),
            ('Svelte', 'Svelte'),
			('Materialize CSS', 'Materialize CSS'),
            ('Foundation', 'Foundation'),
            ('Angular', 'Angular'),
            ('Tailwind CSS', 'Tailwind CSS'),
            ('Bootstrap', 'Bootstrap'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Type = models.CharField(max_length=200, null=True, choices=template)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Template = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    # Optional preview field
    preview = models.URLField(max_length=200, blank=True, null=True, help_text="Optional link to preview the template")
    
    def get_model_name(self):
        return 'Websitetemplate'


    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique template_id based on the Title
            self.template_id = slugify(self.Title)[:20]  # Limit to first 20 characters to fit max_length
        super().save(*args, **kwargs)

class ReviewWebsitetemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Websitetemplate', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)

class Mobiletemplate(models.Model):
    template = (
			('React native', 'React native'),
            ('Flutter', 'Flutter'),
            ('SwiftUI', 'SwiftUI'),
            ('Jetpack Compose', 'Jetpack Compose'),
            ('Ionic Framework', 'Ionic Framework'),
            ('Xamarin', 'Xamarin'),
            ('PhoneGap (Apache Cordova)', 'PhoneGap (Apache Cordova)'),
            ('NativeScript', 'NativeScript'),
            ('Framework7', 'Framework7'),
            ('Onsen UI', 'Onsen UI'),
            ('jQuery Mobile', 'jQuery Mobile'),
            ('Sencha Touch', 'Sencha Touch'),
            ('Kivy', 'Kivy'),
            ('Bootstrap Mobile Templates', 'Bootstrap Mobile Templates'),
            ('Quasar Framework', 'Quasar Framework'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Type  = models.CharField(max_length=200, null=True, choices=template)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Template = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique mobiletemplate_id based on the Title
            self.mobiletemplate_id = slugify(self.Title)[:20]  # Limit to first 20 characters to fit max_length
        super().save(*args, **kwargs)


class ReviewMobiletemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Mobiletemplate', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Desktoptemplate(models.Model):
    template = (
            ('Kivy', 'Kivy'),
			('Pyqt', 'Pyqt'),
            ('Tkinter', 'Tkinter'),
			('C++', 'C++'),
            ('C#', 'C#'),
			('Java', 'Java'),
            ('Electron (JavaScript, HTML, CSS)', 'Electron (JavaScript, HTML, CSS)'),
			('Swift', 'Swift'),
            ('Rust', 'Rust'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Type  = models.CharField(max_length=200, null=True, choices=template)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Template = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique template_id based on the Title
            self.template_id = slugify(self.Title)[:20]  # Limit to first 20 characters to fit max_length
        super().save(*args, **kwargs)

class ReviewDesktoptemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Desktoptemplate', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Microsofttemplate(models.Model):
    template = (
            ('word', 'word'),
			('powerpoint', 'powerpoint'),
            ('excell', 'excell'),
			('publisher', 'publisher'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Type  = models.CharField(max_length=200, null=True, choices=template)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Template = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique template_id based on the Title
            self.template_id = slugify(self.Title)[:20]  # Limit to first 20 characters to fit max_length
        super().save(*args, **kwargs)

class ReviewMicrosofttemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Microsofttemplate', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
    
class Adobetemplate(models.Model):
    template = (
            ('Adobe Photoshop', 'Adobe Photoshop'),
			('Adobe Primier Pro', 'Adobe Primier Pro'),
            ('Adobe Illustrator', 'Adobe Illustrator'),
            ('Adobe InDesign', 'Adobe InDesign'),
			('Adobe XD', 'Adobe XD'),
            ('Adobe Lightroom', 'Adobe Lightroom'),
            ('Adobe Lightroom Classic', 'Adobe Lightroom Classic'),
			('Adobe After Effects', 'Adobe After Effects'),
            ('Adobe Animate', 'Adobe Animate'),
            ('Adobe Dreamweaver', 'Adobe Dreamweaver'),
			('Adobe Audition', 'Adobe Audition'),
            ('Adobe Bridge', 'Adobe Bridge'),
            ('Adobe Dimension', 'Adobe Dimension'),
			('Adobe Fresco', 'Adobe Fresco'),
            ('Adobe Character Animator', 'Adobe Character Animator'),
            ('Adobe Media Encoder', 'Adobe Media Encoder'),
			('Adobe Rush', 'Adobe Rush'),
            ('Adobe Spark', 'Adobe Spark'),
            ('Adobe Substance 3D Painter', 'Adobe Substance 3D Painter'),
			('Adobe Substance 3D Designer', 'Adobe Substance 3D Designer'),
            ('Adobe Substance 3D Sampler', 'Adobe Substance 3D Sampler'),
            ('Adobe Substance 3D Stager', 'Adobe Substance 3D Stager'),
			('Adobe Acrobat Pro DC', 'Adobe Acrobat Pro DC'),
            ('Adobe Sign', 'Adobe Sign'),
            ('Adobe FrameMaker', 'Adobe FrameMaker'),
            ('Marketo Engage', 'Marketo Engage'),
			('Adobe Presenter', 'Adobe Presenter'),
			)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=700)
    Type  = models.CharField(max_length=200, null=True, choices=template)
    Explanation = models.CharField(max_length=500)
    Image =models.ImageField(upload_to="home/", validators=[validate_file_size])
    Preview_Video = models.FileField(upload_to="home/", blank=True, null=True, help_text="Optional", validators=[validate_file_size])
    Template = models.FileField(upload_to="home/", validators=[validate_file_size])
    amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique template_id based on the Title
            self.template_id = slugify(self.Title)[:20]  # Limit to first 20 characters to fit max_length
        super().save(*args, **kwargs)
    
class ReviewAdobetemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey('Adobetemplate', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rate between 1 (worst) and 5 (best)"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')  # Prevent duplicate reviews
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star Review of {self.template.Title}"

    def get_stars(self):
        """Returns the rating in stars format."""
        return "★" * self.rating + "☆" * (5 - self.rating)
     
# FOR TEMPLATE PAYMENT MODELS
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    template = models.ForeignKey(Websitetemplate, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentMobiletemplate(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    mobiletemplate = models.ForeignKey(Mobiletemplate, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentDesktoptemplate(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    desktoptemplate = models.ForeignKey(Desktoptemplate, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)


class PaymentMicrosofttemplate(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    microsofttemplate = models.ForeignKey(Microsofttemplate, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentAdobetemplate(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    adobetemplate = models.ForeignKey(Adobetemplate, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
# FOR COURSES PAYMENT MODELS
class PaymentWebsite(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentMobile(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentDesktop(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    desktop = models.ForeignKey(Desktop, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentEmbeded(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    embeded = models.ForeignKey(Embeded, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentGraphics(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    graphics = models.ForeignKey(Graphics, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        

# PROJECT PAYMENT
class PaymentProject(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentBook(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentPrintable(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Printable, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentMusic(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Music, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentMultimedia(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Multimedia, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentDigitalArt(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(DigitalArt, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentCAD(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(CAD, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
                
class PaymentSoftware(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Software, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class PaymentBusiness(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)


# IMAGE PAYMENT
class PaymentImage(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
    
    # MY AMOUNT
class Myamount(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    My_amount = models.DecimalField(max_digits=10, decimal_places=2)
    Reducted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    Withdrawed_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # WITHDRAW
class Withdraw(models.Model):
    status = (
        ('Completed', 'Completed'),
        ('Processing', 'Processing'),
        ('Declined', 'Declined'),
    )
    country = (
        ('Abkhazia and South Ossetia', 'Abkhazia and South Ossetia'),
        ('Afghanistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Antigua and Barbuda', 'Antigua and Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo (Congo-Brazzaville)', 'Congo (Congo-Brazzaville)'),
        ('Costa Rica', 'Costa Rica'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic (Czechia)', 'Czech Republic (Czechia)'),
        ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor (Timor-Leste)', 'East Timor (Timor-Leste)'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Eswatini (Swaziland)', 'Eswatini (Swaziland)'),
        ('Ethiopia', 'Ethiopia'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Greece', 'Greece'),
        ('Grenada', 'Grenada'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Honduras', 'Honduras'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea, North', 'Korea, North'),
        ('Korea, South', 'Korea, South'),
        ('Kosovo', 'Kosovo'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Malaysia', 'Malaysia'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mexico', 'Mexico'),
        ('Micronesia', 'Micronesia'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montenegro', 'Montenegro'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar (Burma)', 'Myanmar (Burma)'),
        ('Namibia', 'Namibia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherlands', 'Netherlands'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('North Macedonia', 'North Macedonia'),
        ('Northern Cyprus', 'Northern Cyprus'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau', 'Palau'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Palestine ', 'Palestine '),
        ('Peru', 'Peru'),
        ('Philippines', 'Philippines'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Qatar', 'Qatar'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
        ('Saint Lucia', 'Saint Lucia'),
        ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
        ('Samoa', 'Samoa'),
        ('San Marino', 'San Marino'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Serbia', 'Serbia'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('South Sudan', 'South Sudan'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tonga', 'Tonga'),
        ('Transnistria ', 'Transnistria '),
        ('Trinidad and Tobago', 'Trinidad and Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('United Kingdom', 'United Kingdom'),
        ('United States', 'United States'),
        ('Uruguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City', 'Vatican City'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Western Sahara', 'Western Sahara'),
        ('Yemen', 'Yemen'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, choices=status, default='Processing')
    Card_Number = models.CharField(max_length=500)
    First_Name = models.CharField(max_length=500)
    Last_Name = models.CharField(max_length=500)
    Card_Name = models.CharField(max_length=500)
    Amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    Phone_Number = models.CharField(max_length=500)
    Email = models.CharField(max_length=500)
    Country = models.CharField(max_length=50, choices=country)
    Card_Type = models.CharField(max_length=500)
    Withdraw_date = models.DateTimeField(auto_now_add=True)
    
    # WITHDRAW
class MasterWithdraw(models.Model):
    status = (
        ('Completed', 'Completed'),
        ('Processing', 'Processing'),
        ('Declined', 'Declined'),
    )
    country = (
        ('Abkhazia and South Ossetia', 'Abkhazia and South Ossetia'),
        ('Afghanistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Antigua and Barbuda', 'Antigua and Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo (Congo-Brazzaville)', 'Congo (Congo-Brazzaville)'),
        ('Costa Rica', 'Costa Rica'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic (Czechia)', 'Czech Republic (Czechia)'),
        ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor (Timor-Leste)', 'East Timor (Timor-Leste)'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Eswatini (Swaziland)', 'Eswatini (Swaziland)'),
        ('Ethiopia', 'Ethiopia'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Greece', 'Greece'),
        ('Grenada', 'Grenada'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Honduras', 'Honduras'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea, North', 'Korea, North'),
        ('Korea, South', 'Korea, South'),
        ('Kosovo', 'Kosovo'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Malaysia', 'Malaysia'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mexico', 'Mexico'),
        ('Micronesia', 'Micronesia'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montenegro', 'Montenegro'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar (Burma)', 'Myanmar (Burma)'),
        ('Namibia', 'Namibia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherlands', 'Netherlands'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('North Macedonia', 'North Macedonia'),
        ('Northern Cyprus', 'Northern Cyprus'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau', 'Palau'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Palestine ', 'Palestine '),
        ('Peru', 'Peru'),
        ('Philippines', 'Philippines'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Qatar', 'Qatar'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
        ('Saint Lucia', 'Saint Lucia'),
        ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
        ('Samoa', 'Samoa'),
        ('San Marino', 'San Marino'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Serbia', 'Serbia'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('South Sudan', 'South Sudan'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tonga', 'Tonga'),
        ('Transnistria ', 'Transnistria '),
        ('Trinidad and Tobago', 'Trinidad and Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('United Kingdom', 'United Kingdom'),
        ('United States', 'United States'),
        ('Uruguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City', 'Vatican City'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Western Sahara', 'Western Sahara'),
        ('Yemen', 'Yemen'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, choices=status, default='Processing')
    Card_Number = models.CharField(max_length=500)
    Card_Name = models.CharField(max_length=500)
    Amount_in_USD = models.DecimalField(max_digits=10, decimal_places=2)
    Phone_Number = models.CharField(max_length=500)
    Email = models.CharField(max_length=500)
    Country = models.CharField(max_length=50, choices=country)
    Card_Type = models.CharField(max_length=500)
    Withdraw_date = models.DateTimeField(auto_now_add=True)
    
class Card(models.Model):
    cardtype = (
        ('Visa', 'Visa'),
        ('MasterCard', 'MasterCard'),
    )
    country = (
        ('Abkhazia and South Ossetia', 'Abkhazia and South Ossetia'),
        ('Afghanistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Antigua and Barbuda', 'Antigua and Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo (Congo-Brazzaville)', 'Congo (Congo-Brazzaville)'),
        ('Costa Rica', 'Costa Rica'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic (Czechia)', 'Czech Republic (Czechia)'),
        ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor (Timor-Leste)', 'East Timor (Timor-Leste)'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Eswatini (Swaziland)', 'Eswatini (Swaziland)'),
        ('Ethiopia', 'Ethiopia'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Greece', 'Greece'),
        ('Grenada', 'Grenada'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Honduras', 'Honduras'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea, North', 'Korea, North'),
        ('Korea, South', 'Korea, South'),
        ('Kosovo', 'Kosovo'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Malaysia', 'Malaysia'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mexico', 'Mexico'),
        ('Micronesia', 'Micronesia'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montenegro', 'Montenegro'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar (Burma)', 'Myanmar (Burma)'),
        ('Namibia', 'Namibia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherlands', 'Netherlands'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('North Macedonia', 'North Macedonia'),
        ('Northern Cyprus', 'Northern Cyprus'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau', 'Palau'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Palestine ', 'Palestine '),
        ('Peru', 'Peru'),
        ('Philippines', 'Philippines'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Qatar', 'Qatar'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
        ('Saint Lucia', 'Saint Lucia'),
        ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
        ('Samoa', 'Samoa'),
        ('San Marino', 'San Marino'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Serbia', 'Serbia'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('South Sudan', 'South Sudan'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tonga', 'Tonga'),
        ('Transnistria ', 'Transnistria '),
        ('Trinidad and Tobago', 'Trinidad and Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('United Kingdom', 'United Kingdom'),
        ('United States', 'United States'),
        ('Uruguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City', 'Vatican City'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Western Sahara', 'Western Sahara'),
        ('Yemen', 'Yemen'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Card_Type = models.CharField(max_length=10, choices=cardtype)
    Card_Number = models.CharField(max_length=500)
    Card_Name = models.CharField(max_length=500)
    First_Name = models.CharField(max_length=500)
    Last_Name = models.CharField(max_length=500)
    Phone_Number = models.CharField(max_length=500)
    Email = models.CharField(max_length=500)
    Country = models.CharField(max_length=50, choices=country)
    added_date = models.DateTimeField(auto_now_add=True)
    
    # MY MASTER AMOUNT
class MasterAmount(models.Model):
    My_amount = models.DecimalField(max_digits=10, decimal_places=2)
    Gateway_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    Withdrawed_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        super().save(*args, **kwargs)
        
class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Assuming the user is from the auth.User model
    message = models.CharField(max_length=5000)
    status = models.CharField(max_length=1000)  # e.g., Completed, Processing, Declined
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)  # To track if the user has viewed the notification

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    

