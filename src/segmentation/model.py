import pandas as pd

def compute_rfm_scores(df):

    snapshot = df['last_purchase_date'].max() + pd.Timedelta(days=1)

    df['recency'] = (snapshot - df['last_purchase_date']).dt.days
    df['frequency'] = round(df['total_spent'] / df['avg_order_value'], 0)
    df.rename(columns={'total_spent': 'monetary'}, inplace=True)
    df['R_score'] = pd.qcut(df['recency'], 5, labels=[5,4,3,2,1]).astype(int)
    df['F_score'] = pd.qcut(df['frequency'], 5, labels=[1,2,3,4,5]).astype(int)
    df['M_score'] = pd.qcut(df['monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    df['RFM_code'] = (
        df['R_score'].astype(str) + 
        df['F_score'].astype(str) + 
        df['M_score'].astype(str)
    ).astype(str)
    return df

def rule_matches(row, rule: dict) -> bool:
    if 'any_of' in rule:
        return any(rule_matches(row, sub) for sub in rule['any_of'])
    
    r, f, m = row['R_score'], row['F_score'], row['M_score']

    if 'R_min' in rule and r < rule['R_min']:
        return False
    if 'R_max' in rule and r > rule['R_max']:
        return False
    if 'R' in rule and r != rule['R']:
        return False

    if 'F_min' in rule and f < rule['F_min']:
        return False
    if 'F_max' in rule and f > rule['F_max']:
        return False
    if 'F' in rule and f != rule['F']:
        return False

    if 'M_min' in rule and m < rule['M_min']:
        return False
    if 'M_max' in rule and m > rule['M_max']:
        return False
    if 'M' in rule and m != rule['M']:
        return False

    return True

def assign_segment(row, rules: dict) -> str:
    for key, rule in rules.items():
        if rule_matches(row, rule):
            return key.replace('_', ' ').title()
    return 'Others - Premium' if row.get('subscription', False) else 'Others - Not premium'