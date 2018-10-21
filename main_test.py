import mock

import main


class TestGCFPyGCSSample(object):
    def test_file_upload_trigger(self, capsys):
        event = {
            'bucket': 'some-bucket',
            'name': 'some-filename',
            'metageneration': 'some-metageneration',
            'timeCreated': '0',
            'updated': '0'
        }
        context = mock.MagicMock()
        context.event_id = 'some-id'
        context.event_type = 'gcs-event'

        main.file_upload_trigger(event, context)

        out, _ = capsys.readouterr()

        assert 'some-bucket' in out
        assert 'some-id' in out
