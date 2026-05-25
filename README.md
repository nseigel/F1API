***Response Summary***

**Base**
- URL: http://livetiming.formula1.com/static/Index.json
- Response: Contains paths to available years. As of the most recent commit, it only displays 2026, but all years ranging back to 2023 can be accessed.

**Year**
- URL: http://livetiming.formula1.com/static/YEAR/Index.json
- Response: List of meetings held in that year with each meeting containing multiple sessions. Paths to each session are available.
- To identify a circuit, the circuit key is currently being used as it is currently consistent across all available years.
