from ruleset import RuleSet
from rule import Rule


class GaOgcWs(RuleSet):
    """
    GA OGC rules
    """
    def __init__(self):
        ruleset_id = 'ga_ogcws'
        ruleset_name = 'GA OGC WS'
        passed = True
        rules_results = []

        # make a Graph from the string or file


        #
        #   Run all the rules
        #
        service_pass = r'http://services.ga.gov.au/gis/services/NEXIS_Building_Exposure/MapServer/WFSServer?request=GetCapabilities'
        service_fail = r'http://www.ga.gov.au/gis/services/topography/National_Ferry_Terminals/MapServer/WFSServer?request=GetCapabilities'

        #rules_results.append(GaTitle(service_pass).get_result())
        rules_results.append(GaTitle(service_pass).get_result())

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


class GaTitle(Rule):
    #Base constructor:
    #   id,                     name,                       business_definition,    authority,
    #   functional_definition,  component_name,             passed,                 fail_reasons,
    #   components_total_count, components_failed_count,    failed_components
    def __init__(self, service_get_caps_uri):
        #
        #   Rule details
        #
        self.rule_id = 'GaTitle'
        self.rule_name = 'WS Has a GA-compliant title'
        self.rule_business_definition = '...according to the policy'
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


if __name__ == "__main__":
    g = GaOgcWs()
    print g.get_result()