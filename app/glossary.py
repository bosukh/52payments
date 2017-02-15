
glossary = {
'pricing methods': '''Pricing method is how each transaction is priced.
                    It usually comes with per transaction fee and rate.</br>
                    ex) 1.5% + $0.20''',
'business types': '''Business Types are the category of business that payment processors
                    work with. Card associations(Visa, MC, and etc.) define classifies the business by
                    Merchant Classification Codes and impose different requirements and pricing.''',
'terminals':'''Terminal is the mean to accept the card payments. There's physical stand-alone terminal,
                wireless terminal, mobile terminal(to be used with smartphones), Point-of-Sales(POS) System,
                virtual terminal/gateway, and etc.''',
'complimentary services':'''Complimentary Services are services offered in addition to payment processing.
                            Different payment processors have different unique set of complimentary services.
                            These include reporting/analytics, data security, fraud prevention, chargeback,
                            recuring bill, ach, loyalty program, and etc.''',
'professional/personal services': '''Professiona/Personal Services can include lawyers, doctors, personal trainers,
                                     freelancers, and any other service providers. Virtual Teminal/Gateway with
                                     recurring billing is most popular.
                                  ''',
'retail': ''' Retailers would be the merchants who physically accept payments on counter.
             Stand-alone terminal and Point-of-Sales(POS) System are most popular.
          ''',
'restaurant': '''Restaurants would usually utilize Point-of-Sales(POS) System and wireless terminal.
                Restuanrants have speical requirements due to tip-adjustment.
                ''',
'e-commerce': '''E-commerce business type includes any business that utilize some kind of web
                to receive payments in exchange for services and goods. These merchants would usually
                want a virtual terminal/gateway to accept card payments without swiping the actual cards.
                It is important to check virtual terminal's compatibility with the shoping cart or any softwares being used.
                ''',
 'mobile': '''Mobile business type would be any merchants who need to flexibly accept
              payments regardless of location. These merchants would usually utilize
              mobile terminal that is attached with smartphones or tablets.
              A good example would be food truck.''',
 'non-profit': '''Non-profit organizations would usually utilize virtual terminal/gateway to
                accept payments online. They would often use recurring billing. Many payment processors
                would negotiate the pricing further if the organization is registered as 501(c)(3).''',
'high-risk': '''Banks and card associations consider some business as riskier than the other, usually due to
                vulnerability to fraud and chargeback. </br>
                These merchants are often called high-risk. They include pornography, e-cigarette, vape,
                guns, and etc. </br>
                If a merchant has history of high chargeback and/or fraud, the merchant
                might need to consult as a high-risk even if it's not considered to be in high-risk industry.
''',
'enterprise': '''Enterprise business type is for the merchants with large processing volumes who need specialized solutions.''',
'non-us': '''Non-US refers to the merchants with need for merchant account outside of the United States.
            While most of the payment processors primarily focus on the United States, some can
            still help outside of US as well.''',
'analytics/reporting':'''Some payment processors provide more than just monthly statement.
                        Analytics/Reporting services can include real-time transaction monitor, transactions by demographic,
                        card-type, and different filter, and etc.
                    ''',
'recurring billing': '''Recurring billing is when a merchant automatically charge the given card/account on recurring bases.
                    ''',
'chargeback': '''Chargeback is when banks demand a retailer to make good the loss and focibly return the funds to customers
                 on a fraudulent or disputed transaction. Chargeback solutions helps informing merchants about such events so
                 that the merchants can prepare and win the dispute.
                ''',
'fraud': '''Fraud prevention services usually include velocity check, cvv verification, and etc.''',
'security': '''Card associations require that merchants to become PCI comliance,
                complying with Payment Card Industry(PCI) Data Security Standard.
                Payment processors can help merchants by providing services like data tokenization, storage vault, and etc.
            ''',
'ach':'''
     Automated Clearing House(ACH) payments is the service the transaction processed by electronic network of financial institutions.
     It's usually cheaper and faster than credit cards and checks.
     ''',
'digital wallet': '''Digital wallet refers to an electronic device, mostly smartphones, that links information about user's bank account, and other
                    card data. It can then be used to make payments. Most prominent digital wallets are Apple Pay, Samsung Pay, and Android Pay.
                    ''',
'loyalty program': '''Loyalty program is set of services/promotions provided by business to grow and maintain existing customer base.
                    Payment processors can help in such efforts by issuing gift-cards, managing rewards, coupons, and etc.''',
'terminal': ''' Terminal refers to physical stand-alone terminal that is solely dedicated to accepting card payments.
            ''',
'wireless terminal': '''Wireless Terminal is similary to traditional terminal, but wireless. It enables the merchant to move around with the terminal.''',
'mobile terminal': '''Mobile Terminal refers to a small card reader connected to mobile devices like smartphones.
                     It allows merchant to be even more mobile than wireless terminal. It usually requires some kine of internet
                     connection, but some works even if the connection is lost temporarily.''',
'pos solution': '''Point-of-Sales(POS) solution refers to complete solution that can replace cash register. It would usually come with
                    retail management software, card reader, barcode reader, screen or tablet, and others. It can be integrated into other CRM softwares as well.
                    ''',
'virtual/gateway':'''Virtual Terminal or Gateway refers the online application which enables merchants to accept card payments by
                     feeding card information. It does not require physical card to be swiped. Merchants can manually provide card information or
                     integrate it to their website or any other applications to enable payments.''',
'tiered':'''Tiered pricing refers to the pricing structure where card transactions are categorized into buckets with different rates.
            3-tiered pricing is the most common pricing structure. Often, three tiers are called qualified, mid-qualified, and non-qualified, and the rates increases respectively.''',
'interchange plus':'''Interchange Plus refers to the pricing structure where merchants pays interchange to card associations and another margin to payment processors.
                     Interchange is the pricing for card transactions imposed by card assocations. Interchange rate varies for each transaction and card.
                     Therefore, Interchange Plus pricing would look something like "interchange rate + x.xx% + $0.xx".''',
'interchange':'''Interchange is the pricing for card transactions imposed by card assocations. Interchange rate varies for each transaction and card.
                It's strictly forced by card associations in that every payment processor has to pay the same price.
                It's usually cheaper to swipe(Card-siwped) than to key-in(Card-not-Present).
                Debit cards are the cheapest, and the perks, rewards, and international cards are the most expensive ones.
                ''',
'custom':'''Cutom pricing refers to the pricing structure that can vary by each merchant. This could mean that the pricing is tailored
            for specific needs or the pricing had to be adjusted due to other circumstances like history of high chargebacks and frauds.''',
'card-swiped':'''
''',
'card-not-present':'''
''',
'pci compliance fee':'''
''',
'qualified':'''
''',
'mid-qualified':'''
''',
'non-qualified':'''
'''
}
glossary['ach/echeck'] = glossary.get('ach')
glossary['gateway'] = glossary.get('virtual/gateway')
def add_sticky_note(term):
    note = glossary.get(term.lower(), '') or glossary.get(term.lower()+'s', '')
    if not note:
        return term.strip()
    else:
        return '<span style="text-decoration:underline;" onmouseover="javascript:show_hover_message(this)" onmouseout="javascript:hide_hover_message(this)" onclick="javascript:hide_hover_message(this)">%s<p class="hover_message">%s</p></span>'%(term.strip(), note)
from flask import render_template_string
def add_notes(companies):
    def mapping(company):
        company.pricing_method = map(add_sticky_note, company.pricing_method)
        company.provided_srvs= map(add_sticky_note, company.provided_srvs)
        company.complementary_srvs = map(add_sticky_note, company.complementary_srvs)
        company.equipment = map(add_sticky_note, company.equipment)
        company.pricing_table = render_template_string(company.pricing_table)
        return company
    if type(companies) != list:
        return mapping(companies)
    for company in companies:
        company = mapping(company)
    return companies
