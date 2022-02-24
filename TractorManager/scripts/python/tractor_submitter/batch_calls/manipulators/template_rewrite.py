import sys
import os


def rewrite(base_path, template_cmd, incoming):

    template_path_dir = os.path.dirname(base_path)
    open_template = open(template_cmd)
    list_of_lines = open_template.readlines()

    for i, line in enumerate(list_of_lines):
        if "template_nodes = []" in line:
            list_of_lines[i] = "    template_nodes = {}\n".format(incoming)
            # print(list_of_lines)

    # replace the content in the templates_nodes variables
    # with the nodes that need to be rendered online
    # write the file in /tmp/temporary...

    # if "OpenGL" in template_cmd:
    template_path = os.path.join(template_path_dir, "CallWithHip.py")

    new_temporary_script = open(template_path, "w")
    new_temporary_script.writelines(list_of_lines)
    new_temporary_script.close()


if __name__ == "__main__":

    batch_calls_path = sys.argv[1]
    template_cmd_path = sys.argv[2]
    incoming_node_info = sys.argv[3:]

    print(batch_calls_path)
    print(template_cmd_path)
    print(incoming_node_info)

    rewrite(batch_calls_path, template_cmd_path, incoming_node_info)
