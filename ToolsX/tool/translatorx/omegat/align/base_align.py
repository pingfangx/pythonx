class BaseAlign:
    name = ''
    print_info = False

    def align(self, source, target) -> dict:
        self.align_start(source, target)
        translation = self.align_inner(source, target)
        self.align_finish(translation)
        return translation

    def align_inner(self, source, target) -> dict:
        raise NotImplementedError(f'method of {self.__class__.__name__} not implemented')

    def align_start(self, source, target):
        if self.print_info:
            print(f'对齐{self.name}\n{source}\n{target}')

    def align_finish(self, translation):
        if self.print_info:
            print(f'{self.name}对齐结果{len(translation)} 项')
