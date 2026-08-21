import unittest

from app.utils import markdown_to_telegram_html
from app.services.llm_service import LLMService


class ModelSelectionTests(unittest.TestCase):
    def setUp(self):
        self.service = LLMService(default_model_alias="light")

    def test_aliases_are_resolved(self):
        self.assertEqual(self.service.resolve_model_name("standard"), "gemma4:e4b")
        self.assertEqual(self.service.resolve_model_name("light"), "gemma4:e2b")
        self.assertEqual(self.service.resolve_model_name("cloud"), "gemma4:31b-cloud")
        self.assertEqual(self.service.resolve_model_name("gemma4:e2b"), "gemma4:e2b")

    def test_active_model_is_single_user_state(self):
        self.service.set_active_model("light", chat_id=100)
        self.assertEqual(self.service.get_active_model(chat_id=100), "gemma4:e2b")
        self.assertEqual(self.service.get_active_model(chat_id=200), "gemma4:e2b")

        self.service.set_active_model("standard", chat_id=200)
        self.assertEqual(self.service.get_active_model(chat_id=100), "gemma4:e4b")
        self.assertEqual(self.service.get_active_model(chat_id=200), "gemma4:e4b")

    def test_agent_object_is_reused_until_model_changes(self):
        first_agent = self.service.agent

        # Default model is already light, so selecting light should keep same object.
        self.service.set_active_model("light")
        self.assertIs(self.service.agent, first_agent)

        self.service.set_active_model("cloud")
        self.assertEqual(self.service.get_active_model(), "gemma4:31b-cloud")
        self.assertIsNot(self.service.agent, first_agent)

        second_agent = self.service.agent
        self.service.set_active_model("cloud")
        self.assertIs(self.service.agent, second_agent)

    def test_unknown_model_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.resolve_model_name("gemma")

    def test_markdown_is_converted_for_telegram(self):
        text = "**bold** and *italic* and `code`\n\t- item one\n\t- item two\n# Heading\n```python\nprint('hi')\n```"
        converted = markdown_to_telegram_html(text)

        self.assertIn("<b>bold</b>", converted)
        self.assertIn("<i>italic</i>", converted)
        self.assertIn("<code>code</code>", converted)
        self.assertIn("• item one", converted)
        self.assertIn("<b>Heading</b>", converted)
        self.assertIn("<pre>print(&#x27;hi&#x27;)</pre>", converted)
        self.assertNotIn("\t- item one", converted)
        self.assertNotIn("\t- item two", converted)


if __name__ == "__main__":
    unittest.main()
