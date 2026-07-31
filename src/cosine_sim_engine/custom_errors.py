class InvalidTop_KError(Exception):
    def __init__(self, value, message="Invalid top-K value"):
        super().__init__(message)
        self.value = value

    def __str__(self):
        if self.value < 1:
            return f"InvalidTop_KError: {self.value} is not a valid top-K value. K must be a positive integer greater than 0."
        else:
            return f"InvalidTop_KError: {self.value} is not a valid top-K value. K must be less than or equal to the number of available labels."

class InvalidLabelColumnError(Exception):
    def __init__(self, label, message="Invalid label column"):
        super().__init__(message)
        self.label = label

    def __str__(self):
        if self.label is None:
            return "InvalidLabelColumnError: The label column must be specified as a valid string and cannot be None."
        else:
            return f"InvalidLabelColumnError: The label column '{self.label}' is not present in the model DataFrame."

class InvalidVectorSizeError(Exception):
    def __init__(self, model_columns, vector_size, message="Invalid input vector"):
        super().__init__(message)
        self.model_columns = model_columns
        self.vector_size = vector_size

    def __str__(self):
        return f"InvalidVectorSizeError: The input vector must have size {self.model_columns} to match the model's feature columns, but got size {self.vector_size}."

class InvalidVectorTypeError(Exception):
    def __init__(self, resulting_type, message="Invalid input vector type"):
        super().__init__(message)
        self.type = resulting_type

    def __str__(self):
        return f"InvalidVectorTypeError: The vector's type is {self.type}. The input vector must be a numpy array, list, pandas Series, or a single-column pandas DataFrame."

