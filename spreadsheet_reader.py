import pandas as pd


def remove_duplicates(source):
    seen = set()  # Create a set to track seen elements
    unique_array = []
    for element in source:
        # Check if element is hashable (not a list in this case)
        if not isinstance(element, list):
            # If element is hashable (likely a non-list type)
            if element not in seen:
                seen.add(element)
                unique_array.append(element)
        else:
            # If element is a list, process its elements individually
            for inner_element in element:
                if inner_element not in seen:
                    seen.add(inner_element)
                    unique_array.append(inner_element)
    return unique_array


class CSVReader:
    def __init__(self, filename, columns: list[str]):
        self.filename = filename
        self.target_columns = columns

    def read_target(self):
        df = pd.read_csv(self.filename, delimiter=';')
        target = []
        for target_column in self.target_columns:
            if target_column in df.columns:
                target.append(df[target_column].to_list())

        return remove_duplicates(target)
