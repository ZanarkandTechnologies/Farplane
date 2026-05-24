# Data Viz Architecture

## Tool Selection Logic
- **Recharts**: Best for rapid dashboard development and standard UI-integrated charts. Uses SVG and React-friendly syntax.
- **D3.js**: Best for bespoke visualizations, force-directed graphs (knowledge graphs), and large-scale data manipulation. Use D3's `scale`, `axis`, and `shape` modules.

## Knowledge Graphs
- Use D3's `d3-force` simulation to position nodes and links.
- Map data nodes to visual elements using a unique identifier (`id`).

