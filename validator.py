import fbx


def load_fbx(file_path):
    manager = fbx.FbxManager.Create()

    ios = fbx.FbxIOSettings.Create(manager, fbx.IOSROOT)
    manager.SetIOSettings(ios)

    importer = fbx.FbxImporter.Create(manager, "")

    if not importer.Initialize(file_path, -1, manager.GetIOSettings()):
        error = importer.GetStatus().GetErrorString()
        raise Exception(f"Import failed: {error}")

    scene = fbx.FbxScene.Create(manager, "scene")

    importer.Import(scene)
    importer.Destroy()

    return manager, scene


def traverse_scene(scene):
    result = []

    def traverse(node, depth=0):
        if not node:
            return

        name = node.GetName()
        attr = node.GetNodeAttribute()

        attr_type = "None"

        if attr:
            attr_type = attr.GetAttributeType()

        result.append(f"{' ' * depth} - {name} (type: {attr_type})")

        for i in range(node.GetChildCount()):
            traverse(node.GetChild(i), depth + 1)

    root = scene.GetRootNode()
    traverse(root)

    return result


def get_mesh_nodes(scene):
    mesh_nodes=[]

    def traverse(node):
        if not node:
            return

        attr = node.GetNodeAttribute()

        if attr:
            try:
                is_mesh = attr.GetAttributeType() == fbx.FbxNodeAttribute.EType.eMesh
            except:
                is_mesh = attr.GetAttributeType() == 2

            if is_mesh:
                mesh_nodes.append(node)

        for i in range(node.GetChildCount()):
            traverse(node.GetChild(i))

    root = scene.GetRootNode()
    traverse(root)

    return mesh_nodes


def process_file(file_path,process_type, output_path = None, axis=None):
    manager,scene = load_fbx(file_path)

    try:
        if process_type == "analyze":
            return traverse_scene(scene)

        elif process_type == "find_meshes":
            meshes = get_mesh_nodes(scene)
            return [m.GetName() for m in meshes]

        elif process_type == 'export_all':
            pass

    finally:
        manager.Destroy()