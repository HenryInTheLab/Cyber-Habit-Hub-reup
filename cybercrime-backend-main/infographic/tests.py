from django.test import SimpleTestCase

from infographic.models import FinancialLoss, OnlineBehaviour, Victimisation


class VictimisationSimpleTestCase(SimpleTestCase):
    def setUp(self):
        self.victim = Victimisation(
            tab="Tab1",
            main_type="Fraud",
            subcategory="Online Scam",
            incident_type="Phishing",
            gender="Male",
            age="25-34",
            sme_status="No",
            prevalence_2024=12.5,
            adjusted_2023=10.0,
            adjusted_2024=13.0,
            significant_diff="Yes"
        )

    def test_victimisation_fields(self):
        self.assertEqual(self.victim.tab, "Tab1")
        self.assertEqual(self.victim.main_type, "Fraud")
        self.assertEqual(self.victim.subcategory, "Online Scam")
        self.assertEqual(self.victim.incident_type, "Phishing")
        self.assertEqual(self.victim.gender, "Male")
        self.assertEqual(self.victim.age, "25-34")
        self.assertEqual(self.victim.sme_status, "No")
        self.assertEqual(self.victim.prevalence_2024, 12.5)
        self.assertEqual(self.victim.adjusted_2023, 10.0)
        self.assertEqual(self.victim.adjusted_2024, 13.0)
        self.assertEqual(self.victim.significant_diff, "Yes")

class OnlineBehaviourSimpleTestCase(SimpleTestCase):
    def setUp(self):
        self.behaviour = OnlineBehaviour(
            tab="Tab2",
            behaviour_type="Social Media",
            variable="Posting",
            tech_level="Advanced",
            gender="Female",
            age="35-44",
            sme_status="Yes",
            adjusted_2023=20.0,
            adjusted_2024=22.0
        )

    def test_online_behaviour_fields(self):
        self.assertEqual(self.behaviour.tab, "Tab2")
        self.assertEqual(self.behaviour.behaviour_type, "Social Media")
        self.assertEqual(self.behaviour.variable, "Posting")
        self.assertEqual(self.behaviour.tech_level, "Advanced")
        self.assertEqual(self.behaviour.gender, "Female")
        self.assertEqual(self.behaviour.age, "35-44")
        self.assertEqual(self.behaviour.sme_status, "Yes")
        self.assertEqual(self.behaviour.adjusted_2023, 20.0)
        self.assertEqual(self.behaviour.adjusted_2024, 22.0)

class FinancialLossSimpleTestCase(SimpleTestCase):
    def setUp(self):
        self.loss = FinancialLoss(
            median_type="Median",
            cybercrime="Ransomware",
            value=5000,
            tooltip="Median loss for ransomware"
        )

    def test_financial_loss_fields(self):
        self.assertEqual(self.loss.median_type, "Median")
        self.assertEqual(self.loss.cybercrime, "Ransomware")
        self.assertEqual(self.loss.value, 5000)
        self.assertEqual(self.loss.tooltip, "Median loss for ransomware")