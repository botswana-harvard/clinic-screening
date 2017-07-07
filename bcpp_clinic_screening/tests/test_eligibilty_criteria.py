import unittest

from django.apps import apps as django_apps
from django.test import tag

from edc_constants.constants import YES, NO, POS, NEG, IND, UNK

from ..eligibility import AgeEvaluator, CitizenshipEvaluator
from ..eligibility import LiteracyEvaluator, Eligibility
from bcpp_clinic_screening.eligibility import HivStatusEvaluator


@tag('eligibility')
class TestClinicEligibility(unittest.TestCase):

    def test_eligibility_invalid_age_in_years(self):
        app_config = django_apps.get_app_config('bcpp_clinic_screening')

        age_evaluator = AgeEvaluator(
            age=app_config.eligibility_age_adult_lower - 1)
        self.assertFalse(age_evaluator.eligible)

        age_evaluator = AgeEvaluator(
            age=app_config.eligibility_age_adult_lower)
        self.assertTrue(age_evaluator.eligible)

        age_evaluator = AgeEvaluator(
            age=app_config.eligibility_age_adult_upper)
        self.assertTrue(age_evaluator.eligible)

        age_evaluator = AgeEvaluator(
            age=app_config.eligibility_age_adult_upper + 1)
        self.assertFalse(age_evaluator.eligible)

    def test_eligibility_invalid_age_in_years_reasons(self):
        age_evaluator = AgeEvaluator(age=15)
        self.assertIn('age<18', age_evaluator.reason)
        age_evaluator = AgeEvaluator(age=100)
        self.assertIn('age>64', age_evaluator.reason)

    def test_eligibility_citizen(self):
        """Assert not a citizen, not legally married to a citizen, is not eligible.
        """
        citizenship_evaluator = CitizenshipEvaluator(citizen=YES)
        self.assertTrue(citizenship_evaluator.eligible)

    def test_eligibility_not_acitizen(self):
        """Assert not a citizen, not legally married to a citizen, is not eligible.
        """
        citizenship_evaluator = CitizenshipEvaluator(
            citizen=NO, legal_marriage=NO)
        self.assertFalse(citizenship_evaluator.eligible)

    def test_eligibility_not_acitizen1(self):
        """Assert not a citizen, legal married to a citizen and has marriage
        certificate is eligible.
        """
        citizenship_evaluator = CitizenshipEvaluator(
            citizen=NO, marriage_certificate=YES, legal_marriage=YES)
        self.assertTrue(citizenship_evaluator.eligible)

    def test_eligibility_not_acitizen2(self):
        """Assert not a citizen, legal married to a citizen and has marriage
        certificate is eligible.
        """
        citizenship_evaluator = CitizenshipEvaluator(
            citizen=NO, marriage_certificate=NO, legal_marriage=YES)
        self.assertFalse(citizenship_evaluator.eligible)

    def test_eligibility_literacy(self):
        """Assert literate participant is eligible.
        """
        literacy_evaluator = LiteracyEvaluator(literate=YES)
        self.assertTrue(literacy_evaluator.eligible)

    def test_eligibility_literacy1(self):
        """Assert illerate, no guardian is not eligible.
        """
        literacy_evaluator = LiteracyEvaluator(
            literate=NO, guardian=NO)
        self.assertFalse(literacy_evaluator.eligible)
        self.assertTrue(literacy_evaluator.reason)

    def test_eligibility_literacy2(self):
        """Assert illerate, no guardian is not eligible.
        """
        literacy_evaluator = LiteracyEvaluator(
            literate=NO, guardian=None)
        self.assertFalse(literacy_evaluator.eligible)
        self.assertTrue(literacy_evaluator.reason)

    def test_eligibility_literacy3(self):
        """ Assert literate with guardian is eligible.
        """
        literacy_evaluator = LiteracyEvaluator(
            literate=NO, guardian=YES)
        self.assertTrue(literacy_evaluator.eligible)

    def test_hiv_status_evaluator(self):
        """ Assert hiv status POS is eligible.
        """
        hiv_status_evaluator = HivStatusEvaluator(hiv_status=POS)
        self.assertTrue(hiv_status_evaluator.eligible)

    def test_hiv_status_evaluator2(self):
        """ Assert hiv status POS is eligible.
        """
        hiv_status_evaluator = HivStatusEvaluator(hiv_status=NEG)
        self.assertFalse(hiv_status_evaluator.eligible)

    def test_eligibility(self):
        """ Assert within age range and literate is eligible.
        """
        obj = Eligibility(
            age=25,
            literate=YES,
            guardian=None,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertTrue(obj.eligible)

    def test_eligibility_reason(self):
        """ Assert within age range and literate is eligible.
        """
        obj = Eligibility(
            age=25,
            literate=YES,
            guardian=None,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertTrue(obj.eligible)
        self.assertEqual(obj.reasons, [])

    def test_eligibility1(self):
        """ Assert within age range and literate is eligible.
        """
        obj = Eligibility(
            age=18,
            literate=YES,
            guardian=None,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertTrue(obj.eligible)
        self.assertEqual(obj.reasons, [])

    def test_eligibility2(self):
        """ Assert within age range and not literate with guardian is eligible.
        """
        obj = Eligibility(
            age=64,
            literate=NO,
            guardian=YES,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertTrue(obj.eligible)
        self.assertEqual(obj.reasons, [])

    def test_eligibility3(self):
        """ Assert not a citizen, legal married to a citizen and marriage
            certificates available is eligible.
        """
        obj = Eligibility(
            age=64,
            literate=NO,
            guardian=YES,
            legal_marriage=YES,
            marriage_certificate=YES,
            citizen=NO,
            hiv_status=POS)
        self.assertTrue(obj.eligible)
        self.assertEqual(obj.reasons, [])

    def test_eligibility_not_eligible(self):
        """ Assert less than age range is not eligible.
        """
        obj = Eligibility(
            age=15,
            literate=YES,
            guardian=None,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertFalse(obj.eligible)
        self.assertIn('age<18', obj.reasons[0])

    def test_eligibility_not_eligible1s(self):
        """ Assert illiterate and no guardian is not eligible.
        """
        obj = Eligibility(
            age=16,
            literate=NO,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertFalse(obj.eligible)
        self.assertIn('Illiterate', obj.reasons[0])

    def test_eligibility_hiv_status(self):
        """ Assert hiv status POS is eligible.
        """
        obj = Eligibility(
            age=64,
            literate=NO,
            guardian=YES,
            legal_marriage=NO,
            marriage_certificate=NO,
            citizen=YES,
            hiv_status=POS)
        self.assertTrue(obj.eligible)
        self.assertEqual(obj.reasons, [])

    def test_eligibility_hiv_status2(self):
        """ Assert hiv status not POS is not eligible.
        """
        hiv_status_values = [NEG, IND, UNK, 'not_answering']
        for hiv_status in hiv_status_values:
            obj = Eligibility(
                age=64,
                literate=NO,
                guardian=YES,
                legal_marriage=NO,
                marriage_certificate=NO,
                citizen=YES,
                hiv_status=hiv_status)
            self.assertFalse(obj.eligible)
        self.assertIn('Not a positive participant', obj.reasons[0])
