import datetime
import pytest

from comanage_nacha import TransactionCodes
from comanage_nacha.entries.entrybase import EntryBase
from comanage_nacha.exceptions import EntryClosedError
from comanage_nacha.nacha_file import NachaFile


def test_add_batch():
    nacha = NachaFile()
    assert len(nacha.batches) == 0
    batch = nacha.add_batch()
    assert len(nacha.batches) == 1
    assert nacha.batches == [batch]


def test_calculate_entry_addenda_record_count():
    nacha = NachaFile()
    batch = nacha.add_batch()
    batch.add_entry()
    assert nacha.calculate_entry_addenda_record_count() == 1
    batch.add_entry().add_addenda()
    assert nacha.calculate_entry_addenda_record_count() == 3


def test_calculate_block_count():
    nacha = NachaFile()
    assert nacha.calculate_block_count() == 1
    batch = nacha.add_batch()
    assert nacha.calculate_block_count() == 1
    batch.add_entry()
    assert nacha.calculate_block_count() == 1
    for _ in range(100):
        batch.add_entry()
    assert nacha.calculate_block_count() == 11


def test_file_control():
    nacha = NachaFile()
    nacha.close()
    assert nacha.file_control is not None
    assert nacha.file_control.code == '9'
    assert nacha.file_control.batch_count == 0
    assert nacha.file_control.block_count == 1
    assert nacha.file_control.entry_addenda_record_count == 0
    assert nacha.file_control.entry_hash_total == '0'
    assert nacha.file_control.total_file_credit_entry_amount == 0
    assert nacha.file_control.total_file_debit_entry_amount == 0
    nacha = NachaFile()
    batch = nacha.add_batch()
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=TransactionCodes.CHECKING_CREDIT,
                    amount=10000)
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=TransactionCodes.CHECKING_CREDIT,
                    amount=10000)
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=TransactionCodes.CHECKING_DEBIT,
                    amount=33300)
    batch.close()
    nacha.close()
    assert nacha.file_control.batch_count == 1
    assert nacha.file_control.block_count == 1
    assert nacha.file_control.entry_addenda_record_count == 3
    assert nacha.file_control.entry_hash_total == '37037034'
    assert nacha.file_control.total_file_credit_entry_amount == 20000
    assert nacha.file_control.total_file_debit_entry_amount == 33300


def test_cannot_add_batch_after_close():
    nacha = NachaFile()
    nacha.close()
    with pytest.raises(EntryClosedError):
        nacha.add_batch()


def test_lines():
    nacha = NachaFile()
    nacha.close()
    assert len(list(nacha.lines)) == 2
    nacha.file_control = None
    batch = nacha.add_batch()
    batch.close()
    nacha.close()
    assert len(list(nacha.lines)) == 4
    nacha.file_control = batch.batch_control = None
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=TransactionCodes.CHECKING_CREDIT,
                    amount=10000)
    batch.close()
    nacha.close()
    assert len(list(nacha.lines)) == 5
    nacha.file_control = batch.batch_control = None
    batch.add_entry(receiving_dfi_routing_number='12345678', transaction_code=TransactionCodes.CHECKING_CREDIT,
                    amount=10000).add_addenda()
    batch.close()
    nacha.close()
    assert len(list(nacha.lines)) == 7
    assert all(isinstance(line, EntryBase) for line in nacha.lines)
