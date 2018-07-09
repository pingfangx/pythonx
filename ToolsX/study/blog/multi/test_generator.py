class TestGenerator:
    def get_x(self):
        for x in range(10):
            print(f'before generate {x}')
            yield x
            print(f'after generate {x}')

    def main(self):
        for x in self.get_x():
            print(f'before get {x}')
            print(x)
            print(f'after get {x}')


if __name__ == '__main__':
    TestGenerator().main()
