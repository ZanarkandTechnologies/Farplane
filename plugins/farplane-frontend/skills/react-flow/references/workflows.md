# React Flow Workflows

## 1. Custom Node Implementation
```javascript
import { Handle, Position } from 'reactflow';

function CustomNode({ data }) {
  return (
    <div className="custom-node">
      <Handle type="target" position={Position.Top} />
      <div>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
```

## 2. Handling Connections
Use the `addEdge` utility to manage new connections between nodes.
```javascript
const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);
```

