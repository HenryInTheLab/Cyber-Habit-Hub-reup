import whois

from ai.services import generate_url_analysis
from common.utils import extract_fields


class UrlValidateService:
   
    def validate(self, url):
        analysis = generate_url_analysis(url)
        return {
            "url": url,
            "details": self.get_domain_info(url),
            **analysis.model_dump(mode="json")
        }
    
    def get_domain_info(self, domain):
        whois_fields = ["domain_name", "registrar", "name_servers"]
        return extract_fields(whois.whois(domain), whois_fields)
    