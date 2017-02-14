import logging
from .models import Company
# Empty
empty = {
'title': '',
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
'company_profile_name':'dharma',
'website':'https://dharmamerchantservices.com',
'phones':['Toll-free: (866) 615-5157','Local: (415) 632-1920','Fax: (415) 632-1921', 'Online-Chat: No'],
'verified': True,
'highlights':[
                'Small Business Friendly',
                'Interchange Plus Pricing with Full Disclosure',
                'Non-Profit Friendly',
                'Clover Equipment',
                'Loyalty Program with Flok',
                'Two Options for gateway, NMI and Authorize.Net'
                ],
'full_description': '''Dharma Merchant Services, Dharma hereafter, is founded in 2007. Dharma has maintained good reputation since then. Better Business Bureau (BBB) has been keeping Dharma's profile since Jan 2010. Dharma maintains clean record of only one complaint and A+ rating.
<br><br>
Dharma works with all kind of business types. It will give special discounted rate to non-profit organizations. However, Dharma does not work with High-Risk merchants.
<br><br>
Dharma provides many options for terminal. For traditional terminal, Dharma has options like First Data, Verifone, and etc. For mobile and wireless terminals, Dharma provides Clover products, Authorize.Net mobile swiper and etc. For virtual terminal/gateway, Dharma provide two options, NMI and Authorize.Net. They both come at at $20 per month and $0.05 per transaction.
<br><br>
Dharma is small-business friendly payment processor in that it puts efforts to provide the complimentary services that are well-suited for small businesses. Those services come with Dharma's partnership with Flok for loyalty program, Kabbage for small loans, 4aGoodCause for donation/events pages, SinglePlatform for managing online presence, and more.
<br><br>
In summary, Dharma is a small-business friendly payment processor with good reputation.''',
'pricing_table':'''<table class='pricing-table'>
  <thead>
    <tr>
      <th style='border-right:0.1rem solid #e1e1e1'></th>
      <th>Fees</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Card-not-Present</td>
      <td>0.35% + $0.10</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Restaurant</td>
      <td>0.20% + $0.07</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Card-not-Present(Non-Profit)</td>
      <td>0.30% + $0.10</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Card-Swiped(Non-Profit)</td>
      <td>0.20% + $0.10</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Card-Swiped</td>
      <td>0.25% + $0.10</td>
    </tr>

    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Monthly Fee</td>
      <th style='text-align:center;' colspan="5">$10</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>PCI Compliance Fee</td>
      <th style='text-align:center;' colspan="5">$7.95/month</td>
    </tr>
    <tr>
      <td style='border-right:0.1rem solid #e1e1e1'>Termination Fee</td>
      <th style='text-align:center;' colspan="5">$25</td>
    </tr>
  </tbody>
</table>''',
'year_founded':2007,
'provided_srvs':['Retail', 'Restaurant', 'E-Commerce',
                 'Mobile', 'Professional/Personal Services',
                  'Non-Profit', 'Enterprise', 'Other'],
'complementary_srvs':['Analytics/Reporting', 'Recurring Bill',
                      'Security', 'Fraud', 'ACH', 'Digital Wallet',
                      'Loyalty Program', 'Other'],
'equipment':['Terminal', 'Wireless Terminal', 'Mobile Terminal',
             'POS Solution', 'Virtual/Gateway', 'Other'],
'pricing_method':['Interchange Plus', 'Custom', 'Other'],
'landing_page':'https://dharmamerchantservices.com/52-payments/',
'featured':True
}

def import_companies():
    # Dharma
    if load_company(company_form['company_profile_name']):
        logging.warning('The entered Url End Point is taken.')
    a = Company(**dharma)
    a.put()
