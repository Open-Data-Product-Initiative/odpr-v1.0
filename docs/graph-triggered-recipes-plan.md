# Graph-Triggered Recipes Plan

ODPR should keep three clear concepts:

Recipe is the shared declarative workflow structure.

Product Delivery Recipe is the handoff agreement for delivering or changing one
data product.

Graph-Triggered Recipe is a normal recipe that becomes applicable when an ODPG
graph change matches a declared trigger.

The MVP should not create a new root object, graph query language, workflow
engine, scheduler, run log, or approval model. ODPG owns graph structure and
state. The runtime owns observation, execution, and run evidence. ODPR owns only
the recipe contract.

A graph-triggered recipe adds two optional fields to the existing `Recipe`
structure. `trigger` declares the graph change pattern. `graphContext` requests
the minimal graph context needed after the trigger matches.

The trigger stays small: `source`, `event`, `subject`, and optional
`condition`. The graph context stays small: `graphRef`, `start`, and optional
`depth`.

The MVP event set is closed: `node.added`, `node.removed`,
`node.attributeChanged`, `edge.added`, `edge.removed`, `edge.attributeChanged`,
and `graph.conditionMatched`.

Attribute-change triggers must name the attribute explicitly. `subject.nodeType`
may be a controlled node type or `*`, but `*` means any node type, not any
attribute.

The recipe steps remain ordinary ODPR steps. One step can materialize graph
context to a file, and a later step can use that file as input.
