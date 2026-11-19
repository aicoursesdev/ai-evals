# RAG scorecard, hd-1, 60 questions

## Finding the page (55 questions with an answer)
- right page in the top 3: 52/55 = 95% (95% range 85% to 98%)
- mean reciprocal rank: 0.910
- archived page in the top 3: 4 questions (Q-17, Q-18, Q-19, Q-24); cited in 2, wrong because of it in 2

## Using the page (all 60, Arjun's labels)
- answer correct: 46/60 = 77% (95% range 65% to 86%)
- answer grounded in the chunks shown: 44/60 = 73% (95% range 61% to 83%)
- questions with no answer handled correctly: 1/5

## Wrong answers and the half that failed
- Q-02 (generation): Free pickup is right, but 'items under 500 rupees need not come back' is the rule for damaged items, lifted into an ordinary return
- Q-03 (retrieval): Says yes, swap; the help centre says exchanges are not done, return and reorder. No retrieved text says swapping is allowed
- Q-17 (retrieval): Cash on delivery limit of 5,000 rupees with a 40 rupee fee comes from the archived page; the current limit is 10,000 and there is no fee
- Q-18 (retrieval): Says yes, free over 1,500 rupees, and express 199: all from the archived page; the current rule is 2,000 and 249
- Q-23 (generation): Right that it does not ship to Australia, then says the shop is working on expanding: no page says so
- Q-24 (generation): Free shipping and express answers are right; adds that no discounts apply to this region, which no page says
- Q-26 (generation): Says to email if the parcel is not found within 48 hours; the page says to tell us within 48 hours, so the deadline is reversed
- Q-31 (retrieval): Only points to the missing items page; gives none of its steps and promises the item will be sent, which the retrieved text does not say
- Q-47 (generation): 106 cm is in the L range (104-112); the reply says M, against the table it was given
- Q-55 (generation): Right that no collection is possible; then says all orders ship within India, but the shop also ships to three other countries
- Q-56 (nothing to find): Unanswerable. Invents the bag's features and cites product-details, which does not exist
- Q-58 (nothing to find): Unanswerable. Says the Ghats Trekker is waterproof and rated IPX6; the page it read is about the DryTrek and Roll-Top backpacks
- Q-59 (nothing to find): Unanswerable. States the shop has no student discounts; no page says so. The sale and bulk facts it adds are right
- Q-60 (nothing to find): Unanswerable. Does not invent a date; says it has no stock data, which no page says, and names a sales team that is not in the help centre
