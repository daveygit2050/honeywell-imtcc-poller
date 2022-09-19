import sys
import pytest

import honeywell_imtcc_poller

def test_main(mocker):
    mocker.patch.object(sys, "argv", ["poll-honeywell", "--help"])
    with pytest.raises(SystemExit) as system_exit:
        honeywell_imtcc_poller.run_cli()
    assert system_exit.value.code == 0
