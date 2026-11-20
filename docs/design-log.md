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

- **Chart:** Data-centre electricity share in a selected country or region compared with the world (`views/where_it_lands.py`).
- **Visual task:** Compare magnitude. Show whether data centres account for a larger or smaller share of electricity demand in the selected place than globally, using figures from the same year.
- **Form chosen:** A horizontal bar chart with both bars starting at zero. The percentage labels show the exact values without hovering, while the year and location controls let readers explore how the comparison changes.
- **Alternative rejected:** A pie chart showing the selected place alongside the world.
- **Why it lost:** These percentages are not separate pieces of one total. Each uses electricity demand within its own geography as the denominator, and the selected place is already included in the world figure. Putting them into a pie would suggest a relationship the data does not support. Bar lengths make the comparison clearer.
- **Second decision:** Keep the horizontal axis fixed at 0–6% when readers change the filters. This keeps the scale consistent, so a small percentage does not suddenly look large because the axis has changed.
- **Colour and context:** The selected location uses blue, while the world reference uses grey. This draws attention to the chosen place while keeping the global benchmark visible.
- **Interpretation and limits:** A sentence below the chart expresses the selected place’s share as a multiple of the world share. The page also explains that these figures cover all data centres and cannot isolate AI electricity use or establish whether a particular local grid has enough capacity.

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

---

## Sai: 5. Concentration

- **Chart:** Top AI organizations and primary countries by training compute share, 2020 to 2026 (`views/concentration.py`)
- **Visual task:** Compare magnitude and ranking. Show how heavily frontier AI training compute is concentrated in a tiny handful of organizations and one country, rather than being an evenly distributed industry load.
- **Form chosen:** Horizontal bar charts with direct percentage labels on every bar. The horizontal layout lets long lab names ("Google DeepMind", "Rest of industry") be read clearly without diagonal tilting.
- **Alternative rejected:** A pie chart or multi-level treemap of organization shares.
- **Why it lost:** A pie chart asks readers to compare slice angles rather than lengths on a common baseline. With several organizations holding 2% to 4% shares, pie slices become thin, illegible slivers that hide the exact numbers. Treemaps similarly require estimating 2D rectangular areas, which human perception judges far less accurately than 1D bar lengths.
- **Color consistency & data alignment:** Both charts use a unified geographic color scheme: Blue (`#2a78d6`) for the United States and US-headquartered organizations, Orange (`#eb6834`) for China and Chinese organizations, and Grey (`#b4b2a9`) for the rest of the world. To ensure perfect data transparency and eliminate discrepancies between charts, remaining organizations in Chart 1 are partitioned into geographic tiers (`Other US organizations` at 3.6%, `Other Chinese organizations` at 6.1%, and `Rest of world organizations` at 1.3%). This guarantees that the sum of the blue bars in Chart 1 matches Chart 2's 90.6% US total, the orange bars match the 8.1% China total, and the grey bar matches the 1.3% Rest of world total.
- **Interactive control:** A multiselect allowing users to filter organizations, paired with an informative empty-state message so the chart never breaks into a blank space or error.
