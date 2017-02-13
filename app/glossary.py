
glossary = {
'pricing method': '''Pricing method is how each transaction is priced.
                    It usually comes with per transaction fee and rate.</br>
                    ex) 1.5% + $0.20''',
'business type': '''Business Types are the category of business that payment processors
                    work with. Card associations(Visa, MC, and etc.) define classifies the business by
                    Merchant Classification Codes and impose different requirements and pricing.''',
'terminal':'''Terminal is the mean to accept the card payments. There's physical stand-alone terminal,
                wireless terminal, mobile terminal(to be used with smartphones), Point-of-Sales(POS) System,
                virtual terminal/gateway, and etc.''',
'complimentary service':'''Complimentary Services are services offered in addition to payment processing.
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
'digital wallet': '''Digital wallets
                    '''

}
srv_type = ['Marketing', 'Analytics/Reporting', 'Recurring Bill',
            'Chargeback', 'Security', 'Fraud', 'ACH', 'Digital Wallet',
            'Loyalty Program', 'Gift Cards', 'Other']
equip_type = ['Terminal', 'Wireless Terminal', 'Mobile', 'POS', 'Tablet',
              'Tablet POS', 'Virtual Terminal','Other']
pricing_type = ['Tiered', 'Interchange Plus', 'Flat', 'Custom', 'Other']

def add_sticky_note(term):
    note = glossary.get(term.lower(), '') or glossary.get(term.lower()+'s', '')
    if not note:
        return term
    else:
        return '''
        <span onmouseover="javascript:show_hover_message(this)" onmouseout="javascript:hide_hover_message(this)" onclick="javascript:hide_hover_message(this)">
          %s
          <p class="hover_message">
            %s
          </p>
        </span>
        '''%(term, note)
