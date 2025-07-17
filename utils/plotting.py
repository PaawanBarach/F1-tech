import re, io, ast
import matplotlib.pyplot as plt
from PIL import Image

def line_plot(x, y, title="Graph", xlabel="X", ylabel="Y"):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return Image.open(buf)

def dynamic_plots(context: str) -> list[Image.Image]:
    images = []
    for m in re.finditer(r"\[([0-9\.\-,\s]+)\]", context):
        try:
            data = ast.literal_eval(f"[{m.group(1)}]")
            if all(isinstance(v, (int, float)) for v in data):
                fig, ax = plt.subplots()
                ax.plot(data, marker='o')
                ax.set_title("Data Series")
                buf = io.BytesIO()
                fig.tight_layout()
                fig.savefig(buf, format="png")
                plt.close(fig)
                buf.seek(0)
                images.append(Image.open(buf))
        except:
            continue
    return images
