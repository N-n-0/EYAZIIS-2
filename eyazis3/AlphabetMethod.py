from Document import Document


class AlphabetMethod:
    def __init__(self, russian_doc_path: str, german_doc_path: str) -> None:
        self.russian_alphabet = self.get_alphabet(
            self.get_text(russian_doc_path))
        self.german_alphabet = self.get_alphabet(
            self.get_text(german_doc_path))

    def get_language(self, file_path: str):
        alphabet = self.get_alphabet(self.get_text(file_path))

        test_len = len(alphabet)
        ger_intersect_len = len(alphabet.intersection(self.german_alphabet))
        rus_intersect_len = len(alphabet.intersection(self.russian_alphabet))

        ger_measure = ger_intersect_len / test_len * 100
        rus_measure = rus_intersect_len / test_len * 100

        if rus_measure > ger_measure:
            return 'russian'
        else:
            return 'german'

    @staticmethod
    def get_alphabet(text: str):
        alphabet = set()

        for sign in text:
            alphabet.add(sign)

        return alphabet

    @staticmethod
    def get_text(document_path: str) -> str:
        return Document(document_path).get_text(document_path)
