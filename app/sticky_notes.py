import logging
from jinja2 import Markup
from flask import render_template_string
from .glossary import glossary

def add_sticky_note(term):
    note = glossary.get(term.lower(), '') or glossary.get(term.lower()+'s', '')
    if not note:
        return term.strip()
    else:
        return Markup('<span class="sticky_note" style="text-decoration:underline;" onmouseover="javascript:show_hover_message(this)" onmouseout="javascript:hide_hover_message(this)" onclick="javascript:hide_hover_message(this)">%s<p class="hover_message">%s</p></span>'%(term.strip(), note))

def add_notes(companies):
    def mapping(company):
        company.pricing_method = map(add_sticky_note, company.pricing_method)
        company.provided_srvs= map(add_sticky_note, company.provided_srvs)
        company.complementary_srvs = map(add_sticky_note, company.complementary_srvs)
        company.equipment = map(add_sticky_note, company.equipment)
        company.pricing_table = render_template_string(company.pricing_table)
        company.highlights = map(render_template_string, company.highlights)
        company.full_description = company.full_description.replace('\n', '<br>')
        return company
    if type(companies) != list:
        return mapping(companies)
    for company in companies:
        company = mapping(company)
    return companies
