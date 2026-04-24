import os
import unittest
from unittest.mock import Mock, patch

from lex_client import interpret_query


class LexClientTest(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "LEX_BOT_ID": "bot-id",
            "LEX_BOT_ALIAS_ID": "alias-id",
            "LEX_LOCALE_ID": "en_US",
        },
        clear=True,
    )
    @patch("lex_client._boto3_client")
    def test_interpret_query_reads_keywords_from_lex_slots(self, mock_boto3_client):
        client = Mock()
        client.recognize_text.return_value = {
            "sessionState": {
                "intent": {
                    "slots": {
                        "KeywordOne": {
                            "value": {"interpretedValue": "trees"}
                        }
                    }
                }
            }
        }
        mock_boto3_client.return_value = client

        self.assertEqual(interpret_query("show me trees"), ["trees"])
        mock_boto3_client.assert_called_once_with("lexv2-runtime")
        client.recognize_text.assert_called_once_with(
            botId="bot-id",
            botAliasId="alias-id",
            localeId="en_US",
            sessionId="photo-search-session",
            text="show me trees",
        )

    @patch.dict(
        os.environ,
        {
            "LEX_BOT_ID": "bot-id",
            "LEX_BOT_ALIAS_ID": "alias-id",
            "LEX_LOCALE_ID": "en_US",
        },
        clear=True,
    )
    @patch("lex_client._boto3_client")
    def test_interpret_query_reads_two_keywords_from_lex_slots(
        self, mock_boto3_client
    ):
        client = Mock()
        client.recognize_text.return_value = {
            "sessionState": {
                "intent": {
                    "slots": {
                        "KeywordOne": {
                            "value": {"interpretedValue": "trees"}
                        },
                        "KeywordTwo": {
                            "value": {"interpretedValue": "birds"}
                        },
                    }
                }
            }
        }
        mock_boto3_client.return_value = client

        self.assertEqual(
            interpret_query("show me photos with trees and birds in them"),
            ["trees", "birds"],
        )

    @patch.dict(
        os.environ,
        {
            "LEX_BOT_ID": "bot-id",
            "LEX_BOT_ALIAS_ID": "alias-id",
            "LEX_LOCALE_ID": "en_US",
        },
        clear=True,
    )
    @patch("lex_client._boto3_client")
    def test_interpret_query_falls_back_to_message_content(self, mock_boto3_client):
        client = Mock()
        client.recognize_text.return_value = {
            "messages": [
                {"content": "trees and birds"}
            ]
        }
        mock_boto3_client.return_value = client

        self.assertEqual(interpret_query("show me photos with trees and birds"), ["trees", "birds"])

    def test_interpret_query_with_empty_input(self):
        self.assertEqual(interpret_query(""), [])
        self.assertEqual(interpret_query(None), [])

    @patch.dict(os.environ, {}, clear=True)
    def test_interpret_query_requires_lex_environment_variables(self):
        with self.assertRaisesRegex(RuntimeError, "Missing Lex configuration"):
            interpret_query("trees")


if __name__ == "__main__":
    unittest.main()
