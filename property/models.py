from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from customer_register.models import Customer_User

DAYS_OF_THE_WEEK = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
)

HOURS_OF_THE_DAY = (
    (0, '12:00 AM'),
    (1, '1:00 AM'),
    (2, '2:00 AM'),
    (3, '3:00 AM'),
    (4, '4:00 AM'),
    (5, '5:00 AM'),
    (6, '6:00 AM'),
    (7, '7:00 AM'),
    (8, '8:00 AM'),
    (9, '9:00 AM'),
    (10, '10:00 AM'),
    (11, '11:00 AM'),
    (12, '12:00 PM'),
    (13, '1:00 PM'),
    (14, '2:00 PM'),
    (15, '3:00 PM'),
    (16, '4:00 PM'),
    (17, '5:00 PM'),
    (18, '6:00 PM'),
    (19, '7:00 PM'),
    (20, '8:00 PM'),
    (21, '9:00 PM'),
    (22, '10:00 PM'),
    (23, '11:00 PM'),
)



class Company(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default='')

    # State abbreviations
    alabama        = 'AL'
    alaska         = 'AK'
    arizona        = 'AZ'
    arkansas       = 'AR'
    california     = 'CA'
    colorado       = 'CO'
    connecticut    = 'CT'
    delaware       = 'DE'
    florida        = 'FL'
    georgia        = 'GA'
    hawaii         = 'HI'
    idaho          = 'ID'
    illinois       = 'IL'
    indiana        = 'IN'
    iowa           = 'IA'
    kansas         = 'KS'
    kentucky       = 'KY'
    louisiana      = 'LA'
    maine          = 'ME'
    maryland       = 'MD'
    massachusetts  = 'MA'
    michigan       = 'MI'
    minnesota      = 'MN'
    mississippi    = 'MS'
    missouri       = 'MO'
    montana        = 'MT'
    nebraska       = 'NE'
    nevada         = 'NV'
    new_hampshire  = 'NH'
    new_jersey     = 'NJ'
    new_mexico     = 'NM'
    new_york       = 'NY'
    north_carolina = 'NC'
    north_dakota   = 'ND'
    ohio           = 'OH'
    oklahoma       = 'OK'
    oregon         = 'OR'
    pennsylvania   = 'PA'
    rhode_island   = 'RI'
    south_carolina = 'SC'
    south_dakota   = 'SD'
    tennessee      = 'TN'
    texas          = 'TX'
    utah           = 'UT'
    vermont        = 'VT'
    virginia       = 'VA'
    washington     = 'WA'
    west_virginia  = 'WV'
    wisconsin      = 'WI'
    wyoming        = 'WY'

    states = (
        ('', 'State'),
    	(alabama, 'Alabama'),
    	(alaska, 'Alaska'),
    	(arizona, 'Arizona'),
    	(arkansas, 'Arkansas'),
    	(california, 'California'),
    	(colorado, 'Colorado'),
    	(connecticut, 'Connecticut'),
    	(delaware, 'Delaware'),
    	(florida, 'Florida'),
    	(georgia, 'Georgia'),
    	(hawaii, 'Hawaii'),
    	(idaho, 'Idaho'),
    	(illinois, 'Illinois'),
    	(indiana, 'Indiana'),
    	(iowa, 'Iowa'),
    	(kansas, 'Kansas'),
    	(kentucky, 'Kentucky'),
    	(louisiana, 'Louisiana'),
    	(maine, 'Maine'),
    	(maryland, 'Maryland'),
    	(massachusetts, 'Massachusetts'),
    	(michigan, 'Michigan'),
    	(minnesota, 'Minnesota'),
    	(mississippi, 'Mississippi'),
    	(missouri, 'Missouri'),
    	(montana, 'Montana'),
    	(nebraska, 'Nebraska'),
    	(nevada, 'Nevada'),
    	(new_hampshire, 'New Hampshire'),
    	(new_jersey, 'New Jersey'),
    	(new_mexico, 'New Mexico'),
    	(new_york, 'New York'),
    	(north_carolina, 'North Carolina'),
    	(north_dakota, 'North Dakota'),
    	(ohio, 'Ohio'),
    	(oklahoma, 'Oklahoma'),
    	(oregon, 'Oregon'),
    	(pennsylvania, 'Pennsylvania'),
    	(rhode_island, 'Rhode Island'),
    	(south_carolina, 'South Carolina'),
    	(south_dakota, 'South Dakota'),
    	(tennessee, 'Tennessee'),
    	(texas, 'Texas'),
    	(utah, 'Utah'),
    	(vermont, 'Vermont'),
    	(virginia, 'Virginia'),
    	(washington, 'Washington'),
    	(west_virginia, 'West Virginia'),
    	(wisconsin, 'Wisconsin'),
    	(wyoming, 'Wyoming')
    )

    state = models.CharField(max_length=10, choices=states, default='')
    zip = models.CharField(max_length=10, default='')
    auto_respond_text = models.CharField(null=True, max_length=500)
    auto_respond_number = PhoneNumberField(null=True, blank=False, unique=True)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    email = models.EmailField(max_length=100)
    customer_user = models.ForeignKey(Customer_User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    days_of_the_week_enabled = MultiSelectField(choices=DAYS_OF_THE_WEEK, max_choices=7, default=None)
    hours_of_the_day_enabled = MultiSelectField(choices=HOURS_OF_THE_DAY, max_choices=24, default=None)

    def __str__(self):
        return str(self.id) + '-' + self.name + '-' + self.address
