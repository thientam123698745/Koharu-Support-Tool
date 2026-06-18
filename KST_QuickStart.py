import argparse
import subprocess

def run_translate(port):
    subprocess.run(["python", "KST1_ExportScene.py", str(port)])
    subprocess.run(["python", "KST2_exactNotTranslate.py"])
    subprocess.run(["python", "KST2-5_PreTranslate.py"])
    subprocess.run(["python", "KST3_translate.py"])
    subprocess.run(["python", "KST4_Modify.py", str(port)])
    subprocess.run(["python", "KST5_SendTranslate.py", str(port)])
    subprocess.run(["python", "KST6_RenderAllTranslatedPage.py", str(port)])

def run_inpaint(port):
    subprocess.run(["python", "KST9_ExactNode.py"])
    subprocess.run(["python", "KST10_GetSource.py", str(port)])
    subprocess.run(["python", "KST11_Getsegment.py", str(port)])
    subprocess.run(["python", "KST12_Inpaint.py"])
    subprocess.run(["python", "KST13_Inpaint2.py"])
    subprocess.run(["python", "KST14_PutBlush.py"])

def run_transform(port):
    subprocess.run(["python", "KST15_ExactTransform.py"])
    subprocess.run(["python", "KST16_ModifyTransform.py"])
    subprocess.run(["python", "KST17_SendTransform.py", str(port)])

def run_export(port):
    subprocess.run(["python", "KST1_ExportScene.py", str(port)])
    subprocess.run(["python", "KST18_exactPageInfo.py", str(port)])
    subprocess.run(["python", "KST19_RenderAllPage.py", str(port)])
    subprocess.run(["python", "KST20_ExportRendered.py", str(port)])

def main():
    parser = argparse.ArgumentParser(description="Run KST pipeline tasks")
    parser.add_argument("task", choices=["translate", "inpaint", "transform", "export", "all"],
                        help="Chọn tác vụ cần chạy")
    parser.add_argument("--port", type=int, default=4000,
                        help="Port để kết nối server (mặc định: 4000)")
    args = parser.parse_args()

    if args.task == "translate":
        run_translate(args.port)
    elif args.task == "inpaint":
        run_inpaint(args.port)
    elif args.task == "transform":
        run_transform(args.port)
    elif args.task == "export":
        run_export(args.port)
    elif args.task == "all":
        run_translate(args.port)
        run_inpaint(args.port)
        run_transform(args.port)

if __name__ == "__main__":
    main()
