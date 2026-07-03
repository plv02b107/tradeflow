from engines.matching import match_trade

if match_trade("TRD001"):
    print("Trade matched successfully.")
else:
    print("Matching failed.")