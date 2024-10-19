# Trendy
### Development Path
- Find correlations between cyclic events (triggers) and price changes patterns
  - Trigger first
    - Surprise trigger (e.g. school shootings)
    - Anticipated trigger (e.g. Olympics)
      1. List pivotal dates/times of events
      2. Set bar size (daily/hourly/...)
      3. Set relative pre and post event cutoff times (e.g. [-30 bars, 15 bars]), collective set of bars referred to as event timeline
      4. Select sets of securities
      5. For each security, get price data over the event timeline
      6. For each bar, calculate new bars $\delta\text{price}_j = \dfrac{\text{price}_j - \text{price}_{j-1}}{\text{price}_{j-1}}$ (result: each security is a matrix where each row is an event timeline, and each column is $\delta\text{price}_j$, where $j$ is a bar in the event timeline)
      7. Repeat steps 5 and 6 for the market index which represents the macro effects surrounding the security, subtract the security's $\delta\text{price}_j$ from that of the market index 
      8. For each security, perform similarity testing between different timelines (variance of $\delta$price)
         - **Assumption**: $\delta$price should occur on the same relative bar in all event timelines (if spike occurs on bar -2 for one event timeline, it should occur on all other event timelines)
         <!-- - keep track of a punishment factor for each security (as each punishment is specific to a trigger-security pair)
         - if spike occurs further away, the punishment increases
         - "attention" between $\delta$price (exponentially decaying weights on both sides of each bar) -->
         - Minimise mean squared error (MSE) with variable parameter being the column shift
         - Calculate MSE for row pairs [(0, 1), (0, 2), ..., (0, n)]
  - $\delta$price pattern first


### Variables
### Data Integrity Concerns
- Stock splits cause price changes? (ideally should not)
- Broker's definition of "end of day" for EOD prices (might be last traded price instead)