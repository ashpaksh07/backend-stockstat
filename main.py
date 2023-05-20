from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from fastapi.encoders import jsonable_encoder

#App Object
app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def read_root():
    return{"stock":"stat"}

# BaseModel class for defining the json structure of request
class Item(BaseModel):
    particulars: str = None
    posting_date: str = None
    cost_center: str = None
    voucher_type: str = None
    debit: float | str = None
    credit: float | str = None
    net_balance: float | str = None

class Items(BaseModel):
    items: list[Item]

# api to analyse zerodha ledger
@app.post("/api/analyse/")
def analyse_data(items: Items):

    bank_transfer = 0
    upi_transfer = 0
    intraday_charges = 0
    long_term_sell_charge = 0
    kite_connect_charges = 0
    smallcase_charges = 0
    streak_charges = 0
    security_tax = 0
    stamp_duty = 0
    account_maintenance_charges = 0
    fno_debit = 0
    fno_credit = 0
    fno_pnl = 0
    quarterly_settlement = 0
    payout = 0
    other_mode_transfer = 0
    total_amount_added = 0
    being_payment_gateway_charges = 0
    payment_delay_charges = 0
    mf_redemption = 0

    data = jsonable_encoder(items)

    for item in data['items']:
        if("Funds added using NEFT/IMPS/RTGS" in item['particulars']):
            bank_transfer += item['credit']
        elif("Funds added using UPI" in item['particulars']):
            upi_transfer += item['credit']
        elif("Call and Trade charges for" in item['particulars']):
            intraday_charges += item['debit'] 
        elif("DP Charges for Sale of" in item['particulars']):
            long_term_sell_charge += item['debit']
        elif("Kite Connect API Charges" in item['particulars']):
            kite_connect_charges += item['debit']
        elif("Being fee for smallcase" in item['particulars']):
            smallcase_charges += item['debit']
        elif("Streak Monthly Subscription" in item['particulars']):
            streak_charges += item['debit']
        elif("Securities Transaction Tax" in item['particulars']):
            security_tax += item['debit']
        elif("Stamp Duty" in item['particulars']):
            stamp_duty += item['debit']
        elif("AMC for Demat Account" in item['particulars']):
            account_maintenance_charges += item['debit']
        elif("Net obligation for Equity F&O" in item['particulars']):
            fno_debit += item['debit']
            fno_credit += item['credit']
        elif("Funds transferred back as part of quarterly settlement" in item['particulars']):
            quarterly_settlement += item['debit']
        elif("Payout of" in item['particulars']):
            payout += item['debit']
        elif("Funds added using payment gateway" in item['particulars']):
            other_mode_transfer += item['credit']
        elif("Being payment gateway charges" in item['particulars']):
            being_payment_gateway_charges += item['debit']
        elif("Delayed payment charges for" in item['particulars']):
            payment_delay_charges += item['debit']
        elif("MF Redemption credit for" in item['particulars']):
            mf_redemption += item['credit']
        # if("Funds added using payment gateway" in item['particulars']):
        #     other_mode_transfer += item['credit']
            
    fno_pnl = fno_credit - fno_debit
    total_amount = (bank_transfer + upi_transfer + other_mode_transfer) - (quarterly_settlement + payout)
    total_amount_added = bank_transfer + upi_transfer + other_mode_transfer

    result_data = {
    "bank_transfer": round(bank_transfer, 2),
    "upi_transfer": round(upi_transfer, 2),
    "intraday_charges": round(intraday_charges, 2),
    "long_term_sell_charge": round(long_term_sell_charge, 2),
    "kite_connect_charges": round(kite_connect_charges, 2),
    "smallcase_charges": round(smallcase_charges, 2),
    "streak_charges": round(streak_charges, 2),
    "security_tax": round(security_tax, 2),
    "stamp_duty": round(stamp_duty, 2),
    "account_maintenance_charges": round(account_maintenance_charges, 2),
    "fno_debit": round(fno_debit, 2),
    "fno_credit": round(fno_credit, 2),
    "fno_pnl": round(fno_pnl, 2),
    "quarterly_settlement": round(quarterly_settlement, 2),
    "payout": round(payout, 2),
    "other_mode_transfer": round(other_mode_transfer, 2),
    "total_amount": round(total_amount, 2),
    "being_payment_gateway_charges": round(being_payment_gateway_charges, 2),
    "payment_delay_charges": round(payment_delay_charges, 2),
    "mf_redemption": round(mf_redemption, 2),
    "fno_pnl": round(fno_pnl, 2),
    "total_amount_added": round(total_amount_added, 2)
    }
    
    #json_result_data = json.dumps(result_data)

    return result_data