import os
import sys
from grpc_tools import protoc

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOS_DIR = os.path.join(PROJECT_ROOT, "protos")
OUT_DIR = os.path.join(PROJECT_ROOT, "app", "rpc", "generated")

def generate_protos():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
        with open(os.path.join(OUT_DIR, "__init__.py"), "w") as f:
            f.write("")

    print(f"Generating protos from {PROTOS_DIR} to {OUT_DIR}...")

    proto_files = [f for f in os.listdir(PROTOS_DIR) if f.endswith(".proto")]

    if not proto_files:
        print("No .proto files found!")
        return

    for proto_file in proto_files:
        full_path = os.path.join(PROTOS_DIR, proto_file)

        command = [
            "grpc_tools.protoc",
            f"-I{PROTOS_DIR}",
            f"--python_out={OUT_DIR}",
            f"--grpc_python_out={OUT_DIR}",
            full_path
        ]

        exit_code = protoc.main(command)

        if exit_code != 0:
            print(f"Error generating {proto_file}")
            sys.exit(exit_code)

    print("Done! Fixing imports...")
    fix_imports(OUT_DIR)
    print("Success.")

def fix_imports(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content.replace("import pricing_pb2", "from . import pricing_pb2")

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

if __name__ == "__main__":
    generate_protos()