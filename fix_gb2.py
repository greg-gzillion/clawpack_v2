from pathlib import Path
f = Path(r'C:\Users\greg\dev\clawpack_v2\agents\mathematicaclaw\visualization\graph_builder.py')
c = f.read_text(encoding='utf-8')

# Add imports
c = c.replace(
    'import matplotlib.pyplot as plt',
    'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport os'
)

# Replace the exact 2-line pattern
old = '            plt.show(block=True)\n            plt.close()'
new = '            path = "exports/temp_plot.png"\n            plt.savefig(path, dpi=150, bbox_inches="tight")\n            plt.close()\n            os.startfile(path)'
c = c.replace(old, new)

f.write_text(c, encoding='utf-8')
print('Fixed')
