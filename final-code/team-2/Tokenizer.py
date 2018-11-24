class Tokenizer:

    def parse(self, root, tokens=[]):
        """Return token sequence from ast"""
        if root:
            kind = root['Kind']
            if kind == 'While':
                tokens.append('while')
                self.parse(root['Condition'], tokens)
                tokens.extend(['do', '{'])
                self.parse(root['Body'], tokens)
                tokens.append('}')
            elif kind == 'If':
                tokens.append('if')
                self.parse(root['Condition'], tokens)
                tokens.extend(['then', '{'])
                self.parse(root['Then'], tokens)
                tokens.extend(['}', 'else', '{'])
                self.parse(root['Else'], tokens)
                tokens.append('}')
            elif kind == 'Declare':
                tokens.extend([root['Label'], root['Var']])
            elif kind == 'Int':
                tokens.append(root['Value'])
            elif kind == 'Var':
                tokens.append(root['Name'])
            elif kind == 'Seq':
                self.parse(root['Left'], tokens)
                tokens.append(';')  # without space
                self.parse(root['Right'], tokens)
            else:
                tokens.append('(')
                self.parse(root['Left'], tokens)
                tokens.append(self.get_operator_symbol(root['Kind']))
                self.parse(root['Right'], tokens)
                tokens.append(')')
        return tokens

    def get_operator_symbol(self, kind):
        """Return operator symbol from kind"""
        if kind == 'Assign':
            return ':='
        elif kind == 'Seq':
            return '; '
        elif kind == 'Add':
            return '+'
        elif kind == 'Sub':
            return '-'
        elif kind == 'Equal':
            return '=='
        elif kind == 'Less':
            return '<'
        else:
            raise RuntimeError("Unknown kind {}".format(kind))
