import unittest

from formatters import markdown_to_telegram_html
from llm_service import get_active_model, resolve_model_name, set_active_model


class ModelSelectionTests(unittest.TestCase):
    def test_aliases_are_resolved(self):
        self.assertEqual(resolve_model_name("gemma"), "gemma4:e4b")
        self.assertEqual(resolve_model_name("light"), "gemma4:e2b")
        self.assertEqual(resolve_model_name("gemma4:e2b"), "gemma4:e2b")

    def test_active_model_can_be_set_per_chat(self):
        chat_id = 42
        set_active_model(chat_id, "light")
        self.assertEqual(get_active_model(chat_id), "gemma4:e2b")

        set_active_model(chat_id, "gemma")
        self.assertEqual(get_active_model(chat_id), "gemma4:e4b")

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
