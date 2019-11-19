#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

"""
    Variety quote plugin sourcing quotes from www.viedemerde.fr
    This script is placed in '~/.config/variety/plugins' and then activated from inside Variety's
    Preferences Quotes menu
"""

import logging
import random
from locale import gettext as _
from variety.Util import Util
from variety.plugins.IQuoteSource import IQuoteSource
import urllib.request
from bs4 import BeautifulSoup

logger = logging.getLogger("variety")


class GoodreadsSource(IQuoteSource):
    """
        Retrives quotes from www.viedemerde.fr. Reads the last quotes.
        Attributes:
            quotes(list): list containing the quotes
    """

    def __init__(self):
        super(IQuoteSource, self).__init__()
        self.quotes = []

    @classmethod
    def get_info(cls):
        return {
            "name": "Vie de merde - VDM",
            "description": _("Popular quotes from www.viedemerde.fr"),
            "author": "Luis Gomes",
            "version": "0.1"
        }

    def supports_search(self):
        return False

    def activate(self):
        if self.active:
            return
        self.active = True

        self.quotes = []
        self.fetch_vdm_quotes()

    def deactivate(self):
        self.quotes = []
        self.active = False

    def fetch_vdm_quotes(self):
        BASE_URL = 'https://www.viedemerde.fr/rss'

        self.quotes = []

        req = urllib.request.Request(BASE_URL)
        req.add_header('Referer', BASE_URL)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36')
        parse_xml_url = urllib.request.urlopen(req)
        
        xml_page = parse_xml_url.read()
        parse_xml_url.close()

        soup_page = BeautifulSoup(xml_page, "xml")
        news_list = soup_page.findAll("item")

        for getfeed in news_list:
            
            self.quotes.append({
                "quote": getfeed.description.text.strip(), 
                "author": getfeed.title.text.strip(),
                "sourceName": "VDM", 
                "link": getfeed.link.text.strip()})
            
        if not self.quotes:
            logger.warning("Could not find quotes for URL " + BASE_URL)

    def get_for_author(self, author):
        return []

    def get_for_keyword(self, keyword):
        return []

    def get_random(self):
        if self.quotes:
            return [random.choice(self.quotes)]
        else:
            return self.quotes
