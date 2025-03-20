[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

Nested approach to modelling records in the relational database.

Challenge: A record (i.e. `TableA.record`) references another record (i.e. `TableB.record`) via a Foreign Key identifier (i.e. `804`). With a join on the appropriate table, we need to fetch the data of the referenced record and integerate it into the starting record.

```mermaid
flowchart TB

subgraph database


    B1@{ shape: cyl, label: "Table A" }

    C1@{ shape: lean-r, label: "TableA.record" }

    B2@{ shape: cyl, label: "Table B" }

    C2@{ shape: lean-r, label: "TableB.record" }

    B1 -.-> C1
    B2 -.-> C2

end


    D@{ shape: circle, label: "Select row" }

    D1@{ shape: lean-l, label: "TableA.record.dict" }


    D -.-> C1

    D --- D1

    F@{ shape: diamond, label: "Has foreign key?" }

    D --- F

    G@{ shape: subproc, label: "Select record by ID" }

    F ---|yes| G
    G -.-> C2

    H@{ shape: subproc, label: "Model data" }

    C2 -.-> H

    G --- H

    I@{ shape: subproc, label: "Update row dict"}

    I2@{ shape: braces, label: "Replace foreign key in TableA.record with modelled / validated TableB.record data" }

    I ~~~ I2

    I --- D1
    H --- I

    J@{ shape: dbl-circ, label: "Model data" }

    D1 --- J

    I --- J

    F -->|no| J

```