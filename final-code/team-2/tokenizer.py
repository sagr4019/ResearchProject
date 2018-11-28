import sys
sys.path.append('../../data-generation-and-validation/security-type-system')
from codegenerator import get_operator_symbol


class Tokenizer:

    def tokenize(self, root, tokens=[]):
        """Return token sequence from ast"""
        if root:
            kind = root['Kind']
            if kind == 'While':
                tokens.append('while')
                self.tokenize(root['Condition'], tokens)
                # tokens.extend(['do', '{'])
                self.tokenize(root['Body'], tokens)
                # tokens.append('}')
            elif kind == 'If':
                tokens.append('if')
                self.tokenize(root['Condition'], tokens)
                # tokens.extend(['then', '{'])
                self.tokenize(root['Then'], tokens)
                # tokens.extend(['}', 'else', '{'])
                self.tokenize(root['Else'], tokens)
                # tokens.append('}')
            elif kind == 'Declare':
                tokens.extend([root['Label'], root['Var']])
            elif kind == 'Int':
                tokens.append('int')
            elif kind == 'Var':
                tokens.append(root['Name'])
            elif kind == 'Seq':
                self.tokenize(root['Left'], tokens)
                tokens.append(';')  # without space
                self.tokenize(root['Right'], tokens)
            else:
                # tokens.append('(')
                self.tokenize(root['Left'], tokens)
                tokens.append(get_operator_symbol(root['Kind']))
                self.tokenize(root['Right'], tokens)
                # tokens.append(')')
        return tokens
