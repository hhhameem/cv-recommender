from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
# Create your models here.

JOB_CATEGORY = (
    ('swe', 'Software Engineering'),
    ('wdd', 'Web Design & Development'),
    ('dsa', 'Data Science & Analytics'),
    ('gd', 'Graphic Design'),
    ('sqa', 'Software Quality Assurance'),
    ('nsa', 'Network & System Admin'),
    ('it', 'Information Technology'),
    ('cce', 'Cloud Computing & Engineering'),
    ('cc', 'Cyber Security'),
)

JOB_TYPE = (
    ('ft', 'Full Time'),
    ('pt', 'Part Time'),
    ('ip', 'Internship'),
    ('re', 'Remote'),
    ('ct', 'Contractual'),
)
CITY = (
    ('dhk', 'Dhaka'),
    ('ctg', 'Chittagong'),
    ('rjs', 'Rajshahi'),
    ('khl', 'Khulna'),
    ('bar', 'Barishal'),
    ('syl', 'Sylhet'),
    ('rng', 'Rangpur'),
)

STATUS = (
    ('publish', 'Publish'),
    ('hide', 'Hide'),
)

EDU = (
    ('postgraduate', 'Post Graduate'),
    ('graduate', 'Graduate'),
    ('hsc', 'HSC'),
    ('ssc', 'SSC'),
    ('noneed', 'Doesn\'t Matter'),
)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='publish')


class Job(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True,
                            help_text='You may keep it blank')
    company_name = models.CharField(max_length=200)
    starting_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    salary = models.PositiveIntegerField()
    vacancy = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)])
    job_category = models.CharField(max_length=3, choices=JOB_CATEGORY)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE)
    email = models.EmailField(max_length=254,)
    phone = models.CharField(max_length=11, blank=True, null=True)
    company_website = models.URLField()
    logo = models.ImageField(null=True, blank=True)
    address = models.TextField(max_length=200)
    division = models.CharField(max_length=4, choices=CITY)
    description = models.TextField()
    responsibility = models.TextField()
    min_education = models.CharField(max_length=12, choices=EDU)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    experience = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15)])
    skill_req = models.TextField(help_text='Input skills with comma')
    skill_bonus = models.CharField(
        max_length=255, blank=True, null=True, help_text='Input skills with comma')

    status = models.CharField(max_length=10, choices=STATUS)
    publish = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    recruiter = models.ForeignKey('account.Recruiter',
                                  on_delete=models.CASCADE,
                                  related_name='jobs')
    applicant = models.ManyToManyField('account.Applicant',
                                       related_name='jobs', blank=True)

    objects = models.Manager()         # default manager
    published = PublishedManager()    # custom manager for all published job post

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.title+'-'+self.company_name+'-'+str(self.deadline))
        super(Job, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('job_detail', args=[self.slug])
