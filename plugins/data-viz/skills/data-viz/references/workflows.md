# Data Viz Workflows

## 1. Recharts Simple Bar Chart
```javascript
import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

const MyChart = ({ data }) => (
  <BarChart width={600} height={300} data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
    <Bar dataKey="value" fill="#8884d8" />
  </BarChart>
);
```

## 2. D3 with React (Math Pattern)
Use D3 to calculate paths/scales, but let React render the SVG elements.
```javascript
const xScale = d3.scaleLinear().domain([0, 100]).range([0, width]);
// ... in JSX ...
<circle cx={xScale(dataPoint.value)} cy={50} r={5} />
```

