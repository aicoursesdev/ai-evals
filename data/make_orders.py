"""Build data/orders.db: Tidewater Goods' customers, orders, order items and returns for 2026.

Run it from the repo root:  uv run python data/make_orders.py

The database is a snapshot of the shop on Monday 19 October 2026 at 09:00 IST,
the morning the weekend's emails are waiting. The same seed always builds the
same database, byte for byte in content.

Two kinds of orders go in:
- PINNED orders, written out below, are the ones the inbox, the refund
  scenarios and the red-team talk about. Their IDs, items, dates and statuses
  must not change, or those files stop agreeing with the database.
- Every other order ID is filled with a random but plausible order, placed
  between its pinned neighbours, so IDs rise with time.

Every total follows the shop's rules: items at catalogue price (20% off,
rounded down to the rupee, during the Onam Sale, gift cards excepted), plus
shipping: standard ₹99, free when the items come to more than ₹2,000; express
₹249; international by country; e-gift cards are emailed for free.
"""

import csv
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "orders.db"
SEED = 2026
SNAPSHOT = datetime(2026, 10, 19, 9, 0)
FIRST_ORDER = datetime(2026, 1, 2, 9, 0)
N_ORDERS = 300

ONAM_SALE = (datetime(2026, 8, 18), datetime(2026, 8, 28))  # 18 August 00:00 to 27 August 23:59
INTERNATIONAL_RATE = {"United Arab Emirates": 1499, "Singapore": 1799, "United Kingdom": 2299}
EXPRESS_CITIES = {"Mumbai", "New Delhi", "Gurugram", "Noida", "Bengaluru", "Chennai", "Hyderabad",
                  "Kolkata", "Pune", "Ahmedabad", "Kochi"}
ORDER_STATUSES = ("placed", "packed", "shipped", "delivered", "cancelled", "returned", "refunded")
RETURN_STATUSES = ("requested", "picked_up", "received", "refunded", "rejected")
PAYMENTS = ("upi", "card", "netbanking", "cod", "emi")
SHIPPING = ("standard", "express", "international", "email")

CATALOGUE = {row["sku"]: row for row in csv.DictReader(open(HERE / "catalogue.csv", encoding="utf-8"))}


# --- pinned: the orders the inbox, refund scenarios and red-team talk about; change one and they disagree ---
PINNED_CUSTOMERS = [
    ('Nisha Varghese', 'nisha.varghese@example.com', 'Thrissur', 'India', '2025-03-14T10:22:00+05:30'),
    ('Prakash Iyer', 'prakash.iyer@example.com', 'Chennai', 'India', '2025-06-28T19:05:00+05:30'),
    ('Abhishek Ghoshal', 'abhishek.ghoshal@example.com', 'Kolkata', 'India', '2025-09-10T11:00:00+05:30'),
    ('Jessy Mathai', 'jessy.mathai@example.in', 'Kottayam', 'India', '2025-11-20T16:00:00+05:30'),
    ('Teena Philip', 'teena.philip@example.com', 'Kochi', 'India', '2025-12-02T18:40:00+05:30'),
    ('Rashmi Venkatesh', 'rashmi.venkatesh@example.in', 'Bengaluru', 'India', '2026-01-10T11:19:00+05:30'),
    ('Ayesha Rahman', 'ayesha.rahman@example.com', 'Hyderabad', 'India', '2026-02-06T18:00:00+05:30'),
    ('Ganesh Murthy', 'ganesh.murthy@example.com', 'Mysuru', 'India', '2026-02-14T09:00:00+05:30'),
    ('Gowri Shankar', 'gowri.shankar@example.com', 'Coimbatore', 'India', '2026-03-03T10:36:00+05:30'),
    ('Callum Reid', 'callum.reid@example.com', 'Edinburgh', 'United Kingdom', '2026-04-20T14:29:00+05:30'),
    ('Sandeep Nair', 'sandeep.nair@example.com', 'Kochi', 'India', '2026-05-09T10:47:00+05:30'),
    ('Femina Ashraf', 'femina.ashraf@example.com', 'Kozhikode', 'India', '2026-06-03T11:18:00+05:30'),
    ('Yogesh Rathod', 'yogesh.rathod@example.in', 'Mumbai', 'India', '2026-06-12T15:50:00+05:30'),
    ('Kevin Antony', 'kevin.antony@example.in', 'Kozhikode', 'India', '2026-07-02T13:33:00+05:30'),
    ('Hrishikesh Nair', 'hrishikesh.nair@example.com', 'Pune', 'India', '2026-07-10T09:57:00+05:30'),
    ('Sunil Mathew', 'sunil.mathew@example.com', 'Kottayam', 'India', '2026-07-25T17:43:00+05:30'),
    ('Lijo Jose', 'lijo.jose@example.in', 'Kochi', 'India', '2026-08-05T09:13:00+05:30'),
    ('Chetan Gowda', 'chetan.gowda@example.com', 'Bengaluru', 'India', '2026-08-19T18:39:00+05:30'),
    ('Vivek Ramesh', 'vivek.ramesh@example.com', 'Bengaluru', 'India', '2026-08-20T19:16:00+05:30'),
    ('Aravind Sekhar', 'aravind.sekhar@example.com', 'Kochi', 'India', '2026-08-21T18:42:00+05:30'),
    ('Victor Pinto', 'victor.pinto@example.in', 'Panaji', 'India', '2026-08-22T10:02:00+05:30'),
    ('Farah Siddiqui', 'farah.siddiqui@example.com', 'Dubai', 'United Arab Emirates', '2026-08-22T12:50:00+05:30'),
    ('Rohit Bansal', 'rohit.bansal@example.in', 'Chandigarh', 'India', '2026-08-24T20:47:00+05:30'),
    ('Govind Acharya', 'govind.acharya@example.in', 'Udupi', 'India', '2026-09-03T10:25:00+05:30'),
    ('Vikram Joshi', 'vikram.joshi@example.com', 'Pune', 'India', '2026-09-03T21:45:00+05:30'),
    ('Vikas Bhardwaj', 'vikas.bhardwaj@example.com', 'Shimla', 'India', '2026-09-05T11:31:00+05:30'),
    ('Sheela George', 'sheela.george@example.in', 'Thiruvananthapuram', 'India', '2026-09-10T09:47:00+05:30'),
    ('Oliver Hughes', 'oliver.hughes@example.com', 'Bristol', 'United Kingdom', '2026-09-10T13:31:00+05:30'),
    ('Devan Pillai', 'devan.pillai@example.com', 'Kochi', 'India', '2026-09-12T09:53:00+05:30'),
    ('Mahesh Subramaniam', 'mahesh.s@example.in', 'Chennai', 'India', '2026-09-12T17:25:00+05:30'),
    ('Firoz Basheer', 'firoz.basheer@example.in', 'Kozhikode', 'India', '2026-09-14T17:45:00+05:30'),
    ('Pooja Meena', 'pooja.meena@example.in', 'Jaipur', 'India', '2026-09-15T10:05:00+05:30'),
    ('Amelia Grant', 'amelia.grant@example.com', 'Manchester', 'United Kingdom', '2026-09-15T10:12:00+05:30'),
    ('Leena Mathews', 'leena.mathews@example.com', 'Kochi', 'India', '2026-09-15T10:35:00+05:30'),
    ('Anand Gopalan', 'anand.gopalan@example.com', 'Chennai', 'India', '2026-09-20T15:34:00+05:30'),
    ('Neha Agarwal', 'neha.agarwal@example.com', 'Hyderabad', 'India', '2026-09-21T11:41:00+05:30'),
    ('Priti Sanghvi', 'priti.sanghvi@example.com', 'Ahmedabad', 'India', '2026-09-22T10:10:00+05:30'),
    ('Lekshmi Pillai', 'lekshmi.pillai@example.in', 'Thiruvananthapuram', 'India', '2026-09-24T08:47:00+05:30'),
    ('Grace Whitmore', 'grace.whitmore@example.com', 'Leeds', 'United Kingdom', '2026-09-25T17:52:00+05:30'),
    ('Aditi Deshpande', 'aditi.deshpande@example.in', 'Nagpur', 'India', '2026-09-25T18:34:00+05:30'),
    ('Midhun Thomas', 'midhun.thomas@example.in', 'Alappuzha', 'India', '2026-09-26T12:54:00+05:30'),
    ('Vishal Patil', 'vishal.patil@example.in', 'Pune', 'India', '2026-09-26T19:50:00+05:30'),
    ('Lalitha Raghavan', 'lalitha.raghavan@example.in', 'Chennai', 'India', '2026-09-27T14:46:00+05:30'),
    ('Clement Rodrigues', 'clement.rodrigues@example.in', 'Mangaluru', 'India', '2026-09-28T09:35:00+05:30'),
    ('Mei Ling Chua', 'meiling.chua@example.com', 'Singapore', 'Singapore', '2026-09-28T10:24:00+05:30'),
    ('Shreya Kulkarni', 'shreya.kulkarni@example.in', 'Mumbai', 'India', '2026-09-28T11:02:00+05:30'),
    ('Joel Fernandes', 'joel.fernandes@example.com', 'Panaji', 'India', '2026-09-29T09:27:00+05:30'),
    ('Sneha Rajan', 'sneha.rajan@example.in', 'Hyderabad', 'India', '2026-09-30T12:19:00+05:30'),
    ('Ann Mary Jose', 'annmary.jose@example.com', 'Alappuzha', 'India', '2026-09-30T16:54:00+05:30'),
    ('Shibu Kuriakose', 'shibu.kuriakose@example.in', 'Thrissur', 'India', '2026-10-01T08:40:00+05:30'),
    ('Kritika Bhalla', 'kritika.bhalla@example.in', 'Chandigarh', 'India', '2026-10-01T09:49:00+05:30'),
    ('Rhea Thampi', 'rhea.thampi@example.com', 'Kochi', 'India', '2026-10-01T12:15:00+05:30'),
    ('Deepak Shenoy', 'deepak.shenoy@example.in', 'Udupi', 'India', '2026-10-01T17:23:00+05:30'),
    ('Dinesh Raghunath', 'dinesh.raghunath@example.com', 'Bengaluru', 'India', '2026-10-02T08:14:00+05:30'),
    ('Varun Shetty', 'varun.shetty@example.com', 'Bengaluru', 'India', '2026-10-02T09:33:00+05:30'),
    ('Bhavya Naidu', 'bhavya.naidu@example.com', 'Hyderabad', 'India', '2026-10-02T10:50:00+05:30'),
    ('Shabna Kareem', 'shabna.kareem@example.com', 'Sharjah', 'United Arab Emirates', '2026-10-02T14:53:00+05:30'),
    ('Harish Menon', 'harish.menon@example.com', 'Kochi', 'India', '2026-10-02T20:38:00+05:30'),
    ('Rosamma Jacob', 'rosamma.jacob@example.in', 'Kochi', 'India', '2026-10-03T09:55:00+05:30'),
    ('Amit Kumar Singh', 'amitkumar.singh@example.in', 'Patna', 'India', '2026-10-03T10:45:00+05:30'),
    ('Merin Kurian', 'merin.kurian@example.com', 'Kottayam', 'India', '2026-10-03T11:16:00+05:30'),
    ('Neeraj Yadav', 'neeraj.yadav@example.com', 'Noida', 'India', '2026-10-03T12:53:00+05:30'),
    ('Manjula Bhat', 'manjula.bhat@example.com', 'Bengaluru', 'India', '2026-10-03T20:10:00+05:30'),
    ('Ramya Krishnamurthy', 'ramya.krishnamurthy@example.com', 'Bengaluru', 'India', '2026-10-04T12:30:00+05:30'),
    ('Anagha Suresh', 'anagha.suresh@example.com', 'Kochi', 'India', '2026-10-05T08:21:00+05:30'),
    ('Abhinav Tyagi', 'abhinav.tyagi@example.com', 'New Delhi', 'India', '2026-10-05T09:55:00+05:30'),
    ('Harpreet Gill', 'harpreet.gill@example.com', 'Chandigarh', 'India', '2026-10-05T10:00:00+05:30'),
    ('Rajeev Nambisan', 'rajeev.nambisan@example.com', 'Kochi', 'India', '2026-10-05T18:36:00+05:30'),
    ('Rekha Iyengar', 'rekha.iyengar@example.com', 'Bengaluru', 'India', '2026-10-06T07:48:00+05:30'),
    ('Ashok Banerjee', 'ashok.banerjee@example.com', 'Kolkata', 'India', '2026-10-06T10:05:00+05:30'),
    ('Sudhir Warrier', 'sudhir.warrier@example.com', 'Kochi', 'India', '2026-10-06T10:15:00+05:30'),
    ('Thomas Cherian', 'thomas.cherian@example.in', 'Kottayam', 'India', '2026-10-06T11:20:00+05:30'),
    ('Ankit Verma', 'ankit.verma@example.in', 'Lucknow', 'India', '2026-10-06T12:37:00+05:30'),
    ('Hemanth Kumar', 'hemanth.kumar@example.com', 'Bengaluru', 'India', '2026-10-06T20:24:00+05:30'),
    ('Karan Malhotra', 'karan.malhotra@example.com', 'New Delhi', 'India', '2026-10-07T08:24:00+05:30'),
    ('Mathew Paul', 'mathew.paul@example.com', 'Kochi', 'India', '2026-10-07T09:37:00+05:30'),
    ('Karthik Subramanian', 'karthik.subramanian@example.com', 'Coimbatore', 'India', '2026-10-07T15:56:00+05:30'),
    ('Ajay Kurup', 'ajay.kurup@example.com', 'Bengaluru', 'India', '2026-10-07T21:42:00+05:30'),
    ('Pavithra Sundar', 'pavithra.sundar@example.in', 'Chennai', 'India', '2026-10-08T09:15:00+05:30'),
    ('Sunita Gupta', 'sunita.gupta@example.in', 'Lucknow', 'India', '2026-10-08T11:49:00+05:30'),
    ('Sachin Pillai', 'sachin.pillai@example.in', 'Thiruvananthapuram', 'India', '2026-10-08T17:58:00+05:30'),
    ('Gautam Rao', 'gautam.rao@example.com', 'Bengaluru', 'India', '2026-10-08T19:06:00+05:30'),
    ('Sanjana Kamath', 'sanjana.kamath@example.in', 'Mysuru', 'India', '2026-10-08T20:09:00+05:30'),
    ('Rahul Nambiar', 'rahul.nambiar@example.com', 'Kannur', 'India', '2026-10-08T21:14:00+05:30'),
    ('Rakesh Yadav', 'rakesh.yadav@example.in', 'New Delhi', 'India', '2026-10-09T07:32:00+05:30'),
    ('Dhruv Malik', 'dhruv.malik@example.com', 'Gurugram', 'India', '2026-10-09T10:22:00+05:30'),
    ('Alok Mishra', 'alok.mishra@example.com', 'Bhopal', 'India', '2026-10-09T10:32:00+05:30'),
    ('Pradeep Naik', 'pradeep.naik@example.com', 'Panaji', 'India', '2026-10-09T11:21:00+05:30'),
    ('Mohammed Shibili', 'mohammed.shibili@example.com', 'Kozhikode', 'India', '2026-10-09T12:39:00+05:30'),
    ('Pallavi Baruah', 'pallavi.baruah@example.in', 'Guwahati', 'India', '2026-10-09T13:31:00+05:30'),
    ('Faisal Ahmed', 'faisal.ahmed@example.com', 'Bhopal', 'India', '2026-10-09T15:38:00+05:30'),
    ("Celine D'Souza", 'celine.dsouza@example.com', 'Mumbai', 'India', '2026-10-10T09:28:00+05:30'),
    ('Nakul Sethi', 'nakul.sethi@example.in', 'New Delhi', 'India', '2026-10-10T10:00:00+05:30'),
    ('Sameer Ansari', 'sameer.ansari@example.com', 'Hyderabad', 'India', '2026-10-10T10:52:00+05:30'),
    ('Shweta Rawat', 'shweta.rawat@example.in', 'Dehradun', 'India', '2026-10-10T12:52:00+05:30'),
    ('Siddharth Bhat', 'siddharth.bhat@example.com', 'Mangaluru', 'India', '2026-10-10T15:08:00+05:30'),
    ('Sahil Arora', 'sahil.arora@example.com', 'New Delhi', 'India', '2026-10-10T16:56:00+05:30'),
    ('Ishita Bose', 'ishita.bose@example.com', 'Kolkata', 'India', '2026-10-11T13:40:00+05:30'),
    ('Nikhita Bhandari', 'nikhita.bhandari@example.in', 'Pune', 'India', '2026-10-12T08:17:00+05:30'),
    ('Kavya Iyer', 'kavya.iyer@example.com', 'Chennai', 'India', '2026-10-12T11:15:00+05:30'),
    ('Pratik Joshi', 'pratik.joshi@example.in', 'Nashik', 'India', '2026-10-12T12:55:00+05:30'),
    ('Manish Tiwari', 'manish.tiwari@example.com', 'Indore', 'India', '2026-10-12T17:25:00+05:30'),
    ('Anusha Reddy', 'anusha.reddy@example.com', 'Hyderabad', 'India', '2026-10-13T08:43:00+05:30'),
    ('Arvind Hegde', 'arvind.hegde@example.com', 'Bengaluru', 'India', '2026-10-13T09:27:00+05:30'),
    ('Sunaina Grover', 'sunaina.grover@example.com', 'Gurugram', 'India', '2026-10-13T11:05:00+05:30'),
    ('Fathima Rasheed', 'fathima.rasheed@example.com', 'Kozhikode', 'India', '2026-10-13T11:58:00+05:30'),
    ('Girish Kartha', 'girish.kartha@example.com', 'Kochi', 'India', '2026-10-13T15:25:00+05:30'),
    ('Rajat Khanna', 'rajat.khanna@example.in', 'New Delhi', 'India', '2026-10-13T19:22:00+05:30'),
    ('Sonal Mehta', 'sonal.mehta@example.com', 'Ahmedabad', 'India', '2026-10-14T08:15:00+05:30'),
    ('Lavanya Srinivasan', 'lavanya.srinivasan@example.com', 'Chennai', 'India', '2026-10-14T09:07:00+05:30'),
    ('Tessa Joseph', 'tessa.joseph@example.com', 'Kochi', 'India', '2026-10-14T10:06:00+05:30'),
    ('Nasreen Beegum', 'nasreen.beegum@example.in', 'Kozhikode', 'India', '2026-10-14T12:15:00+05:30'),
    ('Nitin Chawla', 'nitin.chawla@example.com', 'Gurugram', 'India', '2026-10-14T14:45:00+05:30'),
    ('Sreelakshmi Unni', 'sreelakshmi.unni@example.in', 'Kalpetta', 'India', '2026-10-14T19:05:00+05:30'),
    ('Bindu Raj', 'bindu.raj@example.in', 'Madurai', 'India', '2026-10-15T07:55:00+05:30'),
    ('Rajeev Saxena', 'rajeev.saxena@example.com', 'Lucknow', 'India', '2026-10-15T08:55:00+05:30'),
    ('Gayathri Menon', 'gayathri.menon@example.com', 'Thrissur', 'India', '2026-10-15T09:06:00+05:30'),
    ('Vineeth Mohan', 'vineeth.mohan@example.in', 'Thiruvananthapuram', 'India', '2026-10-15T13:20:00+05:30'),
    ('Tanvi Desai', 'tanvi.desai@example.in', 'Ahmedabad', 'India', '2026-10-15T22:42:00+05:30'),
    ('Gaurav Chauhan', 'gaurav.chauhan@example.in', 'Dehradun', 'India', '2026-10-16T07:11:00+05:30'),
    ('Swati Pandey', 'swati.pandey@example.com', 'Lucknow', 'India', '2026-10-16T09:13:00+05:30'),
    ('Smitha Prakash', 'smitha.prakash@example.com', 'Kochi', 'India', '2026-10-16T09:45:00+05:30'),
    ('Kunal Shirodkar', 'kunal.shirodkar@example.com', 'Mumbai', 'India', '2026-10-16T11:44:00+05:30'),
    ('Mridula Sen', 'mridula.sen@example.com', 'Kolkata', 'India', '2026-10-16T15:30:00+05:30'),
    ('Shalini Prasad', 'shalini.prasad@example.com', 'Visakhapatnam', 'India', '2026-10-16T21:04:00+05:30'),
    ('Mahima Jain', 'mahima.jain@example.in', 'Jaipur', 'India', '2026-10-17T10:14:00+05:30'),
    ('Ebin Chacko', 'ebin.chacko@example.com', 'Kottayam', 'India', '2026-10-17T19:18:00+05:30'),
    ('Ritika Sood', 'ritika.sood@example.com', 'Noida', 'India', '2026-10-17T20:18:00+05:30'),
    ('Benny Joseph', 'benny.joseph@example.in', 'Kottayam', 'India', '2026-10-18T09:51:00+05:30'),
    ('Harshita Mehra', 'harshita.mehra@example.com', 'Pune', 'India', '2026-10-18T17:27:00+05:30'),
    ('Akash Menon', 'akash.menon@example.com', 'Kochi', 'India', '2026-10-18T20:34:00+05:30'),
    ('Zainab Hussain', 'zainab.hussain@example.com', 'Mumbai', 'India', '2026-10-18T21:50:00+05:30'),
    ('Arun Mohandas', 'arun.mohandas@example.in', 'Thrissur', 'India', '2026-10-19T06:22:00+05:30'),
]
# (id, customer email, placed_at, items [(sku, qty)], payment, shipping, status, delivered_at,
#  returns [(sku, requested_at, reason, status)])
PINNED_ORDERS = [
    ('TW-10004', 'rashmi.venkatesh@example.in', '2026-01-10T12:00:00+05:30', [('JKT-COASTAL-M', 1)], 'upi', 'standard', 'delivered', '2026-01-15T13:20:00+05:30', []),
    ('TW-10018', 'ayesha.rahman@example.com', '2026-02-06T18:20:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'standard', 'delivered', '2026-02-11T12:00:00+05:30', []),
    ('TW-10031', 'gowri.shankar@example.com', '2026-03-03T11:00:00+05:30', [('BTL-INSUL-750', 1)], 'upi', 'standard', 'delivered', '2026-03-07T12:30:00+05:30', []),
    ('TW-10056', 'callum.reid@example.com', '2026-04-20T15:00:00+05:30', [('JKT-STORM-L', 1)], 'card', 'international', 'delivered', '2026-05-05T12:00:00+05:30', []),
    ('TW-10065', 'sandeep.nair@example.com', '2026-05-09T11:00:00+05:30', [('JKT-MONSOON-M', 1)], 'upi', 'standard', 'delivered', '2026-05-13T15:30:00+05:30', []),
    ('TW-10078', 'femina.ashraf@example.com', '2026-06-03T12:00:00+05:30', [('POU-PHONE-STD', 2)], 'upi', 'standard', 'delivered', '2026-06-08T14:00:00+05:30', []),
    ('TW-10083', 'yogesh.rathod@example.in', '2026-06-12T16:00:00+05:30', [('BPK-TREKKER-55', 1)], 'emi', 'standard', 'delivered', '2026-06-17T11:00:00+05:30', []),
    ('TW-10093', 'kevin.antony@example.in', '2026-07-02T14:00:00+05:30', [('TNT-COMPACT-3', 1)], 'card', 'standard', 'delivered', '2026-07-07T16:10:00+05:30', []),
    ('TW-10098', 'hrishikesh.nair@example.com', '2026-07-10T10:42:00+05:30', [('BPK-DRYTREK-40', 1)], 'card', 'standard', 'delivered', '2026-07-15T13:00:00+05:30', []),
    ('TW-10108', 'sunil.mathew@example.com', '2026-07-25T18:30:00+05:30', [('TNT-COMPACT-2', 1)], 'upi', 'standard', 'delivered', '2026-07-30T15:00:00+05:30', []),
    ('TW-10114', 'lijo.jose@example.in', '2026-08-05T09:30:00+05:30', [('SND-TREK-9', 1)], 'cod', 'standard', 'delivered', '2026-08-10T14:30:00+05:30', []),
    ('TW-10125', 'chetan.gowda@example.com', '2026-08-19T19:00:00+05:30', [('JKT-MONSOON-M', 1), ('BTL-INSUL-500', 1)], 'card', 'standard', 'delivered', '2026-08-24T12:00:00+05:30', []),
    ('TW-10127', 'vivek.ramesh@example.com', '2026-08-20T20:00:00+05:30', [('TNT-COMPACT-2', 1)], 'card', 'standard', 'delivered', '2026-08-25T13:30:00+05:30', []),
    ('TW-10130', 'aravind.sekhar@example.com', '2026-08-21T19:30:00+05:30', [('TNT-COMPACT-2', 1), ('ACC-SEAM-SEALER', 1)], 'upi', 'standard', 'delivered', '2026-08-26T15:00:00+05:30', []),
    ('TW-10132', 'victor.pinto@example.in', '2026-08-22T10:16:00+05:30', [('BPK-ROLLTOP-30', 1)], 'card', 'standard', 'delivered', '2026-08-27T13:00:00+05:30', []),
    ('TW-10133', 'farah.siddiqui@example.com', '2026-08-22T13:30:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'international', 'refunded', '2026-09-04T12:00:00+05:30', [('BPK-DRYTREK-25', '2026-09-20T16:00:00+05:30', 'Colour not as expected', 'refunded')]),
    ('TW-10138', 'rohit.bansal@example.in', '2026-08-24T21:00:00+05:30', [('JKT-STORM-L', 1)], 'upi', 'standard', 'delivered', '2026-08-29T12:40:00+05:30', []),
    ('TW-10153', 'govind.acharya@example.in', '2026-09-03T10:37:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'standard', 'delivered', '2026-09-08T14:00:00+05:30', []),
    ('TW-10154', 'vikram.joshi@example.com', '2026-09-03T22:10:00+05:30', [('TNT-COMPACT-3', 1)], 'card', 'standard', 'returned', '2026-09-08T17:20:00+05:30', [('TNT-COMPACT-3', '2026-09-14T08:55:00+05:30', 'Too small for 3 adults', 'received')]),
    ('TW-10155', 'vikas.bhardwaj@example.com', '2026-09-05T12:00:00+05:30', [('JKT-STORM-M', 1)], 'card', 'standard', 'delivered', '2026-09-10T14:00:00+05:30', []),
    ('TW-10161', 'sheela.george@example.in', '2026-09-10T10:25:00+05:30', [('JKT-COASTAL-M', 1)], 'upi', 'standard', 'refunded', '2026-09-15T13:00:00+05:30', [('JKT-COASTAL-M', '2026-09-20T10:00:00+05:30', 'Too big', 'refunded')]),
    ('TW-10162', 'oliver.hughes@example.com', '2026-09-10T14:00:00+05:30', [('JKT-MONSOON-L', 1)], 'card', 'international', 'delivered', '2026-09-24T11:30:00+05:30', [('JKT-MONSOON-L', '2026-10-05T13:00:00+05:30', 'Too long in the sleeves', 'requested')]),
    ('TW-10164', 'devan.pillai@example.com', '2026-09-12T10:30:00+05:30', [('BPK-DRYTREK-25', 1)], 'upi', 'standard', 'delivered', '2026-09-16T14:00:00+05:30', []),
    ('TW-10165', 'mahesh.s@example.in', '2026-09-12T18:00:00+05:30', [('BTL-INSUL-1000', 1)], 'upi', 'standard', 'delivered', '2026-09-17T12:00:00+05:30', []),
    ('TW-10167', 'firoz.basheer@example.in', '2026-09-14T18:11:00+05:30', [('SND-TREK-8', 1)], 'upi', 'standard', 'delivered', '2026-09-18T12:00:00+05:30', []),
    ('TW-10168', 'pooja.meena@example.in', '2026-09-15T10:20:00+05:30', [('JKT-COASTAL-S', 1)], 'cod', 'standard', 'returned', '2026-09-21T14:45:00+05:30', [('JKT-COASTAL-S', '2026-09-25T18:00:00+05:30', 'Size too small', 'received')]),
    ('TW-10169', 'amelia.grant@example.com', '2026-09-15T10:33:00+05:30', [('JKT-MONSOON-M', 1)], 'card', 'international', 'delivered', '2026-10-01T14:00:00+05:30', []),
    ('TW-10170', 'leena.mathews@example.com', '2026-09-15T10:54:00+05:30', [('JKT-MONSOON-L', 1)], 'upi', 'standard', 'delivered', '2026-09-19T13:00:00+05:30', []),
    ('TW-10171', 'nisha.varghese@example.com', '2026-09-18T20:14:00+05:30', [('JKT-MONSOON-M', 1)], 'upi', 'standard', 'refunded', '2026-09-22T15:40:00+05:30', [('JKT-MONSOON-M', '2026-09-28T11:02:00+05:30', 'Too big', 'refunded')]),
    ('TW-10174', 'anand.gopalan@example.com', '2026-09-20T16:20:00+05:30', [('JKT-STORM-L', 1)], 'card', 'standard', 'returned', '2026-09-24T13:10:00+05:30', [('JKT-STORM-L', '2026-09-30T19:30:00+05:30', "Doesn't suit me", 'received')]),
    ('TW-10175', 'neha.agarwal@example.com', '2026-09-21T12:00:00+05:30', [('TNT-FAMILY-4', 1)], 'emi', 'standard', 'returned', '2026-09-25T16:30:00+05:30', [('TNT-FAMILY-4', '2026-10-03T11:45:00+05:30', 'Family plans changed', 'received')]),
    ('TW-10176', 'priti.sanghvi@example.com', '2026-09-22T10:34:00+05:30', [('JKT-COASTAL-S', 1)], 'upi', 'standard', 'delivered', '2026-09-26T12:00:00+05:30', []),
    ('TW-10178', 'lekshmi.pillai@example.in', '2026-09-24T09:30:00+05:30', [('DRY-BAG-20L', 1), ('DRY-BAG-5L', 1)], 'upi', 'standard', 'refunded', '2026-09-29T15:00:00+05:30', [('DRY-BAG-20L', '2026-10-01T20:10:00+05:30', 'Not needed', 'refunded'), ('DRY-BAG-5L', '2026-10-01T20:10:00+05:30', 'Not needed', 'refunded')]),
    ('TW-10180', 'grace.whitmore@example.com', '2026-09-25T18:00:00+05:30', [('TNT-SOLO-1', 1)], 'card', 'international', 'shipped', None, []),
    ('TW-10181', 'aditi.deshpande@example.in', '2026-09-25T19:00:00+05:30', [('SND-TREK-8', 1), ('DRY-BAG-5L', 1)], 'card', 'standard', 'cancelled', None, []),
    ('TW-10182', 'midhun.thomas@example.in', '2026-09-26T13:05:00+05:30', [('SND-TREK-9', 1)], 'cod', 'standard', 'returned', '2026-10-01T12:30:00+05:30', [('SND-TREK-9', '2026-10-03T09:40:00+05:30', 'Too tight', 'received')]),
    ('TW-10183', 'vishal.patil@example.in', '2026-09-26T20:00:00+05:30', [('TNT-COMPACT-2', 1)], 'emi', 'standard', 'delivered', '2026-10-01T14:15:00+05:30', []),
    ('TW-10184', 'lalitha.raghavan@example.in', '2026-09-27T15:00:00+05:30', [('SND-TREK-7', 1)], 'cod', 'standard', 'returned', '2026-10-03T13:00:00+05:30', [('SND-TREK-7', '2026-10-06T10:30:00+05:30', 'Too big', 'received')]),
    ('TW-10185', 'clement.rodrigues@example.in', '2026-09-28T10:09:00+05:30', [('DRY-BAG-10L', 1)], 'upi', 'standard', 'delivered', '2026-10-03T14:00:00+05:30', []),
    ('TW-10186', 'meiling.chua@example.com', '2026-09-28T10:30:00+05:30', [('JKT-COASTAL-S', 1)], 'card', 'international', 'delivered', '2026-10-09T15:00:00+05:30', []),
    ('TW-10187', 'shreya.kulkarni@example.in', '2026-09-28T11:10:00+05:30', [('BTL-INSUL-500', 1), ('BTL-INSUL-1000', 1), ('DRY-BAG-10L', 1)], 'upi', 'standard', 'delivered', '2026-10-01T18:00:00+05:30', [('BTL-INSUL-1000', '2026-10-10T10:15:00+05:30', 'Too big for my bag; unused', 'picked_up')]),
    ('TW-10188', 'joel.fernandes@example.com', '2026-09-29T10:00:00+05:30', [('BPK-ROLLTOP-30', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10189', 'sneha.rajan@example.in', '2026-09-30T13:00:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'standard', 'delivered', '2026-10-05T15:30:00+05:30', [('BPK-DRYTREK-25', '2026-10-08T09:10:00+05:30', 'Too small for my laptop', 'picked_up')]),
    ('TW-10190', 'annmary.jose@example.com', '2026-09-30T17:00:00+05:30', [('JKT-MONSOON-S', 1)], 'upi', 'standard', 'delivered', '2026-10-05T12:00:00+05:30', []),
    ('TW-10191', 'shibu.kuriakose@example.in', '2026-10-01T09:10:00+05:30', [('JKT-COASTAL-S', 1)], 'cod', 'standard', 'returned', '2026-10-05T12:00:00+05:30', [('JKT-COASTAL-S', '2026-10-07T10:00:00+05:30', 'Too small', 'received')]),
    ('TW-10192', 'kritika.bhalla@example.in', '2026-10-01T10:00:00+05:30', [('BTL-INSUL-500', 1)], 'upi', 'standard', 'delivered', '2026-10-07T12:00:00+05:30', []),
    ('TW-10193', 'rhea.thampi@example.com', '2026-10-01T12:20:00+05:30', [('JKT-COASTAL-M', 1)], 'upi', 'standard', 'delivered', '2026-10-06T15:00:00+05:30', []),
    ('TW-10194', 'deepak.shenoy@example.in', '2026-10-01T18:00:00+05:30', [('BTL-INSUL-750', 1)], 'upi', 'standard', 'delivered', '2026-10-06T14:00:00+05:30', []),
    ('TW-10195', 'dinesh.raghunath@example.com', '2026-10-02T09:00:00+05:30', [('JKT-STORM-M', 1)], 'card', 'standard', 'delivered', '2026-10-07T12:00:00+05:30', [('JKT-STORM-M', '2026-10-09T10:00:00+05:30', 'Too big', 'picked_up')]),
    ('TW-10196', 'varun.shetty@example.com', '2026-10-02T10:00:00+05:30', [('JKT-COASTAL-L', 1)], 'card', 'standard', 'delivered', '2026-10-07T16:00:00+05:30', []),
    ('TW-10197', 'bhavya.naidu@example.com', '2026-10-02T11:27:00+05:30', [('DRY-BAG-20L', 1), ('DRY-BAG-10L', 1)], 'cod', 'standard', 'returned', '2026-10-07T14:00:00+05:30', [('DRY-BAG-20L', '2026-10-09T09:00:00+05:30', 'Not needed', 'received'), ('DRY-BAG-10L', '2026-10-09T09:00:00+05:30', 'Not needed', 'received')]),
    ('TW-10198', 'priti.sanghvi@example.com', '2026-10-02T11:51:00+05:30', [('JKT-MONSOON-S', 1)], 'upi', 'standard', 'delivered', '2026-10-07T15:00:00+05:30', []),
    ('TW-10199', 'shabna.kareem@example.com', '2026-10-02T15:00:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'international', 'shipped', None, []),
    ('TW-10200', 'harish.menon@example.com', '2026-10-02T21:00:00+05:30', [('GFT-EGIFT-2500', 1)], 'card', 'email', 'delivered', '2026-10-02T21:02:00+05:30', []),
    ('TW-10201', 'rosamma.jacob@example.in', '2026-10-03T10:01:00+05:30', [('TNT-COMPACT-3', 1), ('JKT-STORM-M', 1)], 'card', 'standard', 'delivered', '2026-10-07T16:00:00+05:30', []),
    ('TW-10202', 'amitkumar.singh@example.in', '2026-10-03T11:30:00+05:30', [('JKT-MONSOON-M', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10203', 'merin.kurian@example.com', '2026-10-03T12:00:00+05:30', [('BPK-COMMUTER-20', 1), ('ACC-NAME-PATCH', 1)], 'upi', 'standard', 'delivered', '2026-10-09T11:20:00+05:30', []),
    ('TW-10204', 'neeraj.yadav@example.com', '2026-10-03T13:00:00+05:30', [('JKT-COASTAL-L', 1)], 'upi', 'standard', 'delivered', '2026-10-09T13:40:00+05:30', []),
    ('TW-10205', 'manjula.bhat@example.com', '2026-10-03T20:19:00+05:30', [('GFT-EGIFT-5000', 1)], 'upi', 'email', 'delivered', '2026-10-03T20:21:00+05:30', []),
    ('TW-10208', 'ramya.krishnamurthy@example.com', '2026-10-04T12:53:00+05:30', [('SND-TREK-7', 1)], 'cod', 'standard', 'delivered', '2026-10-08T15:00:00+05:30', []),
    ('TW-10213', 'anagha.suresh@example.com', '2026-10-05T09:00:00+05:30', [('DRY-BAG-5L', 1), ('DRY-BAG-10L', 1)], 'upi', 'standard', 'delivered', '2026-10-08T13:00:00+05:30', []),
    ('TW-10214', 'abhinav.tyagi@example.com', '2026-10-05T10:28:00+05:30', [('JKT-MONSOON-M', 1)], 'card', 'standard', 'delivered', '2026-10-09T13:00:00+05:30', []),
    ('TW-10215', 'harpreet.gill@example.com', '2026-10-05T10:44:00+05:30', [('TNT-FAMILY-4', 1)], 'card', 'standard', 'delivered', '2026-10-09T15:00:00+05:30', []),
    ('TW-10216', 'rajeev.nambisan@example.com', '2026-10-05T19:00:00+05:30', [('JKT-STORM-M', 1)], 'card', 'express', 'delivered', '2026-10-06T15:30:00+05:30', []),
    ('TW-10219', 'rekha.iyengar@example.com', '2026-10-06T08:30:00+05:30', [('JKT-COASTAL-M', 1)], 'card', 'standard', 'delivered', '2026-10-13T14:40:00+05:30', []),
    ('TW-10220', 'ashok.banerjee@example.com', '2026-10-06T10:18:00+05:30', [('BPK-DRYTREK-40', 1), ('JKT-STORM-L', 1)], 'card', 'standard', 'delivered', '2026-10-10T13:00:00+05:30', []),
    ('TW-10221', 'sudhir.warrier@example.com', '2026-10-06T11:00:00+05:30', [('BPK-DRYTREK-40', 2)], 'card', 'standard', 'delivered', '2026-10-10T12:30:00+05:30', []),
    ('TW-10222', 'thomas.cherian@example.in', '2026-10-06T11:36:00+05:30', [('BPK-COMMUTER-20', 1), ('ACC-NAME-PATCH', 1)], 'upi', 'standard', 'delivered', '2026-10-10T13:00:00+05:30', []),
    ('TW-10223', 'ankit.verma@example.in', '2026-10-06T13:00:00+05:30', [('SND-TREK-8', 1)], 'upi', 'standard', 'delivered', '2026-10-10T12:00:00+05:30', []),
    ('TW-10224', 'hemanth.kumar@example.com', '2026-10-06T21:00:00+05:30', [('TNT-COMPACT-2', 1), ('DRY-BAG-20L', 1)], 'card', 'standard', 'delivered', '2026-10-14T15:30:00+05:30', []),
    ('TW-10225', 'karan.malhotra@example.com', '2026-10-07T09:00:00+05:30', [('BTL-INSUL-500', 1), ('POU-PHONE-STD', 1)], 'upi', 'standard', 'delivered', '2026-10-12T13:20:00+05:30', [('BTL-INSUL-500', '2026-10-13T10:00:00+05:30', "Unused, don't need it", 'picked_up')]),
    ('TW-10226', 'mathew.paul@example.com', '2026-10-07T10:08:00+05:30', [('BPK-DRYTREK-25', 1)], 'upi', 'standard', 'delivered', '2026-10-12T13:00:00+05:30', []),
    ('TW-10227', 'karthik.subramanian@example.com', '2026-10-07T16:30:00+05:30', [('SND-TREK-8', 1)], 'cod', 'standard', 'delivered', '2026-10-13T13:30:00+05:30', []),
    ('TW-10228', 'ajay.kurup@example.com', '2026-10-07T22:00:00+05:30', [('TNT-COMPACT-2', 1), ('ACC-TENT-FOOTPRINT-2', 1)], 'card', 'standard', 'delivered', '2026-10-15T14:00:00+05:30', []),
    ('TW-10231', 'pavithra.sundar@example.in', '2026-10-08T10:02:00+05:30', [('BTL-INSUL-1000', 1)], 'upi', 'standard', 'delivered', '2026-10-12T14:00:00+05:30', []),
    ('TW-10232', 'sunita.gupta@example.in', '2026-10-08T12:00:00+05:30', [('BTL-INSUL-1000', 1), ('BTL-INSUL-350', 1)], 'upi', 'standard', 'delivered', '2026-10-15T16:00:00+05:30', []),
    ('TW-10233', 'sachin.pillai@example.in', '2026-10-08T18:30:00+05:30', [('BPK-COMMUTER-20', 1)], 'cod', 'standard', 'delivered', '2026-10-13T17:30:00+05:30', []),
    ('TW-10234', 'gautam.rao@example.com', '2026-10-08T19:45:00+05:30', [('BPK-DRYTREK-40', 1)], 'card', 'express', 'delivered', '2026-10-10T13:00:00+05:30', []),
    ('TW-10235', 'sanjana.kamath@example.in', '2026-10-08T20:40:00+05:30', [('BPK-COMMUTER-20', 1)], 'upi', 'standard', 'delivered', '2026-10-16T13:10:00+05:30', []),
    ('TW-10236', 'rahul.nambiar@example.com', '2026-10-08T21:30:00+05:30', [('JKT-MONSOON-L', 1)], 'upi', 'standard', 'delivered', '2026-10-12T15:00:00+05:30', [('JKT-MONSOON-L', '2026-10-13T12:30:00+05:30', 'Too big', 'picked_up')]),
    ('TW-10237', 'rakesh.yadav@example.in', '2026-10-09T07:50:00+05:30', [('BTL-INSUL-750', 2)], 'upi', 'standard', 'cancelled', None, []),
    ('TW-10238', 'dhruv.malik@example.com', '2026-10-09T10:50:00+05:30', [('TNT-SOLO-1', 1)], 'emi', 'standard', 'delivered', '2026-10-14T13:00:00+05:30', []),
    ('TW-10239', 'alok.mishra@example.com', '2026-10-09T11:20:00+05:30', [('JKT-MONSOON-XL', 1)], 'upi', 'standard', 'delivered', '2026-10-15T14:50:00+05:30', []),
    ('TW-10240', 'pradeep.naik@example.com', '2026-10-09T12:00:00+05:30', [('TNT-FAMILY-4', 1), ('DRY-BAG-30L', 1)], 'card', 'standard', 'delivered', '2026-10-17T11:40:00+05:30', []),
    ('TW-10241', 'mohammed.shibili@example.com', '2026-10-09T13:00:00+05:30', [('BPK-DRYTREK-40', 1)], 'card', 'standard', 'delivered', '2026-10-14T16:20:00+05:30', []),
    ('TW-10242', 'pallavi.baruah@example.in', '2026-10-09T14:00:00+05:30', [('JKT-COASTAL-S', 1)], 'netbanking', 'standard', 'delivered', '2026-10-16T15:30:00+05:30', []),
    ('TW-10243', 'faisal.ahmed@example.com', '2026-10-09T16:00:00+05:30', [('SND-TREK-10', 1)], 'cod', 'standard', 'delivered', '2026-10-15T13:00:00+05:30', []),
    ('TW-10244', 'celine.dsouza@example.com', '2026-10-10T10:00:00+05:30', [('BPK-ROLLTOP-30', 1)], 'card', 'express', 'delivered', '2026-10-12T15:10:00+05:30', []),
    ('TW-10245', 'nakul.sethi@example.in', '2026-10-10T10:17:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'standard', 'delivered', '2026-10-15T13:00:00+05:30', []),
    ('TW-10246', 'sameer.ansari@example.com', '2026-10-10T10:59:00+05:30', [('JKT-STORM-XL', 1)], 'card', 'standard', 'delivered', '2026-10-13T13:00:00+05:30', []),
    ('TW-10247', 'shweta.rawat@example.in', '2026-10-10T13:00:00+05:30', [('JKT-COASTAL-S', 1)], 'upi', 'standard', 'delivered', '2026-10-15T12:30:00+05:30', []),
    ('TW-10248', 'siddharth.bhat@example.com', '2026-10-10T15:20:00+05:30', [('DRY-BAG-10L', 2), ('ACC-SEAM-SEALER', 1)], 'upi', 'standard', 'delivered', '2026-10-15T13:00:00+05:30', []),
    ('TW-10249', 'sahil.arora@example.com', '2026-10-10T17:00:00+05:30', [('JKT-MONSOON-L', 1)], 'upi', 'standard', 'delivered', '2026-10-17T13:00:00+05:30', []),
    ('TW-10251', 'ishita.bose@example.com', '2026-10-11T14:00:00+05:30', [('POU-DOC-A5', 1), ('POU-PHONE-STD', 1)], 'upi', 'standard', 'delivered', '2026-10-16T12:40:00+05:30', []),
    ('TW-10255', 'nikhita.bhandari@example.in', '2026-10-12T09:00:00+05:30', [('BTL-INSUL-500', 1), ('POU-PHONE-STD', 1)], 'upi', 'standard', 'delivered', '2026-10-15T12:00:00+05:30', []),
    ('TW-10256', 'kavya.iyer@example.com', '2026-10-12T11:45:00+05:30', [('JKT-MONSOON-M', 1)], 'card', 'express', 'delivered', '2026-10-13T17:10:00+05:30', []),
    ('TW-10257', 'pratik.joshi@example.in', '2026-10-12T13:00:00+05:30', [('JKT-STORM-XL', 1)], 'card', 'standard', 'delivered', '2026-10-17T16:30:00+05:30', []),
    ('TW-10258', 'manish.tiwari@example.com', '2026-10-12T18:00:00+05:30', [('SND-TREK-10', 1)], 'cod', 'standard', 'delivered', '2026-10-17T12:15:00+05:30', []),
    ('TW-10261', 'anusha.reddy@example.com', '2026-10-13T09:00:00+05:30', [('BTL-INSUL-500', 2), ('POU-WAIST', 1)], 'upi', 'express', 'delivered', '2026-10-14T18:30:00+05:30', []),
    ('TW-10262', 'arvind.hegde@example.com', '2026-10-13T10:05:00+05:30', [('SND-TREK-9', 1), ('DRY-BAG-10L', 1)], 'card', 'express', 'delivered', '2026-10-16T11:00:00+05:30', []),
    ('TW-10263', 'sunaina.grover@example.com', '2026-10-13T11:45:00+05:30', [('TNT-FAMILY-4', 1)], 'card', 'standard', 'delivered', '2026-10-17T17:00:00+05:30', []),
    ('TW-10264', 'fathima.rasheed@example.com', '2026-10-13T12:30:00+05:30', [('POU-PHONE-STD', 1)], 'upi', 'standard', 'delivered', '2026-10-16T14:10:00+05:30', []),
    ('TW-10265', 'girish.kartha@example.com', '2026-10-13T15:52:00+05:30', [('POU-DOC-A5', 1)], 'upi', 'standard', 'delivered', '2026-10-17T18:00:00+05:30', []),
    ('TW-10266', 'rajat.khanna@example.in', '2026-10-13T20:00:00+05:30', [('BPK-COMMUTER-20', 1)], 'card', 'standard', 'delivered', '2026-10-17T15:00:00+05:30', []),
    ('TW-10267', 'sonal.mehta@example.com', '2026-10-14T08:30:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'express', 'delivered', '2026-10-15T15:00:00+05:30', []),
    ('TW-10268', 'lavanya.srinivasan@example.com', '2026-10-14T09:50:00+05:30', [('JKT-COASTAL-M', 1), ('POU-PHONE-STD', 1)], 'upi', 'standard', 'delivered', '2026-10-17T12:20:00+05:30', []),
    ('TW-10269', 'tessa.joseph@example.com', '2026-10-14T10:15:00+05:30', [('JKT-MONSOON-S', 1)], 'card', 'express', 'delivered', '2026-10-15T16:30:00+05:30', []),
    ('TW-10270', 'nasreen.beegum@example.in', '2026-10-14T12:35:00+05:30', [('POU-PHONE-STD', 1)], 'upi', 'standard', 'delivered', '2026-10-17T16:00:00+05:30', []),
    ('TW-10271', 'nitin.chawla@example.com', '2026-10-14T15:00:00+05:30', [('POU-PHONE-XL', 1)], 'upi', 'express', 'delivered', '2026-10-16T12:00:00+05:30', []),
    ('TW-10272', 'sreelakshmi.unni@example.in', '2026-10-14T19:30:00+05:30', [('JKT-MONSOON-S', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10273', 'bindu.raj@example.in', '2026-10-15T08:00:00+05:30', [('SND-TREK-7', 1)], 'cod', 'standard', 'cancelled', None, []),
    ('TW-10274', 'gayathri.menon@example.com', '2026-10-15T09:20:00+05:30', [('DRY-BAG-20L', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10275', 'rajeev.saxena@example.com', '2026-10-15T09:43:00+05:30', [('BPK-ROLLTOP-30', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10276', 'vineeth.mohan@example.in', '2026-10-15T14:00:00+05:30', [('BPK-COMMUTER-20', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10277', 'tanvi.desai@example.in', '2026-10-15T23:10:00+05:30', [('POU-WAIST', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10279', 'gaurav.chauhan@example.in', '2026-10-16T07:30:00+05:30', [('BTL-INSUL-750', 1), ('DRY-BAG-5L', 1)], 'cod', 'standard', 'shipped', None, []),
    ('TW-10280', 'swati.pandey@example.com', '2026-10-16T10:00:00+05:30', [('BPK-DRYTREK-40', 1)], 'card', 'standard', 'shipped', None, []),
    ('TW-10281', 'smitha.prakash@example.com', '2026-10-16T10:26:00+05:30', [('JKT-MONSOON-M', 1)], 'card', 'express', 'delivered', '2026-10-17T12:00:00+05:30', []),
    ('TW-10282', 'kunal.shirodkar@example.com', '2026-10-16T12:00:00+05:30', [('SND-TREK-10', 1), ('BTL-INSUL-500', 1)], 'card', 'standard', 'shipped', None, []),
    ('TW-10283', 'mridula.sen@example.com', '2026-10-16T16:00:00+05:30', [('POU-WAIST', 1), ('POU-PHONE-STD', 1)], 'upi', 'standard', 'shipped', None, []),
    ('TW-10284', 'shalini.prasad@example.com', '2026-10-16T21:30:00+05:30', [('BPK-ROLLTOP-30', 1)], 'card', 'standard', 'packed', None, []),
    ('TW-10286', 'mahima.jain@example.in', '2026-10-17T11:00:00+05:30', [('JKT-COASTAL-M', 1), ('BTL-INSUL-500', 1)], 'upi', 'standard', 'packed', None, []),
    ('TW-10289', 'ebin.chacko@example.com', '2026-10-17T19:40:00+05:30', [('SND-TREK-9', 1), ('POU-PHONE-STD', 1)], 'upi', 'standard', 'placed', None, []),
    ('TW-10290', 'ritika.sood@example.com', '2026-10-17T20:30:00+05:30', [('JKT-MONSOON-M', 1)], 'upi', 'standard', 'placed', None, []),
    ('TW-10292', 'benny.joseph@example.in', '2026-10-18T10:00:00+05:30', [('TNT-COMPACT-3', 1), ('ACC-TENT-FOOTPRINT-2', 1)], 'card', 'standard', 'placed', None, []),
    ('TW-10294', 'harshita.mehra@example.com', '2026-10-18T18:00:00+05:30', [('JKT-COASTAL-S', 1)], 'upi', 'standard', 'placed', None, []),
    ('TW-10295', 'akash.menon@example.com', '2026-10-18T21:10:00+05:30', [('BPK-DRYTREK-25', 1)], 'card', 'standard', 'placed', None, []),
    ('TW-10296', 'zainab.hussain@example.com', '2026-10-18T22:00:00+05:30', [('JKT-STORM-M', 1)], 'upi', 'standard', 'placed', None, []),
    ('TW-10297', 'arun.mohandas@example.in', '2026-10-19T06:45:00+05:30', [('JKT-MONSOON-M', 1)], 'upi', 'standard', 'placed', None, []),
]
# --- end pinned ---


def iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%S+05:30")


def parse(text):
    return datetime.fromisoformat(text[:19])


def unit_price(sku, placed_at):
    price = int(CATALOGUE[sku]["price_inr"])
    on_sale = ONAM_SALE[0] <= placed_at < ONAM_SALE[1] and CATALOGUE[sku]["category"] != "gift-card"
    return price * 8 // 10 if on_sale else price


def shipping_fee(method, items_total, country):
    if method == "email":
        return 0
    if method == "international":
        return INTERNATIONAL_RATE[country]
    if method == "express":
        return 249
    return 0 if items_total > 2000 else 99


def check_order(order, customer):
    """Refuse an order that breaks one of the shop's rules."""
    oid, total, items_total = order["id"], order["total_inr"], order["items_total"]
    assert order["status"] in ORDER_STATUSES, oid
    assert order["payment_method"] in PAYMENTS, oid
    assert order["shipping_method"] in SHIPPING, oid
    abroad = customer["country"] != "India"
    assert (order["shipping_method"] == "international") == (abroad and order["shipping_method"] != "email"), oid
    if order["shipping_method"] == "express":
        assert customer["city"] in EXPRESS_CITIES, f"{oid}: express only to metro cities"
    if order["shipping_method"] == "email":
        assert all(CATALOGUE[s]["category"] == "gift-card" for s, _ in order["items"]), oid
    if order["payment_method"] == "cod":
        assert not abroad and total <= 10000, f"{oid}: cash on delivery is India-only, up to ₹10,000"
    if order["payment_method"] == "emi":
        assert not abroad and total >= 3000, f"{oid}: EMI needs ₹3,000 or more"
    if abroad:
        assert order["payment_method"] == "card", f"{oid}: international orders pay by card"
    delivered = order["status"] in ("delivered", "returned", "refunded")
    assert delivered == (order["delivered_at"] is not None), f"{oid}: delivered_at goes with delivered status"
    if order["delivered_at"]:
        assert order["placed_at"] < order["delivered_at"] <= iso(SNAPSHOT), oid
    assert items_total > 0 and total >= items_total, oid


# ---------- random orders ----------

FIRST = ["Bhavna", "Dhruv", "Ebin", "Farah", "Geetha", "Gopal", "Harini", "Hari", "Hemant", "Isha", "Irfan", "Jaya",
         "Jithin", "Leela", "Merin", "Nandini", "Nasreen", "Nikhil", "Pranav", "Rakhi", "Revathi", "Rohini", "Sabu",
         "Sherin", "Siddhi", "Suresh", "Tejas", "Vandana", "Vivek", "Yash", "Zoya", "Aisha", "Abhay",
         "Chitra", "Bincy", "Deepthi", "Elsa", "Fasil", "Jomon", "Mansi", "Ojas", "Rinu", "Shyam", "Treesa"]
LAST = ["Nair", "Menon", "Pillai", "Varghese", "Thomas", "Joseph", "Iyer", "Rao", "Reddy", "Sharma", "Verma",
        "Gupta", "Singh", "Patel", "Shah", "Desai", "Kulkarni", "Joshi", "Das", "Bose", "Sen", "Ghosh",
        "Krishnan", "Raman", "Hegde", "Shetty", "Bhat", "Fernandes", "D'Souza", "Pereira", "Ahmed",
        "Siddiqui", "Qureshi", "Gill", "Sandhu", "Bhatia", "Mathew", "Kurian", "Abraham", "Chacko",
        "Naidu", "Sinha", "Mishra", "Pandey", "Saxena"]
ABROAD_NAMES = {
    "United Arab Emirates": ["Rizwan Ali", "Sajna Basheer", "Thomas Kuruvilla", "Ameena Hussain", "Prakash Menon",
                             "Noushad Kunhi", "Reshma Pillai", "Sajid Mohammed"],
    "Singapore": ["Wei Ling Tan", "Daniel Lim", "Siew Mei Goh", "Ravi Chandran", "Hui Min Ong", "Marcus Teo",
                  "Kavin Raj", "Shu Fen Yeo"],
    "United Kingdom": ["Emily Harcourt", "Hannah Price", "James Whitfield", "Amrit Sohal", "Lucy Barnes",
                       "Tom Ashworth", "Priya Dhaliwal", "Owen Pritchard"],
}
CITIES = [("Kochi", 14), ("Thiruvananthapuram", 7), ("Kozhikode", 5), ("Thrissur", 4), ("Kottayam", 3),
          ("Kannur", 2), ("Alappuzha", 2), ("Bengaluru", 12), ("Chennai", 7), ("Mumbai", 8), ("Pune", 5),
          ("Hyderabad", 5), ("New Delhi", 5), ("Gurugram", 2), ("Noida", 2), ("Kolkata", 3), ("Ahmedabad", 2),
          ("Jaipur", 2), ("Lucknow", 1), ("Coimbatore", 3), ("Mysuru", 2), ("Mangaluru", 2), ("Panaji", 2),
          ("Bhopal", 1), ("Indore", 1), ("Chandigarh", 1), ("Guwahati", 1), ("Bhubaneswar", 1),
          ("Visakhapatnam", 1), ("Madurai", 2), ("Dehradun", 1)]
ABROAD_CITIES = {"United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah"], "Singapore": ["Singapore"],
                 "United Kingdom": ["London", "Manchester", "Leicester", "Edinburgh"]}
CATEGORY_WEIGHT = {"jacket": 25, "backpack": 14, "dry-bag": 15, "bottle": 15, "pouch": 12, "sandals": 10,
                   "tent": 5, "accessory": 6}
RETURN_REASONS = ["Too big", "Too small", "Changed my mind", "Not the colour I expected", "Ordered two by mistake",
                  "Bought a different model", "Didn't need it after all", "Heavier than I expected"]


def business_days_after(moment, days):
    """Move forward by business days (Monday to Saturday)."""
    while days > 0:
        moment += timedelta(days=1)
        if moment.weekday() != 6:
            days -= 1
    return moment


def at_hour(moment, rng, start=10, end=19):
    return moment.replace(hour=rng.randint(start, end - 1), minute=rng.randint(0, 59), second=rng.randint(0, 59))


def random_customer(rng, used_emails, used_names):
    """A new customer whose name nobody else in the database has, so a name finds one person."""
    while True:
        if rng.random() < 0.06:
            country = rng.choice(list(ABROAD_NAMES))
            name, city = rng.choice(ABROAD_NAMES[country]), rng.choice(ABROAD_CITIES[country])
        else:
            country, name = "India", f"{rng.choice(FIRST)} {rng.choice(LAST)}"
            city = rng.choices([c for c, _ in CITIES], [w for _, w in CITIES])[0]
        if name not in used_names:
            break
    used_names.add(name)
    base = name.lower().replace(" ", ".").replace("'", "")
    domain = "example.in" if country == "India" and rng.random() < 0.4 else "example.com"
    email, n = f"{base}@{domain}", 2
    while email in used_emails:
        email, n = f"{base}{n}@{domain}", n + 1
    used_emails.add(email)
    return {"name": name, "email": email, "city": city, "country": country}


def random_items(rng, placed_at):
    if rng.random() < 0.03:
        return [(rng.choice(["GFT-EGIFT-1000", "GFT-EGIFT-2500", "GFT-EGIFT-5000"]), 1)]
    skus = [s for s, row in CATALOGUE.items() if row["category"] in CATEGORY_WEIGHT and int(row["stock"]) > 0]
    weights = [CATEGORY_WEIGHT[CATALOGUE[s]["category"]] for s in skus]
    lines = rng.choices([1, 2, 3], [65, 27, 8])[0]
    items = {}
    while len(items) < lines:
        sku = rng.choices(skus, weights)[0]
        many = CATALOGUE[sku]["category"] in ("bottle", "dry-bag", "pouch") and rng.random() < 0.2
        items[sku] = 2 if many else 1
    return list(items.items())


def random_order(rng, oid, placed_at, customer):
    items = random_items(rng, placed_at)
    items_total = sum(unit_price(s, placed_at) * q for s, q in items)
    abroad = customer["country"] != "India"
    if all(CATALOGUE[s]["category"] == "gift-card" for s, _ in items):
        shipping = "email"
    elif abroad:
        shipping = "international"
    elif customer["city"] in EXPRESS_CITIES and rng.random() < 0.15:
        shipping = "express"
    else:
        shipping = "standard"
    total = items_total + shipping_fee(shipping, items_total, customer["country"])
    if abroad:
        payment = "card"
    else:
        options = [("upi", 45), ("card", 25), ("netbanking", 8)]
        if total <= 10000 and shipping != "email":
            options.append(("cod", 15))
        if total >= 3000:
            options.append(("emi", 7))
        payment = rng.choices([p for p, _ in options], [w for _, w in options])[0]

    # Packed within about 12 hours, never on a Sunday; then the courier's business days.
    packed = placed_at + timedelta(hours=rng.uniform(1, 11))
    if packed.weekday() == 6 or packed.hour >= 18:
        packed = business_days_after(packed.replace(hour=10), 1)
    if shipping == "email":
        delivered = placed_at + timedelta(minutes=2)
    else:
        days = {"standard": (3, 6), "express": (1, 2), "international": (7, 14)}[shipping]
        delivered = at_hour(business_days_after(packed, rng.randint(*days)), rng)

    status, delivered_at, returns = "delivered", delivered, []
    if rng.random() < 0.04 and shipping != "email":
        status, delivered_at = "cancelled", None
    elif delivered > SNAPSHOT:
        status = "placed" if packed > SNAPSHOT else ("packed" if packed + timedelta(hours=20) > SNAPSHOT else "shipped")
        delivered_at = None
    elif rng.random() < 0.09 and shipping != "email" and "ACC-NAME-PATCH" not in dict(items):
        requested = at_hour(delivered + timedelta(days=rng.randint(1, 20)), rng, 8, 22)
        picked = business_days_after(requested, 2)
        received = business_days_after(picked, rng.randint(3, 5) if not abroad else rng.randint(8, 12))
        refunded = business_days_after(received, rng.randint(5, 7))
        if requested < SNAPSHOT:
            if rng.random() < 0.1:
                ret_status, reason = "rejected", "Used: mud on the soles"
            elif refunded <= SNAPSHOT:
                ret_status, status = "refunded", "refunded"
            elif received <= SNAPSHOT:
                ret_status, status = "received", "returned"
            elif picked <= SNAPSHOT and not abroad:
                ret_status = "picked_up"
            else:
                ret_status = "requested"
            if ret_status != "rejected":
                reason = rng.choice(RETURN_REASONS)
            returns = [(sku, iso(requested), reason, ret_status) for sku, _ in items]

    return {"id": oid, "placed_at": iso(placed_at), "items": items, "payment_method": payment,
            "shipping_method": shipping, "status": status,
            "delivered_at": iso(delivered_at) if delivered_at else None, "returns": returns}


def build():
    rng = random.Random(SEED)
    customers = {c[1]: dict(zip(("name", "email", "city", "country", "joined_at"), c)) for c in PINNED_CUSTOMERS}
    used_emails = set(customers)
    used_names = {c["name"] for c in customers.values()}
    orders = {}

    for oid, email, placed, items, payment, shipping, status, delivered, returns in PINNED_ORDERS:
        orders[oid] = {"id": oid, "email": email, "placed_at": placed, "items": items, "payment_method": payment,
                       "shipping_method": shipping, "status": status, "delivered_at": delivered,
                       "returns": [tuple(r) for r in returns]}

    # Fill every free ID with a random order placed between its pinned neighbours.
    ids = [f"TW-{10000 + n}" for n in range(1, N_ORDERS + 1)]
    pinned_times = {oid: parse(o["placed_at"]) for oid, o in orders.items()}
    last_time = FIRST_ORDER
    for i, oid in enumerate(ids):
        if oid in pinned_times:
            assert pinned_times[oid] > last_time, f"{oid} is placed before an earlier ID"
            last_time = pinned_times[oid]
            continue
        nxt = next((pinned_times[o] for o in ids[i + 1:] if o in pinned_times), SNAPSHOT - timedelta(minutes=30))
        free_run = next((j for j, o in enumerate(ids[i:]) if o in pinned_times), len(ids) - i)
        step = (nxt - last_time) / (free_run + 1)
        placed = last_time + step * rng.uniform(0.6, 1.4)
        placed = min(max(placed, last_time + timedelta(minutes=5)), nxt - timedelta(minutes=5))
        # Most orders arrive between 07:00 and 23:00; nudge night orders into the evening.
        if placed.hour < 7:
            placed = placed.replace(hour=rng.randint(7, 9))
            placed = min(max(placed, last_time + timedelta(minutes=5)), nxt - timedelta(minutes=5))
        if rng.random() < 0.3 and len(customers) > len(PINNED_CUSTOMERS):
            customer = rng.choice([c for c in customers.values() if c.get("random")])
        else:
            customer = random_customer(rng, used_emails, used_names)
            customer["joined_at"] = iso(placed - timedelta(minutes=rng.randint(3, 40)))
            customer["random"] = True
            customers[customer["email"]] = customer
        order = random_order(rng, oid, placed, customer)
        order["email"] = customer["email"]
        orders[oid] = order
        last_time = placed

    # Customer IDs follow the order people joined.
    by_join = sorted(customers.values(), key=lambda c: (c["joined_at"], c["email"]))
    for n, c in enumerate(by_join, start=1):
        c["id"] = f"C-{2000 + n}"

    DB_PATH.unlink(missing_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE customers (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL, country TEXT NOT NULL, joined_at TEXT NOT NULL);
        CREATE TABLE orders (
            id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES customers(id),
            placed_at TEXT NOT NULL, status TEXT NOT NULL, payment_method TEXT NOT NULL,
            shipping_method TEXT NOT NULL, total_inr INTEGER NOT NULL, delivered_at TEXT);
        CREATE TABLE order_items (
            order_id TEXT NOT NULL REFERENCES orders(id), sku TEXT NOT NULL,
            qty INTEGER NOT NULL, price_inr INTEGER NOT NULL);
        CREATE TABLE returns (
            order_id TEXT NOT NULL REFERENCES orders(id), sku TEXT NOT NULL, requested_at TEXT NOT NULL,
            reason TEXT NOT NULL, status TEXT NOT NULL);
    """)
    for c in by_join:
        db.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
                   (c["id"], c["name"], c["email"], c["city"], c["country"], c["joined_at"]))
    for oid in ids:
        o = orders[oid]
        customer = customers[o["email"]]
        placed = parse(o["placed_at"])
        assert customer["joined_at"] <= o["placed_at"], f"{oid}: customer joined after ordering"
        o["items_total"] = sum(unit_price(s, placed) * q for s, q in o["items"])
        o["total_inr"] = o["items_total"] + shipping_fee(o["shipping_method"], o["items_total"], customer["country"])
        check_order(o, customer)
        db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (oid, customer["id"], o["placed_at"], o["status"], o["payment_method"],
                    o["shipping_method"], o["total_inr"], o["delivered_at"]))
        for sku, qty in o["items"]:
            db.execute("INSERT INTO order_items VALUES (?, ?, ?, ?)", (oid, sku, qty, unit_price(sku, placed)))
        for sku, requested, reason, status in o["returns"]:
            assert status in RETURN_STATUSES and sku in dict(o["items"]), oid
            db.execute("INSERT INTO returns VALUES (?, ?, ?, ?, ?)", (oid, sku, requested, reason, status))
    db.commit()
    counts = {t: db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("customers", "orders", "order_items", "returns")}
    db.close()
    print(f"Wrote {DB_PATH.name}: " + ", ".join(f"{n} {t}" for t, n in counts.items()))


if __name__ == "__main__":
    build()
