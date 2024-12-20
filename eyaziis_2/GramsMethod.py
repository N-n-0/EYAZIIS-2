from GramCreator import GramCreator


class GramsMethod:
    def __init__(self, rus_doc_path: str, german_doc_path: str) -> None:
        self.max = 1000
        self.russian_grams = GramCreator(rus_doc_path).sorted_grams
        self.german_grams = GramCreator(german_doc_path).sorted_grams

    def get_measure(self, grams_a: list, grams_b: list):
        measure = 0
        for i in range(len(grams_a)):
            if grams_a[i] in grams_b:
                temp = grams_b.index(grams_a[i])
                measure += temp
            else:
                measure += self.max

        return measure

    def get_language(self, file_path: str):
        grams = GramCreator(file_path).sorted_grams

        russian_measure = self.get_measure(grams, self.russian_grams)
        german_measure = self.get_measure(grams, self.german_grams)

        print(russian_measure)
        print(german_measure)

        if russian_measure < german_measure:
            return 'Russian', russian_measure, german_measure
        else:
            return 'German', russian_measure, german_measure
