from schema import RecallRecord
from pydantic import ValidationError
import pytest

def test_valid_us_record_passes():
    record = RecallRecord(
        recall_number="F-0001-2024", status="Terminated", classification="Class I",
        state="FL", country="United States", recalling_firm="Test Co",
        product_description="Test product", reason_for_recall="Test reason",
        voluntary_mandated="Voluntary: Firm initiated",
        recall_initiation_date="20240101", report_date="20240115",
        termination_date="20240201"
    )
    assert record.classification == "Class I"

def test_invalid_classification_rejected():
    with pytest.raises(ValidationError):
        RecallRecord(
            recall_number="F-0002-2024", status="Terminated", classification="Class IV",
            state="FL", country="United States", recalling_firm="Test Co",
            product_description="Test", reason_for_recall="Test",
            voluntary_mandated="Voluntary: Firm initiated",
            recall_initiation_date="20240101", report_date="20240115",
            termination_date="20240201"
        )

def test_malformed_date_rejected():
    with pytest.raises(ValidationError):
        RecallRecord(
            recall_number="F-0003-2024", status="Terminated", classification="Class I",
            state="FL", country="United States", recalling_firm="Test Co",
            product_description="Test", reason_for_recall="Test",
            voluntary_mandated="Voluntary: Firm initiated",
            recall_initiation_date="2024-01-01", report_date="20240115",
            termination_date="20240201"
        )

def test_us_missing_state_rejected():
    with pytest.raises(ValidationError):
        RecallRecord(
            recall_number="F-0004-2024", status="Terminated", classification="Class I",
            state=None, country="United States", recalling_firm="Test Co",
            product_description="Test", reason_for_recall="Test",
            voluntary_mandated="Voluntary: Firm initiated",
            recall_initiation_date="20240101", report_date="20240115",
            termination_date="20240201"
        )

def test_international_missing_state_allowed():
    record = RecallRecord(
        recall_number="F-0005-2024", status="Terminated", classification="Class I",
        state=None, country="Israel", recalling_firm="Test Co",
        product_description="Test", reason_for_recall="Test",
        voluntary_mandated="Voluntary: Firm initiated",
        recall_initiation_date="20240101", report_date="20240115",
        termination_date="20240201"
    )
    assert record.country == "Israel"
