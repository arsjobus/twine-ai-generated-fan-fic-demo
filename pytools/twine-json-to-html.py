import json
import uuid

def build_twine_html(data):
    title = data["name"]
    nodes = data["nodes"]

    node_map = {n["id"]: n for n in nodes}

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{title}</title></head>
<body>

<tw-storydata name="{title}" startnode="1" format="Harlowe" format-version="3.3.9">
"""

    pid_map = {}
    pid = 1

    # SORT BY DEPTH (THIS FIXES VISUAL LAYOUT)
    nodes_sorted = sorted(nodes, key=lambda x: (x["depth"], x["type"]))

    for node in nodes_sorted:
        pid_map[node["id"]] = pid
        pid += 1

    for node in nodes_sorted:
        tags = " ".join(node.get("tags", []))
        text = node.get("text", "")

        # convert links safely
        for target_id in node.get("links", []):
            if target_id in node_map:
                target_name = node_map[target_id]["name"]
                text += f'\n[[Next->{target_name}]]'

        html += f"""
<tw-passagedata pid="{pid_map[node['id']]}" name="{node['name']}" tags="{tags}">
{text}
</tw-passagedata>
"""

    html += """
</tw-storydata>
</body>
</html>
"""
    return html


def export_graphviz(data, out_file="graph.dot"):
    nodes = data["nodes"]

    lines = ["digraph Twine {", "rankdir=LR;"]

    for n in nodes:
        for link in n.get("links", []):
            lines.append(f'"{n["name"]}" -> "{link}";')

    lines.append("}")

    with open(out_file, "w") as f:
        f.write("\n".join(lines))


def compile(json_path, output_html):
    with open(json_path, "r") as f:
        data = json.load(f)

    html = build_twine_html(data)

    with open(output_html, "w") as f:
        f.write(html)

    # optional debug graph
    export_graphviz(data)

    print("Build complete.")


if __name__ == "__main__":
    import sys
    compile(sys.argv[1], sys.argv[2])