<!-- # Market Analysis Tools -->

## SymbolEvent (Project Trendy)
### Goal
- Find correlations between cyclic events (triggers) and price changes patterns
- Built to analyse day-to-day stock price changes, focusing on price changes over 1-3 months (likely not a good day trading tool)
- **Event timeline**: pre-event, event, post-event, over which trends are analysed
- Since in different cycles, the market reaction may lag or lead the event, the event date can be offset by a certain number of days (**max_offset**)
### Parameters
- `symbol`: stock symbol, e.g. 'NVDA'
- `event_dates`: a list of dates when the cyclic event happened
- `pre_event`: number of days before the event to include in trend analysis
- `post_event`: number of days after the event to include in trend analysis
- `max_offset`: maximum number of days to offset the event date, used by event dates other than the latest one

### Data Structures
1. `raw_df`: raw stock price data sorted by date in ascending order, contains all dates from earliest to latest
2. `raw_tensor`: a 2D tensor of shape (n, m), where m is the number of event dates, and n is the number of days in an event timeline plus 2 times `max_offset`

###