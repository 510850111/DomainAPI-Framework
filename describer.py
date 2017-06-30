import json
from types import SimpleNamespace as Namespace


class Describer(object):
    """将km文件转化为python对象，并遍历生成路由"""

    def json_to_namespace(self, data):
        return json.loads(data, object_hook=lambda d: Namespace(**d))

    def load_describe_file(self, file):
        if file:
            with open(file) as f:
                data = f.read()
        return data

    def load_file(self, filename):
        self.raw_data = self.load_describe_file(filename)
        self.tree = self.json_to_namespace(self.raw_data)

    def __init__(self, filename):
        self.load_file(filename)
        self._route = []
        self.traversal(self.tree)

    def get_children(self, root):
        return root.children

    def traversal(self, tree):
        """
        遍历数据并生成路由路径
        """
        data = None
        if 'data' in dir(tree):
            data = tree.data
            self.make_a_route(self._route, data)
        if 'children' in dir(tree):
            self._route.append(data)
            tree = self.get_children(tree)
        if isinstance(tree, (list, set)):
            for t in tree:
                self.traversal(t)
            self._route.remove(data)

    def make_a_route(self, route, data):
        print([r.text for r in route])
        print(data.text)
        if "note" in dir(data):
            note = self.json_to_namespace(data.note)
            print(note)

if __name__ == '__main__':
    des = Describer('Gateway.km')
    des.traversal(des.tree.root)
