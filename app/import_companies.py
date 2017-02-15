import logging
from .models import Company
# Empty
empty = {
'title': '',
'share':0,
'location':'',
'company_profile_name':'',
'website':'',
'phones':['Toll-free: (000) 000-0000', 'Online-Chat: No'],
'verified': True,
'highlights':[],
'full_description': '',
'pricing_table':'',
'year_founded':000,
'provided_srvs':[],
'complementary_srvs':[],
'equipment':[],
'pricing_method':[],
'landing_page':'',
'featured': False
}
dharma = {
'title': 'Dharma Merchant Services',
'share':20,
'location': 'San Francisco, CA',
'company_profile_name':'dharma',
'website':'https://dharmamerchantservices.com',
'phones':['Toll-free: (866) 615-5157','Local: (415) 632-1920','Fax: (415) 632-1921', 'Online-Chat: No'],
'verified': True,
'highlights':[
                'Interchange Plus Pricing with Full Disclosure',
                'Non-Profit Friendly',
                'Clover Equipments',
                'Loyalty Program with Flok',
                'Small Business Friendly',
                'For Business with at Least $10k/month Volume'
                ],
'full_description': '''Dharma Merchant Services, Dharma hereafter, is founded in 2007. Dharma has maintained good reputation since then. Better Business Bureau (BBB) has been keeping Dharma's profile since Jan 2010. Dharma maintains clean record of only one complaint and A+ rating.
<br><br>
Dharma works with all kind of business types. Please note, it works with the merchants with at least $10k/month in processing volume. It will give special discounted rate to non-profit organizations. However, Dharma does not work with High-Risk merchants.
<br><br>
Dharma provides many options for terminal. For traditional terminal, Dharma has options like First Data, Verifone, and etc. For mobile and wireless terminals, Dharma provides Clover products, Authorize.Net mobile reader and etc. For virtual terminal/gateway, Dharma provide two options, NMI and Authorize.Net. They both come at at $20 per month and $0.05 per transaction.
<br><br>
Dharma is small-business friendly payment processor in that it puts efforts to provide the complimentary services that are well-suited for small businesses. Those services come with Dharma's partnership with Flok for loyalty program, Kabbage for small loans, 4aGoodCause for donation/events pages, SinglePlatform for managing online presence, and more.
<br><br>
In summary, Dharma is a small-business friendly payment processor with good reputation.''',
'pricing_table':'''
<table class='pricing-table'>
  <thead>
    <tr>
      <th style='border-right:0.1rem solid #e1e1e1'></th>
      <th style='font-weight:bold;'>Fees</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-not-Present') | safe}}</td>
      <td>0.35% + $0.10*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-Swiped') | safe}}</td>
      <td>0.25% + $0.10*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Restaurant</td>
      <td>0.20% + $0.07*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-not-Present') | safe}}(Non-Profit)</td>
      <td>0.30% + $0.10*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-Swiped') | safe}}(Non-Profit)</td>
      <td>0.20% + $0.10*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Monthly Fee</td>
      <th colspan="5">$10</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('PCI Compliance Fee') | safe}}</td>
      <th colspan="5">$7.95/month</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Termination Fee</td>
      <th colspan="5">$25</td>
    </tr>
  </tbody>
</table>
<span class='footnote'>
  *These rates are added above {{sticky_note('Interchange') | safe}}.
</span>

''',
'year_founded':2007,
'provided_srvs':['Retail', 'Restaurant', 'E-Commerce',
                 'Mobile', 'Professional/Personal Services',
                  'Non-Profit', 'Enterprise', 'Other'],
'complementary_srvs':['Analytics/Reporting', 'Recurring Billing',
                      'Security', 'Fraud', 'ACH', 'Digital Wallet',
                      'Loyalty Program', 'Other'],
'equipment':['Terminal', 'Wireless Terminal', 'Mobile Terminal',
             'POS Solution', 'Virtual/Gateway', 'Other'],
'pricing_method':['Interchange Plus', 'Custom'],
'landing_page':'https://dharmamerchantservices.com/52-payments/',
'featured':True
}

epd = {
'title': 'Easy Pay Direct',
'share':20,
'location':'Austin, TX',
'company_profile_name':'easypaydirect',
'website':'https://www.easypaydirect.com/',
'phones':['Phone: (800) 805-4949', 'Online-Chat: Yes'],
'verified': True,
'highlights':['Live Customer Support',
              'High-Risk Friendly',
              'Enterprise Friendly',
              'International Processing',
              'Load Balancing with Multiple Accounts',
              'Tiered Pricing'
],
'full_description': '''
Easy Pay Direct, EPD hereafter, is founded in 2006. EPD has maintained good reputation. It is evident on Better Business Bureau (BBB) profile which has been kept since April 2015. EPD maintains clean record of zero complaint and A+ rating.
<br><br>
EPD works with all kind of business types, including High-Risk. It maintains many relationships with different banks to effectively work with High-Risk merchants. Furthermore, EPD has the relationships outside of  the United States to allow international processing. EPD is also Enterprise-friendly. It will negotiate to provide more competitive custom pricing for those who qualify.
<br><br>
EPD provides different options for terminals. While EPD keeps variety of terminals in stock, PAX S80 is the most cost-effective recommended terminal by EPD. You can bring your own terminal. EPD is compatible with almost all terminals, including, Verifone, Hypercom, Pax, First Data, and etc. For POS system, Clover products are available. Supported mobile readers include Idtech, MagTek, and etc.  EPD has its own EPD virtual terminal/gateway, but EPD will let you use any gateway of your choice.
<br><br>
One noticeable service of EPD is Load Balancing. It will balance out loads of transactions to multiple merchants account with a single login to virtual terminal/gateway. High-risk merchants are likely to have multiple accounts. By automatically distributing transactions, chargebacks, fraud, and volume can be distributed to lower the risk of having accounts suspended.
<br><br>
In summary, EPD is a High-Risk friendly payment processor with noticeable services like load balancing. It is one of a few payment processors to support international processing.
''',
'pricing_table':'''
<table class='pricing-table'>
  <thead>
    <tr>
      <th style='border-right:0.1rem solid #e1e1e1'></th>
      <th style='font-weight:bold;'>Fees</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-not-Present') | safe}}(Non-Profit)</td>
      <td>2.39% + $0.29*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-Swiped') | safe}}(Non-Profit)</td>
      <td>1.59% + $0.17*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('ACH/eCheck') | safe}}</td>
      <td>1.6% + $0.29*</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Monthly Fee</td>
      <th colspan="5">$12(Card-not-Present), $13.95(Card-Swiped)</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>SetUp Fee</td>
      <th colspan="5">$99(Card-not-Present Only)</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('PCI Compliance Fee') | safe}}</td>
      <th colspan="5">Variable</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Termination Fee</td>
      <th colspan="5">None**</td>
    </tr>
  </tbody>
</table>
<span class='footnote'>
  *These rates are for {{sticky_note('Qualified') | safe}}/{{sticky_note('Mid-Qualified') | safe}} transactions.<br>
  **While Easy Pay Direct has a policy not to enforce, the sponsoring banks might enforce it.
</span>
''',
'year_founded':2006,
'provided_srvs':['Retail', 'Restaurant', 'E-Commerce',
                    'Mobile', 'Professional/Personal Services',
                    'Non-Profit', 'High-Risk',  'Enterprise', 'Non-US', 'Other'],
'complementary_srvs':['Analytics/Reporting', 'Recurring Billing',
                    'Chargeback', 'Security', 'Fraud', 'ACH', 'Digital Wallet',
                    'Loyalty Program', 'Other'],
'equipment':['Terminal', 'Wireless Terminal', 'Mobile Terminal', 'POS Solution', 'Virtual/Gateway','Other'],
'pricing_method':['Tiered', 'Custom'],
'landing_page':'https://easypaydirect.offerit.com/tiny/rNavA',
'featured': False
}
cdgcommerce = {
'title': 'CDG Commerce',
'share':30,
'location':'Chesapeake, VA',
'company_profile_name':'cdgcommerce',
'website':'http://www.cdgcommerce.com/',
'phones':['Toll-free: (888) 586-3346', 'Online-Chat: Yes'],
'verified': True,
'highlights':[
            'No Termination Fee',
            'Free Quantum Gateway',
            'Free Mobile and USB Reader',
            'Amortized Cost for Equipments',
            'CDG360 Program with Breach Protection Plan',
            'Tiered Pricing'
            ],
'full_description': '''
CDG Commerce, CDG hereafter, is founded in 1999. CDG has a good reputation which can be seen in the profile kept in Better Business Bureau (BBB). The profile has been kept open since June 2007. The record shows that CDG maintains a good record of five previous complaints and A+ rating. Three of the five complaints were resolved with customers' satisfaction. Given the length of BBB profile of CDG, five complaints don't seem to be many.
<br><br>
CDG works with all ordinary business types. CDG does not explicitly state that it works with High-Risk merchants.
<br><br>
CDG provides very competitive cost for terminals. For basic terminal, it comes at $79/year.  The terminal will be Verifone vx520. You can bring your own terminal and have it re-programmed as long as it is not proprietary and meets the PCI PTS standards.
Wireless terminal's cost is $79/year, but it has additional wireless carrier cost of $20/month + $0.05 per transaction.
<br><br>
The available POS system from CDG is the equipment called Harbortouch Echo with CDG POS+. It comes with free $100,000 breach protection plan for hacking, employee theft, and etc. It is $49/month. There's 30-day free-trial available.
<br><br>
CDG has its own unique and FREE Quantum Gateway. It does not have any fees such as monthly fee, per-transaction fee, and etc. Also, there is a free usb reader available for Quantum Gateway. There's two other options, which are eProcessingNetwork and Authorize.Net. EprocessingNetwork gateway has $15 monthly fee and $0.10 per-transaction fee after 250 free transactions. Authorize.Net has $15 monthly fee and $0.05 per-transaction fee.
<br><br>
For mobile reader, CDG provides ProcessNow card reader and application. Card Reader is free. ProcessNow provides 24x7 support for its products.
<br><br>
CDG has its unique program call CDG360. It includes $100,000 breach protection plan, merchant trust seal, vulnerability scanning, Customized security alert, staff security awareness training, and self-assessment questionnaire wizard. This optional program is $15/month.
<br><br>
In summary, CDG is a well-established payment processor with unique services like Quantum Gateway and CDG360. Its amortized cost of equipments and free equipments make it easier for merchants to start processing without hefty upfront cost.
''',
'pricing_table':'''
<table class='pricing-table'>
  <thead>
    <tr>
      <th style='border-right:0.1rem solid #e1e1e1'></th>
      <th style='font-weight:bold;'>Fees</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-not-Present') | safe}}, ({{sticky_note('Qualified') | safe}}, {{sticky_note('Mid-Qualified') | safe}})</td>
      <td>1.95% + $0.30</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-Swiped') | safe}}, ({{sticky_note('Qualified') | safe}}, {{sticky_note('Mid-Qualified') | safe}})</td>
      <td>1.70% + $0.25</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-not-Present') | safe}}, ({{sticky_note('Non-Qualified') | safe}})</td>
      <td>2.95% + $0.30</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('Card-Swiped') | safe}}, ({{sticky_note('Non-Qualified') | safe}})</td>
      <td>2.90% + $0.30</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Monthly Fee</td>
      <th colspan="5">$10</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>SetUp Fee</td>
      <th colspan="5">None</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>{{sticky_note('PCI Compliance Fee') | safe}}</td>
      <th colspan="5">None</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Termination Fee</td>
      <th colspan="5">None</td>
    </tr>
  </tbody>
</table>
''',
'year_founded':1999,
'provided_srvs':['Retail', 'Restaurant', 'E-Commerce',
                    'Mobile', 'Professional/Personal Services',
                    'Enterprise',  'Other'],
'complementary_srvs':['Analytics/Reporting', 'Recurring Billing',
                    'Chargeback', 'Security', 'Fraud', 'ACH', 'Digital Wallet',
                    'Loyalty Program', 'Other'],
'equipment':['Terminal', 'Wireless Terminal', 'Mobile Terminal', 'POS Solution',
                       'Virtual/Gateway','Other'],
'pricing_method':['Tiered', 'Custom'],
'landing_page':'http://www.cdgcommerce.com/internet-services.php?R=3232',
'featured': True
}
def import_companies():
    for company in [dharma, epd, cdgcommerce]:
        if Company.load_company(company['company_profile_name']):
            logging.warning('(%s) The entered Url End Point is taken.'%company['company_profile_name'])
        else:
            a = Company(**company)
            a.put()
