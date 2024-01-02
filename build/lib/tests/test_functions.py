from unittest import TestCase

from textwordcount.functions import TextWordCount


class FunctionsTestCases(TestCase):
    def setUp(self):
        # Source Text found in https://docs.python.org/3/library/unittest.html
        self.english_text = """
            A testcase is created by subclassing unittest.TestCase. 
            The three individual tests are defined with methods whose names start with 
            the letters test. This naming convention informs the test runner about 
            which methods represent tests. The crux of each test is a call 
            to assertEqual() to check for an expected result; assertTrue() or 
            assertFalse() to verify a condition; or assertRaises() to verify that a 
            specific exception gets raised. These methods are used instead of the assert 
            statement so the test runner can accumulate all test 
            results and produce a report.
            The setUp() and tearDown() methods allow you to define instructions 
            that will be executed before and after each test method. 
            They are covered in more detail in the section Organizing test code.
        """
        # Source Text found in https://docs.python.org/es/3/tutorial/
        self.spanish_text = """
            Python es un lenguaje de programación potente y fácil de aprender. 
            Tiene estructuras de datos de alto nivel eficientes y un simple pero 
            efectivo sistema de programación orientado a objetos. La elegante sintaxis 
            de Python y su tipado dinámico, junto a su naturaleza interpretada lo 
            convierten en un lenguaje ideal para scripting y desarrollo rápido de 
            aplicaciones en muchas áreas, para la mayoría de plataformas.
            El intérprete de Python y la extensa librería estándar se encuentran 
            disponibles libremente en código fuente y de forma binaria para la mayoría 
            de las plataformas desde la Web de Python, https://www.python.org/, 
            y se pueden distribuir libremente. El mismo sitio también contiene 
            distribuciones y referencias a muchos módulos libres de Python de terceros, 
            programas, herramientas y documentación adicional.
            El intérprete de Python es fácilmente extensible con funciones y tipos de 
            datos implementados en C o C++ (u otros lenguajes que permitan ser 
            llamados desde C). Python también es apropiado como un lenguaje para 
            extender aplicaciones modificables.
        """
        self.text_word_count_object_english = TextWordCount(text=self.english_text)
        self.text_word_count_object_spanish = TextWordCount(
            text=self.spanish_text, language="spanish"
        )

    def test_process_text_english_language(self):
        simple_text = (
            "This naming convention informs the test runner about "
            "which methods represent tests"
        )
        t = TextWordCount(text=simple_text)
        _result = t.process_text()
        expected = [
            "naming",
            "convention",
            "informs",
            "test",
            "runner",
            "method",
            "represent",
            "test",
        ]
        self.assertListEqual(sorted(_result), sorted(expected))

    def test_process_text_spanish_language(self):
        simple_text = (
            "Python también es apropiado como un lenguaje para "
            "extender aplicaciones modificables"
        )
        t = TextWordCount(text=simple_text, language="spanish")
        _result = t.process_text()
        expected = [
            "Python",
            "apropiado",
            "lenguaje",
            "extender",
            "aplicaciones",
            "modificables",
        ]
        self.assertListEqual(sorted(_result), sorted(expected))

    def test_top_used_words(self):
        top_five_used_words = self.text_word_count_object_english.top_used_words(
            count=5
        )
        # Appearance in the text:
        # {'test': 7, 'runner': 2, 'result': 1, 'verify': 2, 'method': 1}
        expected = ["test", "runner", "result", "verify", "method"]
        self.assertListEqual(sorted(top_five_used_words), sorted(expected))

    def test_find_most_used_noun_in_text(self):
        noun = self.text_word_count_object_english.find_most_used_by_pos(
            pos_list=["NN"], count=1
        )
        self.assertEqual(noun[0], "test")

    def test_count_word_usage_in_text(self):
        _count_dict = self.text_word_count_object_english.count_word_usage_in_text(
            ["test", "code"]
        )
        expected = {"test": 7, "code": 1}
        self.assertDictEqual(_count_dict, expected)

    def test_count_word_usage_in_text_spanish(self):
        _count_dict = self.text_word_count_object_spanish.count_word_usage_in_text(
            ["Python", "c", "c++"]
        )
        expected = {"python": 7, "c": 2, "c++": 1}
        self.assertDictEqual(_count_dict, expected)

    def test_find_sentences_containing_word_or_phrase(self):
        sentences = (
            self.text_word_count_object_english.find_sentences_contain_word_or_phrase(
                "test code"
            )
        )
        self.assertEqual(len(sentences), 1)
        self.assertEqual(
            sentences[0],
            "They are covered in more detail in the section Organizing test code.",
        )

    def test_find_sentences_contain_word_or_phrase_spanish(self):
        sentences = (
            self.text_word_count_object_spanish.find_sentences_contain_word_or_phrase(
                "programación"
            )
        )
        self.assertEqual(len(sentences), 2)
        for sentence in sentences:
            self.assertTrue("programación" in sentence)

    def test_word_count_from_url_source(self):
        url = "https://docs.python.org/es/3/tutorial/"
        t = TextWordCount(html_source=url, language="spanish")
        _count_dict = t.count_word_usage_in_text(["Python", "tutorial"])
        self.assertSetEqual(set(list(_count_dict.keys())), {"python", "tutorial"})

    def test_find_sentences_contain_word_or_phrase_from_url(self):
        url = "https://docs.python.org/3/tutorial/"
        t = TextWordCount(html_source=url)
        _sentences = t.find_sentences_contain_word_or_phrase(
            "standard objects and modules"
        )
        self.assertEqual(len(_sentences), 1)
        self.assertEqual(
            _sentences[0],
            "For a description of standard objects and modules, see The Python Standard Library.",
        )
