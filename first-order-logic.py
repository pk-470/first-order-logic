from itertools import product


class Symbol:
    def __init__(self, name: str, arity: int):
        self.name = name
        if arity < 0:
            raise Exception("Arity needs to be an integer >= 0.")
        self.arity = arity


class Language:
    def __init__(
        self, function_symbols: set, relation_symbols: set, constant_symbols: set
    ):
        self.function_symbols = function_symbols
        self.relation_symbols = relation_symbols
        self.constant_symbols = constant_symbols
        self.symbols = self.function_symbols.union(
            self.relation_symbols, self.constant_symbols
        )

    def print(self):
        if self.function_symbols:
            print()
            print("Function symbols:")
            print(
                "\n".join(
                    [
                        f"{symbol.name}, of arity {symbol.arity}"
                        for symbol in self.function_symbols
                    ]
                )
            )
        if self.relation_symbols:
            print()
            print("Relation symbols:")
            print(
                "\n".join(
                    [
                        f"{symbol.name}, of arity {symbol.arity}"
                        for symbol in self.relation_symbols
                    ]
                )
            )
        if self.constant_symbols:
            print()
            print("Constant symbols:")
            print("\n".join([symbol.name for symbol in self.constant_symbols]))


class Forall:
    def __init__(self, expression):
        self.expression = expression


class Exists:
    def __init__(self, expression):
        self.expression = expression


class L_Structure:
    def __init__(self, universe: set, language: Language, interpretations: dict):
        if not universe:
            raise Exception("An L-structure must have a non-empty universe.")
        self.universe = universe
        self.language = language
        self.interpretations = interpretations
        try:
            for symbol in self.language.symbols:
                _ = self.interpretations[symbol]
        except:
            raise Exception(
                "Please provide an interpretation for all symbols in the language."
            )
        for symbol in self.language.function_symbols:
            for tuple in cartesian_product(self.universe, symbol.arity):
                if self.interpretations[symbol](tuple) not in self.universe:
                    raise Exception(
                        f"{symbol.name} does not have a valid interpretation."
                    )

    def interpret(self, symbols: set()):
        for symbol in symbols:
            print()
            print(symbol.name + " interpretation:")
            if symbol in self.language.function_symbols:
                print(
                    "\n".join(
                        [
                            f"{symbol.name}{x} = {self.interpretations[symbol](x)}"
                            for x in cartesian_product(self.universe, symbol.arity)
                        ]
                    )
                )
            elif symbol in self.language.relation_symbols:
                print(self.interpretations[symbol])

    def validate(self, sentence):
        if isinstance(sentence, Forall):
            return all(self.validate(sentence.expression(x)) for x in self.universe)
        if isinstance(sentence, Exists):
            return any(self.validate(sentence.expression(x)) for x in self.universe)
        else:
            return sentence

    def is_model_of(self, theory):
        return all([self.validate(sentence) for sentence in theory])


def cartesian_product(set, n):
    if n == 1:
        return set
    else:
        return product(set, repeat=n)


if __name__ == "__main__":
    plus_symbol = Symbol("+", 2)
    inverse_symbol = Symbol("-", 1)
    zero_symbol = Symbol("0", 0)

    group_language = Language(
        function_symbols={plus_symbol, inverse_symbol},
        relation_symbols=set(),
        constant_symbols={zero_symbol},
    )

    universe = {0, 1, 2, 3, 4}
    m = L_Structure(
        universe=universe,
        language=group_language,
        interpretations={
            plus_symbol: lambda x: (x[0] + x[1]) % 5,
            inverse_symbol: lambda y: -y % 5,
            zero_symbol: 0,
        },
    )

    plus = m.interpretations[plus_symbol]
    inverse = m.interpretations[inverse_symbol]
    zero = m.interpretations[zero_symbol]

    theory_of_groups = [
        Forall(
            lambda x: Forall(
                lambda y: Forall(
                    lambda z: plus((x, plus((y, z)))) == plus((plus((x, y)), z))
                )
            )
        ),
        Forall(lambda x: plus((x, inverse(x))) == zero),
        Forall(lambda x: plus((inverse(x), x)) == zero),
        Forall(lambda x: plus((x, zero)) == x),
        Forall(lambda x: plus((zero, x)) == x),
    ]

    print(m.is_model_of(theory_of_groups))
