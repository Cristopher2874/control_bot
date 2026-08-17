import unittest

from llm_service import get_active_model, set_active_model, resolve_model_name


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


if __name__ == "__main__":
    unittest.main()
