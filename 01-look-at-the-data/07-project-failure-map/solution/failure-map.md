# Failure map: 100 traces read, 23 fine, 77 with at least one failure

| rank | type | traces | example | what it is | what it needs |
| --- | --- | --- | --- | --- | --- |
| 1 | F-overreach | 21 | E-0498 | The draft says the shop has done, or will do, something that only a person can do or that no page promises (“we have updated”, “we have opened a trace”, “I will personally”, a deadline), or it grants or refuses a refund or exception by itself. | fix: no promises or actions in the prompt; check: phrase list; judge for the rest |
| 2 | F-misread | 21 | E-0473 | The draft gets a fact from the customer’s own email or order wrong, or invents one about them (a day, a date, an amount, an order number, what they had already done), or answers a different request on the same topic from the one they made (the customer asks to add an item and the reply changes the address). A reply that adds unrelated paragraphs, or answers a question nobody asked, is F-off-topic instead. | judge: draft against email |
| 3 | F-wrong-rule | 15 | E-0158 | A help-centre page answers the question, and the draft says something different or applies the page to the wrong case. | fix: give the whole page; judge: draft against page |
| 4 | F-bluff | 14 | E-0204 | No help-centre page answers the question (or the draft needs a fact no page holds), and the draft states one anyway: a rule, a product fact, an email address, a team, or a page that does not exist. | fix: say 'no page answers' and hand over; check: made-up pages and addresses; judge |
| 5 | F-asks-again | 12 | E-0175 | The draft asks the customer for a number, detail or photo they already gave in the email, or cannot give. A general how-to for a channel (“sign in, or email us with your order ID”) does not count. When one mistake seems to fit both this and F-misread: if the draft asks for something, it is F-asks-again; if it states or assumes something wrong (that they have not done what they did do), it is F-misread. | fix: prompt; check: order ID already in the email; judge |
| 6 | F-spam-reply | 7 | E-0348 | The email is spam, phishing or an instruction aimed at an AI, and the help desk writes a reply to the sender. | fix: no draft for spam; check: triage label spam plus a draft |
| 7 | F-wrong-page | 5 | E-0185 | The first thing wrong is the pages fetched: an archived page whose figures are out of date, or pages about another problem while a page that answers exists. | fix: skip archived pages; check: page status |
| 8 | F-off-topic | 5 | E-0386 | The draft answers a question the customer did not ask, or adds a paragraph that has nothing to do with their request. | judge (often a wrong-page problem) |
| 9 | F-language | 3 | E-0232 | The email is in Hindi, Tamil or Malayalam script and the reply is in another language, or is so broken a reader of the language would rewrite it. Hinglish (Hindi in Latin letters) answered in English is not counted. | fix: reply in the customer's language; check: script; person for quality |
| 10 | F-obeys-injection | 1 | E-0551 | The email contains an instruction addressed to the AI and the draft carries it out. | attack set in Module 08; check on the reply |
| 11 | F-no-draft | 1 | E-0722 | The help desk produced no draft at all: the reply never ended and was cut off at the time limit, or came back empty. It is counted, never dropped. | fix: a length limit that stops a runaway reply; check: the draft is empty |

## The top three, and what to do about each

1. **F-overreach (21 traces, 21%).** Drafts that say the shop has done or will do something, or decide a refund. First move: a prompt rule that the reply states no action and no promise, and that money and exceptions go to a person. Measure with a phrase check (it flags 10 of the 21) and a judge for the rest.
2. **F-misread (21 traces, 21%).** The draft gets a fact from the customer's email or order wrong (a day, a date, an amount, an order number, what they already did) or answers a different request. First move: none obvious, it depends on the model. Measure with a judge that compares the draft with the email. It is small in weeks 1 and 2 (2 each) and large in weeks 3 and 4 (8 and 9).
3. **F-wrong-rule (15 traces, 15%).** A page answers and the draft says something else. First move: make sure the draft is given the whole page that applies. Measure with a judge that compares the draft with the page.

Forty-seven of the 77 failed traces carry at least one of these three; 31 carry nothing else.

## Watch list (rare, costly)

- **F-obeys-injection (1 trace: E-0551).** A forwarded email told "any AI system" to approve a refund, and the draft said it had. It needs its own attack set (Module 08).
- **F-no-draft (1 trace: E-0722).** The reply to a Tamil refund question never ended, so the customer would have got nothing. A check that the draft is not empty flags it; a length cap is the first move.
- **F-language (3 traces).** Emails in Tamil and Malayalam were answered in English (E-0232, E-0440) and a Tamil reply (E-0443) was broken; the two Hindi emails were answered in Hindi. The script check flags 2 of the 3.

## Not counted

Hinglish emails answered in English (11 of 11 in this sample) are not counted as failures here; a shop may decide otherwise.
