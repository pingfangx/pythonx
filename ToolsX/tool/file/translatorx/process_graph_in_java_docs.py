import re


class Utils:
    def process_graph_in_java_docs(self, text: str):
        """去掉前面的注释，合并行"""
        lines = text.splitlines()
        for i, line in enumerate(lines):
            line = re.sub(r'/?\s*\*/?', '', line)
            lines[i] = line
        print(''.join(lines))


if __name__ == '__main__':
    Utils().process_graph_in_java_docs(
        text="""
        """
    )
