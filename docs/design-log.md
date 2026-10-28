# Design log

One entry per person: the chart you own, the visual task, the form you chose, the alternative you rejected and why. This is what you defend in your Part 1 recording.

---

## Yajat: 1. Global scale, main chart

- **Chart:** Data-centre electricity use, 2020 to 2030 (`views/global_scale.py`)
- **Visual task:** Change over time. Show how fast the data-centre load is growing toward the IEA's 2030 projection, in TWh or as a share of world electricity.
- **Form chosen:** Line chart, solid for IEA estimates and dashed for the projection, with a toggle between TWh and share. An Australia reference line gives the persona a familiar yardstick.
- **Alternative rejected:** A donut of the 2025 share (1.5% vs 98.5%).
- **Why it lost:** A donut shows one year as a thin sliver and cannot show growth, which is the point of the page. It also asks readers to compare angles, which people judge less accurately than position along a common axis.
- **Second decision:** The growth chart is indexed to 2020 = 100 on one axis instead of plotting data-centre TWh and world TWh on two y-axes. The two series differ about 65-fold, and a dual-axis chart lets the designer line them up however they like.
- **Data gap handling:** The IEA has no estimates for 2021 and 2022, so that stretch is drawn faint rather than at full strength.

---

## Siddharth: 2. Where it lands

- **Chart:**
- **Visual task:**
- **Form chosen:**
- **Alternative rejected:**
- **Why it lost:**

---

## Niki: 3. Compute vs efficiency

- **Chart:** Training compute of the largest model vs efficiency of the best chip, 2012 to 2025 (`views/compute_vs_efficiency.py`)
- **Visual task:** Compare the growth rates of two series in different units (FLOP and FLOP/s per W), to answer whether efficiency gains keep pace with compute.
- **Form chosen:** Both series indexed to the start year = 1, as two lines on one log axis. The distance between the lines is the gap in growth. A start-year slider re-indexes both lines, so the reader can check the gap is not an artefact of 2012.
- **Alternative rejected:** A dual y-axis line chart, FLOP on the left and FLOP/s per W on the right.
- **Why it lost:** With two independent scales, the lines can be made to cross or run together just by stretching either axis, so the picture shows the designer's axis choice rather than the data. Indexing to a common base answers the actual question (which grew faster?) on one honest scale.
- **Second decision:** Log axis, not linear. Compute grows by about eight orders of magnitude, so on a linear axis the efficiency line sits on zero and every year before 2023 disappears.
- **Labels:** Only the start, each new record and the last year are labelled, so every change is readable without hovering and the labels do not overlap.

---

## Akil: 4. Water

- **Chart:** Google's reported 2025 water use: total consumed, replenished, and The Dalles (`views/water.py`)
- **Visual task:** Compare three quantities of very different size, to show how much of the total lands in one local water system.
- **Form chosen:** Labelled bar chart in one unit (billion US gallons), one axis, with a finding-style title.
- **Alternative rejected:** A pie chart of The Dalles against the rest.
- **Why it lost:** A pie shows The Dalles as a thin sliver, cannot include the replenished figure (a different quantity, not a part of the total), and asks readers to compare angles instead of lengths.
