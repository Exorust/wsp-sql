```python
# Focus on competitive '\n\n' decision points (|margin|<3) and show per-point key neuron contributions
comp=df[(df.margin.abs()<3.5)].sort_values('margin')
print(comp[['i','j','kind','margin','L23n580','L23n932','L23n385','L23n380','L22n796','L22n1267','L22n223','L22n87','L21n206','L20n168','L20n669','L18n128']].round(2).to_string())
```