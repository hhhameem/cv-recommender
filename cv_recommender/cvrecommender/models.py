from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
# Create your models here.

JOB_CATEGORY = (
    ('Software Engineering', 'Software Engineering'),
    ('Web Design and Development', 'Web Design & Development'),
    ('Data Science and Analytics', 'Data Science & Analytics'),
    ('Graphic Design', 'Graphic Design'),
    ('Software Quality Assurance', 'Software Quality Assurance'),
    ('Network and System Admin', 'Network & System Admin'),
    ('Information Technology', 'Information Technology'),
    ('Cloud Computing and Engineering', 'Cloud Computing & Engineering'),
    ('Cyber Security', 'Cyber Security'),
)

JOB_TYPE = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
    ('Contractual', 'Contractual'),
)
CITY = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barishal', 'Barishal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
)

STATUS = (
    ('Published', 'Published'),
    ('Hidden', 'Hidden'),
)

EDU = (
    ('Post Graduate', 'Post Graduate'),
    ('Graduate', 'Graduate'),
    ('HSC', 'HSC'),
    ('SSC', 'SSC'),
)


# manager for fetching only published job
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='Published')


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
    job_category = models.CharField(max_length=50, choices=JOB_CATEGORY)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE)
    email = models.EmailField(max_length=254,)
    phone = models.CharField(max_length=11, blank=True, null=True)
    company_website = models.URLField()
    logo = models.ImageField(null=True, blank=True)
    address = models.TextField(max_length=200)
    division = models.CharField(max_length=15, choices=CITY)
    description = models.TextField()
    responsibility = models.TextField()
    min_education = models.CharField(max_length=20, choices=EDU)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    experience = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15)])
    skill_req = models.TextField(help_text='Input skills with comma')
    skill_bonus = models.CharField(
        max_length=255, blank=True, null=True, help_text='Input skills with comma')

    status = models.CharField(max_length=20, choices=STATUS)
    publish = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    recruiter = models.ForeignKey('account.Recruiter',
                                  on_delete=models.CASCADE,
                                  related_name='recruiters')
    applicant = models.ManyToManyField('account.Applicant',
                                       related_name='applicants', blank=True)

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
        return reverse('jobDetail', args=[self.slug])


class JobApplication(models.Model):
    applicant = models.ForeignKey('account.Applicant',
                                  on_delete=models.CASCADE,
                                  related_name='jobapplicants', blank=True)
    job = models.ForeignKey('Job',
                            on_delete=models.CASCADE,
                            related_name='jobs')
    apply_time = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=11)
    education_application = models.CharField(max_length=20, choices=EDU)
    cgpa_application = models.DecimalField(max_digits=3, decimal_places=2)
    skill_req_application = models.TextField()
    skill_bonus_application = models.CharField(
        max_length=255, blank=True, null=True)
    related_experience_application = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15)])
    total_experience_application = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15)])
    score = models.FloatField(default=0.0)
    note_application = models.TextField(blank=True, null=True)
    cv_application = models.FileField()

    def __str__(self):
        return self.job.title
