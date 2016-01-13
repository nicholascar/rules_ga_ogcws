from ruleset import RuleSet
from rule import Rule


class GaWebServicePubStandards(RuleSet):
    """
    GA OGC rules
    """
    def __init__(self):
        ruleset_id = 'ga_ws_pub_sdts'
        ruleset_name = 'GA Web Service Publication Standards'
        passed = True
        rules_results = []

        # make a Graph from the string or file

        #
        #   Run all the rules
        #
        service_pass = r'http://services.ga.gov.au/gis/services/NEXIS_Building_Exposure/MapServer/WFSServer?request=GetCapabilities'
        service_fail = r'http://www.ga.gov.au/gis/services/topography/National_Ferry_Terminals/MapServer/WFSServer?request=GetCapabilities'

        #rules_results.append(GaTitle(service_pass).get_result())
        rules_results.append(WebServiceTitle(service_pass).get_result())

        # calculate if RuleSet passed
        for rule in rules_results:
            if not rule['passed']:
                passed = False

        #
        #   Call the base RuleSet constructor
        #
        RuleSet.__init__(self,
                         ruleset_id,
                         ruleset_name,
                         'nicholas.car@ga.gov.au',
                         rules_results,
                         passed)


# TODO: complete Rule. get the name from somewhere
class WebServiceName(Rule):
    def __init__(self, service_get_caps_uri):
        #
        #   Rule details
        #
        self.rule_id = 'web_service_name'
        self.rule_name = 'Web Service Name'
        self.rule_business_definition = 'The name is a summarised title (see above) of the service.\n' + \
            'The primary purpose of service name is to support machine-to-machine communications.\n' + \
            'Where possible, the service name should be meaningful to humans.\n' + \
            'The name should be a reflection of the service title (see above), sanitized to be machine readable.\n' + \
            'Describes the Service, not the data.\n' + \
            'Acronyms are allowed ONLY if they are a widely understood standard or an official name (e.g. DEM).\n' + \
            'New service names should be consistent with existing service names.\n' + \
            'Must not duplicate an existing GA web service name.\n'
        self.rule_authority = 'http://pid-dev.ga.gov.au/organisation/ga'
        self.rule_functional_definition = '120 character limit\n' +\
            'alphanumeric characters and underscores only\n' +\
            'machine-readable reflection of the web service title\n' + \
            'acronyms from controlled list only\n' + \
            'not a duplicate of existing name'
        self.component_name = 'string'
        self.passed = True
        self.fail_reasons = []
        self.components_total_count = 1
        self.components_failed_count = 0
        self.failed_components = None

        #
        #   Rule code
        #

        # get the name, from where?

        #
        #   Call the base Rule constructor
        #
        Rule.__init__(self,
                      self.rule_id,
                      self.rule_name,
                      self.rule_business_definition,
                      self.rule_authority,
                      self.rule_functional_definition,
                      self.component_name,
                      self.passed,
                      self.fail_reasons,
                      self.components_total_count,
                      self.components_failed_count,
                      self.failed_components)


class WebServiceTitle(Rule):
    def __init__(self, service_get_caps_uri):
        #
        #   Rule details
        #
        self.rule_id = 'web_service_title'
        self.rule_name = 'Web Service Title'
        self.rule_business_definition = '250 characters or less.\n' + \
            'No tabs, indents, line feeds or carriage returns.\n' + \
            'No unsafe or reserved characters.\n' + \
            'Acronyms are allowed ONLY if they are a widely understood standard or an official name (e.g. DEM).\n' + \
            'Acronyms to be included in parenthesis after the full text.\n' + \
            'Must not duplicate an existing GA web service title.\n'
        self.rule_authority = 'GA'
        self.rule_functional_definition = 'Title must have... (no underscores)'
        self.component_name = 'Web Service title'
        self.passed = True
        self.fail_reasons = []
        self.components_total_count = 1
        self.components_failed_count = 0
        self.failed_components = None

        #
        #   Rule code
        #
        import requests
        r = requests.get(service_get_caps_uri)
        if r.status_code != 200:
            self.passed = False
            self.fail_reasons.append('Web Service not online')

        if "text/xml" not in r.headers["Content-Type"]:
            self.passed = False
            self.fail_reasons.append('Web Service does not return XML')


        #from lxml import etree
        import re
        m = re.search("<ows:Title>(.*)</ows:Title>", r.text)
        if len(m.group(1)) < 5:
            self.passed = False
            self.fail_reasons.append('No title found')

        title = m.group(1)

        # dummy rule 1
        if '_' in title:
            self.passed = False
            self.fail_reasons.append('Title must not contain underscores')

        #
        #   Call the base Rule constructor
        #
        Rule.__init__(self,
                      self.rule_id,
                      self.rule_name,
                      self.rule_business_definition,
                      self.rule_authority,
                      self.rule_functional_definition,
                      self.component_name,
                      self.passed,
                      self.fail_reasons,
                      self.components_total_count,
                      self.components_failed_count,
                      self.failed_components)


